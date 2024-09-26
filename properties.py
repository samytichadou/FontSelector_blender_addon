import bpy
import os

from . import load_fonts as lf
from .addon_prefs import get_addon_preferences


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
    bold_font_name: bpy.props.StringProperty(
        name = "Bold",
    )
    italic_font_name: bpy.props.StringProperty(
        name = "Italic",
    )
    bold_italic_font_name: bpy.props.StringProperty(
        name = "Bold Italic",
    )


class FONTSELECTOR_PR_properties(bpy.types.PropertyGroup):

    fonts : bpy.props.CollectionProperty(
        type=FONTSELECTOR_PR_fonts_properties,
    )
    
    no_callback : bpy.props.BoolProperty()
    

def get_font_datablock(font):
    
    new_font = None
    
    print(f"FONTSELECTOR --- Getting {font.filepath}")
    
    # Local
    try:
        return bpy.data.fonts[font.name]
    
    except KeyError:
        print(f"FONTSELECTOR --- Importing : {font.name}")
        
    # Importing
    new_font = bpy.data.fonts.load(filepath=font.filepath)
    new_font.name = font.name
    
    # Prevent double users
    new_font.user_clear()
    
    return new_font
    
    
def get_font_family(font_entry):
    
    default_font =  bpy.data.fonts["Bfont Regular"]
    new_font = new_bold_font = new_italic_font = new_bold_italic_font = default_font
    
    # Get font
    font_collection = bpy.context.window_manager.fontselector_properties.fonts
    
    # Invalid font
    if not os.path.isfile(font_entry.filepath):
        print(f"FONTSELECTOR --- Invalid font : {font_entry.filepath}, please refresh")
        return None, None, None, None
    
    # Get font
    new_font = get_font_datablock(font_entry)
    
    # Get bold
    if font_entry.bold_font_name:
        try:
            bold_entry = font_collection[font_entry.bold_font_name]
            new_bold_font = get_font_datablock(bold_entry)
        except KeyError:
            print(f"FONTSELECTOR --- No bold : {font_entry.name}")
            
    # Get italic
    if font_entry.italic_font_name:
        try:
            italic_entry = font_collection[font_entry.italic_font_name]
            new_italic_font = get_font_datablock(italic_entry)
        except KeyError:
            print(f"FONTSELECTOR --- No italic : {font_entry.name}")
            
    # Get bold italic
    if font_entry.bold_italic_font_name:
        try:
            bold_italic_entry = font_collection[font_entry.bold_italic_font_name]
            new_bold_italic_font = get_font_datablock(bold_italic_entry)
        except KeyError:
            print(f"FONTSELECTOR --- No bold italic : {font_entry.name}")
    
    return new_font, new_bold_font, new_italic_font, new_bold_italic_font


def clear_font_datas():
    for font in bpy.data.fonts:
        if font.users == 0:
            bpy.data.fonts.remove(font)


def change_objects_font(
    target_font,
    self,
    context,
    bold_font = None,
    italic_font = None,
    bold_italic_font = None,
):
    
    no_font_family = get_addon_preferences().no_font_family_load
    
    # Change active object font
    self.id_data.font = target_font
    self.font_name = target_font.name
    
    # Bold italic
    if not no_font_family:
        self.id_data.font_bold = bold_font
        self.id_data.font_italic = italic_font
        self.id_data.font_bold_italic = bold_italic_font
    
    # Change selected objects
    for obj in context.selected_objects:
        if obj.type == "FONT":
            
            if obj.data == self.id_data:
                continue
            
            obj.data.font = target_font
            
            props = obj.data.fontselector_object_properties
            props.font_index = self.font_index
            props.font_name = target_font.name
            
            # Bold italic
            if not no_font_family:
                obj.data.font_bold = bold_font
                obj.data.font_italic = italic_font
                obj.data.font_bold_italic = bold_italic_font


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
    target_font, bold_font, italic_font, bold_italic_font = get_font_family(
        target_font_props,
        )
    
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
            bold_font,
            italic_font,
            bold_italic_font,
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
        name = "Invert Filters",
        description = "Invert Filters",
    )
    show_font_infos : bpy.props.BoolProperty(
        name = "Show Infos",
        description = "Show Font Infos",
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
