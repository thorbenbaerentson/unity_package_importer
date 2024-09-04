import bpy

class OBJECT_MT_UnityImporterMenu(bpy.types.Menu):
    bl_label = "Example"
    bl_idname = "OBJECT_MT_ExampleMenu"

    def draw(self, context):
        layout = self.layout

        # Call our custom operator by name. 
        layout.operator(
            "import.unity_package_importer", 
            text = "Mark selected objects as asset",
            icon = "ASSET_MANAGER")

def draw_menu(self, context):
    self.layout.menu(OBJECT_MT_UnityImporterMenu.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_MT_UnityImporterMenu)
    bpy.types.VIEW3D_MT_object_asset.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_asset.remove(draw_menu)
    bpy.utils.unregister_class(OBJECT_MT_UnityImporterMenu)