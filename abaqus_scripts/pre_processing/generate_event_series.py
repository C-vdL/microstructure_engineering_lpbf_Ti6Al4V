import csv
import os


def generate_layered_table(filename='laser_event_series.csv', no_layer=10, layer_thickness=0.03, layer_duration=12.0,
                           impulse_duration=0.001, travel_distance=1.0, x_start=4.5, y=5, power_mag=450000,
                           x_start_recoater=-1, x_end_recoater=11, filename_recoater='recoater_event_series.csv',
                           recoat_time=11.0, filename_timepoints='timepoints.csv', offset=0):

    delimiter = "\t"
    delimiter = ","

    #############################################
    ############## LASER ########################
    #############################################
    rows = []

    time = recoat_time + offset  # initial time
    x = x_start
    z = layer_thickness

    for i in range(no_layer):
        # Odd row: laser on
        rows.append([round(time, 6), x, y, round(z, 6), power_mag])

        # Even row: laser off, x displaced, small time increment
        time += impulse_duration
        x += travel_distance
        rows.append([round(time, 6), x, y, round(z, 6), 0])

        # Prepare for next layer
        time += layer_duration - impulse_duration
        z += layer_thickness

        x=x_start

    # Save to CSV in current working directory
    out_path = os.path.join(os.getcwd(), filename)
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        # writer.writerow(['time', 'x', 'y', 'z', 'power'])
        writer.writerows(rows)

    tuple_data = tuple(tuple(sub) for sub in rows)
    print(tuple_data)

    print(f"CSV file saved to: {out_path}")


    #############################################
    ############## RECOATER #####################
    #############################################
    rows = []

    time = 0  # initial time
    z = layer_thickness

    for i in range(no_layer):
        # Odd row: laser on
        rows.append([round(time, 6), x_start_recoater, 0, round(z, 6), 1])

        # Even row: laser off, x displaced, small time increment
        time += recoat_time
        if i == 0:
            time += offset

        x += travel_distance
        rows.append([round(time, 6), x_end_recoater, 0, round(z, 6), 0])

        # Prepare for next layer
        time += layer_duration - recoat_time
        z += layer_thickness

        x=x_start

    # Save to CSV in current working directory
    out_path = os.path.join(os.getcwd(), filename_recoater)
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        # writer.writerow(['start_time', 'end_time', 'step_size'])
        writer.writerows(rows)

    tuple_data = tuple(tuple(sub) for sub in rows)
    print(tuple_data)

    print(f"CSV file saved to: {out_path}")

    #############################################
    ############## TIMEPOINTS ###################
    #############################################
    rows = []

    step_size_laser = 1e-3
    duration_laser = 0.01
    step_size_first_cooling = 1e-2
    duration_first_cooling = 2
    step_size_recoating = 1

    rows.append([round(0, 6), round(recoat_time+offset, 6), step_size_recoating])

    time = recoat_time + offset  # initial time

    for i in range(no_layer):
        # Odd row: laser on
        rows.append([round(time, 6), round(time+duration_laser, 6), step_size_laser])

        rows.append([round(time+duration_laser, 6), round(time+duration_first_cooling, 6), step_size_first_cooling])

        rows.append([round(time+duration_first_cooling, 6), round(time+layer_duration, 6), step_size_recoating])

        time += layer_duration

    # Save to CSV in current working directory
    out_path = os.path.join(os.getcwd(), filename_timepoints)
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        # writer.writerow(['time', 'x', 'y', 'z', 'power'])
        writer.writerows(rows)

    tuple_data = tuple(tuple(sub) for sub in rows)
    print(tuple_data)

    print(f"CSV file saved to: {out_path}")


# Example usage
# generate_layered_table(filename='laser_event_series2.csv', no_layer=10, layer_thickness=0.03, layer_duration=12,
#                        impulse_duration=0.001, travel_distance=1.0, x_start=11, y=5, power_mag=450000,
#                        x_start_recoater=-1, x_end_recoater=11, filename_recoater='recoater_event_series2.csv',
#                        recoat_time=11, filename_timepoints='timepoints2.csv', offset=0)

generate_layered_table(filename='laser_event_series_4-5.csv', no_layer=10, layer_thickness=0.03, layer_duration=4.55,
                       impulse_duration=0.001, travel_distance=1.0, x_start=4.5, y=5, power_mag=450000,
                       x_start_recoater=-1, x_end_recoater=11, filename_recoater='recoater_event_series_4-5.csv',
                       recoat_time=4, filename_timepoints='timepoints_4-5.csv', offset=0.5)
