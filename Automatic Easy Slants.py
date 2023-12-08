# MenuTitle: Automatic Easy Slants
# -*- coding: utf-8 -*-
# Import the GlyphsApp module
from GlyphsApp import *

from uuid import uuid4

# Get the current font
font = Glyphs.font

# Define the italic angle
italic_angle = 9.5

# 1) Add an Axes called “Italic” in the font-info.
axis = GSAxis()
axis.name = "Italic"
axis.axisTag = "ital"
italic_axis_id = axis.id
font.axes.append(axis)

# 2) Set all the masters to "0" on the Italic axes.
for master in font.masters:
	master.internalAxesValues[italic_axis_id] = 0

# 3) Duplicate all the masters and set the new duplicated to "1" on the italic axis.
new_masters = []
for master in font.masters:
	new_master = master.copy()
	new_master.id = str(uuid4())
	new_master.name += " Italic"
	new_master.internalAxesValues[italic_axis_id] = 1
	new_masters.append(new_master)
	
	#the copy of the master only contains metadata (like metrics and axis values), now copy contents from source master:
	addMissing = True  # Add missing glyphs from source to target
	font.copyGlyphs_sourceFontMasterID_targetFontMasterID_addMissing_(font, master.id, new_master.id, addMissing)
	#font.copyInfoForMasterToMaster_(master.id, new_master.id)
	master.id

	source_kerning = font.kerning[master.id]
	font.kerning[new_master.id] = source_kerning


# Add the new masters to the font before setting italic angle
font.masters.extend(new_masters)

# Set the italic angle for the new masters
for new_master in new_masters:
	new_master.italicAngle = italic_angle



# 4) Duplicates all the instances and check their "Italic" checkbox in the "style linking"
for instance in list(font.instances):
	new_instance = instance.copy()
	new_instance.isItalic = True
	new_instance.linkStyle = new_instance.name
	new_instance.name += " Italic"
	new_instance.internalAxesValues[italic_axis_id] = 1
	font.instances.append(new_instance)

# 5) Cursify all the glyphs containing paths in the Italic masters.
for master in new_masters:
	if master.internalAxesValues[italic_axis_id] == 1:
		for glyph in font.glyphs:
			layer = glyph.layers[master.id]
			# Only process if there are paths:
			if len(layer.paths) == 0:
				continue  # no paths: skip glyph
			
			# Calculate half of the x-height
			x_height_half = master.xHeight / 2.0
			# Apply the italic transformation
			layer.slantX_origin_doCorrection_checkSelection_(italic_angle, x_height_half, True, True)


# Update the font metrics and features
#font.metrics.updateMetrics()
font.updateFeatures()


print("Easy Slants completed successfully.")
