import bpy

from . import properties as pr
from .addon_prefs import get_addon_preferences

# TODO Relink informations if needed (regular slot only)

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

        family = families[self.font_family_name]

        datas_list = []

        # Get active object
        datas_list.append(context.active_object.data)

        # Get selected objects
        for obj in context.selected_objects:
            if obj.type == "FONT":
                if obj.data == context.active_object.data:
                    continue
                datas_list.append(obj.data)

        # active_datas = context.active_object.data

        # Find index (clumsy way)
        family_idx = 0
        for fam in families:
            if fam.name == self.font_family_name:
                break
            family_idx += 1

        # Prevent callback
        font_props = context.window_manager.fontselector_properties
        font_props.no_callback = True

        # Iterate through object datas
        for obj_data in datas_list:

            # Remove font type if needed
            if props.remove_existing_type_fonts:
                pr.clear_obj_type_fonts(obj_data)

            # Set fonts
            for font in family.fonts:

                # Set font

                # Get specific datablock, import if necessary
                if font.name in ["Regular", "Bold", "Italic", "Bold Italic"]:
                    font_datablock = pr.get_font_datablock(
                        font,
                        debug,
                    )

                # Regular
                if font.name == "Regular":
                    obj_data.font = font_datablock

                    # Store relink infos
                    obj_props = obj_data.fontselector_object_properties
                    obj_props.relink_family_name = family.name
                    obj_props.relink_type_name = "Regular"

                # Bold
                elif font.name == "Bold":
                    obj_data.font_bold = font_datablock

                # Italic
                elif font.name == "Italic":
                    obj_data.font_italic = font_datablock

                # Bold Italic
                elif font.name == "Bold Italic":
                    obj_data.font_bold_italic = font_datablock

            # Change family index
            obj_data.fontselector_object_properties.family_index = family_idx

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
