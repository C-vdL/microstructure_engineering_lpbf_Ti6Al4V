from abaqus import *
from abaqusConstants import *
import regionToolset
import mesh

# Parameters
z_min = 0.0
layer_thickness = 0.09
num_layers = 10
model_name = 'Model-HT'
part_name = 'Part-lpbf'  # Change to your part name

# Get the part
part = mdb.models[model_name].parts[part_name]

# Loop over each layer
for i in range(num_layers):
    lower_z = z_min + i * layer_thickness
    upper_z = lower_z + layer_thickness
    # layer_name = f'Set-layer{i + 1}'
    layer_name = "Set-layer%i" %(i+1)
    #'%s_%s.csv' % (box['name'], trial_tag)

    selected_elements = []

    for elem in part.elements:
        # Get element nodes
        node_indices = elem.connectivity
        z_coords = [part.nodes[node_id].coordinates[2] for node_id in node_indices]
        avg_z = sum(z_coords) / len(z_coords)

        if lower_z <= avg_z < upper_z:
            selected_elements.append(elem.label)

    if selected_elements:
        region = part.Set(name=layer_name, elements=part.elements.sequenceFromLabels(selected_elements))
        # print(f'Created {layer_name} with {len(selected_elements)} elements')
    # else:
        # print(f'No elements found in {layer_name}')
