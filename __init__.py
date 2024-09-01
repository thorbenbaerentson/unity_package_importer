# If these two lines cause in error inside you IDE: Don´t worry, Blender can resolve these imports.
import bpy
from bpy.props import StringProperty, EnumProperty, IntProperty

# Needed to register each module.
import sys
import importlib
import os

# ----- YOUR MODULES GO HERE ------
# Add further modules here. Each module must be a single python-file
# with its own register and unregister function. The module name is the
# name of the python file without extension.
#
# Further reading: 
# https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/
modulesNames = [
    'MarkSelectedAsAsset',
    'OBJECT_MT_ExampleMenu',
]

# Import current source directory to path so we can import modules from the current source directory.
# This is needed if we want to import files, that do not contain a register and unregister function.
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

# This file simply prints a message to the console on load.
import ImportTest

# This is a sample add-on to demonstrate how add-ons are implemented in Blender. The functionality itself is 
# redundant since blender already implents this behavior. However, it shows how to:
# - implement an operator add-on, 
# - integrate it with blender menus
# - divide an add-on into several files
#
# Therefore it can serve as a template for blender add-on development.
#
# Tips:
# If you start out with add-on development make sure to enable 'Python Tooltips' and 'Development Extras' under:
# Edit -> Preferences -> Interface.
# With the functionality enabled you can right click on a menu item and review its code. This is helpful,
# if you want to integrate your operators with the existing blender UI. 

# Provide Blender with Meta-Data for your add-on. This is required for single file add-ons. 
bl_info = {
    "name": "Extension Template",
    "author": "Thorben Baerentson",
    "description": "This is a template for creating blender addons.",
    "blender": (4, 00, 0),
    "category": "Object",
}

# Get the full name for each module and append it to modulesFullNames ...
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
# ... then import or reload these modules.
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

# Register all modules found using the register method defined in the imported module.
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

# Unregister all modules we´ve imported using the unregister method defined in the imported module.
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()