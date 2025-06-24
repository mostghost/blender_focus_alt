import bpy

bl_info = {
    'name': 'Hotkey Focus Alt',
    'author': 'chromeoculi',
    'description': "Adds an alternative 'focus' function, without zoom.",
    'version': (1, 0, 0),
    'location': 'View3D',
    'category': '3D View',
    'warning': "This does not set any default keybinds. You will need to change your preferred focus key to the new function, 'view3d.focus_alt'."
}

class VIEW3D_OT_focus_alt(bpy.types.Operator):
    """Moves 3D cursor to selected, centers view to cursor, then returns the cursor."""
    bl_idname = "view3d.focus_alt"
    bl_label = "Focus Alternative (No Zoom)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if context.mode == 'SCULPT':
            # The default behavior works just fine for sculpt mode.
            bpy.ops.view3d.view_selected()

        else:
            original_cursor_location = context.scene.cursor.location.copy()
            original_cursor_rotation = context.scene.cursor.rotation_euler.copy()

            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.view3d.view_center_cursor()
            
            context.scene.cursor.location = original_cursor_location
            context.scene.cursor.rotation_euler = original_cursor_rotation

        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_OT_focus_alt)

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_focus_alt)

if __name__ == "__main__":
    register()
