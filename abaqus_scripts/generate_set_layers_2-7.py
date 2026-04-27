from abaqus import *
from abaqusConstants import *

# Parameters
z_min = 0.0
layer_thickness = 10
num_layers = 10
model_name = 'Model-HT'
part_name = 'Part-lpbf'  # Change to your part name

# Get the part object
part = mdb.models[model_name].parts[part_name]

# Loop over each layer
for i in range(num_layers):
    print("hi")
    lower_z = z_min + i * layer_thickness
    upper_z = lower_z + layer_thickness
    layer_name = 'Set-layer' + str(i + 1)

    selected_elements = []

    print(part.elements)

    for elem in part.elements:
        print(elem)
        node_labels = elem.connectivity
        z_sum = 0.0
        count = 0
        for node_id in node_labels:
            # Abaqus node labels start at 1, indexing is 0-based
            z_coord = part.nodes[node_id].coordinates[2]
            z_sum += z_coord
            count += 1
        avg_z = z_sum / count
        print(avg_z)

        if lower_z <= avg_z < upper_z:
            selected_elements.append(elem.label)

    if selected_elements:
        part.Set(name=layer_name, elements=part.elements.sequenceFromLabels(selected_elements))
        print('Created', layer_name, 'with', len(selected_elements), 'elements.')
    else:
        print('No elements found for', layer_name)
