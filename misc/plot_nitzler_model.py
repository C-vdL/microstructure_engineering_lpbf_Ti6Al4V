from pathlib import Path
import matplotlib.pyplot as plt
import torch


from plot_style import apply_rcparams, colors_single, colors_extended, colors_palette


def plot_x_a_equ():
    print("\n\n#######################################")
    print("plot_x_a_equ")

    T_a_start = torch.tensor(1273.0)
    k_a_eq = torch.tensor(0.0068)

    # [Proell eq. 15]
    x_a_eq = lambda temps: torch.min(
        torch.max(1 - torch.exp(-k_a_eq * (T_a_start - temps)),
                  torch.tensor(0.0)), torch.tensor(0.9)
    )
    Ts = torch.linspace(0, 2000, 1250)
    x_a_eqs = x_a_eq(Ts)

    fig, ax = plt.subplots(figsize=(6/2.54, 6/2.54))

    ax.plot(Ts - 273.15, x_a_eqs, color=colors_palette["orange"])

    ax.set_xlabel("Temperature [°C]")
    ax.set_ylabel("Equilibrium $\\alpha$\n phase fraction $x_{\\alpha}^{eq}$ [-]")
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlim([-50, 1250])
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
    fig.tight_layout()

    folder_name = "../figs/nitzler_model"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{folder_name}/nitzler_x_a_equ.png")
    # plt.show()


def plot_x_am_equ():
    print("\n\n#######################################")
    print("plot_x_am_equ")

    x_as = 0

    T_a_m_start = torch.tensor(848.0)
    k_a_m_eq = torch.tensor(0.00415)

    # [Proell eq. 16]
    x_a_m_eq_0 = lambda temps: torch.min(
        torch.max(1 - torch.exp(-k_a_m_eq * (T_a_m_start - temps)),
                  torch.tensor(0.0)), torch.tensor(0.9)
    )

    # [Proell eq. 17]
    factor_effective = (torch.tensor(0.9) - x_as) / torch.tensor(0.9)

    Ts = torch.linspace(0, 2000, 1250)
    x_a_eqs = x_a_m_eq_0(Ts) * factor_effective

    fig, ax = plt.subplots(figsize=(6/2.54, 6/2.54))

    ax.plot(Ts - 273.15, x_a_eqs, color=colors_palette["purple"])

    ax.set_xlabel("Temperature [°C]")
    ax.set_ylabel("Pseudo-equilibrium $\\alpha_{m}$\n phase fraction $x_{\\alpha_{m}}^{eq}$ [-]")
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlim([-50, 1250])
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
    fig.tight_layout()

    folder_name = "../figs/nitzler_model"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{folder_name}/nitzler_x_am_equ.png")
    # plt.show()


def plot_x_a_equ_x_am_equ():
    print("\n\n#######################################")
    print("plot_x_a_equ_x_am_equ")

    T_a_start = torch.tensor(1273.0)
    k_a_eq = torch.tensor(0.0068)

    # [Proell eq. 15]
    x_a_eq = lambda temps: torch.min(
        torch.max(1 - torch.exp(-k_a_eq * (T_a_start - temps)),
                  torch.tensor(0.0)), torch.tensor(0.9)
    )
    Ts = torch.linspace(0, 2000, 1250)
    x_a_eqs = x_a_eq(Ts)

    x_as = 0

    T_a_m_start = torch.tensor(848.0)
    k_a_m_eq = torch.tensor(0.00415)

    # [Proell eq. 16]
    x_a_m_eq_0 = lambda temps: torch.min(
        torch.max(1 - torch.exp(-k_a_m_eq * (T_a_m_start - temps)),
                  torch.tensor(0.0)), torch.tensor(0.9)
    )

    # [Proell eq. 17]
    factor_effective = (torch.tensor(0.9) - x_as) / torch.tensor(0.9)

    Ts = torch.linspace(0, 2000, 1250)
    x_a_m_eqs = x_a_m_eq_0(Ts) * factor_effective

    fig, ax = plt.subplots(figsize=(6/2.54, 6/2.54))

    # ax.plot(Ts - 273.15, x_a_eqs, color=colors_palette["orange"], label="$x_{\\alpha}^{eq}$")
    # ax.plot(Ts - 273.15, x_a_m_eqs, color=colors_palette["purple"], label="$x_{\\alpha_{m}}^{eq}$")
    ax.plot(Ts - 273.15, x_a_eqs, label="$x_{\\alpha}^{eq}$")
    ax.plot(Ts - 273.15, x_a_m_eqs, label="$x_{\\alpha_{m}}^{eq}$")

    ax.set_xlabel("Temperature [°C]")
    ax.set_ylabel("(Pseudo-)Equilibrium phase fraction [-]")
    ax.legend()
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlim([-50, 1250])
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
    fig.tight_layout()

    folder_name = "../figs/nitzler_model"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{folder_name}/nitzler_x_a_equ_x_am_equ.png")
    # plt.show()


def plot_k_as():
    print("\n\n#######################################")
    print("plot_k_as")

    k_1 = torch.tensor(0.294)
    k_2 = torch.tensor(850.0)
    k_3 = torch.tensor(0.0337)

    # [Proell eq. 25]
    k_as = lambda temps: k_1 / (1 + torch.exp(-k_3 * (temps - k_2)))

    Ts = torch.linspace(0, 2000, 1250)
    k_as_T = k_as(Ts)

    fig, ax = plt.subplots(figsize=(6/2.54, 6/2.54))

    ax.plot(Ts - 273.15, k_as_T, color=colors_palette["teal"])

    ax.set_xlabel("Temperature [°C]")
    ax.set_ylabel("Kinetic factor $k_{\\alpha_{s}}$ [-]")
    ax.set_xlim([-50, 1250])
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
    fig.tight_layout()

    folder_name = "../figs/nitzler_model"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{folder_name}/nitzler_k_as.png")
    # plt.show()


def plot_k_b():
    print("\n\n#######################################")
    print("plot_k_b")

    k_1 = torch.tensor(0.294)
    k_2 = torch.tensor(850.0)
    k_3 = torch.tensor(0.0337)
    f = torch.tensor(3.8)

    # [Proell eq. 25]
    k_b = lambda temps: k_1 / (1 + torch.exp(-k_3 * (temps - k_2)))

    Ts = torch.linspace(0, 2000, 1250)
    k_b_T = k_b(Ts) * f

    fig, ax = plt.subplots(figsize=(6/2.54, 6/2.54))

    ax.plot(Ts - 273.15, k_b_T, color=colors_palette["pink"])
    ax.set_xlabel("Temperature [°C]")
    ax.set_ylabel("Kinetic factor $k_{\\beta}$ [-]")
    # ax.set_ylim([-0.05, 1.05])
    ax.set_xlim([-50, 1250])
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
    fig.tight_layout()

    folder_name = "../figs/nitzler_model"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{folder_name}/nitzler_k_b.png")
    # plt.show()


def plot_k_a_k_b():
    print("\n\n#######################################")
    print("plot_k_a_k_b")

    k_1 = torch.tensor(0.294)
    k_2 = torch.tensor(850.0)
    k_3 = torch.tensor(0.0337)
    f = torch.tensor(3.8)

    # [Proell eq. 25]
    k_as = lambda temps: k_1 / (1 + torch.exp(-k_3 * (temps - k_2)))
    k_b = lambda temps: k_1 / (1 + torch.exp(-k_3 * (temps - k_2))) * f

    Ts = torch.linspace(0, 2000, 1250)
    k_as_T = k_as(Ts)
    k_b_T = k_b(Ts)

    fig, ax = plt.subplots(figsize=(6/2.54, 6/2.54))

    # ax.plot(Ts - 273.15, k_as_T, color=colors_palette["teal"], label="$k_{\\alpha_{s}}$")
    # ax.plot(Ts - 273.15, k_b_T, color=colors_palette["pink"], label="$k_{\\beta}$")
    ax.plot(Ts - 273.15, k_as_T, label="$k_{\\alpha_{s}}$")
    ax.plot(Ts - 273.15, k_b_T, label="$k_{\\beta}$")

    ax.set_xlabel("Temperature [°C]")
    ax.set_ylabel("Kinetic factor [-]")
    ax.set_xlim([-50, 1250])
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
    ax.legend()
    fig.tight_layout()

    folder_name = "../figs/nitzler_model"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{folder_name}/nitzler_k_a_k_b.png")
    # plt.show()


if __name__ == "__main__":
    apply_rcparams()

    plot_x_a_equ()
    plot_x_am_equ()
    plot_x_a_equ_x_am_equ()
    plot_k_as()
    plot_k_b()
    plot_k_a_k_b()
