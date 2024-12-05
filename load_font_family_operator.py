import bpy

from . import properties as pr
from .addon_prefs import get_addon_preferences


class FONTSELECTOR_OT_load_font_family(bpy.types.Operator):
    """Load/Remove entire font family (Bold, Italic...)"""
    bl_idname = "fontselector.load_font_family"
    bl_label = "Load/Remove Font Family"
    bl_options = {'INTERNAL', 'UNDO'}
    
    font_family_name : bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return bpy.context.active_object

    def execute(self, context):
        
        debug = get_addon_preferences().debug
        
        families = context.window_manager.fontselector_properties.font_families
        
        active_datas = bpy.context.active_object.data
    
        family = families[self.font_family_name]

        # Set fonts
        for font in family.fonts:

            # Get specific datablock, import if necessary
            if font.font_type in ["Regular", "Bold", "Italic", "Bold Italic"]:
                font_datablock = pr.get_font_datablock(
                    font,
                    debug,
                )

            # Set font
            # Regular
            if font.font_type == "Regular":
                active_datas.font = font_datablock

            # Bold
            elif font.font_type == "Bold":
                active_datas.font_bold = font_datablock

            # Italic
            elif font.font_type == "Italic":
                active_datas.font_italic = font_datablock

            # Bold Italic
            elif font.font_type == "Bold Italic":
                active_datas.font_bold_italic = font_datablock

        # TODO Change family index
        # TODO Clear old fonts

        self.report({'INFO'}, "Font family loaded")
            
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_load_font_family)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_load_font_family)
