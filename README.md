# blender_focus_alt
A simple replacement to blender's default focus behavior.

By default, blender's "view selected" function centers the view on the selected object, while also zooming in on the selection as much as possible to fill the screen.
Instead, this centers the view on the selected object, while keeping the original zoom.

This does not add any new keymaps - instead it adds a new function, `view3d.focus_alt`. By default, 'View Selected' is set to `numpad .`. In keymap preferences, you can change the function that calls from `view3d.view_selected` to `view3d.focus_alt`.
