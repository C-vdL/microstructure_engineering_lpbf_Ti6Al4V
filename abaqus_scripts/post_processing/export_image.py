# -*- coding: mbcs -*-
# Export the current viewport to an image with a given pixel size
# Run inside Abaqus/CAE (File -> Run Script)

from abaqus import *
from abaqusConstants import *
import os

# ---------- User parameters ----------
out_dir = os.getcwd()                 # change to desired output folder
base_name = 'viewport_export'         # file base name (extension will be added)
img_width = 2*1920                      # width in pixels
img_height = 2*1080                     # height in pixels
image_format = PNG                    # PNG or TIFF or SVG etc. (use abaqusConstants)
# -------------------------------------

# Make sure output folder exists
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Get the current viewport (the one you set up manually)
vp_name = session.currentViewportName
vp = session.viewports[vp_name]

# Optional: remove viewport decorations and background for a "clean" image
# (Use OFF/ON, COLOR/GREYSCALE/BLACK_AND_WHITE as needed.)
session.printOptions.setValues(rendition=COLOR, vpDecorations=OFF, vpBackground=OFF, compass=OFF)

# Set format-specific image-size option
if image_format == PNG:
    # imageSize is a tuple (width, height) in pixels for pngOptions
    session.pngOptions.setValues(imageSize=(img_width, img_height))
elif image_format == TIFF:
    session.tiffOptions.setValues(imageSize=(img_width, img_height))
elif image_format == SVG:
    # SVG imageSize accepts symbolic options (e.g. 'SIZE_ON_SCREEN'); SVG is vector so pixel size handling differs.
    # session.svgOptions.setValues(imageSize='SIZE_ON_SCREEN')
    session.svgOptions.setValues(imageSize=(img_width, img_height))
else:
    # For other formats you may need to set the corresponding options object (psOptions/epsOptions/etc.)
    pass

# Prepare full path (printToFile will add extension if missing, but adding extension is explicit)
ext = '.png' if image_format == PNG else ('.tif' if image_format == TIFF else '.svg')
file_path = os.path.join(out_dir, base_name + ext)

# Print the viewport to file (uses the pngOptions/tiffOptions set above)
session.printToFile(fileName=file_path, format=image_format, canvasObjects=(vp,))

print('Viewport exported to:', file_path)
