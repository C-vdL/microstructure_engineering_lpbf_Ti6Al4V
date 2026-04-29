from pathlib import Path
import numpy as np
import itertools
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.ticker as mticker
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import griddata


from plot_style import apply_rcparams, colors_single, colors_extended, colors_palette


def plot_parallel_coordinates(folder_name_exec):

    print("\n\n#######################################")
    print("plot_parallel_coordinates")

    file_path = Path(f"{folder_name_exec}/final_microstr.csv")
    df = pd.read_csv(file_path)
    df["x_a"] = df["x_as"] + df["x_am"]

    df["q_dt"] = df["q_dt"] * -1

    columns_to_plot = ["x_am", "T_bottom", "energy_density", "q_dt"]  
    # Create the parallel coordinates plot
    fig = px.parallel_coordinates(
        df,
        dimensions=columns_to_plot,
        color="x_am",  # Color by x_am for better visualization
        color_continuous_scale=px.colors.sequential.Viridis
    )
    # Show the plot
    # fig.show("browser")

    fig_path = Path(f"{folder_name_exec}/figs/parallel_coord/")
    os.makedirs(fig_path, exist_ok=True)
    fig.write_image(Path(f"{fig_path}/parallel_coord_x_am.png"), scale=2, height=1000, width=1500)
    fig.write_html(Path(f"{fig_path}/parallel_coord_x_am.html"))

  #################################

    columns_to_plot = ["x_as", "T_bottom", "energy_density", "q_dt"]
    # Create the parallel coordinates plot
    fig = px.parallel_coordinates(
        df,
        dimensions=columns_to_plot,
        color="x_as",  # Color by x_am for better visualization
        color_continuous_scale=px.colors.sequential.Viridis
    )
    # Show the plot
    # fig.show("browser")

    fig_path = Path(f"{folder_name_exec}/figs/parallel_coord/")
    os.makedirs(fig_path, exist_ok=True)
    fig.write_image(Path(f"{fig_path}/parallel_coord_x_as.png"), scale=2, height=1000, width=1500)
    fig.write_html(Path(f"{fig_path}/parallel_coord_x_as.html"))

  #################################

    columns_to_plot = ["x_b", "T_bottom", "energy_density", "q_dt"]
    # Create the parallel coordinates plot
    fig = px.parallel_coordinates(
        df,
        dimensions=columns_to_plot,
        color="x_b",  # Color by x_am for better visualization
        color_continuous_scale=px.colors.sequential.Viridis
    )
    # Show the plot
    # fig.show("browser")

    fig_path = Path(f"{folder_name_exec}/figs/parallel_coord/")
    os.makedirs(fig_path, exist_ok=True)
    fig.write_image(Path(f"{fig_path}/parallel_coord_x_b.png"), scale=2, height=1000, width=1500)
    fig.write_html(Path(f"{fig_path}/parallel_coord_x_b.html"))

    fig.data = []
    fig.layout = {}
    del fig


def plot_correlation_scatter(folder_name_exec):
    print("\n\n#######################################")
    print("plot_correlation_scatter")

    file_path = Path(f"{folder_name_exec}/final_microstr.csv")
    df = pd.read_csv(file_path)
    df["x_a"] = df["x_as"] + df["x_am"]

    axes = [("T_bottom", "energy_density"), ("T_bottom", "q_dt"), ("energy_density", "q_dt")]

    for axs in axes:
        # Ensure required columns exist
        required_columns = {"T_bottom", "energy_density", "x_am", "x_as", "x_b"}    
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")

        # Define color bar variables
        color_vars = ["x_am", "x_as", "x_b"]
        titles = ["Color: x_am", "Color: x_as", "Color: x_b"]

        # Create subplots
        fig, axes = plt.subplots(1, 3, figsize=(18, 5), constrained_layout=True)

        # Loop through and create scatter plots
        for i, color_var in enumerate(color_vars):
            sc = axes[i].scatter(
                df[axs[0]], df[axs[1]], c=df[color_var], cmap="viridis", edgecolors="black"
            )
            axes[i].set_title(titles[i])
            axes[i].set_xlabel(axs[0])
            axes[i].set_ylabel(axs[1])

            # Add colorbar
            cbar = fig.colorbar(sc, ax=axes[i])
            cbar.set_label(color_var)

        # Show plot
        fig_path_correlation_scatter = Path(f"{folder_name_exec}/figs/correl_scatter/")
        fig_path_correlation_scatter.mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(f"{fig_path_correlation_scatter}/correl_scatter_{axes[0]}_{axes[1]}.png"))
        # plt.show()
        plt.close()


def plot_3d_scatter(folder_name_exec):
    print("\n\n#######################################")
    print("plot_3d_scatter")

    file_path = Path(f"{folder_name_exec}/final_microstr.csv")
    df = pd.read_csv(file_path)
    df["x_a"] = df["x_as"] + df["x_am"]

    # Ensure relevant columns exist
    required_columns = {"energy_density", "q_dt", "T_bottom", "x_am"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")

    col_columns = ["x_am", "x_as", "x_b"]

    for col_column in col_columns:
        # Create 3D scatter plot
        fig = px.scatter_3d(
            df,
            x="energy_density",
            y="T_bottom",
            z="q_dt",
            color=col_column,
            color_continuous_scale="Viridis",  # Choose a color scale (e.g., "Plasma", "Turbo", "Inferno")
            title="3D Scatter Plot of Laser Power, ILT, and T_buildpl",  
            labels={"energy_density": "energy_density", "q_dt": "ILT", "T_bottom": "T_buildpl"}  
        )
        # fig.show("browser")

        fig_path = Path(f"{folder_name_exec}/figs/3d_scatter/")
        os.makedirs(fig_path, exist_ok=True)
        fig.write_image(Path(f"{fig_path}/3d_scatter_c{col_column}.png"), scale=2, height=1000, width=1500)
        fig.write_html(Path(f"{fig_path}/3d_scatter_c{col_column}.html"))

        fig.data = []
        fig.layout = {}
        del fig


def create_grid_plot(colors_single, column_prop, coly_prop, df_compiled, folder_name_exec, index_prop, plot_columns, suffix, x_prop,
                     df_model_pred=None):

    suffix += ""

    fs = {"q_dt": ".0f", "energy_density": ".0e", "layer_thickness": ".0e", "T_bottom": ".0f", "Q_magnitude": ".0e", "theoretical_buildrate": ".g",
          "ILT [s]": ".0f", "VED [J/mm³]": ".0f", "Layer thickness [µm]": ".0f", "Build plate temperature [°C]": ".0f"}

    col_dict = {"VED [J/mm³]": "energy_density", "ILT [s]": "q_dt", "Build plate temperature [°C]": "T_bottom",
                "Layer thickness [µm]": "layer_thickness", "G": "G"}

    # Get unique sorted values for rows and columns
    row_values = sorted(df_compiled[index_prop].dropna().unique())
    column_values = sorted(df_compiled[column_prop].dropna().unique())
    coly_values = sorted(df_compiled[coly_prop].dropna().unique())
    # Set up the grid of plots
    fig, axes = plt.subplots(len(row_values) + 1, len(column_values), figsize=(5 * len(column_values), 4 * (len(row_values) + 1)), sharex=False,sharey=False)
    # Ensure axes is a 2D array
    if len(row_values) == 1:
        axes = [axes]
    if len(column_values) == 1:
        axes = [[ax] for ax in axes]

    # Iterate through the grid positions
    for i, row_val in enumerate(row_values):
        for j, col_val in enumerate(column_values):
            ax = axes[i][j]

            for coly_value in coly_values:

                # Filter data for current row and column values
                subset = df_compiled[
                    (df_compiled[index_prop] == row_val) & (df_compiled[column_prop] == col_val) & (df_compiled[coly_prop] == coly_value)]

                if df_model_pred is not None:
                    subset_pred = df_model_pred[
                        (df_model_pred[index_prop] == row_val) & (df_model_pred[column_prop] == col_val) & (df_model_pred[coly_prop] == coly_value)]

                # Plot each column in plot_columns
                for plot_col, color in zip(plot_columns, colors_single):
                    ax.plot(subset[x_prop], subset[plot_col], label=plot_col, color=color, alpha=(coly_value / max(coly_values)))
                    if df_model_pred is not None:
                        ax.plot(subset_pred[x_prop], subset_pred[plot_col], label=plot_col, color=color, alpha=(coly_value / max(coly_values)), linestyle="dashed")


            # Set title and labels
            if i == 0:
                ax.set_title(f"{column_prop}\n={col_val:{fs[column_prop]}}", fontsize=15, c="black")
            if j == len(column_values) - 1:
                ax.text(1.2, 0.5, f"{index_prop}\n={row_val:{fs[index_prop]}}", ha='center', va='center', rotation=270, fontsize=18, transform=ax.transAxes, c="black")
            ax.set_ylim(0, 1)
            if i <= len(row_values) - 1:
                ax.set_xlabel(x_prop,  fontsize=15, c="black")
            if i == len(row_values) - 1:
                axes[len(row_values)][j].remove()

            if j >= 0:
                ax.set_ylabel("Phase fractions [-]",  fontsize=18, c="black")

            ax.tick_params(axis='both', labelsize=11, colors="black")


    # Create the color legend below the grid
    legend_ax = plt.subplot(len(row_values) + 1, 1, len(row_values) + 1)
    legend_ax.set_xlim(0, len(coly_values))
    legend_ax.set_ylim(0, len(plot_columns))
    x_ticks_pos = [i + 0.5 for i in range(len(coly_values))]
    legend_ax.set_xticks(x_ticks_pos)
    legend_ax.set_xticklabels(coly_values)
    legend_ax.set_xticklabels(mticker.FormatStrFormatter(f'%{fs[coly_prop]}').format_ticks(coly_values))

    y_ticks_pos = [i + 0.5 for i in range(len(plot_columns))]
    legend_ax.set_yticks(y_ticks_pos)
    legend_ax.set_yticklabels(plot_columns)
    legend_ax.set_xlabel(coly_prop, fontsize=18)
    legend_ax.set_ylabel("Phase fractions", fontsize=18)

    legend_ax.tick_params(axis='both', labelsize=18)

    # Draw the rectangles for the legend
    for row_idx, color in enumerate(colors_single):
        for col_idx, coly_val in enumerate(coly_values):
            alpha_value = coly_val / max(coly_values)
            rect = plt.Rectangle((col_idx, row_idx), 1, 1, color=color, alpha=alpha_value)
            legend_ax.add_patch(rect)

    axis_suffix = f"R{index_prop}_C{column_prop}_X{x_prop}_CY{coly_prop}"
    if "[" in axis_suffix:
        axis_suffix = f"R{col_dict[index_prop]}_C{col_dict[column_prop]}_X{col_dict[x_prop]}_CY{col_dict[coly_prop]}"

    if df_model_pred is None:
        fig_path_x_final_grid_coly = Path(f"{folder_name_exec}/figs/x_final_grid_coly/{suffix}/")
    else:
        fig_path_x_final_grid_coly = Path(f"{folder_name_exec}/figs/x_final_grid_coly_meta/")
    fig_path_x_final_grid_coly.mkdir(parents=True, exist_ok=True)
    plt.savefig(Path(f"{fig_path_x_final_grid_coly}/x_final_grid_coly_{suffix}_{axis_suffix}.png"))

    create_indiv_plot(axes, axis_suffix, col_dict, column_prop, column_values, fig_path_x_final_grid_coly, index_prop, row_values, suffix)

    # plt.show()
    plt.close()


def create_indiv_plot(axes, axis_suffix, col_dict, column_prop, column_values, fig_path_x_final_grid_coly, index_prop, row_values, suffix):
    # Iterate over subplots and plot something
    for i, row_val in enumerate(row_values):
        for j, col_val in enumerate(column_values):
            plt.rcParams.update({
                # --- Figure and layout ---
                "figure.figsize": (6 / 2.54, 5 / 2.54),  # typical one-column figure size (inches)
                "figure.dpi": 300,
                "savefig.dpi": 300,
                "savefig.bbox": "tight",
                "savefig.pad_inches": 0.02,
                "savefig.transparent": False,

                # --- Font settings ---
                "font.family": "sans-serif",
                "font.sans-serif": ["Arial", "DejaVu Sans"],
                "font.size": 7,
                "axes.labelsize": 7,
                "axes.titlesize": 7,
                "xtick.labelsize": 7,
                "ytick.labelsize": 7,
                "legend.fontsize": 7,
                "mathtext.fontset": "stix",  # consistent math font
                "text.usetex": False,  # set True if using LaTeX

                # --- Axes ---
                "axes.linewidth": 0.5,
                "axes.edgecolor": "black",
                "axes.labelpad": 2.5,
                "axes.titlesize": 8,
                "axes.labelcolor": "black",
                "axes.grid": False,  # or True for light grid
                # "axes.spines.right": False,          # hide top/right spines for cleaner look
                # "axes.spines.top": False,

                # --- Lines and markers ---
                "lines.linewidth": 0.8,
                "lines.markersize": 3,
                "lines.markeredgewidth": 0.4,

                # --- Ticks ---
                # "xtick.direction": "in",
                # "ytick.direction": "in",
                "xtick.major.size": 3,
                "ytick.major.size": 3,
                "xtick.minor.size": 1.5,
                "ytick.minor.size": 1.5,
                "xtick.major.width": 0.5,
                "ytick.major.width": 0.5,
                "xtick.minor.width": 0.4,
                "ytick.minor.width": 0.4,
                # "xtick.top": True,
                # "ytick.right": True,

                # --- Legend ---
                "legend.frameon": False,
                "legend.edgecolor": "black",
                "legend.handlelength": 1.0,
                "legend.handletextpad": 0.4,
                "legend.borderaxespad": 0.3,
                "legend.columnspacing": 0.8,

                # --- Grid (optional aesthetic) ---
                "grid.color": "0.9",
                "grid.linewidth": 0.4,
                "grid.linestyle": "--",
            })

            ax = axes[i][j]

            # Create a new figure and copy the current subplot into it
            fig_individual, ax_individual = plt.subplots()
            for line in ax.get_lines():
                ax_individual.plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), color=line.get_color(), alpha=line.get_alpha(),
                                   lw=1)

            ax_individual.set_xlabel(ax.get_xlabel())  # Copy x-label
            ax_individual.set_ylabel("Phase fractions [-]")  # Copy y-label
            ax_individual.set_ylim(0, 1)

            ax_individual.yaxis.set_label_coords(*(-0.18070161, 0.5))
            handles, labels = zip(*[
                (line, line.get_label())
                for line in ax.get_lines()
                if line.get_alpha() == 1
            ])

            labels = [r"$x_{\beta}$", r"$x_{\alpha_s}$", r"$x_{\alpha_m}$"]
            ax_individual.legend(handles, labels, loc="upper right")

            # Save the individual figure (optional)
            fig_path_x_final_grid_coly_indiv = Path(f"{fig_path_x_final_grid_coly}/indiv/x_final_grid_coly_{suffix}_{axis_suffix}/")
            fig_path_x_final_grid_coly_indiv.mkdir(parents=True, exist_ok=True)
            fig_name_indiv = f"{i}{j}_{col_dict[index_prop]}{row_val:.1e}_{col_dict[column_prop]}{col_val:.1e}"
            fig_individual.savefig(Path(f"{fig_path_x_final_grid_coly_indiv}/{fig_name_indiv}.png"))
            plt.close(fig_individual)  # Close to prevent display overlap

            # Extra plots used in accompanying publication

            # extra_plots = [  # (axis_suffix_string, alpha_value_frac, vlines_values, filename_suffix),
            #     ("Rlayer_thickness_CT_bottom_Xenergy_density_CYq_dt", 30 / 120, [47.9, 65.32, 71.85, 79.84, 89.81], "_q_dt3.0e+01_exp"),
            #     ("Rlayer_thickness_CT_bottom_Xenergy_density_CYq_dt", 15 / 120, [47.9, 65.32, 71.85, 79.84, 89.81], "_q_dt1.50e+01_exp"),
            #     ("Rlayer_thickness_CT_bottom_Xenergy_density_CYq_dt", 12 / 120, [50, 70, 100], "_q_dt1.2e+01_50_70_100"),
            #     ("Rlayer_thickness_CT_bottom_Xenergy_density_CYq_dt", 12 / 120, [47.9, 65.32, 71.85, 79.84, 89.81], "_q_dt1.2e+01_exp"),
            #     ("Rlayer_thickness_CT_bottom_Xenergy_density_CYq_dt", 60 / 120, [30, 120], "_q_dt6.0e+01"),
            #     ("Rlayer_thickness_Cenergy_density_Xq_dt_CYT_bottom", 200 / 400, [12, 30, 120], "_T_bottom2.0e+02"),
            #     ("Rlayer_thickness_Cenergy_density_Xq_dt_CYT_bottom", 400 / 400, [12, 30, 120], "_T_bottom4.0e+02"),
            #     ("Rlayer_thickness_Cenergy_density_Xq_dt_CYT_bottom", 300 / 400, [12, 30, 120], "_T_bottom3.0e+02"),
            # ]
            #
            # for extra_plot in extra_plots:
            #     axis_suffix_string = extra_plot[0]
            #     alpha_value_frac = extra_plot[1]
            #     vlines_values = extra_plot[2]
            #     filename_suffix = extra_plot[3]
            #
            #     if axis_suffix == axis_suffix_string:
            #         ax = axes[i][j]
            #
            #         # Create a new figure and copy the current subplot into it
            #         fig_individual, ax_individual = plt.subplots()
            #         for line in ax.get_lines():
            #             if line.get_alpha() == alpha_value_frac:
            #                 ax_individual.plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), color=line.get_color(), alpha=1, lw=1)
            #
            #         ax_individual.set_xlabel(ax.get_xlabel())  # Copy x-label
            #         ax_individual.set_ylabel("Phase fractions [-]")  # Copy y-label
            #         ax_individual.set_ylim(0, 1)
            #
            #         ax_individual.yaxis.set_label_coords(*(-0.18070161, 0.5))
            #         handles, labels = zip(*[
            #             (line, line.get_label())
            #             for line in ax_individual.get_lines()
            #             if line.get_alpha() > 0
            #         ])
            #
            #         labels = [r"$x_{\beta}$", r"$x_{\alpha_s}$", r"$x_{\alpha_m}$"]
            #         ax_individual.legend(handles, labels, loc="upper right")
            #         ax_individual.vlines(vlines_values, lw=1, colors="gray", linestyles="solid", alpha=0.7, ymin=0, ymax=1)
            #
            #         # Save the individual figure (optional)
            #         fig_path_x_final_grid_coly_indiv = Path(f"{fig_path_x_final_grid_coly}/indiv/x_final_grid_coly_{suffix}_{axis_suffix}/")
            #         fig_path_x_final_grid_coly_indiv.mkdir(parents=True, exist_ok=True)
            #         fig_name_indiv = f"{i}{j}_{col_dict[index_prop]}{row_val:.1e}_{col_dict[column_prop]}{col_val:.1e}{filename_suffix}"
            #         fig_individual.savefig(Path(f"{fig_path_x_final_grid_coly_indiv}/{fig_name_indiv}.png"))
            #         plt.close(fig_individual)  # Close to prevent display overlap


def plot_merged_x_final_ternary(folder_name_exec):
    print("\n\n#######################################")
    print("plot_merged_x_final_ternary")

    file_name_doe = Path(f"{folder_name_exec}/doe.csv")
    df_doe = pd.read_csv(file_name_doe)
    doe_unique_cols = [col for col in df_doe.columns if df_doe[col].nunique() > 1 and col != "origin_folder"]

    df_name = "final_microstr.csv"
    # df_name = "df_extend.csv"

    df_compiled_all = pd.read_csv(Path(f"{folder_name_exec}/{df_name}"))

    if "layer_thickness" not in df_compiled_all.columns:
        df_compiled_all["layer_thickness"] = df_compiled_all["L"] / df_compiled_all["N"]
    if "G" not in df_compiled_all.columns:
        df_compiled_all["G"] = 30
    # df_compiled_all["energy_density"] = df_compiled_all["Q_magnitude"] / df_compiled_all["layer_thickness"]

    df_compiled_all["x_b_scaled"] = df_compiled_all["x_b"] / (1)

    split_props = [doe_unique_cols[1], doe_unique_cols[3]]
    axis_props = [prop for prop in doe_unique_cols if prop not in split_props]
    # Get unique values for each column in split_props
    unique_values = {col: df_compiled_all[col].dropna().unique() for col in split_props}

    # Generate all possible combinations of unique values
    combinations = list(itertools.product(*unique_values.values()))

    # Iterate through each combination and filter the dataframe
    for combination in combinations:
        filter_conditions = {col: val for col, val in zip(split_props, combination)}
        suffix = "_".join([f"{col}{val}".replace(".", "-") for col, val in zip(split_props, combination)])
        if "G10" in suffix:
            continue
        df_compiled = df_compiled_all[
            (df_compiled_all[split_props] == pd.Series(filter_conditions)).all(axis=1)
        ]

        index_prop = axis_props[1]
        column_prop = axis_props[0]

        # Get unique sorted values for rows and columns
        row_values = sorted(df_compiled[index_prop].dropna().unique())
        column_values = sorted(df_compiled[column_prop].dropna().unique())

        # Set up the grid of plots
        fig, axes = plt.subplots(len(row_values), len(column_values), figsize=(5 * len(column_values), 4 * len(row_values)), sharex=True, sharey=True)

        # Ensure axes is a 2D array
        if len(row_values) == 1:
            axes = [axes]
        if len(column_values) == 1:
            axes = [[ax] for ax in axes]

        fig = go.Figure()
        colors = plt.cm.inferno(np.linspace(0, 1, len(row_values)))  # Discrete colors from the inferno colormap

        # print(f"opacity based on {column_prop}")
        # print(f"color based on {index_prop}")

        # Iterate through the grid positions
        counter = 0
        for i, (row_val,color) in enumerate(zip(row_values,colors)):
            subset_row = df_compiled[(df_compiled[index_prop] == row_val)]

            # Convert to 0–255 scale
            r, g, b = [int(255 * c) for c in color[0:3]]

            # Create rgb string
            rgb_string = f"rgb({r}, {g}, {b})"

            for j, col_val in enumerate(column_values):
                # Filter data for current row and column values
                subset = df_compiled[(df_compiled[index_prop] == row_val) & (df_compiled[column_prop] == col_val)]

                # Normalize so each row sums to 1
                df_norm = subset

                alpha_opac = (col_val - min(column_values)) / (max(column_values)-min(column_values))
                alpha_opac = 0.5 + alpha_opac * (1 - 0.5)

                if row_val == min(row_values):
                    is_showlegend = True
                else:
                    is_showlegend = False

                # Add trace
                fig.add_trace(go.Scatterternary(
                    a=df_norm['x_as'],
                    b=df_norm['x_am'],
                    c=df_norm['x_b_scaled'],
                    mode='markers',
                    opacity=alpha_opac,
                    marker=dict(
                        size=8,
                        color=rgb_string,
                        opacity=alpha_opac,
                    ),
                    showlegend=is_showlegend,
                ))

                if row_val == min(row_values):
                    fig.data[counter].name = f'{column_prop}{col_val:.1e}'
                else:
                    fig.data[counter].showlegend = False
                counter += 1

            fig.add_trace(go.Scatterternary(
                a=subset_row['x_as'],
                b=subset_row['x_am'],
                c=subset_row['x_b_scaled'],
                mode='lines',
                name=f'{index_prop}{row_val:.1e}',  # gives each group a legend label
                line=dict(
                    color=rgb_string,
                    width=2
                ),
                showlegend=True,

            ))
            counter += 1


        fig.update_layout(
            title='Ternary Plot with Multiple DataFrames',
            ternary=dict(
                sum=1,
                aaxis=dict(title='x_as'),
                baxis=dict(title='x_am'),
                caxis=dict(title='x_b'),  # Limit c-axis
            ),
            legend=dict(
                orientation="h",
                x=0,
                y=-0.2,  # below the plot, adjust as needed
                font=dict(size=12),
                traceorder="normal"
            )
        )

        # Adjust layout and show the plot
        fig_path_x_final_ternary = Path(f"{folder_name_exec}/figs/x_final_ternary/{split_props}")
        fig_path_x_final_ternary.mkdir(parents=True, exist_ok=True)
        axis_suffix = ""
        fig.write_image(Path(f"{fig_path_x_final_ternary}/x_final_ternary_{df_name}_{suffix}_{axis_suffix}.png"), scale=2)
        # fig.write_html(Path(f"{fig_path_x_final_ternary}/x_final_ternary_{df_name}_{suffix}_{axis_suffix}.html"))

        fig.data = []
        fig.layout = {}
        del fig


def plot_merged_x_final_scatter_all(folder_name_exec):
    print("\n\n#######################################")
    print("plot_merged_x_final_scatter_all")

    file_name_doe = Path(f"{folder_name_exec}/doe.csv")
    df_doe = pd.read_csv(file_name_doe)
    doe_unique_cols = [col for col in df_doe.columns if df_doe[col].nunique() > 1 and col != "origin_folder"]

    df_name = "final_microstr.csv"
    # df_name = "df_extend.csv"

    df_compiled_all = pd.read_csv(Path(f"{folder_name_exec}/{df_name}"))

    if "layer_thickness" not in df_compiled_all.columns:
        df_compiled_all["layer_thickness"] = df_compiled_all["L"] / df_compiled_all["N"]
    if "G" not in df_compiled_all.columns:
        df_compiled_all["G"] = 30
        # df_compiled_all["energy_density"] = df_compiled_all["Q_magnitude"] / df_compiled_all["layer_thickness"]

    df_compiled_all["x_b_scaled"] = df_compiled_all["x_b"] / (1)

    split_props = [doe_unique_cols[4]]
    axis_props = [prop for prop in doe_unique_cols if prop not in split_props]
    # Get unique values for each column in split_props
    unique_values = {col: df_compiled_all[col].dropna().unique() for col in split_props}

    # Generate all possible combinations of unique values
    combinations = list(itertools.product(*unique_values.values()))

    # Iterate through each combination and filter the dataframe
    for combination in combinations:
        filter_conditions = {col: val for col, val in zip(split_props, combination)}
        suffix = "_".join([f"{col}{val}".replace(".", "-") for col, val in zip(split_props, combination)])
        if "G10" in suffix:
            continue
        df_compiled = df_compiled_all[
            (df_compiled_all[split_props] == pd.Series(filter_conditions)).all(axis=1)
        ].copy()

        index_prop = axis_props[1]
        column_prop = axis_props[0]
        x_prop = axis_props[2]
        f_prop = axis_props[3]

        # Get unique sorted values for rows and columns
        row_values = sorted(df_compiled[index_prop].dropna().unique())
        column_values = sorted(df_compiled[column_prop].dropna().unique())

        # Set up the grid of plots
        fig, axes = plt.subplots(len(row_values), len(column_values), figsize=(5 * len(column_values), 4 * len(row_values)), sharex=True, sharey=True)

        # Ensure axes is a 2D array
        if len(row_values) == 1:
            axes = [axes]
        if len(column_values) == 1:
            axes = [[ax] for ax in axes]

        df_compiled["q_dt_log"] = np.log10(df_compiled["q_dt"])

        for color_column in axis_props:
            if color_column == "q_dt":
                color_column = "q_dt_log"

            fig, ax = plt.subplots(figsize=(8, 6))

            # Add trace
            sc = ax.scatter(
                df_compiled['x_as'],
                df_compiled['x_am'],
                c=df_compiled[color_column],
                cmap='viridis',
                edgecolors='black',
                s=100,
                alpha=0.8
            )

            # Add colorbar once (based on last scatter)
            cbar = plt.colorbar(sc, ax=ax)
            cbar.set_label(color_column)

            ax.set_xlabel('x_as')
            ax.set_ylabel('x_am')
            ax.set_title('x_as vs x_am Colored by Layer Thickness')

            # Adjust layout and show the plot
            fig_path_x_final_scatter_all = Path(f"{folder_name_exec}/figs/x_final_scatter_all/{split_props}")
            fig_path_x_final_scatter_all.mkdir(parents=True, exist_ok=True)
            axis_suffix = f"F{f_prop}_R{index_prop}_C{column_prop}_X{x_prop}"
            plt.savefig(Path(f"{fig_path_x_final_scatter_all}/x_final_scatter_all_{df_name}_{suffix}_{axis_suffix}_{color_column}.png"))
            plt.close()


def plot_merged_x_final_scatter_all_group(folder_name_exec):
    print("\n\n#######################################")
    print("plot_merged_x_final_scatter_all_group")

    file_name_doe = Path(f"{folder_name_exec}/doe.csv")
    df_doe = pd.read_csv(file_name_doe)
    doe_unique_cols = [col for col in df_doe.columns if df_doe[col].nunique() > 1 and col != "origin_folder"]

    df_compiled_all = pd.read_csv(Path(f"{folder_name_exec}/final_microstr.csv"))
    df_compiled_all["layer_thickness"] = df_compiled_all["L"] / df_compiled_all["N"]
    # df_compiled_all["energy_density"] = df_compiled_all["Q_magnitude"] / df_compiled_all["layer_thickness"]
    df_compiled_all["x_b_scaled"] = df_compiled_all["x_b"] / (1)

    split_props = [doe_unique_cols[4]]
    axis_props = [prop for prop in doe_unique_cols if prop not in split_props]
    # Get unique values for each column in split_props
    unique_values = {col: df_compiled_all[col].dropna().unique() for col in split_props}

    # Generate all possible combinations of unique values
    combinations = list(itertools.product(*unique_values.values()))

    # Iterate through each combination and filter the dataframe
    for combination in combinations:
        filter_conditions = {col: val for col, val in zip(split_props, combination)}
        suffix = "_".join([f"{col}{val}".replace(".", "-") for col, val in zip(split_props, combination)])
        if "G10" in suffix:
            continue
        df_compiled = df_compiled_all[
            (df_compiled_all[split_props] == pd.Series(filter_conditions)).all(axis=1)
        ].copy()

        index_prop = axis_props[1]
        column_prop = axis_props[0]
        x_prop = axis_props[2]
        f_prop = axis_props[3]

        # Get unique sorted values for rows and columns
        row_values = sorted(df_compiled[index_prop].dropna().unique())
        column_values = sorted(df_compiled[column_prop].dropna().unique())

        # Set up the grid of plots
        fig, axes = plt.subplots(len(row_values), len(column_values), figsize=(5 * len(column_values), 4 * len(row_values)), sharex=True, sharey=True)

        # Ensure axes is a 2D array
        if len(row_values) == 1:
            axes = [axes]
        if len(column_values) == 1:
            axes = [[ax] for ax in axes]

        df_compiled["q_dt_log"] = np.log10(df_compiled["q_dt"])

        for color_column in axis_props:
            if color_column == "q_dt":
                color_column = "q_dt_log"

            color_col_values = sorted(df_compiled[color_column].dropna().unique())

            fig, ax = plt.subplots(figsize=(8, 6))

            for color_col_val in color_col_values:
                subset = df_compiled[(df_compiled[color_column] == color_col_val)]

                # Add trace
                plt.scatter(
                    subset['x_as'],
                    subset['x_am'],
                    label=f'{color_column}{color_col_val:.1e}',
                    edgecolors='black',
                    s=100,
                    alpha=0.8
                )

            ax.set_xlabel('x_as')
            ax.set_ylabel('x_am')
            ax.set_title('x_as vs x_am Colored by Layer Thickness')
            ax.legend()

            # Adjust layout and show the plot
            fig_path_x_final_scatter_all_group = Path(f"{folder_name_exec}/figs/x_final_scatter_all_group/{split_props}")
            fig_path_x_final_scatter_all_group.mkdir(parents=True, exist_ok=True)
            axis_suffix = f"F{f_prop}_R{index_prop}_C{column_prop}_X{x_prop}"
            plt.savefig(Path(f"{fig_path_x_final_scatter_all_group}/x_final_scatter_all_group_{suffix}_{axis_suffix}_{color_column}.png"))
            plt.close()


def plot_merged_x_final_scatter(folder_name_exec):
    print("\n\n#######################################")
    print("plot_merged_x_final_scatter")

    df_compiled_all = pd.read_csv(Path(f"{folder_name_exec}/final_microstr.csv"))
    df_compiled_all["layer_thickness"] = df_compiled_all["L"] / df_compiled_all["N"]
    df_compiled_all["h"] = df_compiled_all["x_agb"]

    df_compiled_all["G_actual"] = df_compiled_all["G"].copy()
    df_compiled_all["G_new"] = df_compiled_all["G_actual"] * df_compiled_all["layer_thickness"]
    df_compiled_all["G"] = np.where(df_compiled_all["G_new"] > 0.0008, 30, 10)
    df_compiled_all = df_compiled_all[df_compiled_all["G"] != 10]

    axis_props = ["energy_density", "q_dt", "T_bottom", "layer_thickness"]
    df_compiled_all = df_compiled_all.sort_values(by=["energy_density", "q_dt", "T_bottom", "layer_thickness", "G"])

    for prop in axis_props:
        plt.scatter(df_compiled_all["x_as"], df_compiled_all["x_agb"], c=df_compiled_all[prop])
        plt.xlabel("x_as")
        plt.ylabel("lath thickness")
        plt.colorbar(label=prop)

        fig_path_x_final_scatter = Path(f"{folder_name_exec}/figs/x_final_scatter/")
        fig_path_x_final_scatter.mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(f"{fig_path_x_final_scatter}/x_final_scatter_{prop}.png"))

        # plt.show()
        plt.close()


def plot_merged_x_final_grid_coly_simplified_units(folder_name_exec):
    print("\n\n#######################################")
    print("plot_merged_x_final_grid_coly_simplified_units")

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
    axis_props = [prop for prop in doe_unique_cols if prop not in split_props]
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

        print(f"suffix: {suffix}")

        plot_columns = ["x_b", "x_as", "x_am"]
        colors_single = ["#2171b5", "#238b45", "#d7301f", "black"]

        lx_vals = df_compiled["layer_thickness"].unique()
        q_dt_vals = df_compiled["q_dt"].unique()
        T_bottom_vals = df_compiled["T_bottom"].unique()
        VED_vals = df_compiled["energy_density"].unique()

        counter = 0
        for order in itertools.permutations(axis_props):
            counter += 1

            index_prop = order[0]
            column_prop = order[1]
            x_prop = order[2]
            coly_prop = order[3]

            if df_compiled[index_prop].nunique() > df_compiled[column_prop].nunique():
                continue

            val_relevant = {"layer_thickness": lx_vals, "q_dt": q_dt_vals, "T_bottom": T_bottom_vals, "energy_density": VED_vals}
            val_relevant[col_dict[x_prop]] = df_compiled[col_dict[x_prop]].unique()

            for prop in [index_prop, column_prop, coly_prop, x_prop]:
                df_compiled = df_compiled[df_compiled[col_dict[prop]].isin(val_relevant[col_dict[prop]])]

            print(f"order: {order}")
            create_grid_plot(colors_single, column_prop, coly_prop, df_compiled, folder_name_exec, index_prop, plot_columns, suffix, x_prop)


def plot_merged_x_final_blobs(folder_name_exec):
    print("\n\n#######################################")
    print("plot_merged_x_final_blobs")

    df_compiled_all = pd.read_csv(Path(f"{folder_name_exec}/final_microstr.csv"))
    df_compiled_all["layer_thickness"] = df_compiled_all["L"] / df_compiled_all["N"]
    df_compiled_all["h"] = df_compiled_all["x_agb"]

    df_compiled_all["G_actual"] = df_compiled_all["G"].copy()
    df_compiled_all["G_new"] = df_compiled_all["G_actual"] * df_compiled_all["layer_thickness"]
    df_compiled_all["G"] = np.where(df_compiled_all["G_new"] > 0.0008, 30, 10)
    df_compiled_all = df_compiled_all[df_compiled_all["G"] == 30]

    df_compiled_all = df_compiled_all.sort_values(by=["energy_density", "q_dt", "T_bottom", "layer_thickness", "G"])
    df_compiled_all["VED [J/mm3]"] = df_compiled_all["energy_density"] / 1e9
    df_compiled_all["ILT [s]"] = df_compiled_all["q_dt"]
    df_compiled_all["Build plate temperature [°C]"] = df_compiled_all["T_bottom"] - 273.15
    df_compiled_all["Layer thickness [µm]"] = df_compiled_all["layer_thickness"] * 1e6

    doe_unique_cols = ["VED [J/mm3]", "ILT [s]", "Build plate temperature [°C]", "Layer thickness [µm]", "G"]
    col_dict = {"VED [J/mm3]": "energy_density", "ILT [s]": "q_dt", "Build plate temperature [°C]": "T_bottom",
                "Layer thickness [µm]": "layer_thickness", "G": "G"}
    col_dict_rev = {v: k for k, v in col_dict.items()}

    split_props = [doe_unique_cols[3]]
    axis_props = [prop for prop in doe_unique_cols if prop not in split_props]

    # Get unique values for each column in split_props
    unique_values = {col: df_compiled_all[col].dropna().unique() for col in split_props}

    # Generate all possible combinations of unique values
    combinations = list(itertools.product(*unique_values.values()))

    # Iterate through each combination and filter the dataframe
    for combination in combinations:
        filter_conditions = {col: val for col, val in zip(split_props, combination)}
        suffix = "_".join([f"{col_dict[col]}{val}".replace(".", "-") for col, val in zip(split_props, combination)])
        df_compiled = df_compiled_all[
            (df_compiled_all[split_props] == pd.Series(filter_conditions)).all(axis=1)
        ]

        index_prop = axis_props[0]
        column_prop = axis_props[1]
        x_prop = axis_props[2]

        # Filter DataFrame
        filtered_df = df_compiled[df_compiled['x_as'] >= 0.8]

        # Create 3D plot
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Scatter plot
        ax.scatter(
            filtered_df[index_prop],
            filtered_df[column_prop],
            filtered_df[x_prop],
            c='blue',
            alpha=0.7,
            s=50
        )

        # Set labels
        ax.set_xlabel(index_prop)
        ax.set_ylabel(column_prop)
        ax.set_zlabel(x_prop)
        ax.set_xlim(df_compiled[index_prop].min(), df_compiled[index_prop].max())
        ax.set_ylim(df_compiled[column_prop].min(), df_compiled[column_prop].max())
        ax.set_zlim(df_compiled[x_prop].min(), df_compiled[x_prop].max())
        ax.set_title('3D Scatter of Filtered Data (x_as >= 0.8)')

        fig_path_x_final_blobs = Path(f"{folder_name_exec}/figs/x_final_blobs/")
        fig_path_x_final_blobs.mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(f"{fig_path_x_final_blobs}/x_final_blobs_{combination}.png"))
        # plt.show()
        plt.close()



def plot_merged_x_final_map(folder_name_exec):
    print("\n\n#######################################")
    print("plot_merged_x_final_map")

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
    axis_props = [prop for prop in doe_unique_cols if prop not in split_props]
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

        print(f"suffix: {suffix}")

        plot_columns = ["x_b", "x_as", "x_am"]
        colors_single = ["#2171b5", "#238b45", "#d7301f", "black"]

        lx_vals = df_compiled["layer_thickness"].unique()
        q_dt_vals = df_compiled["q_dt"].unique()
        T_bottom_vals = df_compiled["T_bottom"].unique()
        VED_vals = df_compiled["energy_density"].unique()

        counter = 0
        for order in itertools.permutations(axis_props):
            counter += 1

            index_prop = order[0]
            column_prop = order[1]
            x_prop = order[2]
            coly_prop = order[3]

            if df_compiled[index_prop].nunique() > df_compiled[column_prop].nunique():
                continue

            val_relevant = {"layer_thickness": lx_vals, "q_dt": q_dt_vals, "T_bottom": T_bottom_vals, "energy_density": VED_vals}
            val_relevant[col_dict[x_prop]] = df_compiled[col_dict[x_prop]].unique()

            for prop in [index_prop, column_prop, coly_prop, x_prop]:
                df_compiled = df_compiled[df_compiled[col_dict[prop]].isin(val_relevant[col_dict[prop]])]

            print(f"order: {order}")
            create_map_contour_overlap(colors_single, column_prop, coly_prop, df_compiled, folder_name_exec, index_prop, plot_columns, suffix, x_prop)
            create_map_contour_overlap(colors_single, column_prop, coly_prop, df_compiled, folder_name_exec, index_prop, plot_columns, suffix, x_prop)
            create_map_contour_overlap(colors_single, column_prop, coly_prop, df_compiled, folder_name_exec, index_prop, plot_columns, suffix, x_prop)


def create_map_contour_overlap(colors_single, column_prop, coly_prop, df_compiled, folder_name_exec, index_prop, plot_columns, suffix, x_prop,
                               df_model_pred=None):
    suffix += ""

    fs = {"q_dt": ".0f", "energy_density": ".0e", "layer_thickness": ".0e", "T_bottom": ".0f", "Q_magnitude": ".0e", "theoretical_buildrate": ".g",
          "ILT [s]": ".0f", "VED [J/mm³]": ".0f", "Layer thickness [µm]": ".0f", "Build plate temperature [°C]": ".0f"}

    col_dict = {"VED [J/mm³]": "energy_density", "ILT [s]": "q_dt", "Build plate temperature [°C]": "T_bottom",
                "Layer thickness [µm]": "layer_thickness", "G": "G"}

    # Get unique sorted values for rows and columns
    row_values = sorted(df_compiled[index_prop].dropna().unique())
    column_values = sorted(df_compiled[column_prop].dropna().unique())

    # First, approximate middle, and last values
    row_values = [
        row_values[0],
        row_values[len(row_values) // 2],
        row_values[-1]
    ]

    column_values = [
        column_values[0],
        column_values[len(column_values) // 2],
        column_values[-1]
    ]

    # print(row_values)
    # print(column_values)

    for is_x_am_rich in [False, True]:

        patches = []

        fig, ax = plt.subplots(figsize=(6 / 2.54, 5 / 2.54))

        # one different line color per loop iteration
        line_colors = plt.cm.tab10(np.linspace(0, 1, len(row_values) * len(column_values)))
        color_idx = 0

        for i, row_val in enumerate(row_values):
            for j, col_val in enumerate(column_values):

                subset = df_compiled[
                    (df_compiled[index_prop] == row_val) &
                    (df_compiled[column_prop] == col_val)
                    ]

                if subset.empty:
                    continue

                if is_x_am_rich:
                    levels=[0.75, 1]
                    color_shade = colors_single[2]
                else:
                    levels=[0.0, 0.25]
                    color_shade = colors_single[1]


                x = subset[x_prop].values
                y = subset[coly_prop].values
                z = subset["x_am"].values  # plot_col

                xi = np.linspace(x.min(), x.max(), 10)
                yi = np.linspace(y.min(), y.max(), 10)
                x_grid, y_grid = np.meshgrid(xi, yi)
                z_grid = griddata((x, y), z, (x_grid, y_grid), method='linear')

                plt.contourf(
                    x_grid, y_grid, z_grid,
                    levels=levels,
                    label=f'{coly_prop}={col_val:.1e}, {index_prop}={row_val:.1e}',
                    colors=[color_shade],
                    alpha=0.3,
                )

                ax.contour(
                    x_grid, y_grid, z_grid,
                    levels=[0.75, 1],
                    colors=[line_colors[color_idx]],
                    linewidths=1.5,
                    label=f"{coly_prop}={col_val:.1e}, {index_prop}={row_val:.1e}"
                )


                # Create a proxy patch for the legend
                patch = mpatches.Patch(
                    facecolor=color_shade,
                    edgecolor=line_colors[color_idx],
                    alpha=0.3,
                    label=f'{coly_prop}={col_val:.1e}, {index_prop}={row_val:.1e}',
                )
                patches.append(patch)

                color_idx += 1


        plt.legend(handles=patches, fontsize=3)

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

        if df_model_pred is None:
            fig_path_x_final_grid_coly = Path(f"{folder_name_exec}/figs/x_final_map/{suffix}/")
        fig_path_x_final_grid_coly.mkdir(parents=True, exist_ok=True)
        plt.savefig(Path(f"{fig_path_x_final_grid_coly}/x_final_map{suffix}_{axis_suffix}.png"))

        # plt.show()
        plt.close()


if __name__ == "__main__":
    apply_rcparams()
    path_to_add = r"C:\Program Files\wkhtmltopdf\bin"
    os.environ["PATH"] += os.pathsep + path_to_add

    # Define file path
    folder_name = Path("..\execs\\2026-04-29_22-48-56_304_7914_forw") # <-- change this to your folder path

    plot_correlation_scatter(folder_name)
    plot_3d_scatter(folder_name)
    plot_parallel_coordinates(folder_name)
    plot_merged_x_final_scatter(folder_name)
    plot_merged_x_final_blobs(folder_name)
    plot_merged_x_final_scatter_all(folder_name)
    plot_merged_x_final_scatter_all_group(folder_name)

    plot_merged_x_final_grid_coly_simplified_units(folder_name)
    plot_merged_x_final_ternary(folder_name)

    plot_merged_x_final_map(folder_name)

