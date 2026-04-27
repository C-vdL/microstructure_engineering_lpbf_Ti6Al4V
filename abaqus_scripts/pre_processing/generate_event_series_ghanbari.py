import csv
import os


def generate_amplitudes(layer_start_times, impulse_duration, layer_duration, first_laser):
    # impulse_duration = 0.001
    VED_m3 = 200 / (0.0001 * 1 * 0.00003)  # W/m^3
    W_m3 = VED_m3 / impulse_duration
    VED_mm3 = 200 / (0.1 * 1000 * 0.03)  # W/mm^3
    W_mm3 = VED_mm3 / impulse_duration
    abs_coef = 0.5

    magnitude = int(W_mm3 * abs_coef)

    num_layers = 10
    # layer_duration = 4.55
    # first_laser = 4.5

    layer_time = first_laser

    # layer_start_times = [4.67908, 7.97704, 12.53728, 17.27160, 22.00799, 26.82251, 31.50203, 36.32279, 40.88242,
    #                      45.55777]

    string = ""

    for i in range(num_layers):
        layer_time = layer_start_times[i]

        amp_data = f"{layer_time}, 0.0, {layer_time + 0.0001}, 1.0, {layer_time + impulse_duration}, 1.0, {layer_time + impulse_duration + 0.0001}, 0.0"


        string += f"*Amplitude, name=Amp-layer{i+1}, time=TOTAL TIME\n{amp_data}\n"
        # 4.67908,              0.,         4.67918,              1.,         4.68008,              1.,         4.68018,              0."


        layer_time += layer_duration

    return string


def generate_layered_table(filename='laser_event_series.csv', no_layer=10, layer_thickness=0.03, layer_duration=12.0,
                           impulse_duration=0.001, travel_distance=1.0, x_start=4.5, y=5, power_mag=450000,
                           x_start_recoater=-1, x_end_recoater=11, filename_recoater='recoater_event_series.csv',
                           recoat_time=11.0, filename_timepoints='timepoints.csv', offset=0):

    delimiter = "\t"
    delimiter = ","

    layer_start_times = [4.67908, 7.97704, 12.53728, 17.27160, 22.00799, 26.82251, 31.50203, 36.32279, 40.88242, 45.55777]

    #############################################
    ############## LASER ########################
    #############################################
    rows = generate_laser_series(impulse_duration, layer_duration, layer_start_times, layer_thickness, no_layer,
                                    offset, power_mag, recoat_time, travel_distance, x_start, y)

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
    rows = generate_recoater_series(layer_start_times, layer_thickness, no_layer, offset, recoat_time, x_end_recoater,
                                    x_start_recoater)

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
    rows = generate_timepoints(layer_duration, layer_start_times, no_layer, offset, recoat_time)

    # Save to CSV in current working directory
    out_path = os.path.join(os.getcwd(), filename_timepoints)
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        # writer.writerow(['time', 'x', 'y', 'z', 'power'])
        writer.writerows(rows)

    tuple_data = tuple(tuple(sub) for sub in rows)
    print(tuple_data)

    print(f"CSV file saved to: {out_path}")


def generate_laser_series(impulse_duration, layer_duration, layer_start_times, layer_thickness, no_layer, offset,
                          power_mag, recoat_time, travel_distance, x_start, y):
    rows = []
    time = recoat_time + offset  # initial time
    x = x_start
    z = layer_thickness
    for i in range(no_layer):
        time = layer_start_times[i]
        # Odd row: laser on
        rows.append([round(time, 6), x, y, round(z, 6), power_mag])

        # Even row: laser off, x displaced, small time increment
        time += impulse_duration
        x += travel_distance
        rows.append([round(time, 6), x, y, round(z, 6), 0])

        # Prepare for next layer
        time += layer_duration - impulse_duration
        z += layer_thickness

        x = x_start
    return rows


def generate_recoater_series(layer_start_times, layer_thickness, no_layer, offset, recoat_time, x_end_recoater,
                             x_start_recoater):
    x=x_start_recoater

    rows = []
    time = 0  # initial time
    z = layer_thickness
    for i in range(no_layer):

        time = layer_start_times[i] - recoat_time

        # Odd row: laser on
        rows.append([round(time, 6), x_start_recoater, 0, round(z, 6), 1])

        # Even row: laser off, x displaced, small time increment
        time += recoat_time
        if i == 0:
            time += offset

        rows.append([round(layer_start_times[i], 6), x_end_recoater, 0, round(z, 6), 0])

        # Prepare for next layer
        # time += layer_duration - recoat_time

        z += layer_thickness

    string = '\n'.join(', '.join(str(x) for x in row) for row in rows)
    string += "\n"
    return string


def generate_timepoints(layer_duration, layer_start_times, no_layer, offset, recoat_time):
    rows = []
    step_size_laser = 1e-3
    duration_laser = 0.015
    step_size_first_cooling = 1e-2
    duration_first_cooling = 2
    step_size_recoating = 1
    rows.append([round(0, 6), round(layer_start_times[0], 6), step_size_recoating])
    time = recoat_time + offset  # initial time
    for i in range(no_layer):
        time = layer_start_times[i]
        if i < len(range(no_layer)) - 1:
            time_layer_end = layer_start_times[i + 1]
        else:
            time_layer_end = layer_start_times[i] + layer_duration

        # Odd row: laser on
        rows.append([round(time, 6), round(time + duration_laser, 6), step_size_laser])

        rows.append([round(time + duration_laser, 6), round(time + duration_first_cooling, 6), step_size_first_cooling])

        rows.append([round(time + duration_first_cooling, 6), round(time_layer_end, 6), step_size_recoating])

        time += layer_duration

    string = '\n'.join(', '.join(str(x) for x in row) for row in rows)
    return string


if __name__ == '__main__':

    # Example usage
    # generate_layered_table(filename='laser_event_series2.csv', no_layer=10, layer_thickness=0.03, layer_duration=12,
    #                        impulse_duration=0.001, travel_distance=1.0, x_start=11, y=5, power_mag=450000,
    #                        x_start_recoater=-1, x_end_recoater=11, filename_recoater='recoater_event_series2.csv',
    #                        recoat_time=11, filename_timepoints='timepoints2.csv', offset=0)

    generate_layered_table(filename='laser_event_series_4-5_gh.csv', no_layer=10, layer_thickness=0.03, layer_duration=4.55,
                           impulse_duration=0.001, travel_distance=1.0, x_start=4.5, y=5, power_mag=450000,
                           x_start_recoater=-1, x_end_recoater=11, filename_recoater='recoater_event_series_4-5_gh.csv',
                           recoat_time=3, filename_timepoints='timepoints_4-5_gh.csv', offset=0.5)
