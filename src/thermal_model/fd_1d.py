import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from pathlib import Path
from matplotlib.colors import ListedColormap
import datetime
import PyQt5
import matplotlib as mpl
mpl.use("Qt5Agg")


class ThermalModel(torch.nn.Module):
    def __init__(self, N=100, L=1.0, G=5, no_remelt=0, beta=1 / (800 * 4500), dt=1e-2, t_end=50.0, k_conduction=30, k_radiation=5e-9, h_convection=20,
                 T_inf=298.0, T_bottom=500.0, T_x=298.0, Q_magnitude=5e6, Q_magnitude_remelt=1e6, absorptivity=0.5, **ignore_me):
        super().__init__()
        self.N = N
        self.L = L
        self.G = G
        self.no_remelt = no_remelt
        self.beta = beta
        self.dt = dt
        self.t_end = t_end
        self.k_conduction = k_conduction
        self.k_radiation = k_radiation
        self.h_convection = h_convection
        self.T_inf = torch.tensor([T_inf])
        self.T_bottom = torch.tensor([T_bottom])
        self.T_x = torch.tensor(T_x)
        self.Q_magnitude = Q_magnitude
        self.Q_magnitude_remelt = Q_magnitude_remelt
        self.dx = L / N
        self.time_values = []
        self.times_values_tmp = []
        self.temp_values = []
        self.absorptivity = absorptivity

        self.initialize_decoupled()

    def __call__(self, t, T):
        return self.forward(t, T)

    def v_func_analy(self, ts, time_step, ghost_node):

        vs_analy = self.compute_v_t_impulse(self.Lambda_diags[ghost_node], self.Cs[ghost_node], self.v_0s[ghost_node], time_period=ts, time_step=time_step)

        return vs_analy

    def compute_v_t_step(self,
                         lambda_tensor: torch.Tensor,
                         Q_mag_tensor: torch.Tensor,
                         v0_tensor: torch.Tensor,
                         time_period, # : float | torch.Tensor,
                         time_step, # : float | None = None,
                         ):

        if not torch.is_tensor(time_period):
            time_period = torch.tensor(time_period, device=lambda_tensor.device, dtype=lambda_tensor.dtype)
        if time_step is None:
            eval_time_steps = torch.atleast_1d(time_period)
        else:
            num_steps = torch.ceil((time_period - self.dt) / time_step).to(dtype=torch.int32)
            eval_time_steps = self.dt + torch.arange(0, num_steps, dtype=time_period.dtype, device=time_period.device) * time_step

        # Compute matrix exponential
        exp_lambda_t = torch.exp(lambda_tensor[None, :] * eval_time_steps[:, None])  # (time_steps, lambdas)

        # Initial condition
        # For lambda != 0
        term_non_zero = (exp_lambda_t - 1.0) / lambda_tensor[None, :]  # (time_steps, lambdas)
        # For lambda == 0, use limit (e^{lambda T} - 1 ) / lambda → T
        term_zero = eval_time_steps[:, None] * torch.ones_like(lambda_tensor)[None, :]  # (time_steps, lambdas)

        term = torch.where(lambda_tensor == 0, term_zero, term_non_zero)

        v_t = exp_lambda_t * v0_tensor + Q_mag_tensor * term

        return v_t.T

    def compute_v_t_impulse(self,
                            lambda_tensor: torch.Tensor,
                            Q_mag_tensor: torch.Tensor,
                            v0_tensor: torch.Tensor,
                            time_period, #: float | torch.Tensor,
                            time_step, #: float | None = None,
                            ):

        if not torch.is_tensor(time_period):
            time_period = torch.tensor(time_period, device=lambda_tensor.device, dtype=lambda_tensor.dtype)
        if time_step is None:
            eval_time_steps = torch.atleast_1d(time_period)
        else:
            eval_time_steps = torch.arange(self.dt, time_period, time_step, device=lambda_tensor.device, dtype=lambda_tensor.dtype)

        v0_plus = v0_tensor + Q_mag_tensor
        lambda_t = lambda_tensor[None, :] * eval_time_steps[:, None]  # (time_steps, lambdas)
        exp_lambda_t = torch.exp(lambda_t)  # (time_steps, lambdas)

        # Compute v(t) = v(0+) * e^{lambda t}
        v_t = v0_plus * exp_lambda_t  # (time_steps, lambdas) #

        return v_t.T

    def calculate_thetas(self, vs, ghost_node):
        current_thetas = self.Zs[ghost_node] @ vs

        return current_thetas

    def set_up_matrices(self, topmost_active_element, ghost_node, exposure):

        if ghost_node == exposure:
            Q_magnitude_exp = self.Q_magnitude
        else:
            Q_magnitude_exp = self.Q_magnitude_remelt

        # T_x for linearized radiation (Taylor expansion)
        T_x = self.T_x

        # Construct B
        B = torch.zeros_like(self.T[:topmost_active_element+1])
        B[topmost_active_element] = 1

        # Construct q
        q = torch.atleast_1d(torch.tensor(0.0))
        if ghost_node != 0:
            q += Q_magnitude_exp / (self.dx) * self.absorptivity
            q += + (self.h_convection * self.T_inf) / (self.dx)
            q += + (self.k_radiation * 3 * T_x**4 + self.k_radiation * self.T_inf**4) / (self.dx)
            q *= self.beta
        # print(f"Bq {B.unsqueeze(1) @ q}")

        # Construct A
        A = torch.zeros(size=(topmost_active_element+1, topmost_active_element+1))
        for i in range(1,topmost_active_element+1):
            for j in range(topmost_active_element+1):
                if i == j:
                    A[i,j] = -2 * self.k_conduction / (self.dx) ** 2

                    if i == 0:
                        A[i, j] += 1 * self.k_conduction / (self.dx) ** 2

                    if i == topmost_active_element:
                        A[i, j] = -1 * self.k_conduction / (self.dx) ** 2
                        A[i, j] += - self.h_convection / (self.dx)  - self.k_radiation * 4 * T_x**3 / (self.dx)

                if j-1 == i or j+1 == i:
                    A[i, j] = 1 * self.k_conduction / (self.dx) ** 2
        A *= 1 * self.beta
        # print(f"A {A}")

        # Eigenvalue decomposition
        Lambda_diag, Z = torch.linalg.eig(A)
        Z = Z.real.to(torch.float32)
        Lambda_diag = Lambda_diag.real.to(torch.float32)
        Lambda = torch.diag(Lambda_diag)
        Z_inv = torch.linalg.inv(Z)
        # print(f"Z {Z}")

        C = (Z_inv @ B).unsqueeze(1) @ q

        self.As.append(A)
        self.Bs.append(B)
        self.qs.append(q)

        self.Zs.append(Z)
        self.Z_invs.append(Z_inv)
        self.Lambdas.append(Lambda)
        self.Lambda_diags.append(Lambda_diag)
        self.Cs.append(C)

        # Compute theta_0 and v_0
        if topmost_active_element == (self.N - self.G - 1):
            # Construct Theta
            theta_0 = torch.atleast_2d(self.T[:topmost_active_element + 1]).T
            self.theta_0s.append(theta_0)

            # Compute v_0
            v_0 = Z_inv @ theta_0
            self.v_0s.append(v_0.squeeze(-1))

    def set_up_thermal_model(self):
        # Set up temperature model
        self.q_start_times_real = torch.cat([torch.atleast_1d(torch.tensor(0.0)), torch.cumsum(self.q_delta_times, dim=-1)])
        self.q_start_times = self.q_start_times_real.detach()

        self.layer_durations = torch.cat([self.q_delta_times, torch.atleast_1d(torch.tensor(self.t_end + self.dt)-self.q_start_times[-1])])

        self.q_end_times_real = torch.cat([torch.cumsum(self.q_delta_times, dim=-1), torch.atleast_1d(torch.tensor(self.t_end + self.dt))])
        self.q_end_times = self.q_end_times_real.detach()

        ghost_node = 0
        for exposure in range(self.G+1+self.no_remelt):
            topmost_active_element = (self.N - self.G - 1) + ghost_node

            # Calculate A, B, q, Lambda, Lambda_diag, Z and Z_inv for each new system
            self.set_up_matrices(topmost_active_element, ghost_node, exposure)

            # Calculate v_0 for the five timesteps at the end
            if ghost_node != 0:
                # theta_end of one layer to theta_0 of next layer
                if ghost_node == exposure:
                    self.theta_0s.append(torch.cat([self.theta_ends[exposure-1], torch.atleast_2d(self.T_inf)]))
                else:
                    self.theta_0s.append(self.theta_ends[exposure - 1])
                self.v_0s.append((self.Z_invs[exposure] @ self.theta_0s[exposure]).squeeze(-1))
            self.v_ends.append(self.v_func_analy(self.layer_durations[exposure], time_step=None, ghost_node=exposure))
            self.theta_ends.append(self.calculate_thetas(self.v_ends[exposure], exposure))

            if ghost_node < self.G:
                ghost_node += 1

    def run_simulation_decoupled(self):

        self.set_up_thermal_model()

        # Downsample time values
        time = 0.0
        time_values = []

        while time < self.t_end:
            # Compute distance to nearest q_start_time
            distance = torch.min(torch.abs(self.q_start_times - time)).item()

            # Choose step size based on distance
            if distance <= 1.0:
                dt = 1e-3
            elif distance <= 5.0:
                dt = 1e-1
            else:
                dt = 1e-1

            time_values.append(time)
            time += dt

        self.time_values = torch.tensor(time_values)

        T_history = self.eval_thermal_model(self.time_values)
        return T_history

    def eval_thermal_model(self, ts):
        thetas = []

        for exposure in range(self.G+1+self.no_remelt):
            timesteps_layer_mask = (ts >= self.q_start_times[exposure]) & (ts < self.q_end_times[exposure])
            if timesteps_layer_mask.sum() > 0:
                timesteps_layer = ts[timesteps_layer_mask] - self.q_start_times[exposure]
                vs_layer = self.v_func_analy(timesteps_layer, None, exposure)
                thetas_layer = self.calculate_thetas(vs_layer, exposure)
                thetas_layer_padded = torch.nn.functional.pad(thetas_layer, (0, 0, 0, self.N - thetas_layer.size(0)), mode='constant', value=self.T_inf.item())
                thetas.append(thetas_layer_padded)

        self.times_values_tmp.append(ts)
        self.temp_values_tmp.append(thetas)

        if ts.max() >= self.t_end-200*self.dt:
            time_values = self.times_values_tmp
            temp_values = self.temp_values_tmp
            time_values = torch.atleast_2d(torch.stack(time_values, dim=0))
            temp_values = torch.cat([tensor for sublist in temp_values for tensor in sublist], dim=1).T

            # Find unique time and temp values
            time_values, unique_indices = torch.unique(time_values, return_inverse=False, return_counts=False, dim=-1).sort()
            self.time_values = time_values.squeeze()
            self.temp_values = temp_values[unique_indices].squeeze().T

            self.times_values_tmp = []
            self.temp_values_tmp = []

        return torch.cat(thetas, dim=1)

    def initialize_decoupled(self):

        self.ghost_mask_init = torch.ones(self.N)
        self.ghost_mask_init[1:] = torch.tensor(0)
        self.T = torch.ones(self.N) * self.T_bottom * self.ghost_mask_init
        self.T = self.T + self.T_inf * (torch.ones(self.N) - self.ghost_mask_init)

        self.topmost_active_element = self.N - self.G - 1
        self.layer_activated = 0

        self.As = []
        self.Bs = []
        self.qs = []
        self.Cs = []
        self.Zs = []
        self.Z_invs = []
        self.Lambdas = []
        self.Lambda_diags = []
        self.v_ends = []
        self.v_0s = []
        self.theta_ends = []
        self.theta_0s = []

        self.thetas = []
        self.T_history = []
        self.time_values = []
        self.temp_values = []
        self.times_values_tmp = []
        self.temp_values_tmp = []

    def define_Q_t(self, delta_times, Q_magnitude, Q_magnitude_remelt):

        self.q_delta_times = delta_times
        self.Q_magnitude = Q_magnitude
        self.Q_magnitude_remelt = Q_magnitude_remelt


def plot_thermal_simulation(thermal_model, T_history, temp_model_kwargs, T_upper, elements_to_plot, suffix=""):
    print("\n# Plot thermal history")

    t_end = temp_model_kwargs["t_end"]
    dx = temp_model_kwargs["L"] / temp_model_kwargs["N"]

    # Cap high temperature values caused by instantaneous heat impulse in analytical solution
    T_history = torch.where(T_history > T_upper, torch.tensor(T_upper), T_history)

    # Set up figures
    fig, axs = plt.subplots(1, 2, figsize=(10, 6))
    ax1 = axs[0]
    ax2 = axs[1]

    # Heat map of temperature evolution
    ax1.imshow(T_history, aspect="auto", extent=[0, t_end, 0, dx*10], origin="lower", cmap="hot", interpolation="nearest")
    scalarmap = plt.cm.ScalarMappable(cmap="hot", norm=plt.Normalize(vmin=T_history.min(), vmax=T_history.max()))
    scalarmap.set_array(T_history)
    fig.colorbar(scalarmap, ax=ax1)
    ax1.set_title("Temperature heatmap over time")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Position [m]")

    # Temperature evolution for each element
    for i in range(temp_model_kwargs["N"]):

        if i in elements_to_plot:
            T_history_layer = T_history[-i]
            T_history_layer[T_history_layer == 0] = torch.nan
            ax2.plot(thermal_model.time_values, T_history_layer, ls="-", label=f"{i}")

    ax2.set_ylim(0, T_upper)
    ax2.hlines(995+273.15, xmin=0, xmax=t_end, label="$T_{as,start}$", color="black")
    ax2.hlines(935, xmin=0, xmax=t_end, label="$T_{as,end}$", ls="--", color="black")

    ax2.legend(title="Element from top", fontsize=8)
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Temperature [K]")
    ax2.set_title("Temperature at individual element")

    # Save the figure
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    subfolder = f"{current_date}{suffix}"
    Path(f"./figs/fd1d_time_evol/{subfolder}").mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"./figs/fd1d_time_evol/{subfolder}/fd1d_time_evol.png"))

    # plt.show()
    plt.close()


def plot_thermal_simulation_slider(thermal_model, T_history, time_eval_init, suffix=""):
    hex_colors = [
        "#FF0000", "#FF5C00", "#FFB900", "#E7FF00",
        "#8BFF00", "#2EFF00", "#00FF2E", "#00FF8B",
        "#00FFE7", "#00B9FF", "#005CFF", "#0000FF"
    ]

    hex_colors.reverse()

    time_eval = time_eval_init

    print("\n# Plot thermal history with slider")
    T_history -= 273.15  # Convert to Celsius

    fig, ax = plt.subplots(figsize=(16, 10))
    plt.subplots_adjust(bottom=0.3)  # Leave space for the slider

    x_start = 0
    x_end = 10
    extent = [x_start, x_end, 0, thermal_model.L]

    # Colormap and normalization
    # cmap = plt.cm.get_cmap("jet", 256).with_extremes(over='grey', under='white')
    cmap = ListedColormap(hex_colors).with_extremes(over='#CCCCCC', under='white')

    # Initial time index
    def get_time_index(t):
        return (torch.abs(thermal_model.time_values - t)).argmin()

    time_index = get_time_index(time_eval_init)
    T_at_time = T_history[:, time_index].unsqueeze(0).clone()

    # norm = plt.Normalize(vmin=20, vmax=T_at_time.max())
    norm = plt.Normalize(vmin=20, vmax=1300)

    # Mask trailing plateau values
    last_val = T_at_time[0, -1].clone()
    for i in reversed(range(T_at_time.shape[1])):
        if torch.abs(T_at_time[0, i] - last_val) > 1:
            break
        T_at_time[0, i] = -100.0

    img = ax.imshow(T_at_time.T, aspect="auto", extent=extent,
                    cmap=cmap, norm=norm, origin="lower", interpolation="nearest")

    # Add a fixed colorbar Axes on the right
    cbar_ax = fig.add_axes([0.91, 0.3, 0.02, 0.6], label='<colorbar>')  # [left, bottom, width, height]
    scalarmap = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    scalarmap.set_array([])
    cbar = plt.colorbar(scalarmap, cax=cbar_ax, label="Temperature [°C]", extend='max', ticks=np.linspace(20, 1300, 13))

    # Horizontal and vertical lines
    # mesh_horizontal = [-6., -5.,  -4.,  -3.,  -2.5, -2., -1.5, -1.125, -750.E-03, -656.25E-03, -562.5E-03,
    #                    -468.75E-03, -375.E-03, -281.25E-03, -187.5E-03, -93.75E-03, 0., 30.E-03, 60.E-03,
    #                    90.E-03, 120.E-03, 150.E-03, 180.E-03, 210.E-03, 240.E-03, 270.E-03, 300.E-03]
    # mesh_horizontal = [1e-3*(entry + 6) for entry in mesh_horizontal]
    # ax.hlines(mesh_horizontal, xmin=x_start, xmax=x_end, color="black", linewidth=0.5)
    # # ax.vlines([9*1e-3, 7*1e-3, 6*1e-3], ymin=0, ymax=thermal_model.L, color="black", linewidth=0.5)

    ax.set_xlabel("Length [mm]")
    ax.set_ylabel("Position [m]")
    ax.set_title(f"Temperature distribution at {time_eval_init:.4f}s")
    instr_string = "Press left/right arrow keys to go in 1e-4 s step size."
    instr_string += "\nPress previous/next buttons to go in 1e-2 s step size."
    instr_string += f"\nFirst 10 laser impulses at: {q_timesteps[0:10].numpy()} s"
    ax.annotate(instr_string, xy=(0.5, 0.2), xycoords='axes fraction', fontsize=12, color='black', ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1))

    # Add Slider
    ax_slider = plt.axes([0.15, 0.15, 0.7, 0.03])
    time_slider = Slider(ax_slider, 'Time [s]', float(thermal_model.time_values[0]),
                         float(thermal_model.time_values[-1]), valinit=time_eval_init, valstep=1e-4)


    # Buttons
    ax_prev = plt.axes([0.3, 0.05, 0.1, 0.05])
    ax_next = plt.axes([0.6, 0.05, 0.1, 0.05])
    btn_prev = Button(ax_prev, 'Previous')
    btn_next = Button(ax_next, 'Next')

    # Update function
    def update(val):
        time_eval = time_slider.val
        time_index = get_time_index(time_eval)
        T_new = T_history[:, time_index].unsqueeze(0).clone()

        last_val = T_new[0, -1].clone()
        for i in reversed(range(T_new.shape[1])):
            if torch.abs(T_new[0, i] - last_val) > 0.2:
                break
            T_new[0, i] = -100.0

        # norm = plt.Normalize(vmin=20, vmax=T_new.max())
        norm = plt.Normalize(vmin=20, vmax=1300)

        img.set_norm(norm)

        img.set_data(T_new.T)

        # Update colorbar in the same position
        # cbar_ax.cla()  # clear colorbar axis
        for myaxis in fig.axes[1:]:
            if myaxis._label.startswith('<colorbar>'):
                myaxis.remove()
        scalarmap = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        scalarmap.set_array([])
        cbar = plt.colorbar(scalarmap, cax=fig.add_axes([0.91, 0.3, 0.02, 0.6], label='<colorbar>'), label="Temperature [°C]", extend='max', ticks=np.linspace(20, 1300, 13))

        ax.set_title(f"Temperature distribution at {time_eval:.4f}s")
        fig.canvas.draw_idle()

    time_slider.on_changed(update)

    def on_prev(event):
        new_time = max(float(thermal_model.time_values[0]), time_slider.val - 1e-2)
        time_slider.set_val(new_time)

    def on_next(event):
        new_time = min(float(thermal_model.time_values[-1]), time_slider.val + 1e-2)
        time_slider.set_val(new_time)

    def on_key(event):
        if event.key == 'left':
            new_time = max(float(thermal_model.time_values[0]), time_slider.val - 1e-4)
            time_slider.set_val(new_time)
        elif event.key == 'right':
            new_time = min(float(thermal_model.time_values[-1]), time_slider.val + 1e-4)
            time_slider.set_val(new_time)

    btn_prev.on_clicked(on_prev)
    btn_next.on_clicked(on_next)
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Save the figure
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    subfolder = f"{current_date}{suffix}"
    Path(f"./figs/fd1d_vis/{subfolder}").mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"./figs/fd1d_vis/{subfolder}/fd1d_vis_t-{time_eval}s.png"))

    plt.show()
    # plt.close()


if __name__ == "__main__":

    torch.set_printoptions(linewidth=500, precision=4, sci_mode=True)

    # ####################################################################################
    # Parameters ######################################################################
    temp_model_kwargs = {
        "N": 200,  # [-] Number of elements
        "L": 30e-6 * 200,  # [m] Total length
        "G": 30,  # [-] Number of ghost elements
        "no_remelt": 0,
        "beta": 1 / (500 * 4000),  # 1 / (c_p * rho) [(K m^3)/J]
        "dt": 1e-3,  # [s] Time step
        "t_end": 300.0,  # [s] Total simulation time
        "k_conduction": 20,  # [W/mK] Thermal conductivity coefficient
        "k_radiation": 5.67e-8,  # [W/(m^2K^4)] Radiation coefficient
        "h_convection": 20,  # [W/(m^2K)] Convective heat transfer coefficient
        "T_x": 273.15 + 25,  # [K] Radiation temperature
        "T_inf": 273.15 + 25,  # [K] Ambient temperature for convection
        "T_bottom": 273.15 + 25,  # [K] Constant temperature at the bottom surface
        "Q_magnitude": 1.5e6,  # [W/m^2] Heat flux
        "Q_magnitude_remelt": (1/4) * 10e6,  # [W/m^2] Heat flux
        "Q_coef": 1.0,
        "Q_remelt_coef": 1.0,
        "q_dt_0": 4.5,
        "q_dt": 10,
        "q_dt_remelt": 0.056,
    }

    print("\n# Simulation parameters")
    print(f"k_conduction {temp_model_kwargs['k_conduction']} W/(m^2K), beta {temp_model_kwargs['beta']} (K m^3)/J, alpha {temp_model_kwargs['k_conduction']*temp_model_kwargs['beta']} (m^2)/s")
    print(f"h_convection {temp_model_kwargs['h_convection']} W/(m^2K), k_radiation {temp_model_kwargs['k_radiation']} W/(m^2K^4)")
    print(f"Q_magnitude {temp_model_kwargs['Q_magnitude']} W/m^2, T_bottom {temp_model_kwargs['T_bottom']} K")
    print(f"L {temp_model_kwargs['L']}, t_end {temp_model_kwargs['t_end']} s")
    print(f"dx {temp_model_kwargs['L']/temp_model_kwargs['N']} m, dx {temp_model_kwargs['L']/temp_model_kwargs['N']*10**6} µm")

    q_delta_times = torch.tensor([temp_model_kwargs["q_dt_0"]] + [temp_model_kwargs["q_dt"] for _ in range(temp_model_kwargs["G"])] + [temp_model_kwargs["q_dt_remelt"] for _ in range(temp_model_kwargs["no_remelt"] - 1)], dtype=torch.float32)
    q_timesteps = torch.cumsum(q_delta_times, dim=-1)
    print(f"q_timesteps {q_timesteps} s")

    # ####################################################################################
    # Run simulation #####################################################################
    print("\n# Run simulation")

    # Instantiate finite difference thermal model
    thermal_model_01 = ThermalModel(**temp_model_kwargs)

    # Define laser heat source
    thermal_model_01.define_Q_t(q_delta_times, temp_model_kwargs['Q_magnitude'], temp_model_kwargs['Q_magnitude_remelt'])

    # Run finite difference thermal simulation
    T_history = thermal_model_01.run_simulation_decoupled()

    # Plotting the results
    elements_to_plot = sorted([30, 29, 25, 20, 15, 14, 13],reverse=True)
    T_upper = 3000
    plot_thermal_simulation(thermal_model_01, T_history, temp_model_kwargs, T_upper, elements_to_plot)
    plot_thermal_simulation_slider(thermal_model_01, T_history, q_timesteps[1].item()+6e-4)

    # ####################################################################################


