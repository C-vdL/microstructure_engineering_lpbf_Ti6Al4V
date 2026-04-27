import numpy as np
import cadquery as cq
import math

# Parameters
bottom_edge = 5.0  # mm
height = 6.3       # mm
angle_deg = 45     # degrees

bottom_edge = 2.0  # mm
height = 6.3       # mm
angle_deg = 32.41230662     # degrees

# Convert angle to radians
angle_rad = math.radians(angle_deg)

# Since tan(45°) = 1, the shrink per side is height
shrink = height * math.tan(angle_rad)
top_edge = bottom_edge + 2 * shrink  # both sides

# Build the geometry
pyramid = (
    cq.Workplane("XY")
    .rect(top_edge, top_edge)
    .workplane(offset=-height)
    .rect(bottom_edge, bottom_edge)
    .loft(combine=True)
)

# Export to STEP (use external tools to convert to .PRT if needed)
cq.exporters.export(pyramid, "inverted_pyramid_steeper.step")
