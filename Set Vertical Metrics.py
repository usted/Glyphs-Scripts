#MenuTitle: Set Latin vertical metrics
# -*- coding: utf-8 -*-
__doc__="""Sets vertical metrics for a whole Latin font according to Google's recommendations. First it turns on the 'Use Typo Metrics' custom parameter for the font. It measures the H height for typoAscender/hheaAscender, and the typoDescender/hheaDescender is calculated to add enough whitespace to center the H when it is implemented in UI on the web. The winAscent is set to the highest glyph in the font (usually boldest Ahookabove) and the winDescent is set to the lowest. For more detail read https://github.com/googlefonts/gf-docs/blob/main/VerticalMetrics/README.md"""

Font = Glyphs.font

a_z = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")
upm_multiplier = 1.25
upm = Font.upm
tallest = 0
tallest_glyph = ""
shortest = 0
shortest_glyph = ""
Agrave_height = 0
Aring_height = 0
H_height = 0
a_z_min = 0
a_z_min_glyph = ""

from math import ceil

def round_up(n):
    return ceil(n / 10) * 10

print("Measuring %s glyphs across %s masters..." % (len(Font.glyphs), len(Font.masters)))
for glyph in Font.glyphs:
	if glyph.export == True:
		for layer in glyph.layers:
			if layer.isMasterLayer or layer.isSpecialLayer:
				measure_layer = layer.copyDecomposedLayer()
				if measure_layer.shapes:
					for path in measure_layer.shapes:
						for node in path.nodes:
							if(node.type != "offcurve"):
								if node.y > tallest:
									tallest = node.y
									tallest_glyph = glyph.name 
								if node.y < shortest:
									shortest = node.y
									shortest_glyph = glyph.name
								if glyph.name == "Agrave":
									if node.y > Agrave_height:
										Agrave_height = node.y
								if glyph.name == "Aring":
									if node.y > Aring_height:
										Aring_height = node.y
								if glyph.name == "H":
									if node.y > H_height:
										H_height = node.y
								if glyph.name in a_z:
									if node.y < a_z_min:
										a_z_min = node.y
										a_z_min_glyph = glyph.name


win_ascent = tallest
win_descent = abs(shortest) 

win_ascent_rounded = round_up(win_ascent)
win_descent_rounded = round_up(win_descent)


typo_ascender = (((upm * upm_multiplier) - H_height) / 2) + H_height



if typo_ascender < Agrave_height:
	typo_ascender = Agrave_height


if typo_ascender < Aring_height:
	typo_ascender = Aring_height


typo_descender_positive = (typo_ascender - H_height)
typo_descender = -(typo_descender_positive)
typo_descender_rounded_positive = round_up(typo_descender_positive)


hhea_ascender = typo_ascender
hhea_descender = typo_descender

typo_ascender_rounded = round_up(typo_ascender)
typo_descender_rounded = -(typo_descender_rounded_positive)


hhea_ascender_rounded = typo_ascender_rounded
hhea_descender_rounded = typo_descender_rounded

typo_line_gap = 0
hhea_line_gap = typo_line_gap


print("""
Tallest glyph: %s (%s)
Shortest glyph: %s (%s)
H height: %s
Shortest of a-z: %s (%s)

Setting new vertical metrics and Use Typo Metrics to true:
typoAscender, hheaAscender: %s
typoDescender, hheaDescender: %s
typoAscender, hheaAscender - Rounded: %s
typoDescender, hheaDescender - Rounded: %s
winAscent: %s
winDescent: %s
winAscent - Rounded: %s
winDescent - Rounded: %s
typoLineGap: 0
hheaLineGap 0
""" % (tallest_glyph, tallest ,shortest_glyph, shortest, H_height, a_z_min_glyph, a_z_min, typo_ascender, typo_descender, typo_ascender_rounded, typo_descender_rounded, win_ascent, win_descent, win_ascent_rounded, win_descent_rounded))

Font.customParameters["Use Typo Metrics"] = True	

for master in Font.masters:
	master.customParameters["typoAscender"] = typo_ascender_rounded
	master.customParameters["typoDescender"] = typo_descender_rounded
	master.customParameters["hheaAscender"] = hhea_ascender_rounded
	master.customParameters["hheaDescender"] = hhea_descender_rounded
	master.customParameters["typoLineGap"] = typo_line_gap
	master.customParameters["hheaLineGap"] = hhea_line_gap
	master.customParameters["winAscent"] = win_ascent_rounded
	master.customParameters["winDescent"] = win_descent_rounded

print("...done!")