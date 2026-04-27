from abaqus import *
from abaqusConstants import *
import visualization

# Get the current viewport
vp = session.viewports[session.currentViewportName]

# Example: set camera to isometric view
vp.view.setValues(session.views['Iso'])

# Alternatively, set custom camera orientation
vp.view.setValues(
    # fieldOfViewAngle=50,
    nearPlane=60.0,
    farPlane=80.0,
    width=30.0,
    height=15.0,
    viewOffsetX=1,
    viewOffsetY=-6,
    cameraPosition=(50.0, 50.0, 30.0),   # Camera location
    cameraUpVector=(0.0, 0.0, 10.0),         # "Up" direction
    cameraTarget=(0.0, 0.0, 0.0)            # Where the camera is pointing
)



##### Thin wall #####
# ('Camera Position:', (13.1471138000488, 68.7041320800781, 29.2739906311035))
# ('Camera Target:', (4.52965259552002, -1.47949361801147, -0.726009607315063))
# ('Camera Up Vector:', (-2.08017225666879e-09, -5.95683466997343e-08, 9.99999904632568))
# ('Near Plane:', 63.394157409668)
# ('Far Plane:', 71.0054626464844)
# ('Width:', 24.5422611236572)
# ('Height:', 11.1000003814697)
# ('View Offset X:', 1.0)
# ('View Offset Y:', -6.0)

##### Cube #####
# ('Camera Position:', (50.9047088623047, 51.3649864196777, 20.4606170654297))
# ('Camera Target:', (4.23803901672363, 4.69831657409668, -2.87271738052368))
# ('Camera Up Vector:', (0.0, 0.0, 10.0))
# ('Near Plane:', 59.1742782592773)
# ('Far Plane:', 79.3923873901367)
# ('Width:', 30.6778316497803)
# ('Height:', 13.8750028610229)
# ('View Offset X:', 0.0)
# ('View Offset Y:', 0.0)

##### Inverse pyramid #####
# ('Camera Position:', (49.752025604248, 51.1617393493652, 23.1724662780762))
# ('Camera Target:', (-0.947978138923645, 0.46173620223999, -2.1775369644165))
# ('Camera Up Vector:', (0.0, 0.0, 10.0))
# ('Near Plane:', 65.9392776489258)
# ('Far Plane:', 86.1607360839844)
# ('Width:', 30.6779251098633)
# ('Height:', 13.8750448226929)
# ('View Offset X:', 0.0)
# ('View Offset Y:', 0.0)






##### Inverse pyramid #####
# ('Camera Position:', (50.0, 50.0, 25.0))
# ('Camera Target:', (0.0, 0.0, 0.0))
# ('Camera Up Vector:', (0.0, 0.0, 10.0))
# ('Near Plane:', 65.5087890625)
# ('Far Plane:', 86.5912322998047)
# ('Width:', 36.2103309631348)
# ('Height:', 16.3772468566895)
# ('View Offset X:', 0.797983407974243)
# ('View Offset Y:', -1.95073890686035)

##### Cube #####
# ('Camera Position:', (50.0, 50.0, 25.0))
# ('Camera Target:', (0.0, 0.0, 0.0))
# ('Camera Up Vector:', (0.0, 0.0, 10.0))
# ('Near Plane:', 59.2271461486816)
# ('Far Plane:', 79.3395309448242)
# ('Width:', 32.7380180358887)
# ('Height:', 14.8067865371704)
# ('View Offset X:', 0.987119078636169)
# ('View Offset Y:', -5.92271423339844)

##### Thin wall #####
# ('Camera Position:', (-21.3750953674316, -57.090518951416, 12.8430156707764))
# ('Camera Target:', (3.92675304412842, 12.4256973266602, 0.501599550247192))
# ('Camera Up Vector:', (-0.59391188621521, -1.63175988197327, 9.84808349609375))
# ('Near Plane:', 69.0529556274414)
# ('Far Plane:', 78.0735931396484)
# ('Width:', 28.2453022003174)
# ('Height:', 12.7748155593872)
# ('View Offset X:', 1.04649233818054)
# ('View Offset Y:', -4.11820125579834)
