import bpy

from ..preferences import get_addon_preferences
from ..functions.misc_functions import get_all_font_files, absolute_path

class FontSelectorRefreshToggle(bpy.types.Operator):
    bl_idname = "fontselector.refresh_toggle"
    bl_label = "Refresh"
    bl_description = "Refresh Font List or Stop Refreshing"
    bl_options = {'REGISTER'}

    def execute(self, context):
        wm = context.window_manager
        if wm.fontselector_isrefreshing :
            wm.fontselector_isrefreshing = False
        else :
            bpy.ops.fontselector.modal_refresh()

        return {'FINISHED'}