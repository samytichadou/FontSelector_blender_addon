import bpy
import os

from . import load_fonts as lf


def favorite_callback(self, context):
    
    font_props = context.window_manager.fontselector_properties
    
    if font_props.no_callback:
        print("FONTSELECTOR --- Favorite update function cancelled")
        return
    
    print(f"FONTSELECTOR --- Updating favorite : {self.name}")
    
    # Get favorite datas
    datas = lf.get_existing_favorite_datas()

    # Remove existing favorite entry
    idx = 0
    for font in datas["favorites"]:
        if font == self.name:
            datas["favorites"].pop(idx)
        idx += 1
        
    # Add entry
    if self.favorite:
        datas["favorites"].append(
            self.name,
        )

    # Write json
    path = lf.get_favorite_json_filepath()
    lf.write_json_file(datas, path)

    
class FONTSELECTOR_PR_fonts_properties(bpy.types.PropertyGroup):
    
    filepath: bpy.props.StringProperty(
        name = "Filepath",
    )
    favorite: bpy.props.BoolProperty(
        name = "Favorite",
        update = favorite_callback,
    )
    font_family: bpy.props.StringProperty(
        name = "Font Family",
    )
    font_type: bpy.props.StringProperty(
        name = "Font Type",
    )


class FONTSELECTOR_PR_properties(bpy.types.PropertyGroup):

    fonts : bpy.props.CollectionProperty(
        type=FONTSELECTOR_PR_fonts_properties,
    )
    
    no_callback : bpy.props.BoolProperty()
    

def get_font(font_props):
    
    # Invalid font
    if not os.path.isfile(font_props.filepath):
        print(f"FONTSELECTOR --- Invalid font : {font_props.filepath}, please refresh")
        return None
    
    print(f"FONTSELECTOR --- Getting {font_props.filepath}")
    
    # Local
    try:
        return bpy.data.fonts[font_props.name]
    
    except KeyError:
        print(f"FONTSELECTOR --- Importing : {font_props.name}")
        
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


def font_selection_callback(self, context):
    
    font_props = context.window_manager.fontselector_properties
    
    if font_props.no_callback:
        print("FONTSELECTOR --- Update function cancelled")
        return
    
    print("FONTSELECTOR --- Update function")
    
    target_font_props = font_props.fonts[self.font_index]
    
    # Import font
    target_font = get_font(target_font_props)
    
    # Invalid font
    if target_font is None:
        return
    
    font_props.no_callback = True
    
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
            
    font_props.no_callback = False
    
    # Clear old fonts
    clear_font_datas()
    
    
class FONTSELECTOR_PR_object_properties(bpy.types.PropertyGroup):

    font_search: bpy.props.StringProperty(
        options = {"TEXTEDIT_UPDATE"},
    )
    font_index : bpy.props.IntProperty(
        default = -1,
        update = font_selection_callback,
    )
    font_name : bpy.props.StringProperty()
    
    show_favorite : bpy.props.BoolProperty(
        name = "Show Favorites",
        description = "Show Favorites icon",
        default=True,
    )
    favorite_filter : bpy.props.BoolProperty(
        name = "Favorites Filter",
        description = "Favorites Filter",
    )
    invert_filter : bpy.props.BoolProperty(
        name = "Invert Filter",
        description = "Invert Filters",
    )
    

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
