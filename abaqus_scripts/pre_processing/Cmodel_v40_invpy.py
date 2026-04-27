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
mdb.openStep(
    'C:/Users/cvander/Documents/Git_repos/3D_FEM_thermal_lpbf/inverted_pyramid_steeper.step'
    , scaleFromFile=OFF)
mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='inverted_pyramid', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['inverted_pyramid'].DatumPlaneByPrincipalPlane(
    offset=0.3, principalPlane=XYPLANE)
del mdb.models['Model-1'].parts['inverted_pyramid'].features['Datum plane-1']
mdb.models['Model-1'].parts['inverted_pyramid'].DatumPlaneByPrincipalPlane(
    offset=-0.3, principalPlane=XYPLANE)
mdb.models['Model-1'].parts['inverted_pyramid'].PartitionCellByDatumPlane(
    cells=
    mdb.models['Model-1'].parts['inverted_pyramid'].cells.getSequenceFromMask((
    '[#1 ]', ), ), datumPlane=
    mdb.models['Model-1'].parts['inverted_pyramid'].datums[3])
from customKernel import *
from amModule import *
# Save by cvander on 2025_07_11-16.13.37; build 2023 2022_09_28-20.11.55 183150
# Save by cvander on 2025_07_11-16.14.29; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].parts['inverted_pyramid'].PartitionCellByPlaneThreePoints(
    cells=
    mdb.models['Model-1'].parts['inverted_pyramid'].cells.getSequenceFromMask((
    '[#2 ]', ), ), point1=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[12], MIDDLE), point2=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[7], MIDDLE), point3=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[18], MIDDLE))
mdb.models['Model-1'].parts['inverted_pyramid'].PartitionCellByPlaneThreePoints(
    cells=
    mdb.models['Model-1'].parts['inverted_pyramid'].cells.getSequenceFromMask((
    '[#4 ]', ), ), point1=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[4], MIDDLE), point2=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[10], MIDDLE), point3=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[6], MIDDLE))
mdb.models['Model-1'].parts['inverted_pyramid'].PartitionCellByPlaneThreePoints(
    cells=
    mdb.models['Model-1'].parts['inverted_pyramid'].cells.getSequenceFromMask((
    '[#1 ]', ), ), point1=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[16], MIDDLE), point2=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[6], MIDDLE), point3=
    mdb.models['Model-1'].parts['inverted_pyramid'].InterestingPoint(
    mdb.models['Model-1'].parts['inverted_pyramid'].edges[10], MIDDLE))
# Save by cvander on 2025_07_11-16.16.07; build 2023 2022_09_28-20.11.55 183150
# Save by cvander on 2025_07_11-16.19.58; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].parts['inverted_pyramid'].Set(cells=
    mdb.models['Model-1'].parts['inverted_pyramid'].cells.getSequenceFromMask((
    '[#8 ]', ), ), name='Set-lpbf')
mdb.models['Model-1'].parts['inverted_pyramid'].Set(cells=
    mdb.models['Model-1'].parts['inverted_pyramid'].cells.getSequenceFromMask((
    '[#17 ]', ), ), name='Set-substrate')
mdb.models['Model-1'].parts['inverted_pyramid'].Set(faces=
    mdb.models['Model-1'].parts['inverted_pyramid'].faces.getSequenceFromMask((
    '[#2000000 ]', ), ), name='Set-substrate_bottom')
mdb.models['Model-1'].parts['inverted_pyramid'].Surface(name=
    'Surf-substrate_bottom', side1Faces=
    mdb.models['Model-1'].parts['inverted_pyramid'].faces.getSequenceFromMask((
    '[#2000000 ]', ), ))
mdb.models['Model-1'].Part(name='inverted_pyramid-substrate', objectToCopy=
    mdb.models['Model-1'].parts['inverted_pyramid'])
mdb.models['Model-1'].parts.changeKey(fromName='inverted_pyramid-substrate', 
    toName='Part-substrate')
mdb.models['Model-1'].parts.changeKey(fromName='inverted_pyramid', toName=
    'Part-lpbf')
mdb.models['Model-1'].parts['Part-lpbf'].RemoveFaces(deleteCells=False, 
    faceList=
    mdb.models['Model-1'].parts['Part-lpbf'].faces.getSequenceFromMask(mask=(
    '[#82088 ]', ), ))
mdb.models['Model-1'].parts['Part-substrate'].RemoveFaces(deleteCells=False, 
    faceList=
    mdb.models['Model-1'].parts['Part-substrate'].faces.getSequenceFromMask(
    mask=('[#350000 ]', ), ))
mdb.models['Model-1'].parts['Part-substrate'].RemoveFaces(deleteCells=False, 
    faceList=
    mdb.models['Model-1'].parts['Part-substrate'].faces.getSequenceFromMask(
    mask=('[#200000 ]', ), ))
mdb.models['Model-1'].parts['Part-lpbf'].RemoveFaces(deleteCells=False, 
    faceList=
    mdb.models['Model-1'].parts['Part-lpbf'].faces.getSequenceFromMask(mask=(
    '[#2c4fff ]', ), ))
# Save by cvander on 2025_07_11-16.28.12; build 2023 2022_09_28-20.11.55 183150
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
del mdb.models['Model-1'].parts['Part-lpbf'].sets['Set-substrate_bottom']
del mdb.models['Model-1'].parts['Part-lpbf'].sets['Set-substrate']
del mdb.models['Model-1'].parts['Part-lpbf'].surfaces['Surf-substrate_bottom']
del mdb.models['Model-1'].parts['Part-substrate'].sets['Set-lpbf']
mdb.models['Model-1'].parts['Part-substrate'].Surface(name='Surf-substrate_top'
    , side1Faces=
    mdb.models['Model-1'].parts['Part-substrate'].faces.getSequenceFromMask((
    '[#8000 ]', ), ))
mdb.models['Model-1'].parts['Part-lpbf'].Surface(name='Surf-lpbf_bottom', 
    side1Faces=
    mdb.models['Model-1'].parts['Part-lpbf'].faces.getSequenceFromMask((
    '[#20 ]', ), ))
# Save by cvander on 2025_07_11-16.30.18; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].Material(name='Material-HX')
mdb.models['Model-1'].materials['Material-HX'].Conductivity(table=((0.015, ), 
    ))
mdb.models['Model-1'].materials['Material-HX'].Density(table=((8.22e-06, ), ))
mdb.models['Model-1'].materials['Material-HX'].SpecificHeat(table=((486.0, ), 
    ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-HX', name=
    'Section-HX', thickness=None)
mdb.models['Model-1'].parts['Part-lpbf'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-lpbf'].sets['Set-lpbf'], sectionName=
    'Section-HX', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-substrate'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-substrate'].sets['Set-substrate'], 
    sectionName='Section-HX', thicknessAssignment=FROM_SECTION)
# Save by cvander on 2025_07_11-16.33.13; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-lpbf-1', 
    part=mdb.models['Model-1'].parts['Part-lpbf'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name=
    'Part-substrate-1', part=mdb.models['Model-1'].parts['Part-substrate'])
mdb.models['Model-1'].Tie(adjust=ON, main=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].surfaces['Surf-lpbf_bottom']
    , name='Constraint-Tie_lpbf_substrate', positionToleranceMethod=COMPUTED, 
    secondary=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].surfaces['Surf-substrate_top']
    , thickness=ON, tieRotations=ON)
# Save by cvander on 2025_07_11-16.40.17; build 2023 2022_09_28-20.11.55 183150
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
#* Unknown step type.
# Save by cvander on 2025_07_11-16.50.51; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].HeatTransferStep(deltmx=500.0, initialInc=0.001, maxInc=
    1.0, maxNumInc=100000, minInc=1e-06, name='Step-heating', previous=
    'Initial', timePeriod=120.0)
mdb.models['Model-1'].TemperatureBC(amplitude=UNSET, createStepName=
    'Step-heating', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    magnitude=25.0, name='BC-buildplateT', region=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].sets['Set-substrate_bottom'])
mdb.models['Model-1'].Field(createStepName='Step-heating', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, fieldVariableNum=1, magnitudes=(25.0, ), name=
    'Predefined Field-T0', region=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].sets['Set-substrate'])
mdb.models['Model-1'].rootAssembly.Set(cells=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), ), name='Set-all')
mdb.models['Model-1'].predefinedFields['Predefined Field-T0'].setValues(region=
    mdb.models['Model-1'].rootAssembly.sets['Set-all'])
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER, 
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#68000000 #2 ]', ), ), size=1.0)
mdb.models['Model-1'].rootAssembly.setSeedConstraints(constraint=FIXED, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#68000000 #2 ]', ), ))
mdb.models['Model-1'].rootAssembly.setSeedConstraints(constraint=FREE, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#68000000 #2 ]', ), ))
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER, 
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#540000 #1 ]', ), ), size=0.5)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER, 
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#4001280 ]', ), ), size=0.3)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER, 
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    ('[#10450 ]', ), ), size=0.1)
mdb.models['Model-1'].rootAssembly.seedEdgeBySize(constraint=FINER, 
    deviationFactor=0.1, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    ('[#560 ]', ), ), size=0.03)
mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    ('[#5 ]', ), ), number=20)
mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    mask=('[#a9f ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    mask=('[#93aae92f #c ]', ), ), number=20)
# Save by cvander on 2025_07_14-11.28.19; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#8 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
# Save by cvander on 2025_07_14-11.28.48; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    mask=('[#f ]', ), ))
mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    mask=('[#885 ]', ), )+\
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].edges.getSequenceFromMask(
    mask=('[#12284905 #4 ]', ), ), number=20)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#8 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    ('[#4 ]', ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
# Save by cvander on 2025_07_14-11.34.36; build 2023 2022_09_28-20.11.55 183150
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
mdb.models['Model-HT'].EventSeriesData(createStepName='Initial', data=((4.5, 
    4.5, 5, 0.03, 450000), (4.501, 5.5, 5, 0.03, 0), (9.05, 4.5, 5, 0.06, 
    450000), (9.051, 5.5, 5, 0.06, 0), (13.6, 4.5, 5, 0.09, 450000), (13.601, 
    5.5, 5, 0.09, 0), (18.15, 4.5, 5, 0.12, 450000), (18.151, 5.5, 5, 0.12, 0), 
    (22.7, 4.5, 5, 0.15, 450000), (22.701, 5.5, 5, 0.15, 0), (27.25, 4.5, 5, 
    0.18, 450000), (27.251, 5.5, 5, 0.18, 0), (31.8, 4.5, 5, 0.21, 450000), (
    31.801, 5.5, 5, 0.21, 0), (36.35, 4.5, 5, 0.24, 450000), (36.351, 5.5, 5, 
    0.24, 0), (40.9, 4.5, 5, 0.27, 450000), (40.901, 5.5, 5, 0.27, 0), (45.45, 
    4.5, 5, 0.3, 450000), (45.451, 5.5, 5, 0.3, 0)), eventSeriesType=
    'ABQ_AM_PowerMagnitude', name='Event series-laser_layer', timeSpan=
    STEP_TIME)
mdb.models['Model-ST'].EventSeriesData(createStepName='Initial', data=((0, -1, 
    0, 0.03, 1), (4.5, 11, 0, 0.03, 0), (5.05, -1, 0, 0.06, 1), (9.05, 11, 0, 
    0.06, 0), (9.6, -1, 0, 0.09, 1), (13.6, 11, 0, 0.09, 0), (14.15, -1, 0, 
    0.12, 1), (18.15, 11, 0, 0.12, 0), (18.7, -1, 0, 0.15, 1), (22.7, 11, 0, 
    0.15, 0), (23.25, -1, 0, 0.18, 1), (27.25, 11, 0, 0.18, 0), (27.8, -1, 0, 
    0.21, 1), (31.8, 11, 0, 0.21, 0), (32.35, -1, 0, 0.24, 1), (36.35, 11, 0, 
    0.24, 0), (36.9, -1, 0, 0.27, 1), (40.9, 11, 0, 0.27, 0), (41.45, -1, 0, 
    0.3, 1), (45.45, 11, 0, 0.3, 0)), eventSeriesType=
    'ABQ_AM_MaterialDeposition', name='Event series-roller', timeSpan=
    STEP_TIME)
mdb.models['Model-HT'].EventSeriesData(createStepName='Initial', data=((0, -1, 
    0, 0.03, 1), (4.5, 11, 0, 0.03, 0), (5.05, -1, 0, 0.06, 1), (9.05, 11, 0, 
    0.06, 0), (9.6, -1, 0, 0.09, 1), (13.6, 11, 0, 0.09, 0), (14.15, -1, 0, 
    0.12, 1), (18.15, 11, 0, 0.12, 0), (18.7, -1, 0, 0.15, 1), (22.7, 11, 0, 
    0.15, 0), (23.25, -1, 0, 0.18, 1), (27.25, 11, 0, 0.18, 0), (27.8, -1, 0, 
    0.21, 1), (31.8, 11, 0, 0.21, 0), (32.35, -1, 0, 0.24, 1), (36.35, 11, 0, 
    0.24, 0), (36.9, -1, 0, 0.27, 1), (40.9, 11, 0, 0.27, 0), (41.45, -1, 0, 
    0.3, 1), (45.45, 11, 0, 0.3, 0)), eventSeriesType=
    'ABQ_AM_MaterialDeposition', name='Event series-roller', timeSpan=
    STEP_TIME)
mdb.models['Model-ST'].TableCollection(name='ABQ_AM.Material Input')
mdb.models['Model-HT'].TableCollection(name='ABQ_AM.Material Input')
mdb.models['Model-ST'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition')
mdb.models['Model-HT'].tableCollections['ABQ_AM.Material Input'].ParameterTable(
    name='ABQ_AM_MaterialDeposition')
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
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].PropertyTable(
    name='ABQ_AM_AbsorptionCoeff', properties=('Absorption Coefficient', ))
mdb.models['Model-HT'].tableCollections['ABQ_AM.Moving Heat Source'].propertyTables['ABQ_AM_AbsorptionCoeff'].PropertyTableData(
    data=((0.7, ), ), label='ABQ_AM_AbsorptionCoeff')
mdb.models['Model-HT'].TimePoint(name='TimePoints-4phases', points=((0, 4.5, 
    1), (4.5, 4.51, 0.001), (4.51, 6.5, 0.01), (6.5, 9.05, 1), (9.05, 9.06, 
    0.001), (9.06, 11.05, 0.01), (11.05, 13.6, 1), (13.6, 13.61, 0.001), (
    13.61, 15.6, 0.01), (15.6, 18.15, 1), (18.15, 18.16, 0.001), (18.16, 20.15, 
    0.01), (20.15, 22.7, 1), (22.7, 22.71, 0.001), (22.71, 24.7, 0.01), (24.7, 
    27.25, 1), (27.25, 27.26, 0.001), (27.26, 29.25, 0.01), (29.25, 31.8, 1), (
    31.8, 31.81, 0.001), (31.81, 33.8, 0.01), (33.8, 36.35, 1), (36.35, 36.36, 
    0.001), (36.36, 38.35, 0.01), (38.35, 40.9, 1), (40.9, 40.91, 0.001), (
    40.91, 42.9, 0.01), (42.9, 45.45, 1), (45.45, 45.46, 0.001), (45.46, 47.45, 
    0.01), (47.45, 50.0, 1)))
mdb.models['Model-HT'].fieldOutputRequests['F-Output-1'].setValues(timePoint=
    'TimePoints-4phases')
mdb.models['Model-HT'].RadiationToAmbient(ambientTemperature=25.0, 
    ambientTemperatureAmp='', createStepName='Step-heating', distributionType=
    UNIFORM, dynamicSurfaceActivation=True, emissivity=0.0, name='Int-Rad', 
    radiationType=AMBIENT, region=
    mdb.models['Model-HT'].rootAssembly.allSets['Set-all'])
mdb.models['Model-HT'].FilmCondition(createStepName='Step-heating', definition=
    EMBEDDED_COEFF, dynamicSurfaceActivation=True, filmCoeff=2.5e-05, 
    filmCoeffAmplitude='', name='Int-Conv', region=
    mdb.models['Model-HT'].rootAssembly.allSets['Set-all'], sinkAmplitude='', 
    sinkDistributionType=UNIFORM, sinkTemperature=25.0)
mdb.jobs.changeKey(fromName='Job-HT_v01', toName='Job-HT_Cmodel_v01')
mdb.models['Model-HT'].rootAssembly.Set(cells=
    mdb.models['Model-HT'].rootAssembly.instances['Part-substrate-1'].cells.getSequenceFromMask(
    mask=('[#f ]', ), )+\
    mdb.models['Model-HT'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), ), name='Set-all')
mdb.models['Model-ST'].rootAssembly.translate(instanceList=('Part-lpbf-1',
    'Part-substrate-1'), vector=(5, 5, 0.3))
mdb.models['Model-HT'].rootAssembly.translate(instanceList=('Part-lpbf-1', 
    'Part-substrate-1'), vector=(5, 5, 0.3))
# Save by cvander on 2025_07_14-13.56.45; build 2023 2022_09_28-20.11.55 183150
mdb.models['Model-HT'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-HT'].rootAssembly.instances['Part-lpbf-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models['Model-HT'].rootAssembly.seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['Model-HT'].rootAssembly.instances['Part-lpbf-1'].edges.getSequenceFromMask(
    ('[#560 ]', ), ), number=10)
mdb.models['Model-HT'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'NT', ))
del mdb.models['Model-HT'].predefinedFields['Predefined Field-T0']
mdb.models['Model-HT'].Temperature(createStepName='Initial',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(25.0, ), name='Predefined Field-1', region=
    mdb.models['Model-HT'].rootAssembly.sets['Set-all'])
