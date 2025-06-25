import bpy
import mathutils

bl_info = {
    "name": "Hotkey Focus Alt",
    "author": "chromeoculi",
    "description": "Adds an alternative 'focus' function, without zoom.",
    "version": (1, 1, 0),
    "location": "View3D",
    "category": "3D View",
    "warning": "This does not set any default keybinds. You will need to change your \
    preferred focus key to the new function, 'view3d.focus_alt'.",
}


class VIEW3D_OT_focus_alt_snap(bpy.types.Operator):
    """Moves 3D cursor to selected, snaps view to cursor, then returns the cursor."""

    bl_idname = "view3d.focus_alt_snap"
    bl_label = "Focus Alternative (No Zoom) (Snap)"
    bl_options = {"REGISTER"}

    def execute(self, context):
        if context.mode == "SCULPT":
            # The default behavior works just fine for sculpt mode.
            bpy.ops.view3d.view_selected()

        else:
            original_cursor_location = context.scene.cursor.location.copy()
            original_cursor_rotation = context.scene.cursor.rotation_euler.copy()

            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.view3d.view_center_cursor()

            context.scene.cursor.location = original_cursor_location
            context.scene.cursor.rotation_euler = original_cursor_rotation

        return {"FINISHED"}


class VIEW3D_OT_focus_alt(bpy.types.Operator):
    """Moves 3D cursor to selected, slides view to cursor, then returns the cursor."""

    bl_idname = "view3d.focus_alt"
    bl_label = "Focus Alternative (No Zoom) (Animated)"
    bl_options = {"REGISTER"}

    _counter = 0
    _timer = None
    _viewport = None
    _steps = 5
    _diff_step = None

    def execute(self, context):
        if context.mode == "SCULPT":
            # The default behavior works just fine for sculpt mode.
            bpy.ops.view3d.view_selected()

        else:
            self._counter = 0

            self._timer = context.window_manager.event_timer_add(
                0.01, window=context.window
            )
            context.window_manager.modal_handler_add(self)

            return {"RUNNING_MODAL"}

        return {"FINISHED"}

    def modal(self, context, event):
        if event.type == "TIMER":

            if self._counter >= self._steps:  # FINISH

                # One more update because why not? Just to be sure.
                bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)

                return {"FINISHED"}

            elif self._counter == 0:  # START

                # Find the current pivot point
                self._viewport = bpy.context.area.spaces.active.region_3d
                current_pivot = self._viewport.view_location

                # Find the selected area's pivot point
                original_cursor_location = context.scene.cursor.location.copy()
                original_cursor_rotation = context.scene.cursor.rotation_euler.copy()

                bpy.ops.view3d.snap_cursor_to_selected()
                cursor_pivot = context.scene.cursor.location.copy()

                # Return cursor.
                context.scene.cursor.location = original_cursor_location
                context.scene.cursor.rotation_euler = original_cursor_rotation

                # To get from here to there we'll need to know where to move
                # and how far to move per step
                difference = current_pivot - cursor_pivot
                self._diff_step = difference / self._steps

                # From here it will continue running as below, taking us through the
                # first step.

            # Repeating loop starts here

            move_step = self._viewport.view_matrix.copy()
            move_step @= mathutils.Matrix.Translation(self._diff_step)

            self._viewport.view_matrix = move_step

            self._counter += 1

            # If the screen isn't told to explicitly update then the animation won't
            # actually play.
            bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)

        return {"RUNNING_MODAL"}


def register():
    bpy.utils.register_class(VIEW3D_OT_focus_alt)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_focus_alt)


if __name__ == "__main__":
    register()
