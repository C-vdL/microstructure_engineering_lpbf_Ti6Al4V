import subprocess
import time
import os

magnitudes = [
    # 450000,
    2295918, 1904762, 878906, 401786, 349379, 1691729, 627551,
    835714, 873447, 1334232, 521617, 482143, 776485, 355679,
    831281, 861561, 926471, 581044, 543770, 522321, 861561, 573980
]

base_path1 = r"C:\temp\Cmodel_v23_thinwall_1mm\inputs_4-5" ##
base_path2 = r"C:\temp\Cmodel_v23_thinwall_1mm\inputs" ####
base_path3 = r"C:\temp\Cmodel_v18_largemesh\inputs_4-5" ######
base_path4 = r"C:\temp\Cmodel_v18_largemesh\inputs2"  ########

magnitudes = [
    340136, 282187, 130208, 59524, 51760, 250627, 92971, 123810,
    129400, 197664, 77277, 71429, 115035, 52693, 123153,
    127639, 137255, 86081, 80559, 77381, 127639, 85034
]

base_path1 = r"C:\temp\Cmodel_v32_thinwall_0-22mm_load_3n\inputs_gh" ##
base_path1 = r"C:\temp\Cmodel_v32_thinwall_0-22mm_load_3n\inputs_gh_f15" ##
base_path2 = r"C:\temp\Cmodel_v31_thinwall_0-22mm_load\inputs_gh" ####
base_path3 = r"C:\temp\Cmodel_v28_thinwall_10mm_load\inputs_4-5" ######
base_path3 = r"C:\temp\Cmodel_v29_10mm_load\inputs_4-5"
base_path4 = r"C:\temp\Cmodel_v28_thinwall_0-3mm_load\inputs_4-5"  ########


base_path1 = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_12_f10_Ti64"  # thin wall
base_path2 = r"C:\temp\Cmodel_v34_10mm_load\inputs_12_f10"  # cube
base_path3 = r"C:\temp\Cmodel_v41_invpy\inputs_12_f10_Ti64"  # pyramid
base_path4 = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_gh_f1_Ti64"




base_path1 = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_12_f1"  # thin wall --+
base_path2 = r"C:\temp\Cmodel_v34_10mm_load\inputs_12_f1"  # cube --+
base_path3 = r"C:\temp\Cmodel_v41_invpy\inputs_12_f1"  # pyramid --+

base_path4 = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_12_f1_Ti64"  # thin wall --+
base_path5 = r"C:\temp\Cmodel_v34_10mm_load\inputs_12_f1_Ti64"  # cube --+
base_path6 = r"C:\temp\Cmodel_v41_invpy\inputs_12_f1_Ti64"  # pyramid --+

base_path7 = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_gh_f1"  # thin wall --+
base_path8 = r"C:\temp\Cmodel_v34_10mm_load\inputs_gh_f1"  # cube -x+
base_path9 = r"C:\temp\Cmodel_v41_invpy\inputs_gh_f1"  # pyramid -+

base_path10 = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_gh_f1_Ti64"  # thin wall -+
base_path11 = r"C:\temp\Cmodel_v34_10mm_load\inputs_gh_f1_Ti64"  # cube -+
base_path12 = r"C:\temp\Cmodel_v41_invpy\inputs_gh_f1_Ti64"  # pyramid -+




base_paths = [base_path1, base_path2, base_path3,
              base_path4, base_path5, base_path6,
              base_path7, base_path8, base_path9,
              base_path10, base_path11, base_path12]
print("\nSleeping for 60 minutes...\n")

# time.sleep(60*60)

for (i, base_path) in enumerate(base_paths):

    for (j, mag) in enumerate(reversed(magnitudes)):
        # folder = f"W{mag}"
        # if i == 0:
        #     job_name = f"Job-HT_Cmodel_v23_iw0-001_W{mag}_3ph1e-3_mu0-7_1mm4-5" ##
        # elif i == 1:
        #     job_name = f"Job-HT_Cmodel_v23_iw0-001_W{mag}_3ph1e-3_mu0-7_1mm"  ####
        # elif i == 2:
        #     job_name = f"Job-HT_Cmodel_v18_iw0-001_W{mag}_3ph1e-3_mu0-7_int4-5"  ######
        #     ##########   Job-HT_Cmodel_v18_iw0-001_W482143_3ph1e-3_mu0-7_int4-5
        # elif i == 3:
        #     job_name = f"Job-HT_Cmodel_v18_iw0-001_W{mag}_3ph1e-3_mu0-7"  ########

        mag = int(mag)

        folder = f"Wmm3_{mag}"
        if i == 0:
            job_name = f"Job-HT_Cmodel_v33_thinwall_0-22mm_{mag}_12-cond15"  ####
            wait_time = 5
            continue
        elif i == 1:
            job_name = f"Job-HT_Cmodel_v34_10mm_{mag}_12-cond15"  ####
            wait_time = 5
            continue
        elif i == 2:
            job_name = f"Job-HT_Cmodel_v41_invpy_{mag}_12-cond15"  ######
            wait_time = 5
            continue
        elif i == 3:
            job_name = f"Job-HT_Cmodel_v33_thinwall_0-22mm_{mag}_12-cond15_Ti64"  ####
            continue
            wait_time = 5
        elif i == 4:
            job_name = f"Job-HT_Cmodel_v34_10mm_{mag}_12-cond15_Ti64"  ####
            continue
            wait_time = 5
        elif i == 5:
            job_name = f"Job-HT_Cmodel_v41_invpy_{mag}_12-cond15_Ti64"  ######
            continue
            wait_time = 5
        elif i == 6:
            job_name = f"Job-HT_Cmodel_v33_thinwall_0-22mm_{mag}_4-5-cond15"  ####
            continue

            wait_time = 5
        elif i == 7:
            job_name = f"Job-HT_Cmodel_v34_10mm_{mag}_4-5-cond15"  ####
            continue
            wait_time = 5
        elif i == 8:
            job_name = f"Job-HT_Cmodel_v41_invpy_{mag}_4-5-cond15"  ######
            continue
            wait_time = 5
        elif i == 9:
            job_name = f"Job-HT_Cmodel_v33_thinwall_0-22mm_{mag}_4-5-cond15_Ti64"  ####
            wait_time = 5
            # if mag in [85034, 92971, 127639, 86081]:
            continue
        elif i == 10:
            job_name = f"Job-HT_Cmodel_v34_10mm_{mag}_4-5-cond15_Ti64"  ####
            wait_time = 5
            continue
        elif i == 11:
            job_name = f"Job-HT_Cmodel_v41_invpy_{mag}_4-5-cond15_Ti64"  ######
            wait_time = 5
            if mag not in [123153, 52693, 71429]:
                continue




            # if mag not in [123810, 130208, 250627, 282187, 340136, 51760, 59524, 71429, 92971]:
            #     continue
            # if mag not in [51760, 59524, 71429, 92971]:
            #     continue
            # if mag not in [51760, 59524]:
            #     continue

        folder_path = os.path.join(base_path, folder)

        print(folder_path)
        print(job_name)

        print(f"Running job for magnitude {mag}...")

        command = f"abaqus job={job_name} -terminate"
        print(command)

        # # try:
        # # Change working directory to target folder
        # os.chdir(folder_path)
        #
        # # Run abaqus command
        # subprocess.run(command, check=True)
        #
        # # subprocess.run([
        # #     "abaqus",
        # #     f"job={job_name}",
        # #     "cpus=4"
        # # ], check=True)

        subprocess.run(
            f"abaqus job={job_name} -terminate",
            shell=True,
            cwd=folder_path,
            check=True
        )

        print(f"Job {job_name} submitted successfully.")

        # except Exception as e:
        #     print(f"Error with magnitude {mag}: {e}")

        # Sleep for 10 minutes before next iteration
        if j % 1 == 0 and j != 0:
            print("\nSleeping for 10 minutes...\n")
            time.sleep(5)

    print(f"All jobs processed for {base_path}.")
