import bpy

from . import load_fonts as lf
from .addon_prefs import get_addon_preferences

# TODO Relink and Reload

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

        # Reload families
        datas, change = lf.refresh_font_families_json(debug, True)
        lf.reload_font_families_collections(datas, debug)

        # TODO Relink and Reload
#         lf.relink_font_objects(debug)
#
#         lf.reload_favorites(debug)
            
        self.report({'INFO'}, "Fonts reloaded")
            
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_reload_fonts)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_reload_fonts)
