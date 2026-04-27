# import os
# import shutil
#
# # Folder and file setup
# folder = r"C:\temp\Cmodel_v18_largemesh\inputs"
# base_filename = "Job-HT_Cmodel_v18_iw0-001_W450000_3ph1e-3_mu0-7.inp"
# base_path = os.path.join(folder, base_filename)
#
# # List of replacement values
# values = [
#     2295918, 1904762, 878906, 401786, 349379, 1691729, 627551,
#     835714, 873447, 1334232, 521617, 482143, 776485, 355679,
#     831281, 861561, 926471, 581044, 543770, 522321, 861561, 573980
# ]
#
# # Read the base file content once
# with open(base_path, 'r') as file:
#     base_content = file.read()
#
# # Process each value
# for val in values:
#     # Replace '450000' with the current value in content and filename
#     new_content = base_content.replace('450000', str(val))
#     new_filename = base_filename.replace('450000', str(val))
#     new_path = os.path.join(folder, new_filename)
#
#     # Write the new file
#     with open(new_path, 'w') as file:
#         file.write(new_content)
#
# print("File generation completed.")

import os

# Folder and file setup
folder = r"C:\temp\Cmodel_v18_largemesh\inputs"
base_filename = "Job-HT_Cmodel_v18_iw0-001_W450000_3ph1e-3_mu0-7.inp"

folder = r"C:\temp\Cmodel_v23_thinwall_1mm\inputs"
base_filename = "Job-HT_Cmodel_v23_iw0-001_W450000_3ph1e-3_mu0-7_1mm.inp"

folder = r"C:\temp\Cmodel_v23_thinwall_1mm\inputs_4-5"
base_filename = "Job-HT_Cmodel_v23_iw0-001_W450000_3ph1e-3_mu0-7_1mm4-5.inp"

folder = r"C:\temp\Cmodel_v18_largemesh\inputs_4-5"
base_filename = "Job-HT_Cmodel_v18_iw0-001_W482143_3ph1e-3_mu0-7_int4-5.inp"

# folder = r"C:\temp\Cmodel_v18_largemesh\inputs2"
# base_filename = "Job-HT_Cmodel_v18_iw0-001_W450000_3ph1e-3_mu0-7.inp"

base_path = os.path.join(folder, base_filename)

# List of replacement values
values = [
    2295918, 1904762, 878906, 401786, 349379, 1691729, 627551,
    835714, 873447, 1334232, 521617, 482143, 776485, 355679,
    831281, 861561, 926471, 581044, 543770, 522321, 861561, 573980
]

# Read the base file content once
with open(base_path, 'r') as file:
    base_content = file.read()

# Process each value
for val in values:
    val_str = str(val)

    # Replace '450000' with the current value
    new_content = base_content.replace('482143', val_str)
    new_filename = base_filename.replace('482143', val_str)

    # Create a subfolder W{val}
    subfolder = os.path.join(folder, f"W{val_str}")
    os.makedirs(subfolder, exist_ok=True)

    # Path to the new file inside the subfolder
    new_path = os.path.join(subfolder, new_filename)

    # Write the modified content to the new file
    with open(new_path, 'w') as file:
        file.write(new_content)

print("All files generated in respective subfolders.")

