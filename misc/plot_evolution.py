from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import numpy as np
import pandas as pd
import torch

from plot_style import apply_rcparams, colors_single, colors_extended, colors_palette


def plot_x_evol_results(csv_filenames, folder_name_exec):
    T_offset = 273.15

    for csv_filename in csv_filenames:

        # Read data from CSV
        df = pd.read_csv(f"{folder_name_exec}/x_evol_data/{csv_filename}.csv")

        x_agbs = df["x_agb"]
        x_ams = df["x_am"]
        x_aws = df["x_as"]
        x_bs = df["x_b"]
        times = df["times"]
        Ts = df["temps"]

        # Create two vertically stacked subplots
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(6/2.54, 5/2.54), sharex=True)
        ax1b = ax1.twinx()

        # Plotting the phase fractions on the first subplot
        ax1.plot(times, x_aws, label="$x_{as}$", c="#238b45", lw=0.8)
        ax1.plot(times, x_ams, label="$x_{am}$", c="#d7301f", lw=0.8)
        ax1.plot(times, x_bs, label="$x_{b}$", c="#2171b5", lw=0.8)
        ax1b.plot(times, x_agbs, label="$h_{as}$", c="#ff7f0e", lw=0.8)

        ax1.set_ylabel("Phase fractions [-]")
        ax1.set_ylim(-0.00, 1.00)
        ax1b.legend(loc="lower left")
        ax1b.set_ylabel("Lath thickness [µm]")
        ax1b.set_ylim(-0.00, 2.00)
        ax1.set_xlim(0, max(times))
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

        ax2.hlines(1878 - T_offset, xmin=0, xmax=max(times), label="$T_{b,start}$", color="#2171b5", lw=0.8)
        ax2.hlines(T_a_start - T_offset, xmin=0, xmax=max(times), label="$T_{as,start}$", color="#238b45", lw=0.8)
        ax2.hlines(T_a_end - T_offset, xmin=0, xmax=max(times), label="$T_{as,end}$", ls="--", color="#238b45", lw=0.8)
        ax2.hlines(T_a_m_start - T_offset, xmin=0, xmax=max(times), label="$T_{am,start}$", color="#d7301f", lw=0.8)

        ax2.plot(times, Ts - T_offset, label="$T$", color="#000000", lw=0.8)

        ax2.set_xlabel("Time [s]")
        ax2.set_ylabel("Temperature [°C]")
        ax2.set_ylim(0, 1700)
        ax2.legend(loc="upper right", fontsize=8, ncol=3)
        ax2.grid(True)
        fig.align_labels()

        folder_name = f"{folder_name_exec}/figs/evolution/x_evol_results"
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{folder_name}/{csv_filename}.png")
        plt.close()
        # plt.show()


def plot_x_evol_woAlpha(csv_filenames, folder_name_exec):
    T_offset = 273.15

    for csv_filename in csv_filenames:

        # Read data from CSV
        df = pd.read_csv(f"{folder_name_exec}/x_evol_data/{csv_filename}.csv")

        x_ams = df["x_am"]
        x_aws = df["x_as"]
        x_bs = df["x_b"]
        times = df["times"]
        Ts = df["temps"]

        # Create two vertically stacked subplots
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(6/2.54, 5/2.54), sharex=True)

        # Plotting the phase fractions on the first subplot
        ax1.plot(times, x_bs, label="$x_{\\beta}$", c="#2171b5", lw=0.8)
        ax1.plot(times, x_aws, label="$x_{\\alpha_s}$", c="#238b45", lw=0.8)
        ax1.plot(times, x_ams, label="$x_{\\alpha_m}$", c="#d7301f", lw=0.8)

        ax1.set_ylabel("Phase fractions [-]")
        ax1.set_ylim(-0.00, 1.00)
        ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax1.set_xlim(0, max(times))
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
        ax2.legend(loc="upper right")

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
        
        # Calculate accumulated time inside alpha_s dissolution temperature interval
        # alpha_s dissolution temperature
        # T_low = 450 + 273.15
        # T_high = 1000 + 273.15
        T_low = T_a_end.item()
        T_high = T_a_start.item()
        # Boolean mask for temperatures inside the interval
        mask = (Ts >= T_low) & (Ts <= T_high)
        # Compute time differences between consecutive time points
        dt = times.diff().fillna(0)
        # Accumulated time spent inside the temperature interval
        time_in_interval = dt[mask].sum()
        print(f"\n\n{csv_filename}")
        print(f"Accumulated time in interval: {time_in_interval} \n\n")

        folder_name = f"{folder_name_exec}/figs/evolution/x_evol_woAlpha"
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{folder_name}/{csv_filename}.png")
        plt.close()
        # plt.show()


def plot_x_evol_woAlpha_woColor(csv_filenames, folder_name_exec):
    T_offset = 273.15

    for csv_filename in csv_filenames:

        # Read data from CSV
        df = pd.read_csv(f"{folder_name_exec}/x_evol_data/{csv_filename}.csv")

        x_ams = df["x_am"]
        x_aws = df["x_as"]
        x_bs = df["x_b"]
        times = df["times"]
        Ts = df["temps"]

        # Create two vertically stacked subplots
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(6/2.54, 5/2.54), sharex=True)

        # Plotting the phase fractions on the first subplot
        ax1.plot(times, x_bs, label="$x_{\\beta}$", c="#2171b5", lw=0.8)
        ax1.plot(times, x_aws, label="$x_{\\alpha_s}$", c="#238b45", lw=0.8)
        ax1.plot(times, x_ams, label="$x_{\\alpha_m}$", c="#d7301f", lw=0.8)

        ax1.set_ylabel("Phase fractions [-]")
        ax1.set_ylim(-0.00, 1.00)
        ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax1.set_xlim(0, max(times))
        ax1.legend(loc="upper right", fontsize=8)
        ax1.grid(True)

        # Plotting the temperature on the second subplot
        T_a_start = torch.tensor(1273.0)
        T_a_end = torch.tensor(935.0)
        T_a_m_start = torch.tensor(848.0)

        # ax2.hlines(1878 - T_offset, xmin=0, xmax=max(times), label="$T_{\\beta,start}$", color="#2171b5", lw=0.8)
        ax2.hlines(T_a_start - T_offset, xmin=0, xmax=max(times), label="$T_{\\alpha_s,start}$", color="#238b45", lw=0.8, ls="--")
        # ax2.hlines(T_a_end - T_offset, xmin=0, xmax=max(times), label="$T_{\\alpha_s,end}$", ls="--", color="#238b45", lw=0.8)
        ax2.hlines(T_a_m_start - T_offset, xmin=0, xmax=max(times), label="$T_{\\alpha_m,start}$", color="#d7301f", lw=0.8, ls="--")

        ax2.plot(times, Ts - T_offset, label="$T$", color="#000000", lw=0.8)

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

        folder_name = f"{folder_name_exec}/figs/evolution/x_evol_woAlpha_woColor"
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{folder_name}/{csv_filename}.png")
        # plt.show()
        plt.close()


def plot_x_evol_micro(csv_filenames, folder_name_exec):

    for csv_filename in csv_filenames:
        # Read data from CSV
        df = pd.read_csv(f"{folder_name_exec}/x_evol_data/{csv_filename}.csv")

        x_ams = df["x_am"]
        x_aws = df["x_as"]
        x_bs = df["x_b"]
        times = df["times"]

        # Create two vertically stacked subplots
        fig, ax1 = plt.subplots(nrows=1, figsize=(5.5/2.54, 3.5/2.54))

        # Plotting the phase fractions on the first subplot
        ax1.plot(times, x_aws, label="$x_{as}$", c="#238b45", lw=1)
        ax1.plot(times, x_ams, label="$x_{am}$", c="#d7301f", lw=1)
        ax1.plot(times, x_bs, label="$x_{b}$", c="#2171b5", lw=1)

        ax1.set_ylabel("Phase fractions [-]")
        ax1.set_ylim(-0.00, 1.00)
        ax1.set_xlabel("Time [s]")
        ax1.set_xlim(0, max(times))
        ax1.legend(loc="upper right")
        ax1.grid(True)

        folder_name = f"{folder_name_exec}/figs/evolution/x_evol_micro"
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{folder_name}/{csv_filename}.png")
        # plt.show()
        plt.close()


def plot_x_evol_temp(csv_filenames, folder_name_exec):
    T_offset = 273.15

    for csv_filename in csv_filenames:
        # Read data from CSV
        df = pd.read_csv(f"{folder_name_exec}/x_evol_data/{csv_filename}.csv")

        times = df["times"]
        Ts = df["temps"]

        # Create two vertically stacked subplots
        fig, ax2 = plt.subplots(nrows=1, figsize=(5.5/2.54, 3.5/2.54))

        # Plotting the temperature on the second subplot
        # T_a_start = torch.tensor(1273.0)
        # T_a_end = torch.tensor(935.0)
        # k_a_eq = torch.tensor(0.0068)
        # x_a_eq = lambda temps: torch.min(torch.max(1 - torch.exp(-k_a_eq * (T_a_start - temps)), torch.tensor(0.0)), torch.tensor(0.9))
        # temps_as = np.linspace(T_a_end, T_a_start, 500)
        # x_a_eq_values = x_a_eq(torch.tensor(temps_as))
        # greens_cmap = plt.colormaps["Greens"]
        # for i in range(len(temps_as) - 1):
        #     if temps_as[i] < T_a_start and temps_as[i] > T_a_end:
        #         color = greens_cmap(x_a_eq_values[i])
        #         ax2.axhspan(temps_as[i], temps_as[i + 1], color=color, alpha=0.05)
        #
        # T_a_m_start = torch.tensor(848.0)
        # k_a_m_eq = torch.tensor(0.00415)
        # x_a_m_eq_0 = lambda temps: torch.min(torch.max(1 - torch.exp(-k_a_m_eq * (T_a_m_start - temps)), torch.tensor(0.0)), torch.tensor(0.9))
        # temps_am = np.linspace(273, T_a_m_start, 500)
        # x_a_m_eq_0_values = x_a_m_eq_0(torch.tensor(temps_am))
        # reds_cmap = plt.colormaps["Reds"]
        # for i in range(len(temps_am) - 1):
        #     if temps_am[i] < T_a_m_start:
        #         color = reds_cmap(x_a_m_eq_0_values[i])
        #         ax2.axhspan(temps_am[i], temps_am[i + 1], color=color, alpha=0.05)
       
        # ax2.hlines(1878, xmin=0, xmax=max(times), label="$T_{b,start}$", color="#2171b5", lw=0.8)
        # ax2.hlines(T_a_start, xmin=0, xmax=max(times), label="$T_{as,start}$", color="#238b45", lw=0.8)
        # ax2.hlines(T_a_end, xmin=0, xmax=max(times), label="$T_{as,end}$", ls="--", color="#238b45", lw=0.8)
        # ax2.hlines(T_a_m_start, xmin=0, xmax=max(times), label="$T_{am,start}$", color="#d7301f", lw=0.8)

        ax2.plot(times, Ts - T_offset, label="$T$", color="#000000", lw=1)

        ax2.set_xlabel("Time [s]")
        ax2.set_ylabel("Temperature [°C]")
        ax2.set_ylim(0, 1700)
        ax2.set_xlim(0, max(times))
        ax2.legend(loc="upper right")
        ax2.grid(True)

        folder_name = f"{folder_name_exec}/figs/evolution/x_evol_temp"
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{folder_name}/{csv_filename}.png")
        # plt.show()
        plt.close()



if __name__ == "__main__":
    # These functions allow to (re-)generate microstruture evolution plots from CSV data.
    # The CSV files are expected to have columns: "times", "temps", "x_agb", "x_am", "x_as", "x_b".

    apply_rcparams()
    
    folder_name_exec = Path("..\execs\\2026-04-29_22-48-56_304_7914_forw") # <-- change this to your folder path

    csv_filenames = [           # <-- change this
        "lx3.00E-05_Tb298.15_ILT30_VED1.0E+11G90",
        "lx3.00E-05_Tb473.15_ILT30_VED1.0E+11G90",
        "lx3.00E-05_Tb673.15_ILT30_VED1.0E+11G90",

        "lx9.00E-05_Tb298.15_ILT30_VED1.0E+11G30",
        "lx9.00E-05_Tb473.15_ILT30_VED1.0E+11G30",
        "lx9.00E-05_Tb673.15_ILT30_VED1.0E+11G30",
    ]

    plot_x_evol_woAlpha(csv_filenames, folder_name_exec)
    plot_x_evol_woAlpha_woColor(csv_filenames, folder_name_exec)
    plot_x_evol_results(csv_filenames, folder_name_exec)
    plot_x_evol_temp(csv_filenames, folder_name_exec)
    plot_x_evol_micro(csv_filenames, folder_name_exec)

