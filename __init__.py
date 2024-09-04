import bpy
from bpy.props import StringProperty, EnumProperty, IntProperty

import sys
import importlib

bl_info = {
    "name": "Unity Importer",
    "author": "Thorben Baerentson",
    "description": "This addon helps importing content from unity to blender.",
    "blender": (4, 00, 0),
    "category": "Import-Export",
}

modulesNames = [
    'UnityPackageImporter',
    #'OBJECT_MT_UnityImporterMenu',
]

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()