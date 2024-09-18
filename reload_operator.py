import bpy

from . import load_fonts as lf


class FONTSELECTOR_OT_reload_fonts(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "fontselector.reload_fonts"
    bl_label = "Reload Fonts"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        datas, change = lf.refresh_fonts_json()
        
        if change:
            lf.reload_font_collections(datas)
            
            self.report({'INFO'}, "Font changes detected, reloading")
            
        else:
            
            self.report({'INFO'}, "No font changes detected")
            
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_reload_fonts)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_reload_fonts)
