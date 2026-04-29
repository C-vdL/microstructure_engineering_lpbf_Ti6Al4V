# cmd /k cd /d $(CURRENT_DIRECTORY) && abaqus python $(FILE_NAME)

# This script goes over the OBDs in current directory and extract average temperature history

import os
import re
import csv
from odbAccess import *
from abaqusConstants import *
from time import time  # For tracking and printing time during running the script


def read_odb_nt11(filing_dict, box, IN_S, in_i, is_overwrite):
    time_alpha = time()

    # List odb files
    odb_files = []  # Contains ODB paths
    f_sim = filing_dict['f_storage_dir'] + filing_dict['f_sim'] + filing_dict["sim_id"]
    if f_sim:
        for file in os.listdir(f_sim):
            if file.endswith('.odb'):
                odb_files.append(os.path.join(f_sim, file))
    else:
        for trial in os.walk('.\\'):
            for file in trial[2]:
                if file.endswith('.odb'):
                    if len(trial[0].split('\\')) > 2:
                        continue
                    else:
                        odb_files.append(os.path.join(trial[0], file))

    #  Assuming all odb files share the same geomtery, the node labels
    # are searched for only onces. Here they are initialized as an
    # empty list.
    node_labels = []
    save_folder = filing_dict['f_storage_dir'] + filing_dict['f_csv_rds'] + filing_dict["sim_id"] + "\\" + box['name']

    # Post-processing the detected ODB files
    for cur_odb_file in odb_files:
        node_labels = []
        trial_tag = os.path.basename(cur_odb_file[-0:-4])  # name of the trial
        csv_name = os.path.join(save_folder, 'ins2_nt11_%s_%s.csv' % (box['name'], trial_tag))
        cur_odb_path = os.path.splitext(cur_odb_file)[0]

        if not is_overwrite:
            if os.path.exists(csv_name):
                print('%sAlready processed %s' % (IN_S * in_i, cur_odb_file))
                # continue

        # Delete .lck files if they exist
        lck_was = False
        if os.path.isfile(cur_odb_path + '.lck'):
            os.remove(cur_odb_path + '.lck')
            lck_was = True
        if lck_was:
            print('%sRemoved *.lck files' % (IN_S * in_i))

        # Open ODB
        time_start = time()
        odb = openOdb(path=cur_odb_file)
        ins = odb.rootAssembly.instances.items()[0][1]
        print('%sOpened ODB %s - %.2f sec' % (IN_S * in_i, cur_odb_file, time() - time_start))
        in_i += 1

        # Node search
        # if node_labels == []:
        time_start = time()
        box_limits = {  # Scan Box Limits
            'max': tuple(box['center'][i] + box['dimensions'][i] / 2 for i in range(3)),
            'min': tuple(box['center'][i] - box['dimensions'][i] / 2 for i in range(3))
        }
        for node in ins.nodes:
            if (box_limits['min'][0] < node.coordinates[0] and node.coordinates[0] < box_limits['max'][0] and \
                    box_limits['min'][1] < node.coordinates[1] and node.coordinates[1] < box_limits['max'][1] and \
                    box_limits['min'][2] < node.coordinates[2] and node.coordinates[2] < box_limits['max'][2]):
                node_labels.append(node.label)
        print('%sFound the nodes in the box - %.2f sec' % (IN_S * in_i, time() - time_start))

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        print(node_labels)
        # with open(os.path.join(save_folder,'nodes.txt'), 'w') as nodefile:
        #	nodefile.write(str(node_labels))
        print(os.getcwd())
        nodefile_name = 'nodes_%s.txt' % (os.path.basename(cur_odb_file[-12:-4]))
        with open(os.path.join(save_folder, nodefile_name), 'w') as nodefile:
            nodefile.write(str(node_labels))

        if len(node_labels) > 0:
            # Write data to CSV file
            time_start = time()
            step_keys = odb.steps.keys()  # Define the step
            # Go over frames of all steps
            in_i += 1
            temp_rows = []

            # 'target_step_id': 0,  # ID of the step in the ODB file --> used to be in STG dict
            # for frame in odb.steps[step_keys[STG['target_step_id']]].frames:
            #	# if frame.frameId%300==0:
            #	if True:
            #		print('%sProcessing frame %i'%(IN_S*in_i, frame.frameId))
            #	nt = frame.fieldOutputs['NT11'].values
            #	temp_sum = 0
            #	for label in node_labels:
            #		temp_sum += nt[label-1].data
            #	temp_rows.append([frame.frameValue, temp_sum/len(node_labels)])
            # in_i -= 1

            for ins_no in [0]:
                ins = odb.rootAssembly.instances.items()[ins_no][1]

                for cur_step in step_keys:
                    # for frame in odb.steps[step_keys[STG['target_step_id']]].frames:
                    for frame in odb.steps[cur_step].frames:

                        # if frame.frameId > 20:
                        #     break

                        # if frame.frameId%300==0:
                        if frame.frameId % 1 == 0:
                            print('%sProcessing frame %i' % (IN_S * in_i, frame.frameId))
                        nt = frame.fieldOutputs['NT11'].values
                        # print(nt[0].data)
                        # print(ins.nodes[0].label)
                        temp_sum = 0
                        for label in node_labels:
                            temp_sum += nt[label - 1].data

                        print(len(ins.nodes))
                        print(len(nt))

                        time.sleep(600)

                        for (nt_node, node) in zip(nt, ins.nodes):
                            read_out = [frame.frameValue, nt_node.data, node.coordinates[0], node.coordinates[1], node.coordinates[2]]
                            print(read_out)
                            temp_rows.append(read_out)

                        temp_rows.append([frame.frameValue, temp_sum / len(node_labels)])
            in_i -= 1

            with open(csv_name, 'wb') as csvfile:
                # Prepare csv writer
                temp_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                temp_writer.writerow(['time', 'nt11', 'x', 'y', 'z'])
                temp_writer.writerows(temp_rows)
            print('%sFinished wiritng %s - %.2f sec' % (IN_S * in_i, csv_name, time() - time_start))

            in_i -= 1
        odb.close()

    print('%sFinished the script - %.2f sec' % (IN_S * in_i, time() - time_alpha))


if __name__ == '__main__':

    is_overwrite = False

    filing_dict = {
        'f_storage_dir': 'C:\\temp\\',
        'f_sim': '\\',
        'f_csv_rds': 'csv_rds\\',
    }

    ################ Define sim_ids and boxes ################
    sim_ids = [
        'Cmodel_v32_thinwall_0-22mm_load_3n\inputs_gh_f10\Wmm3_127639',
    ]

    boxes = []
    if False:
        box_01 = {
            'center': (5.0, 5.0, 0.015),
            'dimensions': (8, 8, 0.03),
        }

        box_02 = {
            'center': (5.0, 5.0, 0.075),
            'dimensions': (8, 8, 0.03),
        }

        box_03 = {
            'center': (2, 2, 0.015),
            'dimensions': (0.3, 0.3, 0.03),
        }

        box_04 = {
            'center': (5.0, 5.0, -0.02),
            'dimensions': (8, 8, 0.1),
        }

    else:
        box_01 = {
            'center': (5.0, 5.0, 0.015),
            'dimensions': (12, 12, 0.03),
        }
        box_04 = {
            'center': (5.0, 5.0, -0.02),
            'dimensions': (12, 12, 0.1),
        }

    boxes.append(box_01)
    # boxes.append(box_02)
    # boxes.append(box_03)
    # boxes.append(box_04)

    ###########################################################

    for sim_id in sim_ids:

        filing_dict["sim_id"] = sim_id

        for box in boxes:
            # Create scan box name based on center and dimensions of box
            c_x = re.sub(r"\.", "", "{:.2f}".format(box['center'][0])).zfill(4)
            c_y = re.sub(r"\.", "", "{:.2f}".format(box['center'][1])).zfill(3)
            c_z = re.sub(r"\.", "", "{:.2f}".format(box['center'][2])).zfill(3)
            d_x = re.sub(r"\.", "", "{:.2f}".format(box['dimensions'][0])).zfill(3)
            d_y = re.sub(r"\.", "", "{:.2f}".format(box['dimensions'][1])).zfill(3)
            d_z = re.sub(r"\.", "", "{:.2f}".format(box['dimensions'][2])).zfill(3)

            box["name"] = 'b_c%s-%s-%s_d%s-%s-%s' % (c_x, c_y, c_z, d_x, d_y, d_z)

            # For indenting messages in console
            IN_S = ' > '  # The string to indent
            in_i = 1  # For controlling the level of indentation

            read_odb_nt11(filing_dict, box, IN_S, in_i, is_overwrite)