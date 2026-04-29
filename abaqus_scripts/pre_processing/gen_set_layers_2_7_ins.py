from abaqus import *
from abaqusConstants import *

# Parameters
z_min = 0.0
layer_thickness = 0.03
num_layers = 10
model_name = 'Model-HT'
instance_name = 'Part-lpbf-1'  # <-- Change to your instance name

# Get the instance from the root assembly
assembly = mdb.models[model_name].rootAssembly
instance = assembly.instances[instance_name]

# Loop over each layer
for i in range(num_layers):
    lower_z = z_min + i * layer_thickness
    upper_z = lower_z + layer_thickness
    layer_name = 'Set-layer' + str(i + 1)

    selected_elements = []

    for elem in instance.elements:
        node_labels = elem.connectivity
        z_sum = 0.0
        count = 0
        for node_id in node_labels:
            z_coord = instance.nodes[node_id].coordinates[2]
            z_sum += z_coord
            count += 1
        avg_z = z_sum / count

        if lower_z <= avg_z < upper_z:
            selected_elements.append(elem.label)

    if selected_elements:
        region = assembly.Set(name=layer_name, elements=instance.elements.sequenceFromLabels(selected_elements))
        print('Created', layer_name, 'with', len(selected_elements), 'elements.')
    else:
        print('No elements found for', layer_name)
