import bpy

from .update_functions import update_save_favorites


class FontSelectorFontList(bpy.types.PropertyGroup) :
    '''name = StringProperty() '''
    filepath = bpy.props.StringProperty(name = "filepath")
    missingfont = bpy.props.BoolProperty(name = "missingfont", default = False)
    favorite = bpy.props.BoolProperty(name = "favorite",
                                    default = False, 
                                    update = update_save_favorites,
                                    description = "Mark/Unmark as Favorite Font")
    subdirectory = bpy.props.StringProperty(name="subdirectory")
    
class FontSelectorFontSubs(bpy.types.PropertyGroup) :
    '''name = StringProperty() '''
    filepath = bpy.props.StringProperty(name = "filepath")

class FontFolders(bpy.types.PropertyGroup) :
    '''name = StringProperty() '''
    folderpath = bpy.props.StringProperty(
            name = "Folder path",
            description = "Folders where Fonts are stored",
            subtype = "DIR_PATH",
            )