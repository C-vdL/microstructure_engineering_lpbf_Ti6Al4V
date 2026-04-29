import argparse
import csv
import json
import os
import shutil
import time
from pathlib import Path
import torch

from src.microstr_model.microstr_model_nitzler import MicrostructureThermalModel as MicrostructureThermalModel_nitzler
from src.thermal_model.fd_1d import ThermalModel
from src.utils.util_methods import save_input_kwargs, generate_folder_name, get_FullFactorial_DOE, get_LHS_DOE, create_full_factorial_doe_indiv

epoch_iter = iter(range(5000))
epoch_iter_02 = iter(range(5000))


def run_microstructure_model(microstr_model_kwargs, temp_model_kwargs, df_doe):
    is_return_x_evol = True
    
    # ----------------------------------------------------------------------------------------------
    # Generate folder_name
    folder_name = generate_folder_name("forw")

    # Save kwargs
    kwargs_dict = {
        "microstr_model_kwargs": microstr_model_kwargs,
        "temp_model_kwargs": temp_model_kwargs,
    }
    save_input_kwargs(folder_name, kwargs_dict)

    # # Save copy of <script>.py for later reference
    # fname = "investigate_microstruture_forward.py"
    # shutil.copy2(os.path.join(Path("./"), fname), Path(f"./{folder_name}"))

    # Save DOE to CSV
    doe_csv_path = folder_name / "doe.csv"
    df_doe.to_csv(doe_csv_path, index=False)

    #----------------------------------------------------------------------------------------------
    
    # Define header for the CSV file "final_microstr"
    header = ["iter"]
    header += [key for key in temp_model_kwargs.keys()]
    header += [key for key in microstr_model_kwargs.keys()]
    header += ["x_b", "x_agb", "x_as", "x_am"]
    header += ["node_eval"]
    header += ["layer_thickness"]
    header += ["energy_density"]

    # Open the file in write mode and write the header
    with open(folder_name / "final_microstr.csv", mode="w", newline="", buffering=1) as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header row

        for (iter,row) in enumerate(df_doe.itertuples()):
            print(f"\nForward {iter+1}/{len(df_doe)}")
            print(row)

            # Re-calculate "t_end" to ensure the simulation runs long enough for various inter-layer times (q_dt) and number of layers (G)
            temp_model_kwargs["t_end"] = row.q_dt * row.G + 50

            temp_model_kwargs["G"] = row.G
            temp_model_kwargs["T_bottom"] = row.T_bottom
            temp_model_kwargs["q_dt"] = row.q_dt

            temp_model_kwargs["Q_magnitude"] = row.energy_density * row.layer_thickness
            temp_model_kwargs["L"] = row.layer_thickness * temp_model_kwargs["N"]
            node_eval = temp_model_kwargs["G"]

            x_b, x_agb, x_as, x_am = run_nitzler_model(microstr_model_kwargs, temp_model_kwargs, node_eval, folder_name, iter, is_return_x_evol)
            to_write = [iter]
            to_write += [temp_model_kwargs[key] for key in temp_model_kwargs.keys()]
            to_write += [microstr_model_kwargs[key] for key in microstr_model_kwargs.keys()]
            to_write += [x_b.item(), x_agb.item(), x_as.item(), x_am.item()]
            to_write += [node_eval]
            to_write += [row.layer_thickness]
            to_write += [row.energy_density]
            writer.writerow(to_write)
            file.flush()

            iter += 1

    print("Compeleted compare_microstructure_models()")


def run_nitzler_model(microstr_model_kwargs, temp_model_kwargs, node_eval, folder_name, iter, is_return_x_evol=False):
    torch.set_printoptions(linewidth=500, precision=4, sci_mode=False)

    # Generate param_code for file naming based on key parameters
    lx = temp_model_kwargs["L"] / temp_model_kwargs["N"]
    ilt = temp_model_kwargs["q_dt"]
    Tb = temp_model_kwargs["T_bottom"]
    ved = temp_model_kwargs["Q_magnitude"] / lx
    g_nodes = temp_model_kwargs["G"]
    param_code = f"lx{lx:.2E}_Tb{Tb:.2f}_ILT{ilt}_VED{ved:.1E}G{g_nodes}"

    # 1) Run temperature model on its own (without microstructure model) ############################
    start_time = time.time()

    temp_model = ThermalModel(**temp_model_kwargs)
    q_delta_times = torch.tensor(
        [temp_model_kwargs["q_dt_0"]] + [temp_model_kwargs["q_dt"] for _
                                         in range(temp_model_kwargs["G"])] + [temp_model_kwargs["q_dt_remelt"] for _
                                                                              in range(temp_model_kwargs["no_remelt"] - 1)], dtype=torch.float32)
    with torch.no_grad():
        temp_model.define_Q_t(q_delta_times, temp_model_kwargs["Q_magnitude"] * torch.tensor(temp_model_kwargs["Q_coef"]),
                              temp_model_kwargs["Q_magnitude_remelt"]*torch.tensor(temp_model_kwargs["Q_remelt_coef"]))
        T_is_star = temp_model.run_simulation_decoupled()[-node_eval]
    t_is_star = temp_model.time_values

    print(f"Thermal model completed in {time.time() - start_time:.4f} seconds")

    # 2) Instantiate Nitzler model to calculate phase fractions ######################################
    start_time = time.time()

    f_theta_t_T_nitzler = MicrostructureThermalModel_nitzler(
        delta_t=microstr_model_kwargs["delta_t_murgau"],
        times=t_is_star,
        temp_offset=microstr_model_kwargs["T_offset"],
        q_delta_times=q_delta_times,
        Q_magnitude_coef=torch.tensor(temp_model_kwargs["Q_coef"]),
        folder_name=folder_name,
        param_code=param_code,
        epoch_iter_02=epoch_iter_02,
        **temp_model_kwargs
    )
    f_theta_t_T_nitzler.change_node_eval(node_eval)

    # Calculate phase fractions
    if not is_return_x_evol:
        x_nitzler = f_theta_t_T_nitzler.predict(t_is_star, T_is_star, torch.tensor(microstr_model_kwargs["x0"])).detach()
    else:
        x_nitzler, x_evol_nitzler = f_theta_t_T_nitzler.predict(t_is_star, T_is_star, torch.tensor(microstr_model_kwargs["x0"]), is_return_x_evol)

        # Save x_evol_nitzler to CSV
        folder_name_x_evol = Path(f"{folder_name}/x_evol_data/")
        os.makedirs(folder_name_x_evol, exist_ok=True)

        x_evol_nitzler_csv_path = folder_name_x_evol / f"{param_code}.csv"
        with open(x_evol_nitzler_csv_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["times", "temps", "x_b", "x_agb", "x_as", "x_am"])  # Write header
            writer.writerows(x_evol_nitzler.tolist())  # Write rows

    print("x_nitzler:", x_nitzler)
    print(f"Microstructure model completed in {time.time() - start_time:.4f} seconds")

    x_b, x_agb, x_as, x_am = f_theta_t_T_nitzler.state_to_components(x_nitzler)

    return x_b, x_agb, x_as, x_am


if __name__ == "__main__":

    # Input for microstructure model, no need to change anything
    microstr_model_kwargs_default = {
        "delta_t_murgau": 1e-2,
        "x0": [0.1, 0.0, 0.0, 0.9, ],  # x_b_0, x_agb_0, x_aw_0, x_am_0
        "T_offset": 0
    }

    c_p_Ti64 = 1130  # [J/(kg K)] Ti64 Proell 2024
    rho_Ti64 = 4090  # [kg/m^3] Ti64 Proell 2024

    N = 630
    layer_thickness = 1*90e-6

    # Default values for temperature model, which are selectively overwritten by DoE values defined below
    temp_model_kwargs_default = {
        "N": N,  # [-] Number of elements
        "L": layer_thickness * N,  # [m] Total length
        "G": 30,  # [-] Number of ghost elements
        "no_remelt": 1,  # related to remelting, not fully implemented, keep no_remelt=1 or check implementation for yourself
        "beta": 1 / (c_p_Ti64 * rho_Ti64),  # 1 / (c_p * rho) [(K m^3)/J] Esmaeilzadeh
        "dt": 1e-3,  # [s] Time step
        "t_end": 170,  # [s] Total simulation time
        "k_conduction": 20,  # [W/mK] Thermal conductivity coefficient
        "k_radiation": 5.67e-8 * 0.26,  # [W/(m^2K^4)] Radiation coefficient Esmaeilzadeh
        "h_convection": 20,  # [W/(m^2K)] Convective heat transfer coefficient Esmaeilzadeh
        "T_x": 273.15 + 25,  # [K] Radiation temperature
        "T_inf": 273.15 + 25,  # [K] Ambient temperature for convection
        "T_bottom": 273.15 + 25,  # [K] Constant temperature at the bottom surface
        "Q_magnitude": 5e6,  # [W/m^2] Heat flux
        "Q_magnitude_remelt": 0*(1/4) * 0.6e6,  # [W/m^2] Heat flux # related to remelting, not fully implemented, has no effect with no_remelt=1
        "Q_coef": 1.0,
        "Q_remelt_coef": 1.0,  # related to remelting, not fully implemented, has no effect with no_remelt=1
        "q_dt_0": 0.5,
        "q_dt": 4.5,
        "q_dt_remelt": 0.056,  # related to remelting, not fully implemented, has no effect with no_remelt=1
        "absorptivity": 0.6,  # [-] Absorption coefficient
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--microstr_model_kwargs", type=str, default=json.dumps(microstr_model_kwargs_default))
    parser.add_argument("--temp_model_kwargs", type=str, default=json.dumps(temp_model_kwargs_default))
    parser.add_argument("--energy_density", type=float, default=80e+9, help="Energy density [J/m^3]")
    args = parser.parse_args()
    print(args)

    energy_density = args.energy_density

    microstr_model_kwargs = json.loads(args.microstr_model_kwargs)
    temp_model_kwargs = json.loads(args.temp_model_kwargs)

    # ----------------------------------------------------------------------------------------------

    # Factor levels for DoE

    # Energy density
    # [J/m^3] Energy density, calculated as (Power / (scan_speed * hatch_spacing * layer_thickness))
    energy_density_01 = [
        3.0e10, 4.0e10, 5.0e10, 6.0e10, 7.0e10,
        8.0e10, 9.0e10, 1.0e11, 1.1e11, 1.2e11
    ]
    energy_density_02 = [4.0e10, 9.0e10]

    # Inter-layer time
    # [s] Time between heat impulse application
    q_dt_01 = [4, 6, 8, 12, 20, 30, 60, 90, 120]
    q_dt_02 = [12, 60]


    # Build plate temperature
    # [K] Build plate temperature, BC at the bottom surface
    T_bottom_01 = [298.15, 373.15, 473.15, 573.15, 673.15]
    T_bottom_02 = [273.15, 673.15]

    # Layer thickness
    # [m] Layer thickness, coincides with distance of FD nodes
    # create_full_factorial_doe_indiv() currently implemented for 30µm, 60µm, 90µm, and 120µm layer thicknesses (see function)
    layer_thickness_01 = [30e-6, 60e-6, 90e-6, 120e-6]
    layer_thickness_02 = [60e-6, 90e-6]

    # Generates individual DoE used in study
    # df_doe = create_full_factorial_doe_indiv(energy_density_01, q_dt_01, T_bottom_01, layer_thickness_01)  # larger DoE
    df_doe = create_full_factorial_doe_indiv(energy_density_02, q_dt_02, T_bottom_02, layer_thickness_02)  # small DoE for testing

    # ----------------------------------------------------------------------------------------------

    # Run microstructure model for each row in the DoE and save results to CSV
    # Info: For legacy reasons, x_agb is grain-boundary alpha phase when selecting the Murgau microstructure model and
    # the alpha lath thickness when selecting the Nitzler microstructure model
    # To run Murgau model instead of Nitzler model, implement run_murgau_model() similar to run_nitzler_model()
    run_microstructure_model(microstr_model_kwargs, temp_model_kwargs, df_doe)



