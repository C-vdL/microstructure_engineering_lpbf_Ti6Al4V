from abaqus import *
from abaqusConstants import *

impulse_duration = 0.001
VED_m3 = 200 / (0.0001*1*0.00003)  # W/m^3
W_m3 = VED_m3 / impulse_duration
VED_mm3 = 200 / (0.1*1000*0.03)  # W/mm^3
W_mm3 = VED_mm3 / impulse_duration
abs_coef = 0.5

magnitude = int(W_mm3 * abs_coef)

num_layers = 10
layer_duration = 4.55
first_laser = 4.5

layer_time = first_laser

layer_start_times = [4.67908, 7.97704, 12.53728, 17.27160, 22.00799, 26.82251, 31.50203, 36.32279, 40.88242, 45.55777]

for i in range(num_layers):
    layer_time = layer_start_times[i]

    mdb.models['Model-HT'].TabularAmplitude(data=((layer_time, 0.0), (layer_time + 0.0001, 1.0), (
        layer_time + 0.001, 1.0), (layer_time + 0.0011, 0.0)), name='Amp-layer' + str(i + 1), smooth=SOLVER_DEFAULT,
        timeSpan=TOTAL)
    mdb.models['Model-HT'].BodyHeatFlux(amplitude='Amp-layer' + str(i + 1), createStepName=
        'Step-heating', magnitude=magnitude, name='Load-layer' + str(i + 1), region=
        mdb.models['Model-HT'].rootAssembly.sets['Set-layer' + str(i + 1)])

    layer_time += layer_duration