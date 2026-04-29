from pathlib import Path
from typing import Tuple

import pandas as pd
import torch
from matplotlib import pyplot as plt
from datetime import datetime
from torch import nn
from torchviz import make_dot
import numpy as np

from src.thermal_model.fd_1d import ThermalModel

is_print = False
# epoch_iter = iter(range(5000))
# epoch_iter_02 = iter(range(5000))
is_print_duration = False


class MicrostructureThermalModel(nn.Module):
    def __init__(self, **kwargs):
        super(MicrostructureThermalModel, self).__init__()

        self.folder_name = kwargs.get("folder_name", "./")

        # Set default values similar to ThermalModel
        self.N = kwargs.get("N", 10)
        self.L = kwargs.get("L", 1.0)
        self.G = kwargs.get("G", 5)
        self.no_remelt = kwargs.get("no_remelt", 0)
        self.beta = kwargs.get("beta", 0.01)
        self.dt_temperature_model = kwargs.get("dt", 1e-3)
        self.t_end = kwargs.get("t_end", 10.0)
        self.k_conduction = kwargs.get("k_conduction", 22)
        self.k_radiation = kwargs.get("k_radiation", 5e-9)
        self.h_convection = kwargs.get("h_convection", 1e-6)
        self.T_inf = torch.tensor([kwargs.get("T_inf", 300.0)])
        self._base_T_bottom = torch.tensor([kwargs.get("T_bottom", 400.0)])
        self._base_Q_magnitude = kwargs.get("Q_magnitude", 1.5e6)
        self.q_delta_times_values = kwargs.get("q_delta_times_values", torch.tensor([0.5] + [2 for _ in range(self.G-1)], dtype=torch.float32))

        self.temp_offset = kwargs.get("temp_offset", torch.tensor(0.0))

        self.T_b_coef = nn.Parameter(torch.tensor(1.0, dtype=torch.float32, requires_grad=True))
        # self.T_b_coef = torch.tensor(1.0, dtype=torch.float32, requires_grad=True)
        self.Q_magnitude_coef = nn.Parameter(torch.tensor(kwargs.get("Q_magnitude_coef", 1), dtype=torch.float32, requires_grad=True))

        self.temperature_model = ThermalModel(N=self.N, L=self.L, G=self.G, no_remelt=self.no_remelt, beta=self.beta, dt=self.dt_temperature_model, t_end=self.t_end,
                                              k_conduction=self.k_conduction, k_radiation=self.k_radiation, h_convection=self.h_convection,
                                              T_inf=self.T_inf, T_bottom=self._base_T_bottom * self.T_b_coef,
                                              Q_magnitude=self._base_Q_magnitude * self.Q_magnitude_coef)

        # self.q_delta_times = nn.Parameter(
        #     self.q_delta_times_values.clone().detach().requires_grad_(True)
        # )

        self.q_delta_times = self.q_delta_times_values.clone().detach()

        T_0 = torch.zeros(self.N)
        T_0[:-self.G] = T_0[:-self.G] = self._base_T_bottom*self.T_b_coef
        self.T_0 = T_0
        self.times = []
        self.temps_tmp = []

        # Initialize other parameters
        self.T_melt = kwargs.get("melting_temp", torch.tensor(1600 + 273.15))
        self.T_beta_trans = kwargs.get("beta_transition_temp", torch.tensor(1000 + 273.15))
        self.T_ms = kwargs.get("martensite_start_temp", torch.tensor(575 + 273.15))  # (from Paper, p.12)
        # Constants formation of massive and martensitic alpha phase (from paper, p. 11, adopted from Elmer et al.)
        self.b_km = kwargs.get("b_km", torch.tensor(0.005))
        self.delta_t = kwargs.get("delta_t", torch.tensor(1 / 2000, requires_grad=False))
        self.min_temp = kwargs.get("min_temp", torch.tensor(0.0))
        self.max_temp = kwargs.get("max_temp", torch.tensor(2500.0))
        self.paths = {
            "t_1_gb_p1": Path("./kinetics/t_1_gb_p1.csv"),
            "t_1_gb_p2": Path("./kinetics/t_1_gb_p2.csv"),
            "t_50_gb_p1": Path("./kinetics/t_50_gb_p1.csv"),
            "t_50_gb_p2": Path("./kinetics/t_50_gb_p2.csv"),
            "t_1_w_p1": Path("./kinetics/t_1_w_p1.csv"),
            "t_1_w_p2": Path("./kinetics/t_1_w_p2.csv"),
            "t_50_w_p1": Path("./kinetics/t_50_w_p1.csv"),
            "t_50_w_p2": Path("./kinetics/t_50_w_p2.csv"),
        }
        self._initialized = False
        self._node_eval = 100

        self.x_agbs_tmp = []
        self.x_aws_tmp = []
        self.x_ams_tmp = []
        self.x_bs_tmp = []
        self.x_ms_tmp = []

        self.param_code = kwargs.get("param_code", "param_code_missing")
        self.epoch_iter_02 = kwargs.get("epoch_iter_02", 10)

        self.temperature_model.initialize_decoupled()

    def derive_temperature_profile(
        self,
    ):
        self.temperature_model.T_bottom = self._base_T_bottom * self.T_b_coef
        T_0 = torch.zeros(self.N)
        T_0[:-self.G] = self._base_T_bottom * self.T_b_coef
        self.T_0 = T_0

        self.temperature_model.initialize_decoupled()
        # q_times = torch.cumsum(self.q_delta_times, dim=-1)  # - min(self.q_delta_times[0].item(), 0)
        Q_magnitude = self._base_Q_magnitude*self.Q_magnitude_coef
        self.temperature_model.define_Q_t(self.q_delta_times, Q_magnitude)
        self.temperature_model.set_up_thermal_model()

        # Create computational graph
        if False:
            # Intermediate calculation of non-sensible loss only to generate computational graph
            min_len = min(self.times.size(-1), self.temps_tmp.size(-1))
            absolute_smooth_l1_loss = nn.SmoothL1Loss()
            loss = absolute_smooth_l1_loss(self.times[:min_len], self.temps_tmp[:min_len])
            # Visualize the computational graph before the backward pass
            dot = make_dot(loss, params=dict(self.named_parameters()), show_attrs=True, show_saved=True)
            dot.render("computational_graph", format="png")  # Save the graph as PNG
            print("Computational graph saved")

    def predict(self, times=None, temps=None, x_0=None):
        if temps is None:
            temps = self.temps_tmp
        else:
            self.temps_tmp = temps
        if times is None:
            times = self.times
        else:
            self.times = times
        if x_0 is None:
            x_0 = torch.tensor(
                [
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                ]
            )

        T_t_curve = torch.stack((times, temps + self.temp_offset), dim=1)
        # x_b_0, x_agb_0, x_aw_0, x_am_0 = x_0
        x_b_0, x_agb_0, x_aw_0, x_am_0 = self.state_to_components(x_0)
        x_a_0 = x_agb_0 + x_aw_0 + x_am_0
        x_m_0 = torch.tensor(0.0)

        # print(f"requires grad : T_t_curve: {T_t_curve.is_leaf}")
        x_agbs, x_ams, x_as, x_aws, x_bs, x_ms, times, Ts = self.run_microstr_model(
            times, temps, x_agb_0, x_aw_0, x_am_0, x_a_0, x_b_0, x_m_0, self.delta_t, torch.tensor(0.0), is_plot=True
        )
        # x = torch.tensor([x_agbs[-1], x_aws[-1], x_ams[-1], x_bs[-1], x_ms[-1]]) # breaks grad
        x = torch.vstack([x_bs, x_agbs, x_aws, x_ams]).T[-1]

        return x

    def forward(self, step: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        if not self._initialized:
            self.times_tmp = []
            self.temps_tmp = []
            self.x_agbs_tmp = []
            self.x_aws_tmp = []
            self.x_ams_tmp = []
            self.x_bs_tmp = []
            self.x_ms_tmp = []

            start_time = datetime.now()
            self.derive_temperature_profile()
            end_time = datetime.now()
            duration = end_time - start_time
            if is_print_duration: print("\n\t\tDuration [s] derive_temperature_profile():", duration.total_seconds())

            self._initialized = True
            # self._node_eval = self.G

        start_time = datetime.now()
        x_ip1 = self.run_microstr_model_step(step, x)
        end_time = datetime.now()
        duration = end_time - start_time
        if is_print_duration: print("\t\tDuration [s] run_murgau_step():\t", duration.total_seconds())

        delta_x_ip1 = x_ip1 - x
        derivative_x_ip1 = delta_x_ip1 / self.delta_t
        return derivative_x_ip1.squeeze()

    def reset_temperature_model(self):
        self._initialized = False

    def change_node_eval(self, node):
        self.times_tmp = []
        self.temps_tmp = []
        self.x_agbs_tmp = []
        self.x_aws_tmp = []
        self.x_ams_tmp = []
        self.x_bs_tmp = []
        self.x_ms_tmp = []
        self._node_eval = node

    def run_microstr_model(self, times, temps, x_agb, x_aw, x_am, x_a, x_b, x_m, delta_t, cool_rate, is_plot=False):

        # Set up time series
        # time_end = torch.max(times)
        # ts = torch.arange(0, time_end.item(), delta_t.item())
        ts = times
        num_steps = len(ts)

        # Initialize tensors to save time evolution of variables
        T_start = temps[0]
        Ts = torch.full((num_steps,), float("nan"))
        Ts[0] = T_start
        x_agbs = torch.full((num_steps,), float("nan"))
        x_agbs[0] = x_agb
        x_aws = torch.full((num_steps,), float("nan"))
        x_aws[0] = x_aw
        x_ams = torch.full((num_steps,), float("nan"))
        x_ams[0] = x_am
        x_as = torch.full((num_steps,), float("nan"))
        x_as[0] = x_a
        x_bs = torch.full((num_steps,), float("nan"))
        x_bs[0] = x_b
        x_ms = torch.full((num_steps,), float("nan"))
        x_ms[0] = x_m
        cool_rates = torch.full((num_steps,), float("nan"))
        cool_rates[0] = cool_rate

        # Loop over time steps
        for n in range(num_steps - 1):
            # Get (interpolated) temperature for current time step
            # Ts[n + 1] = self.linear_temp_interpolation(ts[n + 1])
            Ts[n + 1] = self.temps_tmp[n+1]
            if is_print:
                print(f"\nt {ts[n + 1]} T {Ts[n + 1]}")

            # Save cooling rate in list for cooling rate evolution over time
            cool_rates[n + 1] = (Ts[n] - Ts[n + 1]) / delta_t

            # Evaluate Murgau model
            (
                x_agbs[n + 1],
                x_aws[n + 1],
                x_ams[n + 1],
                x_bs[n + 1],
                x_ms[n + 1],
                x_as[n + 1],
                kin_data,
            ) = self.eval_timestep(delta_t, Ts[n + 1], Ts[n], x_bs[n], x_agbs[n], x_aws[n], x_ams[n], self.paths)

        # Plotting
        if is_plot:
            # plot_results_debug(x_agbs.detach(), x_ams.detach(), x_aws.detach(), x_bs.detach(), x_ms.detach(), ts.detach(), Ts.detach(), self.G,
            #                    self.folder_name, self.param_code, self.e_diffuse_am)
            plot_results(x_agbs.detach(), x_ams.detach(), x_aws.detach(), x_bs.detach(), x_ms.detach(), ts.detach(), Ts.detach(), self.G, self._node_eval,
                         self.folder_name, self.param_code)

        return x_agbs, x_ams, x_as, x_aws, x_bs, x_ms, ts, Ts

    def run_microstr_model_step(
            self,
            t_i: torch.Tensor,
            x_i: torch.Tensor,
    ) -> torch.Tensor:
        # Get (interpolated) temperature for current time step
        t_ip1 = t_i + self.delta_t

        Ts_i = self.temperature_model.eval_thermal_model(t_i)[-self._node_eval] + self.temp_offset
        Ts_ip1 = self.temperature_model.eval_thermal_model(t_ip1)[-self._node_eval] + self.temp_offset

        # if t_ip1 >= self.t_end-self.delta_t:
        #     self.times_tmp = self.temperature_model.time_values
        #     self.temps_tmp = self.temperature_model.temp_values[-self.temperature_model.G]

        if is_print:
            print(f"\nt {t_ip1} T {Ts_ip1}")

        # Break to state components
        x_bs_i, x_agbs_i, x_aws_i, x_ams_i = self.state_to_components(x_i)

        # Evaluate Murgau model
        start_time = datetime.now()
        (x_agbs_ip1, x_aws_ip1, x_ams_ip1, x_bs_ip1, x_ms_ip1, *_) = self.eval_timestep(
            self.delta_t, Ts_ip1, Ts_i, x_bs_i, x_agbs_i, x_aws_i, x_ams_i, self.paths
        )
        end_time = datetime.now()
        duration = end_time - start_time
        if is_print_duration: print("\n\t\tDuration [s] eval_timestep():\t", duration.total_seconds())

        if t_i == 0:
            self.times_tmp.append(torch.atleast_1d(t_i))
            self.temps_tmp.append(torch.atleast_1d(Ts_i))
            self.x_agbs_tmp.append(torch.atleast_1d(x_agbs_i))
            self.x_aws_tmp.append(torch.atleast_1d(x_aws_i))
            self.x_ams_tmp.append(torch.atleast_1d(x_ams_i))
            self.x_bs_tmp.append(torch.atleast_1d(x_bs_i))
            self.x_ms_tmp.append(torch.atleast_1d(torch.tensor(0.0)))

        self.times_tmp.append(torch.atleast_1d(t_ip1))
        self.temps_tmp.append(torch.atleast_1d(Ts_ip1))
        self.x_agbs_tmp.append(torch.atleast_1d(x_agbs_ip1))
        self.x_aws_tmp.append(torch.atleast_1d(x_aws_ip1))
        self.x_ams_tmp.append(torch.atleast_1d(x_ams_ip1))
        self.x_bs_tmp.append(torch.atleast_1d(x_bs_ip1))
        self.x_ms_tmp.append(torch.atleast_1d(x_ms_ip1))

        # Recompose state
        # x_ip1 = torch.cat([x_bs_ip1, x_agbs_ip1, x_aws_ip1, x_ams_ip1])
        x_ip1 = self.components_to_state(x_bs_ip1, x_agbs_ip1, x_aws_ip1, x_ams_ip1)

        # Plot results
        if t_ip1 >= self.t_end-self.delta_t:
            self.x_agbs = torch.cat(self.x_agbs_tmp)
            self.x_ams = torch.cat(self.x_ams_tmp)
            self.x_aws = torch.cat(self.x_aws_tmp)
            self.x_bs = torch.cat(self.x_bs_tmp)
            self.x_ms = torch.cat(self.x_ms_tmp)
            self.times = torch.cat(self.times_tmp)
            self.temps = torch.cat(self.temps_tmp)

            plot_results(self.x_agbs.detach(), self.x_ams.detach(), self.x_aws.detach(), self.x_bs.detach(), self.x_ms.detach(), self.times.detach(),
                         self.temps.detach(), self.G, self._node_eval, self.folder_name, self.param_code)

        return x_ip1

    def eval_timestep(self, delta_t, Tnp1, Tn, x_b_n, x_agb_n, x_aw_n, x_am_n, paths):
        # Implementation of Paper "A model for Ti-6Al-4V microstructure evolution for arbitrary temperature changes",
        # Murgau et al. 2012, MSEA and thesis
        if is_print:
            print(f"x_b {x_b_n}, x_agb {x_agb_n}, x_aw {x_aw_n}, x_am {x_am_n}, delta_t {delta_t}, Tnp1 {Tnp1}, Tn {Tn}")

        # Determine current JMAK transformation kinetic parameters
        N_agb, k_agb = self.calc_kinetic_param_agb(
            Tnp1,
            self.T_beta_trans,
            paths["t_1_gb_p1"],
            paths["t_1_gb_p2"],
            paths["t_50_gb_p1"],
            paths["t_50_gb_p2"],
        )
        N_aw, k_aw = self.calc_kinetic_param_aw(
            Tnp1,
            self.T_beta_trans,
            paths["t_1_w_p1"],
            paths["t_1_w_p2"],
            paths["t_50_w_p1"],
            paths["t_50_w_p2"],
        )

        # Compute material parameter for current temperature
        N_am, k_am = self.calc_kinetic_param_am(Tnp1)

        kin_data = {
            "N_agb": N_agb,
            "k_agb": k_agb,
            "N_aw": N_aw,
            "k_aw": k_aw,
            "N_am": N_am,
            "k_am": k_am,
        }

        # Initialize new values with old ones
        x_agb_np1 = x_agb_n.clone()
        x_aw_np1 = x_aw_n.clone()
        x_am_np1 = x_am_n.clone()
        x_b_np1 = x_b_n.clone()
        x_a_n = x_agb_n + x_aw_n + x_am_n
        x_m_np1 = torch.tensor(0)

        # Compute cooling rate
        cool_rate = (Tn - Tnp1) / delta_t
        if is_print:
            print(f"cool_rate {cool_rate.item()}")

        # Evaluate if current temperature is above or below melting temperature
        # Liquid phase
        if Tnp1 >= self.T_melt:
            # Set all volume fractions to zero accordingly
            x_agb_np1 = Tnp1 * 0  # breaks grad
            x_aw_np1 = Tnp1 * 0  # breaks grad
            x_am_np1 = Tnp1 * 0  # breaks grad
            # x_b_np1 = Tnp1 * 0  # breaks grad
            x_a_np1 = x_agb_np1 + x_aw_np1 + x_am_np1
            # x_m_np1 = Tnp1 / Tnp1
            x_m_np1 = Tnp1 * 0  # breaks grad
            x_b_np1 = Tnp1 / Tnp1
        # Solid phase
        else:
            # Calculate equilibrium phase fraction
            x_a_eq_np1, x_b_eq_np1 = self.calc_equ_phase_fracs(Tnp1)
            kin_data["x_a_eq_np1"] = x_a_eq_np1
            kin_data["x_b_eq_np1"] = x_b_eq_np1

            # Check if beta phase is decomposed or recovered (current fraction above or below equilibrium fraction)
            # Decomposition of beta phase into grain boundary, Widmanstaetten and massive/martensitic alpha phase
            if x_b_np1 > x_b_eq_np1 or (x_b_np1 == x_b_eq_np1 and cool_rate > 0):  # ToDo second part necessary
                # current knowledge: (x_b_np1 == x_b_eq_np1 and cool_rate > 0) --> to consider the cases where x_b_np1 == x_b_eq_np1
                # but alpha martensite is supposed to form nevertheless because we are cooling down (=cool_rate>0)

                # Formation of grain boundary alpha phase
                x_agb_np1 = self.form_agb(x_a_eq_np1, x_agb_np1, x_agb_n, x_aw_n, x_b_n, N_agb, k_agb, delta_t)

                # Formation of Widmanstaetten alpha phase
                x_aw_np1 = self.form_aw(x_a_eq_np1, x_aw_np1, x_agb_n, x_aw_n, x_b_n, N_aw, k_aw, delta_t)

                # Formation of massive and martensitic alpha phase
                x_am_np1 = self.form_am(Tnp1, self.T_ms, x_am_np1, x_b_eq_np1, x_am_n, x_b_n, self.b_km, cool_rate)

                # Sum all alpha phase fractions and derive fraction of beta phase
                x_a_np1 = x_agb_np1 + x_aw_np1 + x_am_np1
                x_b_np1 = torch.tensor(1.0) - x_a_np1

            # Recovery of beta phase from various alpha phases
            else:
                # Formation of beta and Widmanstaetten alpha phase due to diffusion of massive and martensitic alpha phase
                x_am_np1, x_aw_np1 = self.diffuse_am(
                    Tnp1,
                    self.T_ms,
                    x_am_n,
                    x_am_np1,
                    x_aw_n,
                    x_aw_np1,
                    x_b_eq_np1,
                    x_b_n,
                    self.b_km,
                    N_am,
                    k_am,
                    delta_t,
                )

                x_a_np1 = x_agb_np1 + x_aw_np1 + x_am_np1

                # Formation of beta phase due to dissolution of alpha phase (parabolic growth law)
                x_agb_np1, x_aw_np1 = self.dissolve_aw_agb(
                    Tnp1,
                    x_a_eq_np1,
                    x_a_np1,
                    x_agb_np1,
                    x_am_np1,
                    x_aw_np1,
                    x_b_eq_np1,
                    x_b_n,
                    delta_t,
                )

                # Compute sum of all alpha phase volume fractions
                x_a_np1 = x_agb_np1 + x_aw_np1 + x_am_np1
                x_b_np1 = torch.tensor(1.0) - x_a_np1

        return x_agb_np1, x_aw_np1, x_am_np1, x_b_np1, x_m_np1, x_a_np1, kin_data

    def calc_equ_phase_fracs(self, T):
        # Equilibrium Phase Fraction (from paper); Temperature in Kelvin
        if T < 924:
            # x_a_eq_np1 = torch.tensor(0.9157)  # breaks grad
            x_a_eq_np1 = torch.tensor(0.9157) * T / T
        else:
            if 924 <= T < 1273:
                x_a_eq_np1 = torch.tensor(0)
                P = torch.tensor(
                    [
                        -31188.514,
                        170526.26,
                        -388991.69,
                        471927.45,
                        -315178.49,
                        99079.891,
                        1667.1991,
                        -9726.8403,
                        1884.728,
                    ]
                )
                for i in range(len(P)):
                    x_a_eq_np1 = x_a_eq_np1 + P[i] * ((T - 273.15) / 1000) ** (8 - i)
                if x_a_eq_np1 < 0:
                    # x_a_eq_np1 = torch.tensor(0)  # breaks grad
                    x_a_eq_np1 = torch.tensor(0) * T
            else:
                # x_a_eq_np1 = torch.tensor(0) # breaks grad
                x_a_eq_np1 = torch.tensor(0) * T

        # Equilibrium Phase Fraction for beta phase (decides if beta is decomposed or formed)
        x_b_eq_np1 = torch.tensor(1) - x_a_eq_np1

        return x_a_eq_np1, x_b_eq_np1

    def form_agb(self, x_a_eq_np1, x_agb_np1, x_agb_n, x_aw_n, x_b_n, N_agb, k_agb, delta_t):
        if is_print:
            print("form_agb")
        if x_a_eq_np1 != 0:  # ToDo if clause necessary?
            if k_agb > 0:

                # Compute fictitious time
                if not (1 - ((x_aw_n + x_agb_n) / (x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n)))) >= 1:
                    t_cgb = (
                                    -torch.log(1 - ((x_aw_n + x_agb_n) / (x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n)))) / k_agb
                            ) ** (1 / N_agb)
                else:
                    t_cgb = x_aw_n * torch.tensor(0)

                # Compute volume fraction of grain boundary alpha phase
                # x_agb_np1 = (1 - np.exp(- k_agb * (t_cgb + delta_t) ** N_agb)) * x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n) - x_aw_n
                e_form_agb = 1 - torch.exp(-k_agb * (t_cgb + delta_t) ** N_agb)
                x_agb_np1 = e_form_agb * x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n) - x_aw_n

            else:
                x_agb_np1 = x_agb_np1 * N_agb / N_agb

        else:
            # x_agb_np1 = torch.tensor(0.0)  # Breaks grad
            x_agb_np1 = torch.tensor(0.0) * x_agb_np1
            # current knowledge: needed for the cases where x_b_np1 == x_b_eq_np1 but we need to enter beta decomposition mode nevertheless
            # as we might form alpha martensite phase

        return x_agb_np1

    def form_aw(self, x_a_eq_np1, x_aw_np1, x_agb_n, x_aw_n, x_b_n, N_aw, k_aw, delta_t):
        if is_print:
            print("form_aw")

        # Current knowledge: because of the case where beta decomposition is only entered to allow alpha martensite formation despite x_b_np1 == x_b_eq_np1
        if x_a_eq_np1 != 0:
            if k_aw > 0:
                # Compute fictitious time
                if not (1 - ((x_aw_n + x_agb_n) / (x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n)))) >= 1:
                    t_cw = (
                                   -torch.log(1 - ((x_aw_n + x_agb_n) / (x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n)))) / k_aw
                           ) ** (1 / N_aw)
                else:
                    t_cw = x_aw_n * torch.tensor(0)

                # Compute volume fraction of Widmannstaetten alpha phase
                # x_aw_np1 = (1 - np.exp(- k_aw * (t_cw + delta_t) ** N_aw)) * x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n) - x_agb_n

                e_form_aw = 1 - torch.exp(-k_aw * (t_cw + delta_t) ** N_aw)
                x_aw_np1 = e_form_aw * x_a_eq_np1 * (x_b_n + x_aw_n + x_agb_n) - x_agb_n

            else:
                x_aw_np1 = x_aw_np1 * N_aw / N_aw
        else:
            x_aw_np1_old = x_aw_np1 * N_aw / N_aw
            # x_aw_np1 = torch.tensor(0.0)  # breaks grad
            x_aw_np1 = torch.tensor(0.0) * x_aw_np1
            # if x_aw_np1_old != x_aw_np1:
            #     print(f"x_aw_n = {x_aw_np1_old} / x_aw_n = {x_aw_np1}")
            # current knowledge: needed for the cases where x_b_np1 == x_b_eq_np1 but we need to enter beta decomposition mode nevertheless
            # as we might form alpha martensite phase

        return x_aw_np1

    def form_am(self, T, T_ms, x_am_np1, x_b_eq_np1, x_am_n, x_b_n, b_km, cool_rate):
        if is_print:
            print("form_am")

        if T <= T_ms:
            # Cooling rate > 410 C/s
            if cool_rate > 410:
                # delta_x_am_np1 = (1 - np.exp(- b_km * (T_ms - T))) * (x_b_n + x_am_n) - x_am_n
                e_form_am = 1 - torch.exp(-b_km * (T_ms - T))
                delta_x_am_np1 = e_form_am * (x_b_n + x_am_n) - x_am_n
                if delta_x_am_np1 > 0:
                    x_am_np1 = x_am_n + delta_x_am_np1
                else:
                    x_am_np1 = x_am_n * T / T

            # 410 C/s > cooling rate > 20 C/s
            elif cool_rate > 20:
                # Note: here mismatch between paper E and paper C in terms of x_b_eq; in thesis
                # delta_x_am_np1 = (1 - np.exp(- b_km * (T_ms - T))) * (x_b_n + x_am_n - x_b_eq_np1) - x_am_n  # ToDo - x_am_n - x_am_n
                e_form_am = 1 - torch.exp(-b_km * (T_ms - T))
                delta_x_am_np1 = e_form_am * (x_b_n + x_am_n - x_b_eq_np1) - x_am_n
                if delta_x_am_np1 > 0:
                    x_am_np1 = x_am_n + delta_x_am_np1
                else:
                    x_am_np1 = x_am_n * T / T

            # Cooling rate < 20 C/s
            else:
                x_am_np1 = x_am_n * T / T

        return x_am_np1

    def diffuse_am(
            self,
            T,
            T_ms,
            x_am_n,
            x_am_np1,
            x_aw_n,
            x_aw_np1,
            x_b_eq_np1,
            x_b_n,
            b_km,
            N_am,
            k_am,
            delta_t,
    ):
        if is_print:
            print("diffuse_am")

        if x_am_n > 0:

            # Compute equilibrium fraction of massive and martensitic alpha phase
            # Note: Calculation of martensite equilibrium not clear
            x_am_eq_np1 = (1 - torch.exp(-b_km * (T_ms - T)))  # * (x_b_n + x_am_n - x_b_eq_np1)

            # T_range = torch.linspace(250, 1400, 1000)
            # x_b_n = 0.5  # Placeholder value for beta phase fraction at current step
            # x_am_n = 0.5  # Placeholder value for martensitic alpha phase
            # x_b_eq_np1 = 0.75  # Placeholder value for equilibrium beta phase fraction
            #
            # x_am_eq_np1_values = [(1 - torch.exp(-b_km * (T_ms - T))) * (x_b_n + x_am_n - x_b_eq_np1) for T in T_range]
            # x_am_eq_np1_values2 = [(1 - torch.exp(-b_km * (T_ms - T)))  for T in T_range]
            #
            #
            # plt.plot(T_range.numpy(), [x.item() for x in x_am_eq_np1_values], label="x_am_eq_np1")
            # plt.plot(T_range.numpy(), [x.item() for x in x_am_eq_np1_values2], label="x_am_eq_np1 2")
            # plt.xlabel("Temperature (T)")
            # plt.ylabel("x_am_eq_np1")
            # plt.title("x_am_eq_np1 vs Temperature")
            # plt.legend()
            # plt.ylim(0, 1)
            # plt.grid()
            # plt.show()
            
            
            
            # (a_eq value minus the other parts or Koistinen-Marburger?)
            # x_am_eq_np1 = x_a_eq_np1 - x_agb_n - x_aw_n
            # x_am_eq_np1 = 1 - exp(-b_km * (T_ms - T)) * x_b_np1
            # x_am_eq_np1 = 1 - x_b_eq_np1
            # x_am_eq_np1 = 0.91

            if x_am_eq_np1 < 0:
                x_am_eq_np1 = torch.tensor(0) * T
            if x_am_n < x_am_eq_np1:
                x_am_eq_np1 = x_am_n
            # if T < 300:
            #     x_am_eq_np1 = torch.tensor(0.9)

            if (k_am > 0) and (x_am_n != x_am_eq_np1):
                # Compute fictitious time
                # Note: Here is also a difference to thesis Paper E in terms of x_am_n difference between paper C and E
                # in terms of the x_am_eq_np1 being within brackets
                t_cm = (-torch.log(((x_am_n - x_am_eq_np1) / (x_b_n + x_am_n - x_am_eq_np1))) / k_am) ** (1 / N_am)

                # Compute new volume fraction of massive and martensitic alpha phase
                # x_am_np1 = x_am_eq_np1 - (np.exp(- k_am * (t_cm + delta_t / 60) ** N_am)) * (x_b_n + x_am_n - x_am_eq_np1)
                # e_diffuse_am = torch.exp(-k_am * (t_cm + delta_t / 60) ** N_am)
                e_diffuse_am = torch.exp(-k_am * (t_cm + delta_t) ** N_am)
                x_am_np1 = x_am_eq_np1 - e_diffuse_am * (x_b_n + x_am_n - x_am_eq_np1)
                if x_am_np1 < 0:
                    x_am_np1 = torch.tensor(0) * T

                # Compute delta of volume fraction of massive and martensitic alpha phase
                delta_x_am_np1 = x_am_np1 - x_am_n

                # Compute new volume fraction of Widmanstaetten alpha phase
                x_aw_np1 = x_aw_n + torch.abs(delta_x_am_np1) * (1 - x_b_eq_np1)  # ToDo Why abs?

                # Compute new volume fraction of beta phase
                x_b_np1 = x_b_n + torch.abs(delta_x_am_np1) * x_b_eq_np1

                e_diffuse_am = x_am_np1

        return x_am_np1, x_aw_np1

    def dissolve_aw_agb(
            self,
            T,
            x_a_eq_np1,
            x_a_np1,
            x_agb_np1,
            x_am_np1,
            x_aw_np1,
            x_b_eq_np1,
            x_b_n,
            delta_t,
    ):
        if is_print:
            print("dissolve_aw_agb")

        # Widmanstaetten alpha phase dissolves first, then grain boundary alpha phase

        # Compute f_diss ToDo
        f_diss = 2.2e-31 * T ** 9.89
        # Compute critical time
        t_crit = f_diss ** -2
        # Compute fictious time
        t_star = (x_b_n / (x_b_eq_np1 * f_diss)) ** 2

        # Compute amount of alpha phase to dissolve
        if (delta_t + t_star) > t_crit:
            X_diss = x_a_eq_np1
            X_diss2 = 1 - x_b_eq_np1
        else:
            X_diss = 1 - x_b_eq_np1 * f_diss * torch.sqrt(delta_t + t_star)

        # Compute new volume fractions of Widmanstaetten and grain boundary alpha phase
        if x_a_np1 > X_diss:
            # Dissolve Widmanstaetten alpha phase first
            if x_aw_np1 > 0:
                x_aw_np1 = X_diss - x_agb_np1 - x_am_np1
                if x_aw_np1 < 0:
                    x_aw_np1 = torch.tensor(0) * T  # ToDo Why mention all phases?
                    x_agb_np1 = X_diss - x_am_np1
                    if x_agb_np1 < 0:
                        x_agb_np1 = torch.tensor(0) * T

            # Dissolve grain boundary alpha phase once Widmanstaetten alpha phase is fully dissolved
            else:
                x_agb_np1 = X_diss - x_am_np1
                if x_agb_np1 < 0:
                    x_agb_np1 = torch.tensor(0) * T

        return x_agb_np1, x_aw_np1

    def calc_kinetic_param_agb(
            self,
            T,
            T_beta_trans,
            path_t_1_gb_p1,
            path_t_1_gb_p2,
            path_t_50_gb_p1,
            path_t_50_gb_p2,
    ):
        # JMAK transformation kinetic parameter for grain boundary phase

        if T_beta_trans > T >= torch.tensor(350.0 + 273.15):

            # TTT curve for 1 % grain boundary alpha phase (Fig. 11 Paper)
            # Note: 1000000 acts as a placeholder value which has to be replaced by T_beta_trans
            t_1_gb_p1 = pd.read_csv(path_t_1_gb_p1).to_numpy()
            t_1_gb_p1 = torch.tensor(t_1_gb_p1, dtype=torch.float32)

            t_1_gb_p2 = pd.read_csv(path_t_1_gb_p2).replace(1000000, T_beta_trans.item() - 273.15).to_numpy()
            t_1_gb_p2 = torch.tensor(t_1_gb_p2, dtype=torch.float32)

            # TTT curve for 50 % GB (Fig. 11 Paper)
            # Note: 1000000 acts as a placeholder value which has to be replaced by T_beta_trans
            t_50_gb_p1 = pd.read_csv(path_t_50_gb_p1).to_numpy()
            t_50_gb_p1 = torch.tensor(t_50_gb_p1, dtype=torch.float32)

            t_50_gb_p2 = pd.read_csv(path_t_50_gb_p2).replace(1000000, T_beta_trans.item() - 273.15).to_numpy()
            t_50_gb_p2 = torch.tensor(t_50_gb_p2, dtype=torch.float32)

            # Transform T from K to C
            T_celsius = T - torch.tensor(273.15)

            # Interpolate time after which 1 % grain boundary alpha is formed at current temperature
            # 350 <= T_celsius < 896
            if 350 <= T_celsius < 896:
                # Find index with temperature closest (and larger) to current temperature
                ind = torch.max(torch.nonzero(t_1_gb_p1[:, 1] >= T_celsius)).item()
                # ind = np.amax(find(T_celsius - t_1_gb_p1(:, 2) <= 0))

                # Interpolate time for current temperature
                t_1_gb = ((t_1_gb_p1[ind + 1, 0] - t_1_gb_p1[ind, 0]) / (t_1_gb_p1[ind + 1, 1] - t_1_gb_p1[ind, 1])) * (
                        T_celsius - t_1_gb_p1[ind, 1]
                ) + t_1_gb_p1[ind, 0]

            else:
                # 896 <= T_celsius < 1000
                if 896 <= T_celsius < 1000:
                    # Find index with temperature closest (and larger) to current temperature
                    ind = torch.max(torch.nonzero(t_1_gb_p2[:, 1] <= T_celsius)).item()
                    # ind = np.amax(find(T_celsius - t_1_gb_p2(:, 2) >= 0))

                    # Interpolate time for current temperature
                    t_1_gb = (
                                     (t_1_gb_p2[ind + 1, 0] - t_1_gb_p2[ind, 0]) / (t_1_gb_p2[ind + 1, 1] - t_1_gb_p2[ind, 1])
                             ) * (T_celsius - t_1_gb_p2[ind, 1]) + t_1_gb_p2[ind, 0]

            # Interpolate time after which 50 % grain boundary alpha is formed at current temperature
            # 350 <= T_celsius < 833
            if 350 <= T_celsius < 833:
                # Find index with temperature closest (and larger) to current temperature
                ind = torch.max(torch.nonzero(t_50_gb_p1[:, 1] >= T_celsius)).item()
                # ind = np.amax(find(T_celsius - t_50_gb_p1(:, 2) <= 0))

                # Interpolate time for current temperature
                t_50_gb = (
                                  (t_50_gb_p1[ind + 1, 0] - t_50_gb_p1[ind, 0]) / (t_50_gb_p1[ind + 1, 1] - t_50_gb_p1[ind, 1])
                          ) * (T_celsius - t_50_gb_p1[ind, 1]) + t_50_gb_p1[ind, 0]

            else:
                # 833 <= T_celsius < 1000
                if 833 <= T_celsius < 1000:
                    # Find index with temperature closest (and larger) to current temperature
                    ind = torch.max(torch.nonzero(t_50_gb_p2[:, 1] <= T_celsius)).item()
                    # ind = np.amax(find(T_celsius - t_50_gb_p2(:, 2) >= 0))

                    # Interpolate time for current temperature
                    t_50_gb = (
                                      (t_50_gb_p2[ind + 1, 0] - t_50_gb_p2[ind, 0]) / (t_50_gb_p2[ind + 1, 1] - t_50_gb_p2[ind, 1])
                              ) * (T_celsius - t_50_gb_p2[ind, 1]) + t_50_gb_p2[ind, 0]

            # Compute JMAK kinetic parameters
            # Note: This value is as expected, about 1.25
            N_agb = torch.log10(
                torch.log(torch.tensor(1.0) - torch.tensor(0.01)) / torch.log(torch.tensor(1.0) - torch.tensor(0.5))
            ) / torch.log10(t_1_gb / t_50_gb)
            # N_agb=1.4;
            # Note: k_gb is a bit smaller than expected (e.g. 0.0012 at 800 C))
            k_agb = -torch.log(torch.tensor(1.0) - torch.tensor(0.01)) / (t_1_gb ** N_agb)

        # !(T_beta_trans > T >= 350 + 273.15)
        else:
            # N_agb = torch.tensor(1.0) # breaks grad
            N_agb = T / T
            # k_agb = torch.tensor(0.0) # breaks grad
            k_agb = T * 0

        return N_agb, k_agb

    def calc_kinetic_param_aw(
            self,
            T,
            T_beta_trans,
            path_t_1_w_p1,
            path_t_1_w_p2,
            path_t_50_w_p1,
            path_t_50_w_p2,
    ):
        # JMAK transformation kinetic parameter for Widmannstaetten alpha-phases

        if T_beta_trans > T >= torch.tensor(260.0 + 273.15):

            # TTT curve for 1 % Widmanstaetten alpha phase (Fig. 11 Paper)
            # Note: 1000000 acts as a placeholder value which has to be replaced by T_beta_trans
            t_1_w_p1 = pd.read_csv(path_t_1_w_p1).to_numpy()
            t_1_w_p1 = torch.tensor(t_1_w_p1, dtype=torch.float32)

            t_1_w_p2 = pd.read_csv(path_t_1_w_p2).replace(1000000, T_beta_trans.item() - 273.15).to_numpy()
            t_1_w_p2 = torch.tensor(t_1_w_p2, dtype=torch.float32)

            # TTT curve for 50 % Widmanstaetten alpha phase (Fig. 11 Paper)
            # Note: 1000000 acts as a placeholder value which has to be replaced by T_beta_trans
            t_50_w_p1 = pd.read_csv(path_t_50_w_p1).to_numpy()
            t_50_w_p1 = torch.tensor(t_50_w_p1, dtype=torch.float32)

            t_50_w_p2 = pd.read_csv(path_t_50_w_p2).replace(1000000, T_beta_trans.item() - 273.15).to_numpy()
            t_50_w_p2 = torch.tensor(t_50_w_p2, dtype=torch.float32)

            # Transform T from K to C
            Tcelsius = T - torch.tensor(273.15)

            # Interpolate time after which 1 % Widmanstaetten alpha is formed at current temperature
            if 260 <= Tcelsius < 706:
                # Find index with temperature closest (and larger) to current temperature
                ind = torch.max(torch.nonzero(t_1_w_p1[:, 1] >= Tcelsius)).item()

                # Interpolate time for current temperature
                t_1_w = ((t_1_w_p1[ind + 1, 0] - t_1_w_p1[ind, 0]) / (t_1_w_p1[ind + 1, 1] - t_1_w_p1[ind, 1])) * (
                        Tcelsius - t_1_w_p1[ind, 1]
                ) + t_1_w_p1[ind, 0]
            else:
                if 706 <= Tcelsius < 1000:
                    # Find index with temperature closest (and larger) to current temperature
                    ind = torch.max(torch.nonzero(t_1_w_p2[:, 1] <= Tcelsius)).item()

                    # Interpolate time for current temperature
                    t_1_w = ((t_1_w_p2[ind + 1, 0] - t_1_w_p2[ind, 0]) / (t_1_w_p2[ind + 1, 1] - t_1_w_p2[ind, 1])) * (
                            Tcelsius - t_1_w_p2[ind, 1]
                    ) + t_1_w_p2[ind, 0]

            # Interpolate time after which 50 % Widmanstaetten alpha is formed at current temperature
            if 260 <= Tcelsius < 727:
                # Find index with temperature closest (and larger) to current temperature
                ind = torch.max(torch.nonzero(t_50_w_p1[:, 1] >= Tcelsius)).item()

                # Interpolate time for current temperature
                t_50_w = ((t_50_w_p1[ind + 1, 0] - t_50_w_p1[ind, 0]) / (t_50_w_p1[ind + 1, 1] - t_50_w_p1[ind, 1])) * (
                        Tcelsius - t_50_w_p1[ind, 1]
                ) + t_50_w_p1[ind, 0]
            else:
                if 727 <= Tcelsius < 1000:
                    # Find index with temperature closest (and larger) to current temperature
                    ind = torch.max(torch.nonzero(t_50_w_p2[:, 1] <= Tcelsius)).item()

                    # Interpolate time for current temperature
                    t_50_w = (
                                     (t_50_w_p2[ind + 1, 0] - t_50_w_p2[ind, 0]) / (t_50_w_p2[ind + 1, 1] - t_50_w_p2[ind, 1])
                             ) * (Tcelsius - t_50_w_p2[ind, 1]) + t_50_w_p2[ind, 0]

            # Compute JMAK kinetic parameters
            # Note: This value is as expected, about 1.25
            N_aw = torch.log10(
                torch.log(torch.tensor(1.0) - torch.tensor(0.01)) / torch.log(torch.tensor(1.0) - torch.tensor(0.5))
            ) / torch.log10(t_1_w / t_50_w)
            # Note: k_w seems to be ok, but varies with temperature
            k_aw = -torch.log(torch.tensor(1.0) - torch.tensor(0.01)) / (t_1_w ** N_aw)

        else:
            # N_aw = torch.tensor(1.0) # breaks grad
            N_aw = T / T
            # k_aw = torch.tensor(0.0) # breaks grad
            k_aw = T * 0
        return N_aw, k_aw

    def calc_kinetic_param_am(self, T):
        # JMAK transformation kinetic parameter for dissolution of martensite alpha-phases

        # Specify parameters to iteratively test
        T_test = torch.tensor([0, 400, 500, 700, 800, 1200], dtype=torch.float32) + 273.15
        k_am_test = torch.log(torch.tensor([1.019, 1.019, 1.0148, 1.0249, 1.031, 1.0413], dtype=torch.float32))
        N_am_test = torch.tensor([0.667, 0.667, 1.106, 1.252, 1.326, 1.4927], dtype=torch.float32)

        # Perform initial test of (potentially) iterative test series
        found = torch.tensor(0, dtype=torch.bool)
        if T < T_test[0]:
            # N_am = N_am_test[0] # breaks grad
            # k_am = k_am_test[0] # breaks grad
            N_am = N_am_test[0] * T / T
            k_am = k_am_test[0] * T / T
            found = torch.tensor(1, dtype=torch.bool)

        # Iteratively test parameters
        ind = torch.tensor(1)
        while not found:

            if T < T_test[ind]:
                N_am = (N_am_test[ind] - N_am_test[ind - 1]) / (T_test[ind] - T_test[ind - 1]) * (T - T_test[ind - 1]) + N_am_test[ind - 1]
                k_am = (k_am_test[ind] - k_am_test[ind - 1]) / (T_test[ind] - T_test[ind - 1]) * (T - T_test[ind - 1]) + k_am_test[ind - 1]
                found = torch.tensor(1, dtype=torch.bool)

            ind = ind + torch.tensor(1)

            if ind > len(T_test) - 1:
                # N_am = N_am_test[-1]  # breaks grad
                # k_am = k_am_test[-1]  # breaks grad
                k_am = k_am_test[-1] * T / T
                N_am = N_am_test[-1] * T / T
                found = torch.tensor(1, dtype=torch.bool)

        return N_am, k_am

    def plot_thetas(self, t_is_star, T_is_star, tau_is_inital, theta_is_initial, tau_is_new, theta_is_new, epoch_iter_02):
        epoch = next(epoch_iter_02)

        # Initialize plot
        f, ax = plt.subplots(1, 1)

        # Plot training data as black stars
        # ax.plot(t_is, T_is.detach().numpy(), "g.", label="T_is")
        ax.plot(t_is_star, T_is_star.detach().numpy(), label="$T_i^*$", color="#FFD700", marker=".")
        ax.plot(tau_is_inital, theta_is_initial.detach().numpy(), label="$T_i^{initial}$", color="#BFBFBF", marker=".")
        ax.plot(tau_is_new, theta_is_new.detach().numpy(), label="$T_i^{e}$", color="#000000", marker=".")
        # ax.set_ylim([self.min_temp, self.max_temp])
        ax.set_ylim([0, 4000])

        ax.legend()
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Temperature [K]")

        # plt.show()
        Path(f"./{self.folder_name}/figs/thetas").mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(f"./{self.folder_name}/figs/thetas/theta_evol_{str(epoch - 1).zfill(5)}.png"))
        plt.close("all")

    @staticmethod
    def plot_x_hist(x_star, x_hist, node, folder_name):
        # Initialize plot
        f, ax = plt.subplots(1, 1)

        # Plot training data as black stars
        ax.plot(x_hist[:, 1].detach().numpy(), ls="None", c="#ff7f0e", marker=".", label="$x_{agb,n}$")
        ax.plot(x_hist[:, 2].detach().numpy(), ls="None", c="#2ca02c", marker=".", label="$x_{aw,n}$")
        ax.plot(x_hist[:, 3].detach().numpy(), ls="None", c="#d62728", marker=".", label="$x_{am,n}$")
        ax.plot(x_hist[:, 0].detach().numpy(), ls="None", c="#9467BD", marker=".", label="$x_{b,n}$")

        ax.hlines(x_star[1].item(), xmin=0, xmax=(~torch.isnan(x_hist[:, 1])).sum(), color="#ff7f0e", label="$x_{agb,n}^*$")
        ax.hlines(x_star[2].item(), xmin=0, xmax=(~torch.isnan(x_hist[:, 2])).sum(), color="#2ca02c", label="$x_{aw,n}^*$")
        ax.hlines(x_star[3].item(), xmin=0, xmax=(~torch.isnan(x_hist[:, 3])).sum(), color="#d62728", label="$x_{am,n}^*$")
        ax.hlines(x_star[0].item(), xmin=0, xmax=(~torch.isnan(x_hist[:, 0])).sum(), color="#9467BD", label="$x_{b,n}^*$")

        ax.set_xlabel("Epoch+1 [-]")
        ax.set_ylabel("Phase fraction [-]")
        ax.set_ylim(-0.05, 1.05)
        ax.legend()

        # plt.show()
        Path(f"./{folder_name}/figs").mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(f"./{folder_name}/figs/x_hist_{str(node).zfill(2)}.png"))
        plt.close("all")

    @staticmethod
    def state_to_components(state_i: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        x_bs_i, x_agbs_i, x_aws_i, x_ams_i = state_i.squeeze()
        return x_bs_i, x_agbs_i, x_aws_i, x_ams_i

    @staticmethod
    def components_to_state(
        x_bs_i: torch.Tensor, x_agbs_i: torch.Tensor, x_aws_i: torch.Tensor, x_ams_i: torch.Tensor
    ) -> torch.Tensor:
        return torch.vstack((x_bs_i, x_agbs_i, x_aws_i, x_ams_i)).T


def plot_results(x_agbs, x_ams, x_aws, x_bs, x_ms, times, Ts, G, node_eval, folder_name, param_code):

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotting the phase fractions on the primary y-axis
    # ax1.plot(times.numpy(), x_ms.numpy(), label="$x_{m,i}^{e}$", marker="D", c="#D9D9D9")
    ax1.plot(times.numpy(), x_agbs.numpy(), label="$x_{agb,i}^{e}$", marker="o", c="#ff7f0e")
    ax1.plot(times.numpy(), x_aws.numpy(), label="$x_{aw,i}^{e}$", marker="s", c="#2ca02c")
    ax1.plot(times.numpy(), x_ams.numpy(), label="$x_{am,i}^{e}$", marker="^", c="#d62728")
    ax1.plot(times.numpy(), x_bs.numpy(), label="$x_{b,i}^{e}$", marker="d", c="#9467BD")
    # ax1.plot(times.numpy(), x_as.numpy(), label="x_a", marker="v")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Phase fractions [-]")
    ax1.set_ylim(-0.05, 1.05)
    ax1.legend(loc="upper left")
    ax1.grid(True)

    # Creating a secondary y-axis for the temperature
    ax2 = ax1.twinx()
    ax2.plot(times.numpy(), Ts.numpy()-273.15, label="$T_i^{e}$", color="#000000", marker="p")
    ax2.set_ylim(0, 2000)
    ax2.set_ylabel("Temperature [°C]")
    ax2.legend(loc="upper right")

    plt.title("Time Series Data")
    Path(f"./{folder_name}/figs/x_evol_sharey").mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"./{folder_name}/figs/x_evol_sharey/{param_code}_murgau.png"))
    plt.close("all")
    plt.show()
    plt.close()

    # Create two vertically stacked subplots
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 10), sharex=True)

    # Plotting the phase fractions on the first subplot
    # ax1.plot(times.numpy(), x_ms.numpy(), label="$x_{m,i}^{e}$", marker="D", c="#D9D9D9")
    # ax1.plot(times.numpy(), x_agbs.numpy(), label="$x_{agb,i}^{e}$", marker="o", c="#ff7f0e")
    ax1.plot(times.numpy(), x_aws.numpy(), label="$x_{aw,i}^{e}$", marker="s", c="#2ca02c")
    ax1.plot(times.numpy(), x_ams.numpy(), label="$x_{am,i}^{e}$", marker="^", c="#d62728")
    ax1.plot(times.numpy(), x_bs.numpy(), label="$x_{b,i}^{e}$", marker="d", c="#9467BD")
    # ax1.plot(times.numpy(), x_as.numpy(), label="x_a", marker="v")
    ax1.set_ylabel("Phase fractions [-]")
    ax1.set_ylim(-0.05, 1.05)
    ax1.legend(loc="upper left")
    ax1.grid(True)
    ax1.set_title("Time Series Data")

    # Plotting the temperature on the second subplot
    ax2.plot(times.numpy(), Ts.numpy(), label="$T_i^{e}$", color="#000000", marker="p")
    # ax2.hlines([1273, 1873], xmin=0, xmax=max(times.numpy()), label=["T_b_trans", "T_melt"], colors=["#FFC0CB","#FFC0CB"])
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Temperature [K]")
    ax2.set_ylim(0, 3000)
    ax2.legend(loc="upper left")
    ax2.grid(True)

    # Save the figure
    Path(f"./{folder_name}/figs/x_evol_sbplt").mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"./{folder_name}/figs/x_evol_sbplt/{param_code}_murgau.png"))
    plt.close("all")  # plt.show()


def plot_results_debug(x_agbs, x_ams, x_aws, x_bs, x_ms, times, Ts, node_eval, folder_name, param_code, e_diffuse_am):

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotting the phase fractions on the primary y-axis
    # ax1.plot(times.numpy(), x_ms.numpy(), label="$x_{m,i}^{e}$", marker="D", c="#D9D9D9")
    ax1.plot(times.numpy(), x_agbs.numpy(), label="$x_{agb,i}^{e}$", marker="o", c="#ff7f0e")
    ax1.plot(times.numpy(), x_aws.numpy(), label="$x_{aw,i}^{e}$", marker="s", c="#2ca02c")
    ax1.plot(times.numpy(), x_ams.numpy(), label="$x_{am,i}^{e}$", marker="^", c="#d62728")
    ax1.plot(times.numpy(), x_bs.numpy(), label="$x_{b,i}^{e}$", marker="d", c="#9467BD")
    # ax1.plot(times.numpy(), x_as.numpy(), label="x_a", marker="v")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Phase fractions [-]")
    ax1.set_ylim(-0.05, 1.05)
    ax1.legend(loc="upper left")
    ax1.grid(True)

    # Creating a secondary y-axis for the temperature
    ax2 = ax1.twinx()
    ax2.plot(times.numpy(), Ts.numpy()-273.15, label="$T_i^{e}$", color="#000000", marker="p")
    ax2.set_ylim(0, 2000)
    ax2.set_ylabel("Temperature [°C]")
    ax2.legend(loc="upper right")

    plt.title("Time Series Data")
    Path(f"./{folder_name}/figs/x_evol_sharey").mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"./{folder_name}/figs/x_evol_sharey/{param_code}_murgau_debug.png"))
    plt.close("all")
    plt.show()
    plt.close()

    # Create two vertically stacked subplots
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 10), sharex=True)

    # Plotting the phase fractions on the first subplot
    # ax1.plot(times.numpy(), x_ms.numpy(), label="$x_{m,i}^{e}$", marker="D", c="#D9D9D9")
    # ax1.plot(times.numpy(), x_agbs.numpy(), label="$x_{agb,i}^{e}$", marker="o", c="#ff7f0e")
    ax1.plot(times.numpy(), x_aws.numpy(), label="$x_{aw,i}^{e}$", marker="s", c="#2ca02c")
    ax1.plot(times.numpy(), x_ams.numpy(), label="$x_{am,i}^{e}$", marker="^", c="#d62728")
    ax1.plot(times.numpy(), x_bs.numpy(), label="$x_{b,i}^{e}$", marker="d", c="#9467BD")
    ax1.plot(times.numpy()[1:], e_diffuse_am.numpy(), label="e_diffuse_am", marker="d", c="#FFC0CB")
    # ax1.plot(times.numpy(), x_as.numpy(), label="x_a", marker="v")
    ax1.set_ylabel("Phase fractions [-]")
    ax1.set_ylim(-0.05, 1.05)
    ax1.legend(loc="upper left")
    ax1.grid(True)
    ax1.set_title("Time Series Data")

    # Plotting the temperature on the second subplot
    ax2.plot(times.numpy(), Ts.numpy(), label="$T_i^{e}$", color="#000000", marker="p")
    ax2.hlines([1273, 1873], xmin=0, xmax=max(times.numpy()), label=["T_b_trans", "T_melt"], colors=["#FFC0CB","#FFC0CB"])
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Temperature [K]")
    ax2.set_ylim(0, 3000)
    ax2.legend(loc="upper left")
    ax2.grid(True)

    # Save the figure
    Path(f"./{folder_name}/figs/x_evol_sbplt").mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"./{folder_name}/figs/x_evol_sbplt/{param_code}_murgau_debug.png"))
    plt.close("all")  # plt.show()

