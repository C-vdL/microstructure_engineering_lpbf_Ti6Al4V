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
mdb.models['Model-1'].parts['Part-substrate'].BaseSolidExtrude(depth=10.0,
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
mdb.models['Model-1'].parts['Part-lpbf'].BaseSolidExtrude(depth=10.0, sketch=
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
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#68000000 #8 ]', ), ), size=1.0)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#4a0000 #1 ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#10680 ]', ), ), size=0.3)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#101050 ]', ), ), size=0.2)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    ('[#285 ]', ), ), size=0.03)
# Save by cvander on 2025_06_24-17.23.02; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#9384c900 #6 ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#a ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    ('[#d7a ]', ), ), size=0.2)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#5 ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.setMeshControls(algorithm=ADVANCING_FRONT,
    regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#5 ]', ), ), technique=SWEEP)
mdb.models['Model-1'].rootAssembly.setSweepPath(edge=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges[0],
    region=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells[0],
    sense=FORWARD)
mdb.models['Model-1'].rootAssembly.setSweepPath(edge=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges[8],
    region=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells[2],
    sense=REVERSE)
mdb.models['Model-1'].rootAssembly.setMeshControls(elemShape=HEX_DOMINATED,
    regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#5 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#8 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FIXED,
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#5 ]', ), ), size=0.2)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.setSeedConstraints(constraint=FREE, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#a ]', ), ))
mdb.models['Model-1'].rootAssembly.setSeedConstraints(constraint=FIXED, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#8000 ]', ), ))
mdb.models['Model-1'].rootAssembly.setSeedConstraints(constraint=FINER, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#a ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#5 ]', ), ), seedConstraintOverride=ON)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#f ]', ), ), seedConstraintOverride=ON)
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#8 ]', ), ))
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.setSeedConstraints(constraint=FIXED, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#82808100 #4 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models['Model-1'].rootAssembly.deleteSeeds(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
# Save by cvander on 2025_06_24-17.42.24; build 2023 2022_09_28-20.11.55 183150