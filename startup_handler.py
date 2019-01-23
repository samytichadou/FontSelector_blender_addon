import bpy
import os
from bpy.app.handlers import persistent

from .preferences import get_addon_preferences
from .misc_functions import get_size, absolute_path
from .function_load_font_subdir import load_font_subdir
from .function_load_favorites import load_favorites

from .functions.check_size import check_size_changes

from .global_variable import fav_list, font_list, subdir_list, size_file
from .global_messages import *

@persistent
def fontselector_startup(scene):
    addon_preferences = get_addon_preferences()
    prefpath = absolute_path(addon_preferences.prefs_folderpath)
    # get prefs files
    preffav = os.path.join(prefpath, fav_list)
    prefflist = os.path.join(prefpath, font_list)
    prefsubdir = os.path.join(prefpath, subdir_list)

    fontlist=bpy.data.window_managers['WinMan'].fontselector_list

    #check preference path exist
    if os.path.isdir(prefpath) :
        #check font list
        if os.path.isfile(prefflist) :

            chk_changes = check_size_changes()

            if chk_changes :
                print("Font Selector --- " + changes_msg)
                #old way
                #bpy.ops.fontselector.refresh()
                #modal
                #bpy.ops.fontselector.modal_test()
                pass
                
            else :
                print("Font Selector --- " + no_changes_msg)
                #load files
                bpy.ops.fontselector.load_fontlist()
                if os.path.isfile(prefsubdir) :
                    load_font_subdir()

            if os.path.isfile(preffav) and len(fontlist) > 0 :
                load_favorites()
                
            print("Font Selector --- Settings loaded")