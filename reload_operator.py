import bpy

from . import load_fonts as lf
from .addon_prefs import get_addon_preferences


class FONTSELECTOR_OT_reload_fonts(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "fontselector.reload_fonts"
    bl_label = "Reload Fonts"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        debug = get_addon_preferences().debug

        # Prevent callback
        font_props = context.window_manager.fontselector_properties
        font_props.no_callback = True

        # Reload families
        datas, change = lf.refresh_font_families_json(debug, True)
        lf.reload_font_families_collections(datas, debug)

        # Relink
        lf.relink_font_objects(debug)

        # Reload favorites
        lf.reload_favorites(debug)

        # Restore callback
        font_props.no_callback = False
            
        self.report({'INFO'}, "Fonts reloaded")
            
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_reload_fonts)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_reload_fonts)
