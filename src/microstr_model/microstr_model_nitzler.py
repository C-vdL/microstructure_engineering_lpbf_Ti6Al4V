from pathlib import Path
from typing import Tuple
import torch
from matplotlib import pyplot as plt
from datetime import datetime
from torch import nn
import numpy as np
from matplotlib.ticker import FixedLocator

from misc.plot_style import apply_rcparams
from src.thermal_model.fd_1d import ThermalModel

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
        self._base_Q_magnitude_remelt = kwargs.get("Q_magnitude_remelt", 0.5e6)
        self.q_delta_times_values = kwargs.get("q_delta_times", torch.tensor([0.4] + [2.5 for _ in range(self.G-1)], dtype=torch.float32))
        self.q_dt_0 = kwargs.get("q_dt_0", 0.5)
        self.q_dt = kwargs.get("q_dt", 4.5)
        self.no_remelt = kwargs.get("no_remelt", 0)

        self.temp_offset = kwargs.get("temp_offset", torch.tensor(0.0))

        self.T_b_coef = nn.Parameter(torch.tensor(1.0, dtype=torch.float32, requires_grad=True))
        self.Q_magnitude_coef = torch.tensor(kwargs.get("Q_magnitude_coef", 1), dtype=torch.float32)
        self.Q_remelt_coef = nn.Parameter(torch.tensor(kwargs.get("Q_remelt_coef", 1), dtype=torch.float32, requires_grad=True))

        self.temperature_model = ThermalModel(N=self.N, L=self.L, G=self.G, no_remelt=self.no_remelt, beta=self.beta, dt=self.dt_temperature_model,
                                              t_end=self.t_end, k_conduction=self.k_conduction, k_radiation=self.k_radiation,
                                              h_convection=self.h_convection, T_inf=self.T_inf, T_bottom=self._base_T_bottom * self.T_b_coef,
                                              Q_magnitude=self._base_Q_magnitude * self.Q_magnitude_coef, Q_magnitude_remelt=self._base_Q_magnitude_remelt * self.Q_remelt_coef)

        self.q_delta_times = nn.Parameter(torch.tensor([self.q_dt_0] + [self.q_dt for _ in range(self.G-1+ self.no_remelt)])).detach()

        T_0 = torch.zeros(self.N)
        T_0[:-self.G] = T_0[:-self.G] = self._base_T_bottom*self.T_b_coef
        self.T_0 = T_0
        self.times = []
        self.temps_tmp = []

        self.delta_t = kwargs.get("delta_t", torch.tensor(1 / 2000, requires_grad=False))

        self._initialized = False
        self._node_eval = 100

        self.x_agbs_tmp = []
        self.x_aws_tmp = []
        self.x_ams_tmp = []
        self.x_bs_tmp = []
        self.x_ms_tmp = []
        
        self.x_dot_b_ams_tmp = []
        self.x_dot_am_bs_tmp = []
        self.x_a_equs_tmp = []
        self.x_am_equs_tmp = []
        self.x_dot_b_ass_tmp = []
        self.x_dot_am_ass_tmp = []      

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
        Q_magnitude = self._base_Q_magnitude*self.Q_magnitude_coef
        Q_magnitude_remelt = self._base_Q_magnitude_remelt*self.Q_remelt_coef
        self.temperature_model.define_Q_t(self.q_delta_times, Q_magnitude, Q_magnitude_remelt)
        self.temperature_model.set_up_thermal_model()

    def predict(self, times=None, temps=None, x_0=None, is_return_x_evol=False):

        q_timesteps = torch.cumsum(self.q_delta_times[:-1], dim=0)

        def downsample_T_t(T_t_curve, is_downsample):
            if is_downsample:
                print(f"original length  {len(T_t_curve)}")
                time_column = T_t_curve[:, 0]
                timestep_threshold = 1e-1
                time_proximity = 1.0  # 1 second

                # Identify rows within 1s of any time in q_timestep
                def is_close_to_q(time, q_timesteps, proximity):
                    return torch.any(torch.abs(q_timesteps - time) <= proximity)

                # Precompute mask for proximity condition
                proximity_mask = torch.tensor([
                    is_close_to_q(t, q_timesteps, time_proximity)
                    for t in time_column
                ])

                # Separate
                within_proximity = T_t_curve[proximity_mask]
                outside_proximity = T_t_curve[~proximity_mask]

                # Downsample outside_proximity
                downsampled = []
                last_time = -float('inf')
                for row in outside_proximity:
                    time = row[0].item()
                    if time - last_time >= timestep_threshold:
                        downsampled.append(row)
                        last_time = time

                if downsampled:
                    outside_downsampled = torch.stack(downsampled)
                    final_combined = torch.cat([within_proximity, outside_downsampled], dim=0)
                else:
                    final_combined = within_proximity

                # Optional: sort by time
                final_combined = final_combined[final_combined[:, 0].argsort()]

                print(f"new length  {len(final_combined)}")
            else:
                final_combined = T_t_curve

            return final_combined


        T_t_curve = torch.stack((times, temps + self.temp_offset), dim=1)

        final_combined = downsample_T_t(T_t_curve, is_downsample=False)
        times, temps = final_combined[:, 0], final_combined[:, 1]

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

        x_b_0, x_agb_0, x_aw_0, x_am_0 = self.state_to_components(x_0)
        x_a_0 = x_agb_0 + x_aw_0 + x_am_0
        x_m_0 = torch.tensor(0.0)

        x_agbs, x_ams, x_as, x_aws, x_bs, x_ms, times, Ts = self.run_microstr_model(
            times, temps, x_agb_0, x_aw_0, x_am_0, x_a_0, x_b_0, x_m_0, self.delta_t, torch.tensor(0.0), is_plot=True
        )
        x = torch.vstack([x_bs, x_agbs, x_aws, x_ams]).T[-1]

        if not is_return_x_evol:
            return x
        else:
            return x, torch.vstack([times, temps, x_bs, x_agbs, x_aws, x_ams]).T

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

            self._initialized = True

        start_time = datetime.now()
        x_ip1 = self.run_microstr_model_step(step, x)
        end_time = datetime.now()
        duration = end_time - start_time

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
            Ts[n + 1] = self.temps_tmp[n+1]

            # Save cooling rate in list for cooling rate evolution over time
            cool_rates[n + 1] = (Ts[n] - Ts[n + 1]) / (ts[n + 1] - ts[n])

            # Evaluate Nitzler model
            (
                x_agbs[n + 1],
                x_aws[n + 1],
                x_ams[n + 1],
                x_bs[n + 1],
                x_ms[n + 1],
                x_as[n + 1],
            ) = self.eval_timestep((ts[n + 1] - ts[n]), Ts[n + 1], Ts[n], x_bs[n], x_agbs[n], x_aws[n], x_ams[n])

        # Plotting
        if is_plot:
            self.x_dot_am_ass = torch.cat(self.x_dot_am_ass_tmp)
            self.x_dot_b_ass = torch.cat(self.x_dot_b_ass_tmp)
            self.x_dot_am_bs = torch.cat(self.x_dot_am_bs_tmp)
            self.x_dot_b_ams = torch.cat(self.x_dot_b_ams_tmp)
            self.x_a_equs = torch.cat(self.x_a_equs_tmp)
            self.x_am_equs = torch.cat(self.x_am_equs_tmp)

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

        # Break to state components
        x_bs_i, x_agbs_i, x_aws_i, x_ams_i = self.state_to_components(x_i)

        # Evaluate Nitzler model
        start_time = datetime.now()
        (x_agbs_ip1, x_aws_ip1, x_ams_ip1, x_bs_ip1, x_ms_ip1, *_) = self.eval_timestep(self.delta_t, Ts_ip1, Ts_i, x_bs_i, x_agbs_i, x_aws_i,
                                                                                        x_ams_i)

        end_time = datetime.now()
        duration = end_time - start_time

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

    def eval_timestep(self, delta_t, Tnp1, Tn, x_b_n, x_agb_n, x_aw_n, x_am_n):
        # Proell et al. 10.1016/j.addma.2024.104380
        eps = 1e-4

        T_as_reg1 = torch.tensor(1273.0)
        T_as_reg2 = torch.tensor(1373.0)

        # Initialize new values with old ones
        x_agb_np1 = x_agb_n.clone()
        x_aw_np1 = x_aw_n.clone()
        x_am_np1 = x_am_n.clone()
        x_b_np1 = x_b_n.clone()
        x_a_n = x_agb_n + x_aw_n + x_am_n
        x_m_np1 = torch.tensor(0)

        h_n = x_agb_n.clone()

        x_as_n = x_aw_n

        # Compute cooling rate
        T_rate = (Tnp1 - Tn) / delta_t

        # Calculate equilibrium phase fraction
        # [Proell eq. 15]
        x_a_eq_np1 = self.calc_x_a_equ(Tnp1)
        # [Proell eq. 16+17]
        x_am_eq_np1 = self.calc_x_am_equ(Tnp1, x_as_n)

        # Calculate diffusive rates
        # [Proell eq. 22]
        x_dot_b_as_np1 = self.calc_x_dot_b_as(Tnp1, x_a_eq_np1, x_as_n, x_am_n)
        # [Proell eq. 23]
        x_dot_am_as_np1 = self.calc_x_dot_am_as(Tnp1, x_as_n, x_am_n)
        # [Proell eq. 24]
        x_dot_as_b = self.calc_x_dot_as_b(Tnp1, x_a_eq_np1, x_as_n, x_am_n)

        # Integrate diffusion based transformations
        # [Proell eq. 30-33]
        x_as_np1_tmp_01 = x_as_n + delta_t * (x_dot_b_as_np1 + x_dot_am_as_np1 - x_dot_as_b)
        # [Proell eq. 30-33]
        x_am_np1_tmp_01 = x_am_n + delta_t * (-x_dot_am_as_np1)

        # Correct integrated phase fractions
        # [Proell p. 5, last paragraph]
        x_as_np1_tmp_02 = torch.max(x_as_np1_tmp_01, torch.tensor(0.0)*(x_as_np1_tmp_01+eps))
        x_am_np1_tmp_02 = torch.max(x_am_np1_tmp_01, torch.tensor(0.0)*(x_am_np1_tmp_01+eps))
        # [Proell p. 5, last paragraph]
        factor_upper_limit_x_a = torch.min(torch.tensor(1.0), torch.tensor(0.9)/(x_am_np1_tmp_02+x_as_np1_tmp_02+eps))
        x_as_np1_tmp_02 *= factor_upper_limit_x_a
        x_am_np1_tmp_02 *= factor_upper_limit_x_a
        # [Proell eq. 28]
        factor = torch.sigmoid(torch.tensor(0.1) * (T_as_reg2 - Tnp1))
        x_as_np1_tmp_03 = x_as_np1_tmp_02 * factor

        # # Calculate equilibrium phase fraction
        # # [Proell eq. 16+17]
        # x_am_eq_np1 = self.calc_x_am_equ(Tnp1, x_as_np1_tmp_03)

        # Instantaneous phase transformations
        # [Proell eq. 26]
        x_dot_b_am_np1 = self.calc_x_dot_b_am(x_am_eq_np1, x_am_np1_tmp_02, delta_t, T_rate, x_a_eq_np1, x_as_np1_tmp_03)
        # [Proell eq. 27]
        x_dot_am_b_np1 = self.calc_x_dot_am_b(x_a_eq_np1, x_as_np1_tmp_03, x_am_np1_tmp_02, delta_t, T_rate)

        # Integrate instantaneous transformations
        # [Proell eq. 30-33]
        x_am_np1_tmp_03 = x_am_np1_tmp_02 + delta_t * (x_dot_b_am_np1 + x_dot_am_b_np1 + eps)

        # Correct integrated phase fractions
        # [Proell p. 5, last paragraph]
        x_am_np1_tmp_04 = torch.max(x_am_np1_tmp_03, torch.tensor(0.0)*x_am_np1_tmp_03+eps)
        # [Proell p. 5, last paragraph]
        factor_upper_limit_x_a = torch.min(torch.tensor(1.0), torch.tensor(0.9)/(x_am_np1_tmp_04+x_as_np1_tmp_03+eps))
        x_as_np1_tmp_03 *= factor_upper_limit_x_a
        x_am_np1_tmp_04 *= factor_upper_limit_x_a

        # Final phase fractions
        x_as_np1 = x_as_np1_tmp_03
        x_am_np1 = x_am_np1_tmp_04

        h_np1 = self.calc_as_lath_width(Tn, x_as_np1, x_as_n, h_n)

        x_agb_np1 = torch.tensor(h_np1)
        x_aw_np1 = x_as_np1
        x_am_np1 = x_am_np1
        # [Proell eq. 21]
        x_b_np1 = torch.tensor(1.0) - x_m_np1 - x_as_np1 - x_am_np1
        x_m_np1 = x_m_np1
        x_a_np1 = x_as_np1 + x_am_np1

        self.x_dot_b_ams_tmp.append(torch.atleast_1d(x_dot_b_am_np1.detach()))
        self.x_dot_am_bs_tmp.append(torch.atleast_1d(x_dot_am_b_np1.detach()))
        self.x_a_equs_tmp.append(torch.atleast_1d(x_a_eq_np1.detach()))
        self.x_am_equs_tmp.append(torch.atleast_1d(x_am_eq_np1.detach()))
        self.x_dot_b_ass_tmp.append(torch.atleast_1d(x_dot_b_as_np1.detach()))
        self.x_dot_am_ass_tmp.append(torch.atleast_1d(x_dot_am_as_np1.detach()))

        return x_agb_np1, x_aw_np1, x_am_np1, x_b_np1, x_m_np1, x_a_np1

    def calc_as_lath_width(self, Tn, x_as_np1, x_as_n, h_n):
        # Irwin 2016, "Predicting Microstructure From Thermal History During Additive Manufacturing for Ti-6Al-4V"

        if torch.isnan(h_n) and x_as_n != 0:
            print("torch.isnan(h_n) and x_as_n != 0")
        if torch.isnan(h_n):
            h_n = torch.tensor(0.0)
        k_lath = torch.tensor(18433)
        R_lath = torch.tensor(10044)
        if x_as_np1 > 0:
            if x_as_np1 > x_as_n:
                h_eq = k_lath * np.exp(-R_lath / Tn)
                h_np1 = (h_n * x_as_n + h_eq * (x_as_np1 - x_as_n)) / x_as_np1
            else:
                h_np1 = h_n
        else:
            h_np1 = torch.tensor(float('nan'))

        # print(h_np1)
        return h_np1


    def calc_x_dot_b_am(self, x_am_eq, x_am, delta_t, T_rate, x_a_eq, x_as):

        # x_dot_b_am = torch.min(torch.max(torch.tensor(0.0), (x_am_eq - x_am)),  torch.max(torch.tensor(0.0), (x_a_eq - x_as - x_am)))
        x_dot_b_am = torch.max(torch.tensor(0.0), (x_am_eq - x_am))
        # x_dot_b_am = torch.max(torch.tensor(0.0), (x_am_eq - x_am - x_as))
        x_dot_b_am /= delta_t

        x_dot_b_am *= torch.sigmoid(1000 * -(T_rate+1e-1))

        return x_dot_b_am

    def calc_x_dot_am_b(self, x_a_eq, x_as, x_am, delta_t, T_rate):

        x_dot_am_b_tmp = (x_a_eq - x_as - x_am)

        x_dot_am_b = torch.max(-x_am, torch.min(x_dot_am_b_tmp,torch.tensor(0.0)))
        x_dot_am_b /= delta_t
        x_dot_am_b *= torch.sigmoid(1000 * (T_rate-1e-1))

        return x_dot_am_b

    def calc_x_a_equ(self, T):
        T_a_start = torch.tensor(1273.0)
        k_a_eq = torch.tensor(0.0068)

        # [Proell eq. 15]
        x_a_eq = lambda temps: torch.min(torch.max(1 - torch.exp(-k_a_eq * (T_a_start - temps)), torch.tensor(0.0)), torch.tensor(0.9))

        x_a_eq_np1 = x_a_eq(T)

        return x_a_eq_np1

    def calc_x_am_equ(self, T, x_as):
        T_a_m_start = torch.tensor(848.0)
        k_a_m_eq = torch.tensor(0.00415)

        # [Proell eq. 16]
        x_a_m_eq_0 = lambda temps: torch.min(torch.max(1 - torch.exp(-k_a_m_eq * (T_a_m_start - temps)), torch.tensor(0.0)), torch.tensor(0.9))

        # [Proell eq. 17]
        factor_effective = (torch.tensor(0.9) - x_as) / torch.tensor(0.9)
        x_a_m_eq_np1 = x_a_m_eq_0(T) * factor_effective

        return x_a_m_eq_np1

    def calc_x_dot_b_as(self, T, x_a_eq, x_as, x_am):
        c_a = torch.tensor(2.51)

        # [Proell eq. 22]
        k_1 = torch.tensor(0.294)
        k_2 = torch.tensor(850.0)
        k_3 = torch.tensor(0.0337)
        k_as = k_1 / (1 + torch.exp(-k_3 * (T - k_2)))  # * torch.tensor(0.5)

        x_a = x_as + x_am

        eps=torch.tensor(1e-2)
        x_dot_b_as = k_as * (x_as+eps)**((c_a-1)/c_a) * torch.abs(x_a_eq - x_a)**((c_a+1)/c_a)
        x_dot_b_as *= torch.sigmoid(-1000 * (x_a - x_a_eq))

        return x_dot_b_as

    def calc_x_dot_am_as(self, T, x_as, x_am):
        c_as = torch.tensor(2.51)

        # [Proell eq. 23]
        k_1 = torch.tensor(0.294)
        k_2 = torch.tensor(850.0)
        k_3 = torch.tensor(0.0337)
        k_as = k_1 / (1 + torch.exp(-k_3 * (T - k_2)))  # * torch.tensor(0.05)

        eps=1e-4

        x_dot_am_as = k_as * (x_as+1e-4)**((c_as-1)/c_as) * (x_am+eps)**((c_as+1)/c_as)
        x_dot_am_as *= torch.sigmoid(1000 * (x_am+eps))

        return x_dot_am_as

    def calc_x_dot_as_b(self, T, x_a_eq, x_as, x_am):

        c_b = torch.tensor(11.0)

        # [Proell eq. 24]
        k_1 = torch.tensor(0.294)
        k_2 = torch.tensor(850.0)
        k_3 = torch.tensor(0.0337)
        k_as = k_1 / (1 + torch.exp(-k_3 * T - k_2))
        # [Proell eq. 24]
        f = torch.tensor(3.8)
        k_b = k_as * f

        x_a = x_as + x_am

        eps = torch.tensor(1e-2)
        # x_dot_as_b = k_b * (torch.tensor(0.9)-x_a)**((c_b-1)/c_b) * (x_a - x_a_eq)**((c_b+1)/c_b)
        x_dot_as_b = k_b * (torch.tensor(0.9)-x_a+eps)**((c_b-1)/c_b) * torch.abs(x_a - x_a_eq)**((c_b+1)/c_b)
        # x_dot_as_b = k_b * (torch.tensor(0.9)-x_a)**((c_b-1)/c_b) * (x_a - x_a_eq)**(torch.tensor(1.0))
        x_dot_as_b *= torch.sigmoid(-1000 * (x_a_eq - x_a))

        return x_dot_as_b

    @staticmethod
    def plot_x_hist(x_star, x_hist, node, folder_name):
        # Initialize plot
        f, ax = plt.subplots(1, 1)

        # Plot training data as black stars
        ax.plot(x_hist[:, 2].detach().numpy(), ls="None", c="#238b45", marker=".", label="$x_{as,n}$")
        ax.plot(x_hist[:, 3].detach().numpy(), ls="None", c="#d7301f", marker=".", label="$x_{am,n}$")
        ax.plot(x_hist[:, 0].detach().numpy(), ls="None", c="#2171b5", marker=".", label="$x_{b,n}$")

        ax.hlines(x_star[2].item(), xmin=0, xmax=(~torch.isnan(x_hist[:, 2])).sum(), color="#238b45", label="$x_{as,n}^*$")
        ax.hlines(x_star[3].item(), xmin=0, xmax=(~torch.isnan(x_hist[:, 3])).sum(), color="#d7301f", label="$x_{am,n}^*$")
        ax.hlines(x_star[0].item(), xmin=0, xmax=(~torch.isnan(x_hist[:, 0])).sum(), color="#2171b5", label="$x_{b,n}^*$")

        ax.set_xlabel("Epoch+1 [-]")
        ax.set_ylabel("Phase fraction [-]")
        ax.set_ylim(-0.05, 1.05)
        ax.legend(loc="upper right")

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
    apply_rcparams()

    T_offset = 273.15

    x_agbs = x_agbs.numpy()
    x_ams = x_ams.numpy()
    x_aws = x_aws.numpy()
    x_bs = x_bs.numpy()
    times = times.numpy()
    Ts = Ts.numpy()

    # Create two vertically stacked subplots
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(6 / 2.54, 5 / 2.54), sharex=True)

    # Plotting the phase fractions on the first subplot
    ax1.plot(times, x_bs, label="$x_{\\beta}$", c="#2171b5", lw=0.8)
    ax1.plot(times, x_aws, label="$x_{\\alpha_s}$", c="#238b45", lw=0.8)
    ax1.plot(times, x_ams, label="$x_{\\alpha_m}$", c="#d7301f", lw=0.8)

    ax1.set_ylabel("Phase fractions [-]")
    ax1.set_ylim(-0.00, 1.00)
    ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # ax1.set_xlim(0, max(times))
    ax1.legend(loc="upper right")
    ax1.grid(True)

    # Plotting the temperature on the second subplot
    T_a_start = torch.tensor(1273.0)
    T_a_end = torch.tensor(935.0)
    k_a_eq = torch.tensor(0.0068)
    x_a_eq = lambda temps: torch.min(torch.max(1 - torch.exp(-k_a_eq * (T_a_start - temps)), torch.tensor(0.0)), torch.tensor(0.9))
    temps_as = np.linspace(T_a_end, T_a_start, 500)
    x_a_eq_values = x_a_eq(torch.tensor(temps_as))
    greens_cmap = plt.colormaps["Greens"]
    for i in range(len(temps_as) - 1):
        if temps_as[i] < T_a_start and temps_as[i] > T_a_end:
            color = greens_cmap(x_a_eq_values[i])
            ax2.axhspan(temps_as[i] - T_offset, temps_as[i + 1] - T_offset, color=color, alpha=0.05)

    T_a_m_start = torch.tensor(848.0)
    k_a_m_eq = torch.tensor(0.00415)
    x_a_m_eq_0 = lambda temps: torch.min(torch.max(1 - torch.exp(-k_a_m_eq * (T_a_m_start - temps)), torch.tensor(0.0)), torch.tensor(0.9))
    temps_am = np.linspace(273, T_a_m_start, 500)
    x_a_m_eq_0_values = x_a_m_eq_0(torch.tensor(temps_am))
    reds_cmap = plt.colormaps["Reds"]
    for i in range(len(temps_am) - 1):
        if temps_am[i] < T_a_m_start:
            color = reds_cmap(x_a_m_eq_0_values[i])
            ax2.axhspan(temps_am[i] - T_offset, temps_am[i + 1] - T_offset, color=color, alpha=0.05)

    ax2.plot(times, Ts - T_offset, label="$T$", color="#000000", lw=0.8)
    # ax2.legend(loc="upper right")

    ax2.hlines(1878 - T_offset, xmin=0, xmax=max(times), label="$T_{\\beta,start}$", color="#2171b5", lw=0.8)
    ax2.hlines(T_a_start - T_offset, xmin=0, xmax=max(times), label="$T_{\\alpha_s,start}$", color="#238b45", lw=0.8)
    ax2.hlines(T_a_end - T_offset, xmin=0, xmax=max(times), label="$T_{\\alpha_s,end}$", ls="--", color="#238b45", lw=0.8)
    ax2.hlines(T_a_m_start - T_offset, xmin=0, xmax=max(times), label="$T_{\\alpha_m,start}$", color="#d7301f", lw=0.8)

    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Temperature [°C]")
    yticks_minor = [200, 600, 1000, 1400]
    yticks_major = [0, 400, 800, 1200, 1600]
    ax2.yaxis.set_major_locator(FixedLocator(yticks_major))
    ax2.yaxis.set_minor_locator(FixedLocator(yticks_minor))
    ax2.set_ylim(0, 1700)
    ax2.legend(loc="upper right", fontsize=8, ncol=3)
    ax2.grid(True)
    fig.align_labels()

    # Save the figure
    Path(f"./{folder_name}/figs").mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"./{folder_name}/figs/{param_code}.png"))
    plt.close("all")
    # plt.show()
