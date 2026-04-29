import itertools
import json
import os
from datetime import datetime
from pathlib import Path

import git
import numpy as np
import pandas as pd
from scipy.stats import qmc


def save_input_kwargs(folder_name, kwargs_dict):

    for key, kwargs in kwargs_dict.items():
        # Save the JSON files in the folder
        kwargs_path = os.path.join(folder_name, f"{key}.json")
        with open(kwargs_path, "w") as f:
            json.dump(kwargs, f, indent=4)

        print(f"{key}: {kwargs}")


def generate_folder_name(suffix):
    # Get the short git hash
    def get_git_short_hash():
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        short_sha = repo.git.rev_parse(sha, short=1)
        return short_sha

    git_short_hash = get_git_short_hash()
    # Generate the folder name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]
    folder_name = Path(f"execs/{timestamp}_{git_short_hash}_{suffix}")
    print(f"\nfolder_name: {folder_name}")
    # Create the subfolder
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


def get_FullFactorial_DOE(bounds, levels, discrete_vars):
    """
    Generates a Full Factorial DOE.

    Parameters:
    - bounds (dict): Variable bounds as {variable_name: (min, max)}
    - levels (dict): Number of levels for each variable
    - discrete_vars (list): List of discrete variable names

    Returns:
    - df_doe (pd.DataFrame): Full Factorial DOE DataFrame
    """
    # Generate all levels for each variable
    grid_values = {
        var: np.linspace(bounds[var][0], bounds[var][1], levels[var])
        if var not in discrete_vars
        else np.arange(bounds[var][0], bounds[var][1] + 1)  # Ensure discrete vars are integers
        for var in bounds
    }

    # Generate full factorial combinations
    full_factorial_samples = list(itertools.product(*grid_values.values()))

    # Convert to DataFrame
    df_doe = pd.DataFrame(full_factorial_samples, columns=bounds.keys())

    # Ensure discrete variables are integers
    for discrete_var in discrete_vars:
        df_doe[df_doe.columns[discrete_var]] = df_doe[df_doe.columns[discrete_var]].astype("int")

    return df_doe


def get_LHS_DOE(bounds, num_samples, discrete_vars):
    """
    Generates a Latin Hypercube DOE.

    Parameters:
    - bounds (dict): Variable bounds as {variable_name: (min, max)}
    - num_samples (int): Number of samples
    - discrete_vars (list): List of discrete variable names

    Returns:
    - df_doe (pd.DataFrame): Latin Hypercube DOE DataFrame
    """

    # Create a Latin Hypercube Sampling (LHS) design
    sampler = qmc.LatinHypercube(d=len(bounds))  # d = number of variables
    lhs_samples = sampler.random(n=num_samples)  # Generate samples

    # Scale the samples to the actual variable ranges
    scaled_samples = qmc.scale(lhs_samples,
                               l_bounds=[bounds[var][0] for var in bounds],
                               u_bounds=[bounds[var][1] for var in bounds])

    # Convert discrete variables to discrete integers
    for discrete_var in discrete_vars:
        scaled_samples[:, discrete_var] = np.round(scaled_samples[:, discrete_var])

    # Convert to a DataFrame for easy handling
    df_doe = pd.DataFrame(scaled_samples, columns=bounds.keys())

    # Ensure discrete variables are integers
    for discrete_var in discrete_vars:
        df_doe[discrete_var] = df_doe[discrete_var].astype("int")

    print(df_doe)

    # # Iterate through DOE samples and print parameters
    # print("Latin Hypercube DOE Samples:")
    # for i, row in df_doe.iterrows():
    #     print(f"Sample {i + 1}: Q_coef={row['Q_coef']:.3f}, q_dt={row['q_dt']:.3f}, T_bottom={row['T_bottom']:.1f}")

    return df_doe


def ofat_doe(bounds, levels, discrete_vars, log_vars):

    # Compute baseline values: arithmetic mean for linear variables, geometric mean for log variables
    baseline = {
        key: (np.sqrt(bounds[key][0] * bounds[key][1]) if key in log_vars else (bounds[key][0] + bounds[key][1]) / 2)
        for key in bounds
    }
    print(f"BASELINE {baseline}")

    # Initialize list to store experiments
    experiments = []

    # Loop through each factor
    for factor, (low, high) in bounds.items():
        # Determine whether to use linear or logarithmic spacing
        if factor in log_vars:
            factor_levels = np.logspace(np.log10(low), np.log10(high), levels[factor])
        else:
            factor_levels = np.linspace(low, high, levels[factor])

        for level in factor_levels:
            # Copy baseline and modify only the current factor
            experiment = baseline.copy()
            experiment[factor] = level
            experiments.append(experiment)

    # Convert list of experiments to DataFrame
    df_doe = pd.DataFrame(experiments).drop_duplicates().sort_values(by=list(bounds.keys()))

    # Ensure discrete variables are integers
    for discrete_var in discrete_vars:
        df_doe[discrete_var] = df_doe[discrete_var].astype("int")

    print(df_doe)

    return df_doe


def ofat_doe_old(bounds, levels, discrete_vars, log_vars):
    # Get baseline (default) values as the midpoint of bounds
    baseline = {key: (bounds[key][0] + bounds[key][1]) / 2 for key in bounds}

    # Initialize list to store experiments
    experiments = []

    # Loop through each factor
    for factor, (low, high) in bounds.items():
        # Generate levels for this factor
        factor_levels = np.linspace(low, high, levels[factor])

        for level in factor_levels:
            # Copy baseline and modify only the current factor
            experiment = baseline.copy()
            experiment[factor] = level
            experiments.append(experiment)

    # Convert list of experiments to DataFrame
    df_doe = pd.DataFrame(experiments).drop_duplicates()

    # Ensure discrete variables are integers
    for discrete_var in discrete_vars:
        df_doe[discrete_var] = df_doe[discrete_var].astype("int")

    print(df_doe)

    return df_doe


def create_full_factorial_doe_indiv(energy_density, q_dt, T_bottom, layer_thickness):
    # G_mapping and N_mapping currently implemented for 30µm, 60µm, 90µm, and 120µm layer thicknesses.
    # For other layer thicknesses, these mappings would need to be updated.

    # Full factorial design
    doe = pd.DataFrame(
        itertools.product(
            energy_density,
            q_dt,
            T_bottom,
            layer_thickness
        ),
        columns=[
            "energy_density",
            "q_dt",
            "T_bottom",
            "layer_thickness",
        ],
    )

    # Mapping for G and N based on layer_thickness
    # G_map = {
    #     30e-6: [10, 90],
    #     60e-6: [5, 45],
    #     90e-6: [3, 30],
    #     120e-6: [2, 23],
    # }

    # Updates G based on layer thickness, so that investigated location is at same build height for all layer thicknesses
    G_map = {
        30e-6: [90],
        60e-6: [45],
        90e-6: [30],
        120e-6: [23],
    }

    # Updates N based on layer thickness, so that total build height is the same for all layer thicknesses
    N_map = {
        30e-6: 630,
        60e-6: 315,
        90e-6: 210,
        120e-6: 158,
    }

    # Attach G as list, then explode once
    doe["G"] = doe["layer_thickness"].map(G_map)
    doe = doe.explode("G", ignore_index=True)

    # Attach N
    doe["N"] = doe["layer_thickness"].map(N_map)

    return doe

