# -*- coding: mbcs -*-
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
from customKernel import *
from amModule import *
# Save by cvander on 2025_06_20-14.29.48; build 2023 2022_09_28-20.11.55 183150
# Save by cvander on 2025_06_20-14.29.50; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-10.0, 0.0),
    point2=(10.0, 20.0))
mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(0.0,
    27.5), point2=(0.0, -13.75))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(-47.5,
    0.0), point2=(-15.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].undo()
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].VerticalDimension(textPoint=(
    -19.9265823364258, 2.61312484741211), value=20.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0])
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-cube', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-cube'].BaseSolidExtrude(depth=20.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
del mdb.models['Model-1'].parts['Part-cube']
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-10.0, 0.0),
    point2=(5.0, 5.0))
mdb.models['Model-1'].sketches['__profile__'].VerticalDimension(textPoint=(
    -12.5169506072998, 0.343142867088318), value=6.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-10.0, 10.0),
    point2=(10.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].VerticalDimension(textPoint=(
    -19.8473510742188, 0.791858673095703), value=6.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1])
mdb.models['Model-1'].sketches['__profile__'].HorizontalDimension(textPoint=(
    9.70579528808594, -5.70135498046875), value=10.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[2])
mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(-33.75,
    0.0), point2=(-25.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(0.0,
    16.25), point2=(0.0, -3.75))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].DistanceDimension(entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7], textPoint=(
    -1.93995475769043, 15.0452451705933), value=5.0)
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-substrate', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-substrate'].BaseSolidExtrude(depth=2,
    sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-10.0, 5.0),
    point2=(10.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalDimension(textPoint=(
    -7.80424499511719, -10.1357421875), value=10.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[2])
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -14.6181106567383, -0.0791816711425781), value=0.3, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1])
mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(-45.0,
    0.0), point2=(-38.75, 0.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(0.0,
    16.25), point2=(0.0, 11.25))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].DistanceDimension(entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7], textPoint=(
    -2.41576480865479, 4.12926292419434), value=5.0)
mdb.models['Model-1'].sketches['__profile__'].DistanceDimension(entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6], textPoint=(
    -10.442554473877, 0.0106447339057922), value=6.3)
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-lpbf', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-lpbf'].BaseSolidExtrude(depth=2, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']





mdb.models['Model-1'].Material(name='Material-Inc718')
mdb.models['Model-1'].materials['Material-Inc718'].Density(table=((8.19e-06, ),
    ))
mdb.models['Model-1'].materials['Material-Inc718'].Conductivity(table=((0.0187,
    ), ))
mdb.models['Model-1'].materials['Material-Inc718'].SpecificHeat(table=((527.0,
    ), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-Inc718', name=
    'Section-lpbf', thickness=None)
mdb.models['Model-1'].sections.changeKey(fromName='Section-lpbf', toName=
    'Section-Inc718')
mdb.models['Model-1'].parts['Part-lpbf'].Set(cells=
    mdb.models['Model-1'].parts['Part-lpbf'].cells.getSequenceFromMask((
    '[#1 ]', ), ), name='Set-lpbf')
mdb.models['Model-1'].parts['Part-lpbf'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-lpbf'].sets['Set-lpbf'], sectionName=
    'Section-Inc718', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-substrate'].Set(cells=
    mdb.models['Model-1'].parts['Part-substrate'].cells.getSequenceFromMask((
    '[#1 ]', ), ), name='Set-substrate')
mdb.models['Model-1'].parts['Part-substrate'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-substrate'].sets['Set-substrate'],
    sectionName='Section-Inc718', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name=
    'Part-substrate-1', part=mdb.models['Model-1'].parts['Part-substrate'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name=
    'Part-substrate-2', part=mdb.models['Model-1'].parts['Part-substrate'])
mdb.models['Model-1'].HeatTransferStep(deltmx=500.0, initialInc=0.001, maxInc=
    1.0, maxNumInc=100000, minInc=1e-06, name='Step-heating', previous=
    'Initial', timePeriod=120.0)
del mdb.models['Model-1'].rootAssembly.features['Part-substrate-2']
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-lpbf-1',
    part=mdb.models['Model-1'].parts['Part-lpbf'])
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(10.0, 0.0,
    0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-lpbf-1', ))
mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(10.0, 0.0,
    0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-substrate-1', ))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-substrate-1',
    ), vector=(0.0, 10.0, 0.0))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-lpbf-1', ),
    vector=(0.0, 10.0, 0.0))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-lpbf-1', ),
    vector=(0.0, 0.0, 6.0))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-substrate-1',
    ), vector=(0.0, 0.0, -6.0))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-lpbf-1', ),
    vector=(0.0, 0.0, -12.0))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-lpbf-1', ),
    vector=(5.0, 0.0, 0.0))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-substrate-1',
    ), vector=(5.0, 0.0, 0.0))
mdb.models['Model-1'].parts['Part-lpbf'].Surface(name='Surf-lpbf_bottom',
    side1Faces=
    mdb.models['Model-1'].parts['Part-lpbf'].faces.getSequenceFromMask((
    '[#2 ]', ), ))
mdb.models['Model-1'].parts['Part-substrate'].Surface(name='Surf-substrate_top'
    , side1Faces=
    mdb.models['Model-1'].parts['Part-substrate'].faces.getSequenceFromMask((
    '[#8 ]', ), ))
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].Tie(adjust=ON, main=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].surfaces['Surf-lpbf_bottom']
    , name='Constraint-Tie_lpbf_substrate', positionToleranceMethod=COMPUTED,
    secondary=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].surfaces['Surf-substrate_top']
    , thickness=ON, tieRotations=ON)
mdb.models['Model-1'].parts['Part-substrate'].Surface(name=
    'Surf-substrate_bottom', side1Faces=
    mdb.models['Model-1'].parts['Part-substrate'].faces.getSequenceFromMask((
    '[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].parts['Part-substrate'].Set(faces=
    mdb.models['Model-1'].parts['Part-substrate'].faces.getSequenceFromMask((
    '[#2 ]', ), ), name='Set-substrate_bottom')
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].TemperatureBC(amplitude=UNSET, createStepName=
    'Step-heating', distributionType=UNIFORM, fieldName='', fixed=OFF,
    magnitude=50.0, name='BC-buildplateT', region=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].sets['Set-substrate_bottom'])
mdb.models['Model-1'].Field(createStepName='Step-heating',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, fieldVariableNum=1, magnitudes=(50.0, ), name=
    'Predefined Field-T0', region=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].sets['Set-substrate'])
mdb.models['Model-1'].rootAssembly.Set(cells=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), ), name='Set-all')
mdb.models['Model-1'].predefinedFields['Predefined Field-T0'].setValues(region=
    mdb.models['Model-1'].rootAssembly.sets['Set-all'])
mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'], ))
mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'], ))
mdb.models['Model-1'].parts['Part-substrate'].PartitionCellByPlanePointNormal(
    cells=
    mdb.models['Model-1'].parts['Part-substrate'].cells.getSequenceFromMask((
    '[#1 ]', ), ), normal=
    mdb.models['Model-1'].parts['Part-substrate'].edges[0], point=
    mdb.models['Model-1'].parts['Part-substrate'].InterestingPoint(
    mdb.models['Model-1'].parts['Part-substrate'].edges[0], MIDDLE))
mdb.models['Model-1'].parts['Part-substrate'].PartitionEdgeByParam(edges=
    mdb.models['Model-1'].parts['Part-substrate'].edges.getSequenceFromMask((
    '[#1000 ]', ), ), parameter=0.311199029286702)
del mdb.models['Model-1'].parts['Part-substrate'].features['Partition edge-1']
mdb.models['Model-1'].parts['Part-substrate'].PartitionCellByPlanePointNormal(
    cells=
    mdb.models['Model-1'].parts['Part-substrate'].cells.getSequenceFromMask((
    '[#1 ]', ), ), normal=
    mdb.models['Model-1'].parts['Part-substrate'].edges[12], point=
    mdb.models['Model-1'].parts['Part-substrate'].InterestingPoint(
    mdb.models['Model-1'].parts['Part-substrate'].edges[12], MIDDLE))
mdb.models['Model-1'].parts['Part-substrate'].PartitionCellByPlanePointNormal(
    cells=
    mdb.models['Model-1'].parts['Part-substrate'].cells.getSequenceFromMask((
    '[#2 ]', ), ), normal=
    mdb.models['Model-1'].parts['Part-substrate'].edges[6], point=
    mdb.models['Model-1'].parts['Part-substrate'].InterestingPoint(
    mdb.models['Model-1'].parts['Part-substrate'].edges[6], MIDDLE))
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1,
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'],
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1']), size=1.0)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#4a0000 #1 ]', ), ), minSizeFactor=0.1, size=0.75)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#4a0000 #1 ]', ), ), minSizeFactor=0.1, size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#10680 ]', ), ), minSizeFactor=0.1, size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#101050 ]', ), ), minSizeFactor=0.1, size=0.3)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    ('[#285 ]', ), ), minSizeFactor=0.1, size=0.03)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#101050 ]', ), ), minSizeFactor=0.1, size=0.1)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    mask=('[#4202020 ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    mask=('[#d7a ]', ), ), minSizeFactor=0.1, size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#f ]', ), ), minSizeFactor=0.1, size=0.75)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'],
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1']))
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'NT', ))
mdb.Model(name='Model-ST', objectToCopy=mdb.models['Model-1'])
mdb.models.changeKey(fromName='Model-1', toName='Model-HT')
del mdb.models['Model-ST'].steps['Step-heating']
mdb.models['Model-ST'].StaticStep(initialInc=120.0, maxInc=120.0, minInc=0.0012
    , name='Step-Activation', previous='Initial', timePeriod=120.0)
mdb.models['Model-HT'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=DC3D8, elemLibrary=STANDARD), ElemType(elemCode=DC3D6,
    elemLibrary=STANDARD), ElemType(elemCode=DC3D4, elemLibrary=STANDARD)),
    regions=(
    mdb.models['Model-HT'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    mask=('[#f ]', ), )+\
    mdb.models['Model-HT'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), ), ))
mdb.models['Model-ST'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF,
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD),
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-ST'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    mask=('[#f ]', ), )+\
    mdb.models['Model-ST'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), ), ))
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF,
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF,
    memory=90, memoryUnits=PERCENTAGE, model='Model-HT', modelPrint=OFF,
    multiprocessingMode=DEFAULT, name='Job-HT_v01', nodalOutputPrecision=SINGLE
    , numCpus=4, numDomains=4, numGPUs=0, numThreadsPerMpiProcess=1, queue=None
    , resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='',
    waitHours=0, waitMinutes=0)
mdb.models['Model-HT'].setValues(absoluteZero=-273.15, stefanBoltzmann=
    5.67e-14)
mdb.models['Model-ST'].EventSeriesType(createStepName='Initial', fieldNums=1,
    fields=('On/Off State', ), name='ABQ_AM_MaterialDeposition')
mdb.models['Model-HT'].EventSeriesType(createStepName='Initial', fieldNums=1,
    fields=('On/Off State', ), name='ABQ_AM_MaterialDeposition')
mdb.models['Model-HT'].EventSeriesType(createStepName='Initial', fieldNums=1,
    fields=('Power Magnitude (unit of JT^-1)', ), name='ABQ_AM_PowerMagnitude')
mdb.models['Model-HT'].EventSeriesType(createStepName='Initial', fieldNums=1,
    fields=('Rule ID', ), name='ABQ_AM_HeatSourceTrajectory_RuleID')
mdb.models['Model-HT'].EventSeriesData(createStepName='Initial', data=((11.0,
    4.5, 5.0, 0.03, 45000.0), (11.01, 5.5, 5.0, 0.03, 0.0), (23.0, 4.5, 5.0,
    0.06, 45000.0), (23.01, 5.5, 5.0, 0.06, 0.0), (35.0, 4.5, 5.0, 0.09,
    45000.0), (35.01, 5.5, 5.0, 0.09, 0.0), (47.0, 4.5, 5.0, 0.12, 45000.0), (
    47.01, 5.5, 5.0, 0.12, 0.0), (59.0, 4.5, 5.0, 0.15, 45000.0), (59.01, 5.5,
    5.0, 0.15, 0.0), (71.0, 4.5, 5.0, 0.18, 45000.0), (71.01, 5.5, 5.0, 0.18,
    0.0), (83.0, 4.5, 5.0, 0.21, 45000.0), (83.01, 5.5, 5.0, 0.21, 0.0), (95.0,
    4.5, 5.0, 0.24, 45000.0), (95.01, 5.5, 5.0, 0.24, 0.0), (107.0, 4.5, 5.0,
    0.27, 45000.0), (107.01, 5.5, 5.0, 0.27, 0.0), (119.0, 4.5, 5.0, 0.3,
    45000.0), (119.01, 5.5, 5.0, 0.3, 0.0)), eventSeriesType=
    'ABQ_AM_PowerMagnitude', name='Event series-laser_layer', timeSpan=
    STEP_TIME)
mdb.models['Model-ST'].EventSeriesData(createStepName='Initial', data=((0.0,
    -1.0, 0.0, 0.03, 1.0), (11.0, 11.0, 0.0, 0.03, 0.0), (12.0, -1.0, 0.0,
    0.06, 1.0), (23.0, 11.0, 0.0, 0.06, 0.0), (24.0, -1.0, 0.0, 0.09, 1.0), (
    35.0, 11.0, 0.0, 0.09, 0.0), (36.0, -1.0, 0.0, 0.12, 1.0), (47.0, 11.0,
    0.0, 0.12, 0.0), (48.0, -1.0, 0.0, 0.15, 1.0), (59.0, 11.0, 0.0, 0.15,
    0.0), (60.0, -1.0, 0.0, 0.18, 1.0), (71.0, 11.0, 0.0, 0.18, 0.0), (72.0,
    -1.0, 0.0, 0.21, 1.0), (83.0, 11.0, 0.0, 0.21, 0.0), (84.0, -1.0, 0.0,
    0.24, 1.0), (95.0, 11.0, 0.0, 0.24, 0.0), (96.0, -1.0, 0.0, 0.27, 1.0), (
    107.0, 11.0, 0.0, 0.27, 0.0), (108.0, -1.0, 0.0, 0.3, 1.0), (119.0, 11.0,
    0.0, 0.3, 0.0)), eventSeriesType='ABQ_AM_MaterialDeposition', name=
    'Event series-roller', timeSpan=STEP_TIME)
mdb.models['Model-HT'].EventSeriesData(createStepName='Initial', data=((0.0,
    -1.0, 0.0, 0.03, 1.0), (11.0, 11.0, 0.0, 0.03, 0.0), (12.0, -1.0, 0.0,
    0.06, 1.0), (23.0, 11.0, 0.0, 0.06, 0.0), (24.0, -1.0, 0.0, 0.09, 1.0), (
    35.0, 11.0, 0.0, 0.09, 0.0), (36.0, -1.0, 0.0, 0.12, 1.0), (47.0, 11.0,
    0.0, 0.12, 0.0), (48.0, -1.0, 0.0, 0.15, 1.0), (59.0, 11.0, 0.0, 0.15,
    0.0), (60.0, -1.0, 0.0, 0.18, 1.0), (71.0, 11.0, 0.0, 0.18, 0.0), (72.0,
    -1.0, 0.0, 0.21, 1.0), (83.0, 11.0, 0.0, 0.21, 0.0), (84.0, -1.0, 0.0,
    0.24, 1.0), (95.0, 11.0, 0.0, 0.24, 0.0), (96.0, -1.0, 0.0, 0.27, 1.0), (
    107.0, 11.0, 0.0, 0.27, 0.0), (108.0, -1.0, 0.0, 0.3, 1.0), (119.0, 11.0,
    0.0, 0.3, 0.0)), eventSeriesType='ABQ_AM_MaterialDeposition', name=
    'Event series-roller', timeSpan=STEP_TIME)
mdb.models['Model-ST'].TableCollection(name='ABQ_AM.Material Input')
mdb.models['Model-HT'].TableCollection(name='ABQ_AM.Material Input')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition')
# Save by cvander on 2025_06_20-14.30.26; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-ST'].TableCollection(name='ABQ_AM.Material Input')
mdb.models['Model-HT'].TableCollection(name='ABQ_AM.Material Input')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].Column(
    description='Event series', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].Column(
    description='Event series', type=STRING)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].Column(
    allowedValues=('Roller', 'Bead'), description='Deposition process', type=
    STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].Column(
    allowedValues=('Roller', 'Bead'), description='Deposition process', type=
    STRING)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].DataTable(
    label='ABQ_AM_MaterialDeposition')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].DataTable(
    label='ABQ_AM_MaterialDeposition')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].dataTables[0].Column(
    data=('Event series-roller', ), id=0)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].dataTables[0].Column(
    data=('Event series-roller', ), id=0)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].dataTables[0].Column(
    data=('Roller', ), id=1)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition'].dataTables[0].Column(
    data=('Roller', ), id=1)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition_Advanced')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition_Advanced')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    allowedValues=('Full', 'Partial'), default='Partial', description=
    'Activation type', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    allowedValues=('Full', 'Partial'), default='Partial', description=
    'Activation type', type=STRING)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0.0, description=
    'Min volume fraction threshold for partial activation', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0.0, description=
    'Min volume fraction threshold for partial activation', type=FLOAT)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0.0, description=
    'Max volume fraction threshold for partial activation', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0.0, description=
    'Max volume fraction threshold for partial activation', type=FLOAT)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0.0, description=
    'Max volume fraction threshold for full activation', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0.0, description=
    'Max volume fraction threshold for full activation', type=FLOAT)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default='Yes', description='Orientation for bead type deposition', type=
    STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default='Yes', description='Orientation for bead type deposition', type=
    STRING)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0, description='Element subdivision order', type=INTEGER)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].Column(
    default=0, description='Element subdivision order', type=INTEGER)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].DataTable(
    label='ABQ_AM_MaterialDeposition_Advanced')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].DataTable(
    label='ABQ_AM_MaterialDeposition_Advanced')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=('Full', ), id=0)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=('Full', ), id=0)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0.0, ), id=1)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0.0, ), id=1)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0.0, ), id=2)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0.0, ), id=2)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0.9, ), id=3)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0.9, ), id=3)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=('Yes', ), id=4)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=('Yes', ), id=4)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0, ), id=5)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Advanced'].dataTables[0].Column(
    data=(0, ), id=5)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition_Bead')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition_Bead')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    allowedValues=('X', 'Y', 'Z'), description='Stack direction', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    allowedValues=('X', 'Y', 'Z'), description='Stack direction', type=STRING)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    default=0.0, description='Bead height', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    default=0.0, description='Bead height', type=FLOAT)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    default=0.0, description='Bead width', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    default=0.0, description='Bead width', type=FLOAT)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    default=0.0, description='Activation offset', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    default=0.0, description='Activation offset', type=FLOAT)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    allowedValues=('Below', 'Above'), description='Deposition position', type=
    STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].Column(
    allowedValues=('Below', 'Above'), description='Deposition position', type=
    STRING)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].DataTable(
    label='ABQ_AM_MaterialDeposition_Bead')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].DataTable(
    label='ABQ_AM_MaterialDeposition_Bead')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=('X', ), id=0)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=('X', ), id=0)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=(0.0, ), id=1)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=(0.0, ), id=1)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=(0.0, ), id=2)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=(0.0, ), id=2)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=(0.0, ), id=3)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=(0.0, ), id=3)
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=('Below', ), id=4)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].parameterTables['ABQ_AM_MaterialDeposition_Bead'].dataTables[0].Column(
    data=('Below', ), id=4)
mdb.models['Model-HT'].rootAssembly.ElementProgressiveActivation(deformation=0,
    elset=mdb.models['Model-HT'].rootAssembly.allSets['Part-lpbf-1.Set-lpbf'],
    freeSurfaceType=NONE, name='ElementProgressiveActivation1')
mdb.models['Model-ST'].rootAssembly.ElementProgressiveActivation(deformation=0,
    elset=mdb.models['Model-ST'].rootAssembly.allSets['Part-lpbf-1.Set-lpbf'],
    freeSurfaceType=NONE, name='ElementProgressiveActivation1')
mdb.models['Model-HT'].steps['Step-heating'].ActivateElement(activation=
    'ElementProgressiveActivation1', expansionTimeConst=2.0, tableCollection=
    'ABQ_AM.Material Input')
mdb.models['Model-ST'].steps['Step-Activation'].ActivateElement(activation=
    'ElementProgressiveActivation1', expansionTimeConst=2.0, tableCollection=
    'ABQ_AM.Material Input')
# Save by cvander on 2025_06_20-14.35.53; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-HT'].TableCollection(name='ABQ_AM.Moving Heat Source')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].ParameterTable(
    name='ABQ_AM_MovingHeatSource')
mdb.models['Model-HT'].TableCollection(name='ABQ_AM.Moving Heat Source')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].ParameterTable(
    name='ABQ_AM_MovingHeatSource')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource'].Column(
    description='Event series', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource'].Column(
    allowedValues=('Concentrated', 'Uniform', 'Goldak'), description=
    'Energy distribution', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource'].DataTable(
    label='ABQ_AM_MovingHeatSource')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource'].dataTables[0].Column(
    data=('Event series-laser_layer', ), id=0)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource'].dataTables[0].Column(
    data=('Uniform', ), id=1)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].ParameterTable(
    name='ABQ_AM_MovingHeatSource_Advanced')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].Column(
    allowedValues=('True', 'False'), default='False', description=
    'Enhance energy conservation', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].Column(
    allowedValues=('True', 'False'), default='False', description=
    'Control increment size', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].Column(
    allowedValues=('Absolute', 'Relative'), default='Relative', description=
    'Offset type', type=STRING)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].Column(
    default=0.0, description='Vector x', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].Column(
    default=0.0, description='Vector y', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].Column(
    default=-1.0, description='Vector z', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].Column(
    default=1.0, description='Field factor', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].DataTable(
    label='ABQ_AM_MovingHeatSource_Advanced')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].dataTables[0].Column(
    data=('False', ), id=0)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].dataTables[0].Column(
    data=('False', ), id=1)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].dataTables[0].Column(
    data=('Relative', ), id=2)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].dataTables[0].Column(
    data=(0.0, ), id=3)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].dataTables[0].Column(
    data=(0.0, ), id=4)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].dataTables[0].Column(
    data=(-1.0, ), id=5)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Advanced'].dataTables[0].Column(
    data=(1.0, ), id=6)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].ParameterTable(
    name='ABQ_AM_MovingHeatSource_Uniform')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0, description='Subdiv x', type=INTEGER)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0, description='Subdiv y', type=INTEGER)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0, description='Subdiv z', type=INTEGER)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0.0, description='Offset x', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0.0, description='Offset y', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0.0, description='Offset z', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0.0, description='Box length x', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0.0, description='Box length y', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].Column(
    default=0.0, description='Box length z', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].DataTable(
    label='ABQ_AM_MovingHeatSource_Uniform')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(0, ), id=0)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(0, ), id=1)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(0, ), id=2)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(0.0, ), id=3)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(0.0, ), id=4)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(0.0, ), id=5)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(15.0, ), id=6)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(15.0, ), id=7)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Uniform'].dataTables[0].Column(
    data=(0.03, ), id=8)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].ParameterTable(
    name='ABQ_AM_MovingHeatSource_Goldak')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0, description='Subdiv x', type=INTEGER)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0, description='Subdiv y', type=INTEGER)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0, description='Subdiv z', type=INTEGER)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0.0, description='a', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0.0, description='b', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0.0, description='cf', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0.0, description='cr', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0.0, description='ff', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0.0, description='fr', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].Column(
    default=0.0, description='Box size factor', type=FLOAT)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].DataTable(
    label='ABQ_AM_MovingHeatSource_Goldak')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0, ), id=0)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0, ), id=1)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0, ), id=2)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0.0, ), id=3)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0.0, ), id=4)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0.0, ), id=5)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0.0, ), id=6)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0.0, ), id=7)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0.0, ), id=8)
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].parameterTables['ABQ_AM_MovingHeatSource_Goldak'].dataTables[0].Column(
    data=(0.0, ), id=9)
mdb.models['Model-HT'].BodyHeatFlux(createStepName='Step-heating',
    distributionType=USER_DEFINED, name='Load-1', region=
    mdb.models['Model-HT'].rootAssembly.allSets['Set-all'],
    tableCollectionName='ABQ_AM.Moving Heat Source')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].PropertyTable(
    name='ABQ_AM_AbsorptionCoeff', properties=('Absorption Coefficient', ))
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].propertyTables['ABQ_AM_AbsorptionCoeff'].PropertyTableData(
    data=((0.5, ), ), label='ABQ_AM_AbsorptionCoeff')
# # Save by cvander on 2025_06_20-14.39.37; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-HT'].TimePoint(name='TimePoints-3phases', points=((0.0, 11.0,
    1.0), (11.0, 11.01, 0.001), (11.01, 13.0, 0.1), (13.0, 23.0, 1.0), (23.0,
    23.01, 0.001), (23.01, 25.0, 0.1), (25.0, 35.0, 1.0), (35.0, 35.01, 0.001),
    (35.01, 37.0, 0.1), (37.0, 47.0, 1.0), (47.0, 47.01, 0.001), (47.01, 49.0,
    0.1), (49.0, 59.0, 1.0), (59.0, 59.01, 0.001), (59.01, 61.0, 0.1), (61.0,
    71.0, 1.0), (71.0, 71.01, 0.001), (71.01, 73.0, 0.1), (73.0, 83.0, 1.0), (
    83.0, 83.01, 0.001), (83.01, 85.0, 0.1), (85.0, 95.0, 1.0), (95.0, 95.01,
    0.001), (95.01, 97.0, 0.1), (97.0, 107.0, 1.0), (107.0, 107.01, 0.001), (
    107.01, 109.0, 0.1), (109.0, 119.0, 1.0), (119.0, 119.01, 0.001), (119.01,
    120.0, 0.1)))
mdb.models['Model-HT'].fieldOutputRequests['F-Output-1'].setValues(timePoint=
    'TimePoints-3phases')
mdb.models['Model-HT'].RadiationToAmbient(ambientTemperature=25.0,
    ambientTemperatureAmp='', createStepName='Step-heating', distributionType=
    UNIFORM, dynamicSurfaceActivation=True, emissivity=0.5, name='Int-Rad',
    radiationType=AMBIENT, region=
    mdb.models['Model-HT'].rootAssembly.allSets['Set-all'])
mdb.models['Model-HT'].FilmCondition(createStepName='Step-heating', definition=
    EMBEDDED_COEFF, dynamicSurfaceActivation=True, filmCoeff=1.5e-05,
    filmCoeffAmplitude='', name='Int-Conv', region=
    mdb.models['Model-HT'].rootAssembly.allSets['Set-all'], sinkAmplitude='',
    sinkDistributionType=UNIFORM, sinkTemperature=25.0)
mdb.jobs.changeKey(fromName='Job-HT_v01', toName='Job-HT_Cmodel_v01')
mdb.models['Model-HT'].rootAssembly.Set(cells=
    mdb.models['Model-HT'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    mask=('[#f ]', ), )+\
    mdb.models['Model-HT'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), ), name='Set-all')
# Save by cvander on 2025_06_20-14.41.01; build 2023 2022_09_28-20.11.55 183150
