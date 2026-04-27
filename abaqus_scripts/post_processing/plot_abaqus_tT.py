import os
import pandas as pd
import matplotlib.pyplot as plt
import re

magnitudes = [
    340136, 282187, 130208, 59524, 51760, 250627, 92971, 123810,
    129400, 197664, 77277, 71429, 115035, 52693, 123153,
    127639, 137255, 86081, 80559, 77381, 127639, 85034
]

magnitudes.sort(reverse=True)


# Base folder containing subfolders with CSV files
base_folder = r"C:\temp\csv_rds\Cmodel_v23_thinwall_1mm\inputs"
base_folder = r"C:\temp\csv_rds\Cmodel_v23_thinwall_1mm\inputs_4-5"

base_folder = r"C:\temp\csv_rds\Cmodel_v18_largemesh\inputs2"
base_folder = r"C:\temp\csv_rds\Cmodel_v18_largemesh\inputs_4-5"


base_folder = r"C:\temp\csv_rds\Cmodel_v32_thinwall_0-22mm_load_3n\inputs_gh"

base_folder = r"C:\temp\csv_rds\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_gh_f1"
# base_folder = r"C:\temp\csv_rds\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_gh_f10_Ti64"
# base_folder = r"C:\temp\csv_rds\Cmodel_v34_10mm_load\inputs_gh_f10"
# base_folder = r"C:\temp\csv_rds\Cmodel_v34_10mm_load\inputs_gh_f10_Ti64"
# base_folder = r"C:\temp\csv_rds\Cmodel_v41_invpy\inputs_gh_f10"
# base_folder = r"C:\temp\csv_rds\Cmodel_v41_invpy\inputs_gh_f10_Ti64"
# base_folder = r"C:\temp\csv_rds\Cmodel_v34_10mm_load\inputs_gh_f2"


base_path1 = r"C:\temp\csv_rds\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_12_f1"  # thin wall --
base_path2 = r"C:\temp\csv_rds\Cmodel_v34_10mm_load\inputs_12_f1"  # cube --
base_path3 = r"C:\temp\csv_rds\Cmodel_v41_invpy\inputs_12_f1"  # pyramid --

base_path4 = r"C:\temp\csv_rds\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_12_f1_Ti64"  # thin wall --
base_path5 = r"C:\temp\csv_rds\Cmodel_v34_10mm_load\inputs_12_f1_Ti64"  # cube --
base_path6 = r"C:\temp\csv_rds\Cmodel_v41_invpy\inputs_12_f1_Ti64"  # pyramid x-

base_path7 = r"C:\temp\csv_rds\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_gh_f1"  # thin wall x
base_path8 = r"C:\temp\csv_rds\Cmodel_v34_10mm_load\inputs_gh_f1"  # cube -
base_path9 = r"C:\temp\csv_rds\Cmodel_v41_invpy\inputs_gh_f1"  # pyramid x-

base_path10 = r"C:\temp\csv_rds\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_gh_f1_Ti64"  # thin wall -
base_path11 = r"C:\temp\csv_rds\Cmodel_v34_10mm_load\inputs_gh_f1_Ti64"  # cube -
base_path12 = r"C:\temp\csv_rds\Cmodel_v41_invpy\inputs_gh_f1_Ti64"  # pyramid x-


base_folder = base_path1








box_name = "b_c0500-500-001_d1200-1200-003"
box_name = "b_c0500-500--002_d1200-1200-010"
box_name = "b_c0500-500--007_d1200-1200-020"
box_name = "b_c0500-500--002_d1200-1300-010"

box_name = "b_c0500-500--000_d1200-1300-010"
# box_name = "b_c0500-500-001_d1200-1200-003"


# Set up plot
plt.figure(figsize=(12, 6))

i = 0
indices = []

# Iterate over first-level subfolders
for subfolder_name in os.listdir(base_folder):
    subfolder_path = os.path.join(base_folder, subfolder_name, box_name)

    # Extract the number after 'Wmm3_'
    match = re.search(r'Wmm3_(\d+)', subfolder_name)
    if match:
        value = int(match.group(1))  # e.g., 115035
        try:
            index = magnitudes.index(value)
            print(f"Index in magnitudes: {index}")
        except ValueError:
            print(f"Value {value} not found in magnitudes.")
    else:
        print("Pattern 'Wmm3_<number>' not found in subfolder_name.")

    if os.path.isdir(subfolder_path):
        # Look for .csv files in the subfolder
        for file_name in os.listdir(subfolder_path):
            if file_name.lower().endswith('.csv'):
                csv_path = os.path.join(subfolder_path, file_name)

                if "W2295918" in file_name or "W1904762" in file_name or "W1691729" in file_name:  # or "W1334232" in file_name:
                    continue

                if "340136" in file_name or "282187" in file_name or "250627" in file_name or "197664" in file_name:  # or "W1334232" in file_name:
                    continue

                try:
                    df = pd.read_csv(csv_path)

                    # Ensure 'time' and 'nt11' columns exist
                    if 'time' in df.columns and 'nt11' in df.columns:
                        # plt.scatter(df['time'], df['nt11']+273.15, label=subfolder_name, s=10)
                        plt.plot(df['time'] + 0.15*index, df['nt11'], label=value)
                        indices.append(index)

                    else:
                        print(f"Missing 'time' or 'nt11' in {csv_path}")
                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")


    i = i + 1

# Final plot formatting
plt.xlabel("Time")
plt.ylabel("nt11")
plt.title("Scatter Plot of nt11 vs Time for Each Subfolder")

# reordering the labels
handles, labels = plt.gca().get_legend_handles_labels()

# specify order
order = [index for index, value in sorted(enumerate(indices), key=lambda t: t[1])]

# pass handle & labels lists along with order as below
plt.legend([handles[i] for i in order], [labels[i] for i in order], title="W/mm^3", loc='upper right', fontsize=8)

# plt.legend(title="Subfolder", loc='upper right', fontsize=8)
plt.grid(True)
plt.ylim(0,3000)
# plt.xlim(0,50)
plt.tight_layout()
print()
plt.savefig(f"{base_folder}/tT_comp.png")
plt.show()
