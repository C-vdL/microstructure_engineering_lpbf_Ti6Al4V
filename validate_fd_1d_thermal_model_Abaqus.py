import copy
import numpy as np
import json
import os
import matplotlib.pyplot as plt
import torch
import pandas as pd
from pathlib import Path

from src.thermal_model.fd_1d import ThermalModel
from misc.plot_style import apply_rcparams


def read_Abaqus_data(parent_dir):
    print("# Read scan-resolved Abaqus simulation data")

    df_list = []

    # Traverse subdirectories
    for root, _, files in os.walk(parent_dir):

        print(root)
        # Filter for csv files with correct box
        csv_files = [f for f in files if f.endswith("c0500-011-000_d010-010-010_comb.csv")]
        json_file = "sim_param.json"
        laser_inp_file = "1_AM_laser.inp"

        if csv_files and json_file in files:
            json_path = os.path.join(root, json_file)

            # Read JSON as text and replace the specific string
            with open(json_path, "r") as f:
                json_text = f.read()

            json_text = json_text.replace(
                '"latent_heat": "1_material.inp",',
                '"latent_heat": "1_material.inp"'
            )

            # Parse the modified JSON
            sim_params = json.loads(json_text)

            # If inp file exists, read it as a DataFrame
            if laser_inp_file in files:
                laser_inp_path = os.path.join(root, laser_inp_file)
                laser_inp_df = pd.read_csv(laser_inp_path, header=None)
                laser_inp_df.columns = ["time", "x", "y", "z", "power"]
                nonzero_power_times = laser_inp_df[laser_inp_df["power"] != 0]["time"].tolist()
                # nonzero_power_times = laser_inp_df[laser_inp_df["power"] == 0]["time"].tolist()
                sim_params["q_timesteps"] = nonzero_power_times[2::3]

            # Process each CSV file
            for csv_file in csv_files:
                csv_path = os.path.join(root, csv_file)
                df = pd.read_csv(csv_path)
                sim_params_tmp = copy.deepcopy(sim_params)
                sim_params_tmp["csv_file"] = csv_path

                df_list.append((df, sim_params_tmp))

    return df_list


def plot_1to1_comparison(temp_model_kwargs_default, base_folder, T_melt, is_display_Abaqus, suffix):

    print("\n# Plot 1 to 1 comparison 3D FEM vs 1D FD")
    print(f"# Part ID:\t{suffix}")
    thermal_sim_data = {}

    # Iterate through Abaqus scan-resolved simulations
    for iter, (df, sim_params) in enumerate(dfs_Abaqus):

        # Read simulation parameters of current Abaqus simulation
        laser_power = sim_params.get("laser_power", "Unknown")  # Default if not found
        laser_speed = sim_params.get("laser_speed", "Unknown") * 1e-3
        hatch_distance = sim_params.get("hatch_distance", "Unknown") * 1e-3
        layer_thickness_Abaqus = sim_params.get("layer_thickness", "Unknown") * 1e-3
        q_timesteps = sim_params.get("q_timesteps", "Unknown")

        # Calculate missing parameters
        energy_density = laser_power / (laser_speed * hatch_distance * layer_thickness_Abaqus)  # W/m^3
        Q_magnitude = energy_density * layer_thickness_Abaqus  # W/m^2
        q_delta_times = torch.diff(torch.cat((torch.tensor([0]), torch.tensor(q_timesteps))))
        Wmm3_value = energy_density / 0.001 * 1e-9  # W/mm^3
        energy_density_Jmm3 = energy_density * 1e-9  # J/mm^3

        # Save parameters for current iteration
        thermal_sim = {}
        temp_model_kwargs_iter = copy.deepcopy(temp_model_kwargs_default)
        temp_model_kwargs_iter["Q_magnitude"] = Q_magnitude
        temp_model_kwargs_iter["q_delta_times"] = q_delta_times
        thermal_sim["temp_model_kwargs"] = temp_model_kwargs_iter

        if energy_density_Jmm3 > 150000:
            # Unrealistically high energy density, skip
            continue
        else:
            print(f"{iter} Energy density:\t{energy_density_Jmm3:.0f} J/mm3")

        # ####################################################################################
        # Run corresponding 1D FD simulation #################################################

        # Instantiate finite difference thermal model
        temp_model_kwargs_iter.pop("L", None)
        thermal_model_01 = ThermalModel(L=layer_thickness * temp_model_kwargs_iter["N"], **temp_model_kwargs_iter)
        thermal_model_01.define_Q_t(temp_model_kwargs_iter["q_delta_times"], temp_model_kwargs_iter["Q_magnitude"], temp_model_kwargs_iter["Q_magnitude_remelt"])

        # Run finite difference thermal simulation
        T_history = thermal_model_01.run_simulation_decoupled()

        # Save results of thermal simulation in thermal_sim_data
        thermal_sim["T_history"] = T_history
        thermal_sim["time_values"] = thermal_model_01.time_values
        thermal_sim_data[iter] = thermal_sim

        # ####################################################################################
        # Plot thermal simulations ###########################################################

        if "HX" in suffix:
            # fig, ax = plt.subplots(1, 1, figsize=(9/2.54, 9/2.54))
            fig, ax = plt.subplots(1, 1, figsize=(9/2.54, 7.5/2.54))
        else:
            fig, ax = plt.subplots(1, 1, figsize=(6 / 2.54, 5 / 2.54))

        # Plot results from 1D FD simulation  ###############################################
        T_history = thermal_sim["T_history"]
        time_values = thermal_sim["time_values"]

        e = 10
        a, b = -e-2, -e+1
        T_history_layer = T_history[(a):(b)].mean(dim=0)
        T_history_layer[T_history_layer == 0] = torch.nan
        ax.plot(time_values, T_history_layer - 273.15, linestyle='-', label=f"1D FD", c="#1C9099", lw=1)

        # Plot  3D FEM results with layer-wise heat source ###################################
        subfolder_name = f"Wmm3_{Wmm3_value:.0f}"
        box = "b_c0500-500--002_d1200-1300-010"
        subfolder_path = os.path.join(base_folder, subfolder_name, box)
        for file_name in os.listdir(subfolder_path):
            if file_name.lower().endswith('.csv'):
                csv_path = os.path.join(subfolder_path, file_name)
        df_Cmodel = pd.read_csv(csv_path)

        if 'time' in df_Cmodel.columns and 'nt11' in df_Cmodel.columns:
            # plt.scatter(df['time'], df['nt11']+273.15, label=subfolder_name, s=10)
            ax.plot(df_Cmodel['time']+0.4, df_Cmodel['nt11'], label=f"3D FEM, layer-wise",  linestyle='-', c="#762A83", lw=1)

        # Plot  3D FEM results with scan-resolved heat source #################################
        if "time_cons" in df.columns and "nt11_comb" in df.columns and is_display_Abaqus:
            ax.plot(df["time_cons"]+0.2, df["nt11_comb"], linestyle='-', label="3D FEM, scan-resolved", c="#E66101", lw=1)

        # Finish plot #########################################################################
        ax.set_ylim(0, T_melt)
        ax.set_xlim(0, 50)
        ax.legend(loc="upper right")
        ax.grid(True)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Temperature [°C]")

        # Save plot  #########################################################################
        geometry_3D_LW = os.path.join(*Path(base_folder).parts[-2:])
        path_fig = Path(f"./figs/thermal_models/{geometry_3D_LW}/{box}")
        path_fig.mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(f"{path_fig}/thermal_sim_Abaqus_FD_{energy_density:.1e}_{suffix}.png"))
        plt.close("all")


def plot_1to1_comparison_MAPE_APE(temp_model_kwargs_default, base_folder, T_melt, is_display_Abaqus, suffix, is_compare_to_layerwise=True):

    print("\n# Plot 1 to 1 comparison 3D FEM vs 1D FD (incl. MAPE and APE)")
    print(f"# Part ID:\t{suffix}")

    thermal_sim_data = {}

    # Iterate through Abaqus scan-resolved simulations
    for iter, (df, sim_params) in enumerate(dfs_Abaqus):

        # Read simulation parameters of current Abaqus simulation
        laser_power = sim_params.get("laser_power", "Unknown")  # Default if not found
        laser_speed = sim_params.get("laser_speed", "Unknown") * 1e-3
        hatch_distance = sim_params.get("hatch_distance", "Unknown") * 1e-3
        layer_thickness_Abaqus = sim_params.get("layer_thickness", "Unknown") * 1e-3
        q_timesteps = sim_params.get("q_timesteps", "Unknown")

        # Calculate missing parameters
        energy_density = laser_power / (laser_speed * hatch_distance * layer_thickness_Abaqus)  # W/m^3
        Q_magnitude = energy_density * layer_thickness_Abaqus  # W/m^2
        q_delta_times = torch.diff(torch.cat((torch.tensor([0]), torch.tensor(q_timesteps))))
        Wmm3_value = energy_density / 0.001 * 1e-9  # W/mm^3
        energy_density_Jmm3 = energy_density * 1e-9  # J/mm^3

        # Save parameters for current iteration
        thermal_sim = {}
        temp_model_kwargs_iter = copy.deepcopy(temp_model_kwargs_default)
        temp_model_kwargs_iter["Q_magnitude"] = Q_magnitude
        temp_model_kwargs_iter["q_delta_times"] = q_delta_times
        thermal_sim["temp_model_kwargs"] = temp_model_kwargs_iter

        if energy_density_Jmm3 > 150000:
            # Unrealistically high energy density, skip
            continue
        else:
            print(f"{iter} Energy density:\t{energy_density_Jmm3:.0f} J/mm3")

        # ####################################################################################
        # Run corresponding 1D FD simulation #################################################

        # Instantiate finite difference thermal model
        temp_model_kwargs_iter.pop("L", None)
        thermal_model_01 = ThermalModel(L=layer_thickness * temp_model_kwargs_iter["N"], **temp_model_kwargs_iter)
        thermal_model_01.define_Q_t(temp_model_kwargs_iter["q_delta_times"], temp_model_kwargs_iter["Q_magnitude"], temp_model_kwargs_iter["Q_magnitude_remelt"])

        # Run finite difference thermal simulation
        T_history = thermal_model_01.run_simulation_decoupled()

        # Save results of thermal simulation in thermal_sim_data
        thermal_sim["T_history"] = T_history
        thermal_sim["time_values"] = thermal_model_01.time_values
        thermal_sim_data[iter] = thermal_sim

        # ####################################################################################
        # Plot thermal simulations ###########################################################

        if "HX" in suffix:
            fig, (ax, ax2) = plt.subplots(2, 1, figsize=(15/2.54, 9/2.54))
        else:
            fig, (ax, ax2) = plt.subplots(2, 1, figsize=(15/2.54, 9/2.54))

        # Plot results from 1D FD simulation  ###############################################
        T_history = thermal_sim["T_history"]
        time_values = thermal_sim["time_values"]

        e = 10
        a, b = -e-2, -e+1
        T_history_layer = T_history[(a):(b)].mean(dim=0)
        T_history_layer[T_history_layer == 0] = torch.nan
        ax.plot(time_values, T_history_layer - 273.15, linestyle='-', label=f"1D FD", c="#1C9099", lw=1)

        # Plot  3D FEM results with layer-wise heat source ###################################
        subfolder_name = f"Wmm3_{Wmm3_value:.0f}"
        box = "b_c0500-500--002_d1200-1300-010"
        subfolder_path = os.path.join(base_folder, subfolder_name, box)
        for file_name in os.listdir(subfolder_path):
            if file_name.lower().endswith('.csv'):
                csv_path = os.path.join(subfolder_path, file_name)
        df_Cmodel = pd.read_csv(csv_path)

        if 'time' in df_Cmodel.columns and 'nt11' in df_Cmodel.columns:
            # plt.scatter(df['time'], df['nt11']+273.15, label=subfolder_name, s=10)
            ax.plot(df_Cmodel['time']+0.1, df_Cmodel['nt11'], label=f"3D FEM, layer-wise",  linestyle='-', c="#762A83", lw=1)

        # Plot  3D FEM results with scan-resolved heat source #################################
        if "time_cons" in df.columns and "nt11_comb" in df.columns and is_display_Abaqus:
            ax.plot(df["time_cons"]+0.05, df["nt11_comb"], linestyle='-', label="3D FEM, scan-resolved", c="#E66101", lw=1)

        # Finish plot #########################################################################
        ax.set_ylim(0, T_melt)
        ax.set_xlim(0, 50)
        ax.legend(loc="upper right")
        ax.grid(True)
        # ax.set_xlabel("Time [s]")
        ax.set_ylabel("Temperature [°C]")

        #################################################################################

        if is_compare_to_layerwise:
            # Calculate cooling errors
            cumsum_values = torch.cumsum(temp_model_kwargs_iter["q_delta_times"], dim=-1)
            abaqus_interp = torch.tensor(np.interp(time_values,df_Cmodel['time'].values, df_Cmodel['nt11'].values))
            mask = (abaqus_interp < T_melt) & (~((time_values[:, None] - cumsum_values).abs() <= 0.2).any(dim=1))
            delta_T = (abaqus_interp[mask] - T_history_layer[mask] + 273.15)
            delta_T_rel = (abaqus_interp[mask] - T_history_layer[mask] + 273.15) / (abaqus_interp[mask]+273.15) * 100

            # Calculate peak errors
            delta_t_peaks = []
            delta_T_peaks = []
            for cumsum_value in cumsum_values:
                mask_window = (time_values >= cumsum_value - 0.4) & (time_values <= cumsum_value + 0.4)
                max_T_history = T_history_layer[mask_window].max()
                mask_window_abaqus = (df_Cmodel['time'] >= cumsum_value.item() - 0.4) & (df_Cmodel['time'] <= cumsum_value.item() + 0.4)
                max_abaqus = df_Cmodel['nt11'][mask_window_abaqus].max() + 273.15
                delta_T_peak_rel = (max_T_history - max_abaqus) / max_abaqus * 100

                if max_abaqus < 1000 + 273.15:
                    delta_T_peaks.append(delta_T_peak_rel)
                    delta_t_peaks.append(cumsum_value.item())

        else:
            # Calculate cooling errors
            cumsum_values = torch.cumsum(temp_model_kwargs_iter["q_delta_times"], dim=-1)
            abaqus_interp = torch.tensor(np.interp(time_values, df['time_cons'].values, df['nt11_comb'].values))
            mask = (abaqus_interp < T_melt) & (~((time_values[:, None] - cumsum_values).abs() <= 0.2).any(dim=1))
            delta_T = (abaqus_interp[mask] - T_history_layer[mask] + 273.15)
            delta_T_rel = (abaqus_interp[mask] - T_history_layer[mask] + 273.15) / (abaqus_interp[mask] + 273.15) * 100

            # Calculate peak errors
            delta_t_peaks = []
            delta_T_peaks = []
            for cumsum_value in cumsum_values:
                mask_window = (time_values >= cumsum_value - 0.4) & (time_values <= cumsum_value + 0.4)
                max_T_history = T_history_layer[mask_window].max()
                mask_window_abaqus = (df['time_cons'] >= cumsum_value.item() - 0.4) & (df['time_cons'] <= cumsum_value.item() + 0.4)
                max_abaqus = df['nt11_comb'][mask_window_abaqus].max() + 273.15
                delta_T_peak_rel = (max_T_history - max_abaqus) / max_abaqus * 100

                if max_abaqus < 1000 + 273.15:
                    delta_T_peaks.append(delta_T_peak_rel)
                    delta_t_peaks.append(cumsum_value.item())

        # Plot absolute error
        ax2.scatter(time_values[mask], delta_T, label="$\Delta T (cooling)$", s=5)
        ax2.scatter(delta_t_peaks, delta_T_peaks, linestyle='-', label="$\Delta T (peak)$")

        # Annotate cooling period with MAPE
        ax2.annotate(f"MAPE {delta_T_rel.abs().mean():.1f}", (30, -250), textcoords="offset points", xytext=(50, -0), ha="center", fontsize=7,
                     color="black")

        # Annotate each peak with its APE
        for x, y in zip(delta_t_peaks, delta_T_peaks):
            ax2.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0, 15), ha="center", fontsize=7, color="#ff7f0e")

        # Finish plot
        ax2.set_ylim(-500, 1000)
        ax2.set_ylabel("$\Delta T$ [K]")
        ax2.set_xlabel("Time [s]")
        ax2.legend()
        ax2.grid(True)

        # Save plot  #########################################################################
        geometry_3D_LW = os.path.join(*Path(base_folder).parts[-2:])
        path_fig = Path(f"./figs/thermal_models/{geometry_3D_LW}/{box}")
        path_fig.mkdir(parents=True, exist_ok=True)
        if is_compare_to_layerwise:
            plt.savefig(Path(f"{path_fig}/thermal_sim_Abaqus_FD_{energy_density:.1e}_{suffix}_MAPE_APE_lw.png"))
        else:
            plt.savefig(Path(f"{path_fig}/thermal_sim_Abaqus_FD_{energy_density:.1e}_{suffix}_MAPE_APE_sr.png"))
        plt.close("all")


if __name__ == "__main__":
    apply_rcparams()
    torch.set_printoptions(linewidth=500, precision=4, sci_mode=True)

    # ####################################################################################
    # Default parameters #################################################################
    N = int(210)
    layer_thickness = 30e-6
    temp_model_kwargs_default = {
        "N": N,  # [-] Number of elements
        "L": layer_thickness * N,  # [m] Total length
        "G": 10,  # [-] Number of ghost elements
        "no_remelt": 0,
        "beta": 1 / (800 * 4500),  # 1 / (c_p * rho) [(K m^3)/J]
        "dt": 0.1e-3,  # [s] Time step
        "t_end": 50.0,  # [s] Total simulation time
        "k_conduction": 20,  # [W/mK] Thermal conductivity coefficient
        "k_radiation": 5.67e-8 * 0.26,  # [W/(m^2K^4)] Radiation coefficient
        "h_convection": 25,  # [W/(m^2K)] Convective heat transfer coefficient
        "T_x": 273.15 + 25,  # [K] Radiation temperature
        "T_inf": 273.15 + 25,  # [K] Ambient temperature for convection
        "T_bottom": 273.15 + 25,  # [K] Constant temperature at the bottom surface
        "Q_magnitude": 1e6,  # [W/m^2] Heat flux
        "Q_magnitude_remelt": 0.5e6,  # [W/m^2] Heat flux
        "Q_coef": 1.0,
        "Q_remelt_coef": 1.0,
        "q_dt_0": 4.5,
        "q_dt": 4.5,
        "absorptivity": 0.48,  # [-] Absorption coefficient
    }

    dfs_Abaqus = read_Abaqus_data("data\Abaqus_3D_scanres")

    ####################################################################################
    # Plot thin wall, cuboid, inverted pyramid for Hastelloy X #########################

    c_p_HX = 486  # [J/(kg K)] Hastelloy X Scheel
    rho_HX = 8220  # [kg/m^3] Hastelloy X Scheel
    absorptivity_HX = 0.48  # [-] Hastelloy X Scheel
    h_convection_HX = 25  # [W/(m^2K)] Hastelloy X Scheel
    k_conduction_HX = 15
    T_melt_HX = 1355 # [C]

    temp_model_kwargs_HX = copy.deepcopy(temp_model_kwargs_default)
    temp_model_kwargs_HX["beta"] = 1 / (c_p_HX * rho_HX)
    temp_model_kwargs_HX["k_conduction"] = k_conduction_HX
    temp_model_kwargs_HX["h_convection"] = h_convection_HX
    temp_model_kwargs_HX["absorptivity"] = absorptivity_HX

    base_folder = r"data\Abaqus_3D_layerw\thin_wall\inputs_gh_f1"
    plot_1to1_comparison(temp_model_kwargs_HX, base_folder, T_melt_HX, True, "thin_wall_HX")
    plot_1to1_comparison_MAPE_APE(temp_model_kwargs_HX, base_folder, T_melt_HX, True, "thin_wall_HX")
    plot_1to1_comparison_MAPE_APE(temp_model_kwargs_HX, base_folder, T_melt_HX, True, "thin_wall_HX", is_compare_to_layerwise=False)


    ####################################################################################
    # Plot thin wall, cuboid, inverted pyramid for Ti-6Al-4V ###########################

    c_p_Ti64 = 1130  # [J/(kg K)] Ti64 Proell 2024
    rho_Ti64 = 4090  # [kg/m^3] Ti64 Proell 2024
    absorptivity_Ti64 = 0.6  # [-] Ti64 Olleak 2024
    h_convection_Ti64 = 20  # [W/(m^2K)] Ti64 Olleak 2024
    k_conduction_Ti64 = 20
    T_melt_Ti64 = 1878-273  # [C] Ti64 Proell 2024

    temp_model_kwargs_Ti64 = copy.deepcopy(temp_model_kwargs_default)
    temp_model_kwargs_Ti64["beta"] = 1 / (c_p_Ti64 * rho_Ti64)
    temp_model_kwargs_Ti64["k_conduction"] = k_conduction_Ti64
    temp_model_kwargs_Ti64["h_convection"] = h_convection_Ti64
    temp_model_kwargs_Ti64["absorptivity"] = absorptivity_Ti64

    base_folder = r"data\Abaqus_3D_layerw\thin_wall\inputs_gh_f1_Ti64"
    plot_1to1_comparison(temp_model_kwargs_Ti64, base_folder, T_melt_Ti64, False, "thin_wall")
    plot_1to1_comparison_MAPE_APE(temp_model_kwargs_Ti64, base_folder, T_melt_Ti64, False, "thin_wall")

    base_folder = r"data\Abaqus_3D_layerw\cuboid\inputs_gh_f1_Ti64"
    plot_1to1_comparison(temp_model_kwargs_Ti64, base_folder, T_melt_Ti64, False, "cuboid")
    plot_1to1_comparison_MAPE_APE(temp_model_kwargs_Ti64, base_folder, T_melt_Ti64, False, "cuboid")

    base_folder = r"data\Abaqus_3D_layerw\inv_pyramid\inputs_gh_f1_Ti64"
    plot_1to1_comparison(temp_model_kwargs_Ti64, base_folder, T_melt_Ti64, False, "inv_pyramid")
    plot_1to1_comparison_MAPE_APE(temp_model_kwargs_Ti64, base_folder, T_melt_Ti64, False, "inv_pyramid")
