import matplotlib.pyplot as plt

def apply_rcparams():
    plt.rcParams.update({
        # --- Figure and layout ---
        # "figure.figsize": (3.5, 2.6),        # typical one-column figure size (inches)
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


# Original colors
colors_single = {
    "blue": "#2171b5",
    "green": "#238b45",
    "red": "#d7301f",
}

# Extended palette (avoiding red/blue/green conflicts)
colors_extended = {
    "orange": "#e66101",
    "purple": "#762a83",
    "teal": "#1c9099",
    "pink": "#E13163",  # swapped magenta
    "yellow": "#e6ab02",
    "dark_gray": "#525252",
    "bright_green": "#00B050",  # swapped light brown
    "turquoise": "#66c2a5",
}

# Merge both dictionaries if needed
colors_palette = {**colors_single, **colors_extended}

