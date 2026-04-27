import os

import generate_event_series_ghanbari as evsgh

string_repl_timepoints = "0., 4.67908, 1.\n4.67908, 4.68908, 0.001\n4.68908, 6.67908, 0.01\n6.67908, 7.97704, 1.\n7.97704, 7.98704, 0.001\n7.98704, 9.97704, 0.01\n9.97704, 12.5373, 1.\n12.5373, 12.5473, 0.001\n12.5473, 14.5373, 0.01\n14.5373, 17.2716, 1.\n17.2716, 17.2816, 0.001\n17.2816, 19.2716, 0.01\n19.2716, 22.008, 1.\n22.008, 22.018, 0.001\n22.018, 24.008, 0.01\n24.008, 26.8225, 1.\n26.8225, 26.8325, 0.001\n26.8325, 28.8225, 0.01\n28.8225, 31.502, 1.\n31.502, 31.512, 0.001\n31.512, 33.502, 0.01\n33.502, 36.3228, 1.\n36.3228, 36.3328, 0.001\n36.3328, 38.3228, 0.01\n38.3228, 40.8824, 1.\n40.8824, 40.8924, 0.001\n40.8924, 42.8824, 0.01\n42.8824, 45.5578, 1.\n45.5578, 45.5678, 0.001\n45.5678, 47.5578, 0.01\n47.5578, 50.1078, 1."
string_repl_roller = "1.67908,-1.,0.,0.03,1.\n4.67908,11.,0.,0.03,0.\n4.97704,-1.,0.,0.06,1.\n7.97704,11.,0.,0.06,0.\n9.53728,-1.,0.,0.09,1.\n12.5373,11.,0.,0.09,0.\n14.2716,-1.,0.,0.12,1.\n17.2716,11.,0.,0.12,0.\n19.008,-1.,0.,0.15,1.\n22.008,11.,0.,0.15,0.\n23.8225,-1.,0.,0.18,1.\n26.8225,11.,0.,0.18,0.\n28.502,-1.,0.,0.21,1.\n31.502,11.,0.,0.21,0.\n33.3228,-1.,0.,0.24,1.\n36.3228,11.,0.,0.24,0.\n37.8824,-1.,0.,0.27,1.\n40.8824,11.,0.,0.27,0.\n42.5578,-1.,0.,0.3,1.\n45.5578,11.,0.,0.3,0.\n"
string_repl_amp = "*Amplitude, name=Amp-layer1, time=TOTAL TIME\n        4.67908,              0.,         4.67918,              1.,         4.68008,              1.,         4.68018,              0.\n*Amplitude, name=Amp-layer2, time=TOTAL TIME\n        7.97704,              0.,         7.97714,              1.,         7.97804,              1.,         7.97814,              0.\n*Amplitude, name=Amp-layer3, time=TOTAL TIME\n       12.53728,              0.,        12.53738,              1.,        12.53828,              1.,        12.53838,              0.\n*Amplitude, name=Amp-layer4, time=TOTAL TIME\n        17.2716,              0.,         17.2717,              1.,         17.2726,              1.,         17.2727,              0.\n*Amplitude, name=Amp-layer5, time=TOTAL TIME\n       22.00799,              0.,        22.00809,              1.,        22.00899,              1.,        22.00909,              0.\n*Amplitude, name=Amp-layer6, time=TOTAL TIME\n       26.82251,              0.,        26.82261,              1.,        26.82351,              1.,        26.82361,              0.\n*Amplitude, name=Amp-layer7, time=TOTAL TIME\n       31.50203,              0.,        31.50213,              1.,        31.50303,              1.,        31.50313,              0.\n*Amplitude, name=Amp-layer8, time=TOTAL TIME\n       36.32279,              0.,        36.32289,              1.,        36.32379,              1.,        36.32389,              0.\n*Amplitude, name=Amp-layer9, time=TOTAL TIME\n       40.88242,              0.,        40.88252,              1.,        40.88342,              1.,        40.88352,              0.\n*Amplitude, name=Amp-layer10, time=TOTAL TIME\n       45.55777,              0.,        45.55787,              1.,        45.55877,              1.,        45.55887,              0.\n"

# Folder and file setup
folder = r"C:\temp\Cmodel_v28_thinwall_10mm_load\inputs_4-5"
base_filename = "Job-HT_Cmodel_v28_10mm_33333_4-5.inp"

folder = r"C:\temp\Cmodel_v28_thinwall_0-3mm_load\inputs_4-5"
base_filename = "Job-HT_Cmodel_v28_thinwall_0-3mm_33333_4-5.inp"

folder = r"C:\temp\Cmodel_v31_thinwall_0-22mm_load\inputs_gh"
base_filename = "Job-HT_Cmodel_v30_thinwall_0-22mm_33333_4-5-cond15.inp"

folder = r"C:\temp\Cmodel_v32_thinwall_0-22mm_load_3n\inputs_gh"
base_filename = "Job-HT_Cmodel_v32_thinwall_0-22mm_33333_4-5-cond15.inp"

folder = r"C:\temp\Cmodel_v32_thinwall_0-22mm_load_3n\inputs_gh_f10"
base_filename = "Job-HT_Cmodel_v32_thinwall_0-22mm_33333_12-cond15.inp"





# thin wall
folder = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_12_f10"
base_filename = "Job-HT_Cmodel_v33_thinwall_0-22mm_33333_12-cond15.inp"

# cube
folder = r"C:\temp\Cmodel_v34_10mm_load\inputs_12_f10"
base_filename = "Job-HT_Cmodel_v34_10mm_33333_12-cond15.inp"

# pyramid
folder = r"C:\temp\Cmodel_v41_invpy\inputs_12_f10"
base_filename = "Job-HT_Cmodel_v41_invpy_33333_12-cond15.inp"


# # cube
# folder = r"C:\temp\Cmodel_v34_10mm_load\inputs_12_f10_Ti64"
# base_filename = "Job-HT_Cmodel_v34_10mm_33333_12-cond15_Ti64.inp"
# #
# # cube
# folder = r"C:\temp\Cmodel_v34_10mm_load\inputs_12_f1_Ti64"
# base_filename = "Job-HT_Cmodel_v34_10mm_33333_12-cond15_Ti64.inp"

if True:
    # thin wall
    folder = r"C:\temp\Cmodel_v33_thinwall_0-22mm_load_3n\inputs_12_f1_Ti64"
    base_filename = "Job-HT_Cmodel_v33_thinwall_0-22mm_33333_12-cond15_Ti64.inp"
if True:
    # pyramid
    folder = r"C:\temp\Cmodel_v41_invpy\inputs_12_f1_Ti64"
    base_filename = "Job-HT_Cmodel_v41_invpy_33333_12-cond15_Ti64.inp"
if True:
    # cube
    folder = r"C:\temp\Cmodel_v34_10mm_load\inputs_12_f1_Ti64"
    base_filename = "Job-HT_Cmodel_v34_10mm_33333_12-cond15_Ti64.inp"


base_path = os.path.join(folder, base_filename)

# List of replacement values
values = [
    340136, 282187, 130208, 59524, 51760, 250627, 92971, 123810,
    129400, 197664, 77277, 71429, 115035, 52693, 123153,
    127639, 137255, 86081, 80559, 77381, 127639, 85034
]

layer_start_times_sets = [
    [4.71560, 8.06834, 12.68336, 17.47246, 22.26363, 27.13293, 31.86723, 36.74277, 41.35718, 46.08731],
    [4.73254, 8.11069, 12.75112, 17.56563, 22.38221, 27.27692, 32.03663, 36.93758, 41.57740, 46.33294],
    [4.68970, 8.00359, 12.57976, 17.33001, 22.08233, 26.91278, 31.60823, 36.44492, 41.02048, 45.71176],
    [4.67234, 7.96019, 12.51032, 17.23453, 21.96081, 26.76522, 31.43463, 36.24528, 40.79480, 45.46004],
    [4.67296, 7.96174, 12.51280, 17.23794, 21.96515, 26.77049, 31.44083, 36.25241, 40.80286, 45.46903],
    [4.71110, 8.05709, 12.66536, 17.44771, 22.23213, 27.09468, 31.82223, 36.69102, 41.29868, 46.02206],
    [4.67750, 7.97309, 12.53096, 17.26291, 21.99693, 26.80908, 31.48623, 36.30462, 40.86188, 45.53486],
    [4.68512, 7.99214, 12.56144, 17.30482, 22.05027, 26.87385, 31.56243, 36.39225, 40.96094, 45.64535],
    [4.70194, 8.03419, 12.62872, 17.39733, 22.16801, 27.01682, 31.73063, 36.58568, 41.17960, 45.88924],
    [4.69620, 8.01984, 12.60576, 17.36576, 22.12783, 26.96803, 31.67323, 36.51967, 41.10498, 45.80601],
    [4.67600, 7.96934, 12.52496, 17.25466, 21.98643, 26.79633, 31.47123, 36.28737, 40.84238, 45.51311],
    [4.67664, 7.97094, 12.52752, 17.25818, 21.99091, 26.80177, 31.47763, 36.29473, 40.85070, 45.52239],
    [4.68094, 7.98169, 12.54472, 17.28183, 22.02101, 26.83832, 31.52063, 36.34418, 40.90660, 45.58474],
    [4.67486, 7.96649, 12.52040, 17.24839, 21.97845, 26.78664, 31.45983, 36.27426, 40.82756, 45.49658],
    [4.69294, 8.01169, 12.59272, 17.34783, 22.10501, 26.94032, 31.64063, 36.48218, 41.06260, 45.75874],
    [4.67908, 7.97704, 12.53728, 17.27160, 22.00799, 26.82251, 31.50203, 36.32279, 40.88242, 45.55777],
    [4.68198, 7.98429, 12.54888, 17.28755, 22.02829, 26.84716, 31.53103, 36.35614, 40.92012, 45.59982],
    [4.67384, 7.96394, 12.51632, 17.24278, 21.97131, 26.77797, 31.44963, 36.26253, 40.81430, 45.48179],
    [4.67350, 7.96309, 12.51496, 17.24091, 21.96893, 26.77508, 31.44623, 36.25862, 40.80988, 45.47686],
    [4.68346, 7.98799, 12.55480, 17.29569, 22.03865, 26.85974, 31.54583, 36.37316, 40.93936, 45.62128],
    [4.67908, 7.97704, 12.53728, 17.27160, 22.00799, 26.82251, 31.50203, 36.32279, 40.88242, 45.55777],
    [4.68704, 7.99694, 12.56912, 17.31538, 22.06371, 26.89017, 31.58163, 36.41433, 40.98590, 45.67319]
]

layer_start_time_set = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119]
layer_start_times_sets = [layer_start_time_set for i in range(22)]

# Read the base file content once
with open(base_path, 'r') as file:
    base_content = file.read()

# Process each value
for val, layer_start_times in zip(values, layer_start_times_sets):
    # if val != 127639:
    #     continue

    factor = 1

    val_str = str(int(val))
    val_str_mag = str(int(val / factor * 0.6))  # 0.6 for Ti64, 0.48 for HX

    # Replace '450000' with the current value
    new_content = base_content.replace('33333', val_str_mag)
    new_filename = base_filename.replace('33333', val_str)

    layer_duration = 12  # 12   # 4.55
    no_layer = 10
    offset = 0
    recoat_time = 8  # 8  # 3
    layer_thickness = 0.03
    x_start = 4.5
    x_start_recoater = -1
    x_end_recoater = 11
    travel_distance = 1.0
    first_laser = 11
    end_time = 130

    # Change timepoints
    string_timepoints = evsgh.generate_timepoints(layer_duration, layer_start_times, no_layer, offset, recoat_time)

    # Change recoater
    string_recoater = evsgh.generate_recoater_series(layer_start_times, layer_thickness, no_layer, offset, recoat_time,
                                                     x_end_recoater, x_start_recoater)

    # Change amplitudes
    string_amplitudes = evsgh.generate_amplitudes(layer_start_times, 0.001 * factor, layer_duration, first_laser)

    new_content = new_content.replace(string_repl_timepoints, string_timepoints)
    new_content = new_content.replace(string_repl_roller, string_recoater)
    new_content = new_content.replace(string_repl_amp, string_amplitudes)

    new_content = new_content.replace("0.001, 120., 1e-06, 1., ", f"0.001, {end_time}, 1e-06, 1., ")
    new_content = new_content.replace("*Conductivity\n 0.0286,", f"*Conductivity\n 0.0200,")


    # Create a subfolder W{val}
    subfolder = os.path.join(folder, f"Wmm3_{val_str}")
    os.makedirs(subfolder, exist_ok=True)

    # Path to the new file inside the subfolder
    new_path = os.path.join(subfolder, new_filename)

    # Write the modified content to the new file
    with open(new_path, 'w') as file:
        file.write(new_content)

print("All files generated in respective subfolders.")
