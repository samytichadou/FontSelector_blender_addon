import bpy

from . import properties as pr
from .addon_prefs import get_addon_preferences

# TODO Relink informations if needed (regular slot only)
# TODO All selected object

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
        
        props = context.window_manager.fontselector_properties
        families = props.font_families
        
        active_datas = bpy.context.active_object.data
    
        family = families[self.font_family_name]

        # Remove font type if needed
        if props.remove_existing_type_fonts:
            pr.clear_obj_type_fonts(active_datas)

        # Set fonts
        for font in family.fonts:

            # Get specific datablock, import if necessary
            if font.name in ["Regular", "Bold", "Italic", "Bold Italic"]:
                font_datablock = pr.get_font_datablock(
                    font,
                    debug,
                )

            # Set font

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
