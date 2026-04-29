from pathlib import Path
import matplotlib.pyplot as plt
import itertools
import numpy as np
import pandas as pd
import os
import matplotlib.patches as mpatches
from scipy.interpolate import griddata

from plot_style import apply_rcparams, colors_single, colors_extended, colors_palette


def plot_achiev_phase_range(folder_name_exec):
    print("\n\n#######################################")
    print("plot_achiev_phase_range")

    df_compiled_all = pd.read_csv(Path(f"{folder_name_exec}/final_microstr.csv"))
    
    df_compiled_all["layer_thickness"] = df_compiled_all["L"] / df_compiled_all["N"]
    df_compiled_all["VED [J/mm3]"] = df_compiled_all["energy_density"] / 1e9
    df_compiled_all["ILT [s]"] = df_compiled_all["q_dt"]
    df_compiled_all["Buildplate temperature [°C]"] = df_compiled_all["T_bottom"] - 273.15
    df_compiled_all["Layer thickness [µm]"] = df_compiled_all["layer_thickness"] * 1e6
    
    df_compiled_all["G_actual"] = df_compiled_all["G"].copy()
    df_compiled_all["G_new"] = df_compiled_all["G_actual"] * df_compiled_all["layer_thickness"]
    df_compiled_all["G"] = np.where(df_compiled_all["G_new"] > 0.0008, 30, 10)
    df_compiled_all = df_compiled_all[df_compiled_all["G"] == 30]

    df_compiled_all = df_compiled_all.sort_values(by=["energy_density", "q_dt", "T_bottom", "layer_thickness", "G"])


    doe_unique_cols = ["VED [J/mm3]", "ILT [s]", "Buildplate temperature [°C]", "Layer thickness [µm]", "G"]
    col_dict = {"VED [J/mm3]": "energy_density", "ILT [s]": "q_dt", "Buildplate temperature [°C]": "T_bottom",
                "Layer thickness [µm]": "layer_thickness", "G": "G"}
    col_dict_rev = {v: k for k, v in col_dict.items()}

    split_props = [doe_unique_cols[4]]
    # Get unique values for each column in split_props
    unique_values = {col: df_compiled_all[col].dropna().unique() for col in split_props}

    # Generate all possible combinations of unique values
    combinations = list(itertools.product(*unique_values.values()))

    # Iterate through each combination and filter the dataframe
    for combination in combinations:
        filter_conditions = {col: val for col, val in zip(split_props, combination)}
        df_compiled = df_compiled_all[
            (df_compiled_all[split_props] == pd.Series(filter_conditions)).all(axis=1)
        ]


        high_heat_set = {"energy_density": 120e9, "q_dt": 12, "T_bottom": 673.15, "layer_thickness": 9e-5}
        # medium_heat_set = {"energy_density": 80e9, "q_dt": 30, "T_bottom": 473.15, "layer_thickness": 6e-5}
        low_heat_set = {"energy_density": 40e9, "q_dt": 90, "T_bottom": 298.15, "layer_thickness": 3e-5}

        sets = {"high_heat_set": high_heat_set, "low_heat_set": low_heat_set, "low_heat_set_unconstr": low_heat_set}

        x_labels = ["Layer thickness [µm]", "ILT [s]", "VED [J/mm3]", "Buildplate temperature [°C]"]

        x = np.arange(len(x_labels))
        width = 0.4  # bar width

        phase_names = ["x_as", "x_am"]
        colors = ["#238b45", "#d7301f"]
        alphas = [1, 1, 1]

        for i, (set_name, param_set) in enumerate(sets.items()):
            fig, ax = plt.subplots(figsize=(6 / 2.54, 5 / 2.54))

            for p, phase_name in enumerate(phase_names):
                lowers, uppers, labels = [], [], []
                for process_param in x_labels:
                    label = ""
                    # Filter df_compiled based on all parameters except the current one
                    mask = np.ones(len(df_compiled), dtype=bool)
                    for k, v in param_set.items():
                        col = k
                        if col == col_dict[process_param]:
                            mask &= np.isclose(df_compiled[col], v)
                            label += f"{v}\n"

                    if set_name != "low_heat_set_unconstr":
                        if process_param != col_dict_rev["T_bottom"]:
                            mask &= np.isclose(df_compiled["T_bottom"], 473.15)
                            # label += f"200C\n"

                    df_filtered = df_compiled[mask]
                    if not df_filtered.empty:
                        lowers.append(df_filtered[phase_name].min())
                        uppers.append(df_filtered[phase_name].max())
                    else:
                        lowers.append(np.nan)
                        uppers.append(np.nan)

                    labels.append(label)

                # Create floating bars
                bottoms = np.array(lowers)
                heights = np.array(uppers) - np.array(lowers)
                position_bar = x + (p - 1 + 0) * width
                if position_bar.min() > 0:
                    position_bar = position_bar
                    if phase_name == "x_as":
                        legend_label = r"$x_{\alpha_s}$"
                    else:
                        legend_label = r"$x_{\alpha_m}$"
                    # legend_label = f"${phase_name}$"
                else:
                    position_bar = position_bar
                    if phase_name == "x_as":
                        legend_label = r"$x_{\alpha_s}$"
                    else:
                        legend_label = r"$x_{\alpha_m}$"
                bars = ax.bar(position_bar, heights, width, bottom=bottoms, color=colors[p], label=legend_label, alpha=alphas[i])

                # print(f"set_name {set_name}")
                # print(f"phase_name {phase_name}")
                # print(f"{lowers}")
                # print(f"{uppers}")

            # Formatting
            x_upper = x - 0.3
            ax.set_xticks(x_upper + 0.1)
            if set_name == "low_heat_set_unconstr" or set_name == "low_heat_set":
                ax.set_xticklabels(["30\nµm", "90\ns", "40\nJ/mm³", "25\n°C"], rotation=0, ha="center")
            else:
                ax.set_xticklabels(["90\nµm", "12\ns", "120\nJ/mm³", "400\n°C"], rotation=0, ha="center")

            # Secondary x-axis for categories (energy level groups)
            secax = ax.secondary_xaxis("bottom")
            secax.set_xticks(x - 0.3 + 0.1)
            secax.set_xticklabels(["$\Delta t$", "$ILT$", "$VED$", "$T_b$"])
            secax.spines['bottom'].set_position(('outward', 20))  # offset to create space

            # --- Make the secondary axis transparent ---
            for spine in secax.spines.values():
                spine.set_visible(False)  # remove axis lines
            secax.tick_params(axis='x', length=0)  # remove tick marks

            ax.set_ylabel(f"Achievable phase fractions [-]")
            ax.legend(loc="upper right", ncol=len(ax.get_legend_handles_labels()[0]), bbox_to_anchor=(1, 1.02), fontsize=9)

            ax.set_ylim(0, 1)
            ax.grid(axis="y", linestyle="--", alpha=0.6)

            plt.tight_layout()
            folder_name = Path(f"{folder_name_exec}/figs/achiev_phase_range/")
            Path(folder_name).mkdir(parents=True, exist_ok=True)
            plt.savefig(f"{folder_name}/phase_range_{set_name}.png")
            # plt.show()


def plot_map_contour_overlap(folder_name_exec):
    print("\n\n#######################################")
    print("plot_map_contour_overlap")

    df_compiled_all = pd.read_csv(Path(f"{folder_name_exec}/final_microstr.csv"))
    df_compiled_all["layer_thickness"] = df_compiled_all["L"] / df_compiled_all["N"]
    df_compiled_all["h"] = df_compiled_all["x_agb"]

    df_compiled_all["G_actual"] = df_compiled_all["G"].copy()
    df_compiled_all["G_new"] = df_compiled_all["G_actual"] * df_compiled_all["layer_thickness"]
    df_compiled_all["G"] = np.where(df_compiled_all["G_new"] > 0.0008, 30, 10)
    df_compiled_all = df_compiled_all[df_compiled_all["G"] == 30]

    df_compiled_all = df_compiled_all.sort_values(by=["energy_density", "q_dt", "T_bottom", "layer_thickness", "G"])
    df_compiled_all["VED [J/mm³]"] = df_compiled_all["energy_density"] / 1e9
    df_compiled_all["ILT [s]"] = df_compiled_all["q_dt"]
    df_compiled_all["Build plate temperature [°C]"] = df_compiled_all["T_bottom"] - 273.15
    df_compiled_all["Layer thickness [µm]"] = df_compiled_all["layer_thickness"] * 1e6

    doe_unique_cols = ["VED [J/mm³]", "ILT [s]", "Build plate temperature [°C]", "Layer thickness [µm]", "G"]
    col_dict = {"VED [J/mm³]": "energy_density", "ILT [s]": "q_dt", "Build plate temperature [°C]": "T_bottom",
                "Layer thickness [µm]": "layer_thickness", "G": "G"}
    col_dict_rev = {v: k for k, v in col_dict.items()}

    split_props = [doe_unique_cols[4]]
    # Get unique values for each column in split_props
    unique_values = {col: df_compiled_all[col].dropna().unique() for col in split_props}

    # Generate all possible combinations of unique values
    combinations = list(itertools.product(*unique_values.values()))

    # Iterate through each combination and filter the dataframe
    for combination in combinations:
        filter_conditions = {col: val for col, val in zip(split_props, combination)}
        suffix = "_".join([f"{col_dict_rev[col]}{val}".replace(".", "-") for col, val in zip(split_props, combination)])
        df_compiled = df_compiled_all[
            (df_compiled_all[split_props] == pd.Series(filter_conditions)).all(axis=1)
        ]

        colors_single = ["#2171b5", "#238b45", "#d7301f", "black"]

        # ["VED [J/mm³]", "ILT [s]", "Build plate temperature [°C]", "Layer thickness [µm]", "G"]
        column_prop="ILT [s]"
        coly_prop="VED [J/mm³]"
        index_prop="Layer thickness [µm]"
        x_prop="Build plate temperature [°C]"

        suffix += ""

        fs = {"q_dt": ".0f", "energy_density": ".0e", "layer_thickness": ".0e", "T_bottom": ".0f", "Q_magnitude": ".0e", "theoretical_buildrate": ".g",
              "ILT [s]": ".0f", "VED [J/mm³]": ".0f", "Layer thickness [µm]": ".0f", "Build plate temperature [°C]": ".0f"}

        col_dict = {"VED [J/mm³]": "energy_density", "ILT [s]": "q_dt", "Build plate temperature [°C]": "T_bottom",
                    "Layer thickness [µm]": "layer_thickness", "G": "G"}

        # Settings for large DoE
        # row_values_01 = [sorted(df_compiled[index_prop].dropna().unique())[i] for i in [2]]
        # column_values_01 = [sorted(df_compiled[column_prop].dropna().unique())[i] for i in [6]]
        # row_values_02 = [sorted(df_compiled[index_prop].dropna().unique())[i] for i in [0,1,2,3]]
        # column_values_02 = [sorted(df_compiled[column_prop].dropna().unique())[i] for i in [6]]
        # row_values_03 = [sorted(df_compiled[index_prop].dropna().unique())[i] for i in [2]]
        # column_values_03 = [sorted(df_compiled[column_prop].dropna().unique())[i] for i in [0,4,6,9]]
        #
        # row_value_list = [row_values_01, row_values_02, row_values_03]
        # column_value_list = [column_values_01, column_values_02, column_values_03]

        # Settings for any DoE
        row_value_list = [sorted(df_compiled[index_prop].dropna().unique())]
        column_value_list = [sorted(df_compiled[column_prop].dropna().unique())]

        for n, (row_values, column_values) in enumerate(zip(row_value_list, column_value_list)):

            # print(row_values)
            # print(column_values)

            for is_x_am_rich in [False, True]:

                patches = []
                alphas = [0.3, 0.51, 0.657, 0.760]
                alphas_rev = list(reversed(alphas))

                fig, ax = plt.subplots(figsize=(6 / 2.54, 5 / 2.54))

                for i, row_val in enumerate(row_values):
                    for j, col_val in enumerate(column_values):

                        subset = df_compiled[
                            (df_compiled[index_prop] == row_val) &
                            (df_compiled[column_prop] == col_val)
                            ]

                        if subset.empty:
                            continue

                        if is_x_am_rich:

                            x = subset[x_prop].values
                            y = subset[coly_prop].values
                            z = subset["x_am"].values  # plot_col

                            xi = np.linspace(x.min(), x.max(), 10)
                            yi = np.linspace(y.min(), y.max(), 10)
                            x_grid, y_grid = np.meshgrid(xi, yi)
                            z_grid = griddata((x, y), z, (x_grid, y_grid), method='linear')

                            if len(row_values) == 1 and len(column_values) == 1:

                                for frac in [0.6, 0.75, 0.895]:
                                    plt.contourf(
                                        x_grid, y_grid, z_grid,
                                        levels=[frac, 1],
                                        colors=[colors_single[2]],
                                        alpha=0.3
                                    )

                                    patch = mpatches.Patch(
                                        facecolor=colors_single[2],
                                        edgecolor="none",
                                        alpha=alphas[len(patches)],
                                        label=f"$\geq${frac*100:.0f}% $\\alpha_m$"
                                    )
                                    patches.append(patch)

                            else:
                                plt.contourf(
                                    x_grid, y_grid, z_grid,
                                    levels=[0.75, 1],
                                    colors=[colors_single[2]],
                                    alpha=0.3,
                                )

                                if len(row_values) == 1:
                                    label_text = f"{col_val:.0f}s"
                                    # Create a proxy patch for the legend
                                    patch = mpatches.Patch(
                                        facecolor=colors_single[2],
                                        edgecolor="none",
                                        alpha=alphas_rev[len(patches)],
                                        label=label_text
                                    )
                                else:
                                    label_text = f"{row_val:.0f}µm"
                                    # Create a proxy patch for the legend
                                    patch = mpatches.Patch(
                                        facecolor=colors_single[2],
                                        edgecolor="none",
                                        alpha=alphas[len(patches)],
                                        label=label_text
                                    )

                                patches.append(patch)

                        else:
                            x_as = subset[x_prop].values
                            y_as = subset[coly_prop].values
                            z_as = subset["x_am"].values  # plot_col

                            xi = np.linspace(x_as.min(), x_as.max(), 10)
                            yi = np.linspace(y_as.min(), y_as.max(), 10)
                            x_as_grid, y_as_grid = np.meshgrid(xi, yi)
                            z_as_grid = griddata((x_as, y_as), z_as, (x_as_grid, y_as_grid), method='linear')

                            if len(row_values) == 1 and len(column_values) == 1:
                                for frac in [0.1, 0.25, 0.4]:
                                    plt.contourf(
                                        x_as_grid, y_as_grid, z_as_grid,
                                        levels=[0, frac],
                                        colors=[colors_single[1]],
                                        alpha=0.3
                                    )

                                    # Create a proxy patch for the legend
                                    patch = mpatches.Patch(
                                        facecolor=colors_single[1],
                                        edgecolor="none",
                                        alpha=alphas_rev[len(patches)],
                                        label=f"$\leq${frac * 100:.0f}% $\\alpha_m$"
                                    )
                                    patches.append(patch)
                            else:

                                plt.contourf(
                                    x_as_grid, y_as_grid, z_as_grid,
                                    levels=[0.0, 0.25],
                                    colors=[colors_single[1]],
                                    alpha=0.3
                                )

                                if len(row_values) == 1:
                                    label_text = f"{col_val:.0f}s"
                                    # Create a proxy patch for the legend
                                    patch = mpatches.Patch(
                                        facecolor=colors_single[1],
                                        edgecolor="none",
                                        alpha=alphas[len(patches)],
                                        label=label_text
                                    )
                                else:
                                    label_text = f"{row_val:.0f}µm"
                                    # Create a proxy patch for the legend
                                    patch = mpatches.Patch(
                                        facecolor=colors_single[1],
                                        edgecolor="none",
                                        alpha=alphas_rev[len(patches)],
                                        label=label_text
                                    )

                                patches.append(patch)

                if is_x_am_rich:
                    plt.legend(handles=patches, loc="upper right")
                else:
                    plt.legend(handles=patches, loc="lower left")

                # # Set title and labels
                ax.set_xlabel(x_prop, c="black")
                ax.set_ylabel(coly_prop, c="black")


                axis_suffix = f"R{index_prop}_C{column_prop}_X{x_prop}_CY{coly_prop}"
                if "[" in axis_suffix:
                    axis_suffix = f"R{col_dict[index_prop]}_C{col_dict[column_prop]}_X{col_dict[x_prop]}_CY{col_dict[coly_prop]}"

                if is_x_am_rich:
                    axis_suffix = axis_suffix + "_red"
                else:
                    axis_suffix = axis_suffix + "_green"

                folder_name = Path(f"{folder_name_exec}/figs/map_contour_overlap/")
                Path(folder_name).mkdir(parents=True, exist_ok=True)
                plt.savefig(f"{folder_name}/map_contour_overlap_{suffix}_{axis_suffix}_{n}.png")
                # plt.show()
                plt.close()


def plot_phase_bars(phase_data, prefix=""):
    print("\n\n#######################################")
    print("plot_phase_bars")

    # --- Ensure output directory exists ---
    out_dir = Path("../figs/trends/barplots")
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- Create figure ---
    fig, ax = plt.subplots(figsize=(9 / 2.54, 6 / 2.54))  # width scales with #bars

    # --- Plot stacked bars ---
    bar_width = 0.6

    for i, (alpha_s, alpha_m, beta, time_s) in enumerate(phase_data):
        # Bottoms for stacking
        bottoms = [0, alpha_s, alpha_s + alpha_m]
        colors = ["#238b45", "#d7301f", "#2171b5"]

        labels = [r"$\alpha_s$", r"$\alpha_m$", r"$\beta$"]

        heights = [alpha_s, alpha_m, beta]

        for j, (h, b, c, lbl) in enumerate(zip(heights, bottoms, colors, labels)):
            ax.bar(i, h, bar_width, bottom=b, color=c)

            # Add label in the middle if the section is tall enough
            if h > 0.05:
                ax.text(i, b + h / 2, lbl,
                        ha="center", va="center",
                        color="white", fontsize=9, fontweight="bold")

        # Add time label below bar
        ax.text(i, -0.08, f"{time_s}", ha="center", va="top", fontsize=7)

    # --- Format ---
    ax.set_xlim(-0.5, len(phase_data) - 0.5)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Phase fraction [-]")
    ax.set_xticks([])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.tick_params(axis="y")

    # --- Aesthetic box ---
    for spine in ax.spines.values():
        spine.set_linewidth(0.4)
        spine.set_color("black")

    fig.tight_layout(pad=0.3)

    # --- Save file ---
    filename = "barplot_multiple_" + f"{prefix}_" + "_".join([f"{t}" for _, _, _, t in phase_data]).replace(" ", "").replace("/", "").replace("³",
                                                                                                                                              "3") + ".png"
    filepath = os.path.join(out_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    apply_rcparams()

    folder_name = Path("..\execs\\2026-04-29_22-48-56_304_7914_forw") # <-- change this to your folder path

    plot_achiev_phase_range(folder_name)
    plot_map_contour_overlap(folder_name)  # Check out function to switch to larger DoE settings

    # x_as, x_am, x_b
    # === Case: Time series, dataset 1 === (yellow)
    phase_set_1 = [
        (0.868764638900756, 0.0289604544639587, 0.102385587990283, "12 s"),
        (0.28009158372879, 0.562836527824401, 0.157071888446807, "30 s"),
        (0.105162322521209, 0.794737577438354, 0.100100100040435, "120 s"),
    ]

    # === Case: Time series, dataset 2 === (green)
    phase_set_2 = [
        (0.885207891464233, 0.0079110087826848, 0.106881096959114, "12 s"),
        (0.883024334907531, 0.0168756004422903, 0.100100062787532, "30 s"),
        (0.826220393180847, 0.0736795142292976, 0.100100092589855, "120 s"),
    ]

    # === Case: Energy density (VED) series === (orange)
    phase_set_3 = [
        (0.0420868024230003, 0.742437064647674, 0.215476155281066, "50 J/mm³"),
        (0.561262845993042, 0.289167314767837, 0.14956983923912, "70 J/mm³"),
        (0.885256826877594, 0.0146431131288409, 0.100100062787532, "100 J/mm³"),
    ]

    # === Case: Layer thickness series === (blue)
    phase_set_4 = [
        (0.0253410805016756, 0.874558925628662, 0.100099980831146, "30 µm"),
        (0.783193528652191, 0.116706401109695, 0.100100070238113, "120 µm"),
    ]

    plot_phase_bars(phase_set_1, "ILT1")
    plot_phase_bars(phase_set_2, "ILT2")
    plot_phase_bars(phase_set_3, "VED1")
    plot_phase_bars(phase_set_4, "LX1")

