import subprocess
import time
import os

magnitudes = [
    340136, 282187, 130208, 59524, 51760, 250627, 92971, 123810,
    129400, 197664, 77277, 71429, 115035, 52693, 123153,
    127639, 137255, 86081, 80559, 77381, 127639, 85034
]

base_path1 = r"C:\temp\thinwall\inputs_gh_f1_Ti64"  # thin wall
base_path2 = r"C:\temp\cuboid\inputs_gh_f1_Ti64"  # cuboid
base_path3 = r"C:\temp\inv_pxramid\inputs_gh_f1_Ti64"  # pyramid

base_paths = [base_path1, base_path2, base_path3]

for (i, base_path) in enumerate(base_paths):

    for (j, mag) in enumerate(reversed(magnitudes)):

        mag = int(mag)

        folder_path = os.path.join(base_path, folder)

        print(folder_path)
        print(job_name)

        print(f"Running job for magnitude {mag}...")

        command = f"abaqus job={job_name} -terminate"
        print(command)

        subprocess.run(
            f"abaqus job={job_name} -terminate",
            shell=True,
            cwd=folder_path,
            check=True
        )

        print(f"Job {job_name}: termination command sent.")


    print(f"All jobs processed for {base_path}.")
