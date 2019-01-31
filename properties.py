import bpy

from .update_functions import update_save_favorites, update_fake_user


class FontSelectorFontList(bpy.types.PropertyGroup) :
    '''name = StringProperty() '''
    filepath = bpy.props.StringProperty(name = "File Path")
    missingfont = bpy.props.BoolProperty(name = "Missing Font", default = False)
    favorite = bpy.props.BoolProperty(name = "Favorite",
                                    default = False, 
                                    update = update_save_favorites,
                                    description = "Mark/Unmark as Favorite Font")
    subdirectory = bpy.props.StringProperty(name="Subdirectory")
    fake_user = bpy.props.BoolProperty(name = "Fake User",
                                    default = False, 
                                    update = update_fake_user,
                                    description = "Fake a User for active font, allowing to keep it in the blend"
                                    )
    
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