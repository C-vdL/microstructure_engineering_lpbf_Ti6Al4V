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
base_path3 = r"C:\temp\inv_pyramid\inputs_gh_f1_Ti64"  # pyramid


base_paths = [base_path1, base_path2, base_path3]

counter_jobs = 0

for (i, base_path) in enumerate(base_paths):

    for (j, mag) in enumerate(reversed(magnitudes)):

        mag = int(mag)

        folder = f"Wmm3_{mag}"

        folder_path = os.path.join(base_path, folder)

        print(folder_path)
        print(job_name)

        print(f"Running job for magnitude {mag}...")

        command = f"abaqus job={job_name} cpus=4"
        print(command)

        success = "THE ANALYSIS HAS COMPLETED SUCCESSFULLY"
        file_path = os.path.join(folder_path, f"{job_name}.sta")

        is_repeat = True  # Default to True

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if success in content:
                    is_repeat = False

        if is_repeat:

            subprocess.run(
                f"abaqus job={job_name} cpus=4",
                shell=True,
                cwd=folder_path,
                check=True
            )

            print(f"Job {job_name} submitted successfully.\n")
            counter_jobs += 1

        else:
            print(f"Job {job_name} already completed.\n")

        if counter_jobs >= 6:
            print(f"\nSleeping for 10 minutes...\n")
            time.sleep(900)
            counter_jobs = 0

    print(f"All jobs processed for {base_path}.")
