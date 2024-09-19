import bpy
import os
    
    
class FONTSELECTOR_PR_fonts_properties(bpy.types.PropertyGroup):
    
    filepath : bpy.props.StringProperty(
        name = "Filepath",
    )
    favorite : bpy.props.BoolProperty(
        name = "Favorite",
    )
    font_family : bpy.props.StringProperty(
        name = "Font Family",
    )
    font_type : bpy.props.StringProperty(
        name = "Font Type",
    )


class FONTSELECTOR_PR_properties(bpy.types.PropertyGroup):

    font_search : bpy.props.StringProperty(
        options = {"TEXTEDIT_UPDATE"},
    )
    
    fonts : bpy.props.CollectionProperty(
        type=FONTSELECTOR_PR_fonts_properties,
    )
    

def get_font(font_props):
    
    # Invalid font
    if not os.path.isfile(font_props.filepath):
        print(f"FONTSELECTOR --- Invalid font : {font_props.filepath}, please refresh")
        return None
    
    print(f"FONTSELECTOR --- Getting {font_props.name}")
    
    # Local
    try:
        return bpy.data.fonts[font_props.name]
    
    except KeyError:
        print(f"FONTSELECTOR --- Importing {font_props.name}")
        
    # Importing
    new_font = bpy.data.fonts.load(filepath=font_props.filepath)
    new_font.name = font_props.name
    
    # Prevent double users
    new_font.user_clear()
    
    return new_font


def clear_font_datas():
    for font in bpy.data.fonts:
        if font.users == 0:
            bpy.data.fonts.remove(font)


def change_objects_font(
    target_font,
    self,
    context,
):
    
    # Change active font
    self.id_data.font = target_font
    self.font_name = target_font.name
    
    # Change selected objects
    for obj in context.selected_objects:
        if obj.type == "FONT":
            
            if obj.data == self.id_data:
                continue
            
            obj.data.font = target_font
            
            props = obj.data.fontselector_object_properties
            props.font_index = self.font_index
            props.font_name = target_font.name


def change_strips_font(
    target_font,
    active_data,
    context,
):
    
    active_strip = context.active_sequence_strip
    
    # Change active font
    active_strip.font = target_font
    active_strip.fontselector_object_properties.font_name = target_font.name
    
    # Change selected objects
    for strip in context.selected_sequences:
        if strip.type == "TEXT":
            
            if strip == active_strip:
                continue
            
            strip.font = target_font
            
            props = strip.fontselector_object_properties
            props.font_index = active_strip.fontselector_object_properties.font_index
            props.font_name = target_font.name


# Global variable to prevent callback
no_callback = False

def font_selection_callback(self, context):
    
    global no_callback
    
    if no_callback:
        print(f"FONTSELECTOR --- Update function cancelled - {self.id_data}")
        return
    
    print(f"FONTSELECTOR --- Update function - {self.id_data}")
    
    target_font_props = context.window_manager.fontselector_properties.fonts[self.font_index]
    
    # Import font
    target_font = get_font(target_font_props)
    
    # Invalid font
    if target_font is None:
        return
    
    no_callback = True
    
    # Find object or strip
    if isinstance(self.id_data, bpy.types.TextCurve):
        
        change_objects_font(
            target_font,
            self,
            context,
        )
        
    else:
        
        change_strips_font(
            target_font,
            self,
            context,
        )
            
    no_callback = False
    
    # Clear old fonts
    clear_font_datas()
    
    
class FONTSELECTOR_PR_object_properties(bpy.types.PropertyGroup):

    font_index : bpy.props.IntProperty(
        update = font_selection_callback,
    )
    font_name : bpy.props.StringProperty()
    
    
### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PR_fonts_properties)
    bpy.utils.register_class(FONTSELECTOR_PR_properties)
    bpy.utils.register_class(FONTSELECTOR_PR_object_properties)
    
    bpy.types.WindowManager.fontselector_properties = \
        bpy.props.PointerProperty(
            type = FONTSELECTOR_PR_properties,
            name="Font Selector Properties",
        )
    bpy.types.TextCurve.fontselector_object_properties = \
        bpy.props.PointerProperty(
            type = FONTSELECTOR_PR_object_properties,
            name="Font Selector Properties",
        )
    bpy.types.TextSequence.fontselector_object_properties = \
        bpy.props.PointerProperty(
            type = FONTSELECTOR_PR_object_properties,
            name="Font Selector Properties",
        )

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PR_fonts_properties)
    bpy.utils.unregister_class(FONTSELECTOR_PR_properties)
    bpy.utils.unregister_class(FONTSELECTOR_PR_object_properties)
    
    del bpy.types.WindowManager.fontselector_properties
    del bpy.types.TextCurve.fontselector_object_properties
    del bpy.types.TextSequence.fontselector_object_properties
