#MenuTitle: Export All Fonts
# -*- coding: utf-8 -*-
__doc__="""
Export All Fonts
"""

from GlyphsApp import OTF, TTF, WOFF, WOFF2, EOT, UFO, GSFont, GSInstance, GSCustomParameter, GSPropertyNameFamilyNamesKey, INSTANCETYPEVARIABLE, PLAIN
import os

# Load your font
font = Glyphs.font

# Get the current document
doc = Glyphs.currentDocument

# Get the file path of the current document
doc_path = doc.filePath

# Get the folder path of the current Glyphs document
folder_path = os.path.dirname(doc_path)

# Define the name of the subfolder
subfolder_name = "Export"

# Create the subfolder if it doesn't exist
export_folder = os.path.join(folder_path, subfolder_name)
if not os.path.exists(export_folder):
    os.mkdir(export_folder)

# Define the names of the subfolders inside the "export" subfolder
subfolder_names = ["OTF", "TTF", "WOFF", "Variable", "Website - Protected files"]

# Create the font family subfolder
font_family_name = font.familyName
font_family_folder = os.path.join(export_folder, font_family_name)
if not os.path.exists(font_family_folder):
    os.mkdir(font_family_folder)

# Create the subfolders inside the font family folder
subfolder_paths = {}
for name in subfolder_names:
    if name != "Website - Protected files":
        subfolder_path = os.path.join(font_family_folder, name)
        if not os.path.exists(subfolder_path):
            os.mkdir(subfolder_path)
    else:
        subfolder_path = os.path.join(export_folder, name)
        if not os.path.exists(subfolder_path):
            os.mkdir(subfolder_path)
    subfolder_paths[name] = subfolder_path
OTF_AutoHint = True
TTF_AutoHint = True
RemoveOverlap = True
UseSubroutines = True
UseProductionNames = True
Web_OutlineFormat = TTF

familyName = font.familyNames["ENG"]



# Website - Protected files

# Temporary Variable Instance - A (Only the space glyph) 
TemporaryVariableInstance_A = GSInstance(type=INSTANCETYPEVARIABLE)
TemporaryVariableInstance_A.name = "Web variable A"
TemporaryVariableInstance_A.customParameters['fileName'] = f"{font.familyName} - A"
TemporaryVariableInstance_A.customParameters['Keep Glyphs'] = "space"
font.instances.append(TemporaryVariableInstance_A)

# Temporary Variable Instance - B (The rest of the glyphs, but the space is 20000 wide) 
TemporaryVariableInstance_B = GSInstance(type=INSTANCETYPEVARIABLE)
TemporaryVariableInstance_B.name = "Web variable B"
TemporaryVariableInstance_B.customParameters['fileName'] = f"{font.familyName} - B"
TemporaryVariableInstance_B.customParameters['Filter'] = "Transformations; Width: +20000; include:space"
font.instances.append(TemporaryVariableInstance_B)

print("== Exporting Website - Protected files ==")
print(font.export(Format=VARIABLE, Containers=[PLAIN, WOFF, WOFF2], FontPath=os.path.expanduser(subfolder_paths["Website - Protected files"]), UseProductionNames=UseProductionNames, AutoHint=TTF_AutoHint))
print()

# Delete the Temporary Variable Instances
font.instances.remove(TemporaryVariableInstance_A)
font.instances.remove(TemporaryVariableInstance_B)



# Actual Variable Export

# Temporary Variable Instance Shich should have the name "FontName - Variable" 
TemporaryVariableInstance_Actual = GSInstance(type=INSTANCETYPEVARIABLE)
TemporaryVariableInstance_Actual.setProperty_value_languageTag_(GSPropertyNameFamilyNamesKey, f"{font.familyName} Variable", None)
TemporaryVariableInstance_Actual.customParameters['fileName'] = f"{font.familyName} - Variable"
font.instances.append(TemporaryVariableInstance_Actual)

print("== Exporting Variable ==")
print(font.export(Format=VARIABLE, Containers=[PLAIN, WOFF, WOFF2], FontPath=os.path.expanduser(subfolder_paths["Variable"]), UseProductionNames=UseProductionNames, AutoHint=TTF_AutoHint))
print()

# Delete the Actual Temporary Variable Instance
font.instances.remove(TemporaryVariableInstance_Actual)


# Export OTF, TTF and WOFF
for instance in font.instances:
    print("== Exporting OTF ==")
    print(instance.generate(Format=OTF, FontPath=os.path.expanduser(subfolder_paths["OTF"]), AutoHint=OTF_AutoHint, RemoveOverlap=RemoveOverlap, UseSubroutines=UseSubroutines, UseProductionNames=UseProductionNames))
print()

for instance in font.instances:
    print("== Exporting TTF ==")
    print(instance.generate(Format=TTF, FontPath=os.path.expanduser(subfolder_paths["TTF"]), AutoHint=TTF_AutoHint, RemoveOverlap=RemoveOverlap, UseProductionNames=UseProductionNames))
print()

for instance in font.instances:
    print("== Exporting Web ==")
    print(instance.generate(Format=Web_OutlineFormat, FontPath=os.path.expanduser(subfolder_paths["WOFF"]), AutoHint=TTF_AutoHint, RemoveOverlap=RemoveOverlap, UseSubroutines=UseSubroutines, UseProductionNames=UseProductionNames, Containers=[WOFF, WOFF2, EOT]))
print()
