mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE,
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#fb840000 #e ]', ), ), size=0.75)
# Save by cvander on 2025_06_20-17.18.51; build 2023 2022_09_28-20.11.55 183150
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#3cec900 #1 ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#1cf8f ]', ), ), size=0.3)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    mask=('[#430307f ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    mask=('[#72 ]', ), ), size=0.1)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    mask=('[#4202020 ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    mask=('[#fff ]', ), ), size=0.03)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#a ]', ), ), size=0.3)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#a ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#8100 ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FREE, 
    deviationFactor=0.5, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    mask=('[#4002000 ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    mask=('[#c50 ]', ), ), size=0.25)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'], 
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1']))
# Save by cvander on 2025_06_20-17.26.57; build 2023 2022_09_28-20.11.55 183150
