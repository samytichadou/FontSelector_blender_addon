import bpy

from . import properties as pr
from .addon_prefs import get_addon_preferences

# TODO Remove font type if not available (if no regular...) with modifier key ?

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
            if font.name in ["Regular", "Bold", "Italic", "Bold Italic"]:
                font_datablock = pr.get_font_datablock(
                    font,
                    debug,
                )

            # Set font
            # TODO Remove font type if not available (if no regular...) with modifier key ?
            # Regular
            if font.name == "Regular":
                active_datas.font = font_datablock

            # Bold
            elif font.name == "Bold":
                active_datas.font_bold = font_datablock

            # Italic
            elif font.name == "Italic":
                active_datas.font_italic = font_datablock

            # Bold Italic
            elif font.name == "Bold Italic":
                active_datas.font_bold_italic = font_datablock

        # Change family index

        # Prevent callback
        font_props = context.window_manager.fontselector_properties
        font_props.no_callback = True

        # Find index (clumsy way)
        idx = 0
        for fam in families:
            if fam.name == self.font_family_name:
                break
            idx += 1

        # Set Index
        active_datas.fontselector_object_properties.family_index = idx

        # Reset callbacks
        font_props.no_callback = False

        # Clear old fonts
        pr.clear_font_datas()

        self.report({'INFO'}, "Font family loaded")
            
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_load_font_family)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_load_font_family)
