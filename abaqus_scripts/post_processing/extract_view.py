# -*- coding: mbcs -*-
# Script to print current view parameters in Abaqus/CAE

from abaqus import *
from abaqusConstants import *

vp = session.viewports[session.currentViewportName]

# Get the current view
current_view = vp.view

# Print out the camera settings
print("Camera Position:", current_view.cameraPosition)
print("Camera Target:", current_view.cameraTarget)
print("Camera Up Vector:", current_view.cameraUpVector)
print("Near Plane:", current_view.nearPlane)
print("Far Plane:", current_view.farPlane)
print("Width:", current_view.width)
print("Height:", current_view.height)
print("View Offset X:", current_view.viewOffsetX)
print("View Offset Y:", current_view.viewOffsetY)
