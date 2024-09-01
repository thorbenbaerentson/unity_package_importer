import bpy

# Derive from operator to create a new operator. This is often times the kind of 
# add-on you want. It allows you to manipulate things in a blender scene.
# Further reading:
# https://docs.blender.org/api/current/bpy.types.Operator.html
class MarkSelectedAsAsset(bpy.types.Operator):
    """Marks all selected objects as asset and then generate the asset browser preview."""
    bl_idname = "object.mark_selected_as_asset"
    bl_label = "Mark selected as asset"

    # Should return true, if the operator can be executed regarding the current
    # state of blender. If this method returns false this operator cannot be executed.
    # If it has a menu entry it will be grayed out.  
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    # Called if the operator is executed ...
    def execute(self, context):
        # Foreach selected object.
        for o in context.selected_objects:
            # Mark that object as asseet ...
            o.asset_mark()
            # .. and generate a preview image for it. 
            o.asset_generate_preview()
        
        # The return type determines how the Undo-Function works. 
        # By convention retrun 'FINISHED' if changes have been made to 
        # the scene, even if it fails eventually. 
        # If no changes have been made choose: 'CANCELED'.
        return { "FINISHED" }

def menu_func(self, context):
    # Add the operator to the menu using its id and present it to the user using the label given in 'bl_info'.
    self.layout.operator(
        MarkSelectedAsAsset.bl_idname, 
        text = MarkSelectedAsAsset.bl_label,
        # Providing an icon is optional. A list of build in icons can be found here:
        # https://docs.blender.org/api/current/bpy_types_enum_items/icon_items.html
        icon = "ASSET_MANAGER")
    
# Register and add to the "object" menu.
def register():
    # Register the operator itself ...
    bpy.utils.register_class(MarkSelectedAsAsset)

    # ... and add it to the 3D object view menu. 
    # In this example we use a separate we use our own menu item inside Object -> Asset (called Example). To 
    # demonstrate how we can create our own submenu inside an existing menu. 
    # 
    # If it is a default menu, you can find the class by searching the corresponding
    # menu script: Go to 'Scripting'-Tab and right click the top level menu item.
    # Then select 'Edit Source'. This will load the script in the text editor.
    #
    # bpy.types.VIEW3D_MT_object_asset.append(menu_func)

# Undo all changes done by the register function.
def unregister():
    bpy.utils.unregister_class(MarkSelectedAsAsset)
    # bpy.types.VIEW3D_MT_object_asset.remove(menu_func)