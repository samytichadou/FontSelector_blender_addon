import bpy
import os
from bpy.app.handlers import persistent

from .preferences import get_addon_preferences
from .misc_functions import get_size, absolute_path
from .function_load_font_subdir import load_font_subdir
from .function_load_favorites import load_favorites

from .functions.check_size import check_size_changes
from .functions.load_json import load_json_font_file

from .global_variable import *
from .global_messages import *

@persistent
def fontselector_startup(scene):
    addon_preferences = get_addon_preferences()
    behavior = addon_preferences.startup_check_behavior
    prefpath = absolute_path(addon_preferences.prefs_folderpath)
    # get prefs files
    preffav = os.path.join(prefpath, fav_list)
    json_list_file = os.path.join(prefpath, json_file)

    font_collection = bpy.data.window_managers['WinMan'].fontselector_list
    subdir_collection = bpy.data.window_managers['WinMan'].fontselector_sub

    #check preference path exist
    if os.path.isdir(prefpath) :
        #check font list
        if os.path.isfile(json_list_file) :

            if behavior in {'AUTOMATIC_UPDATE', 'MESSAGE_ONLY'} :
                chk_changes = check_size_changes()

                if chk_changes :
                    print(print_statement + changes_msg)

                    if behavior == 'AUTOMATIC_UPDATE' :
                        bpy.ops.fontselector.modal_refresh()

                    else :
                        bpy.ops.fontselector.dialog_message('INVOKE_DEFAULT', code = 1)

                else :
                    print(print_statement + no_changes_msg)
                    # load json list
                    load_json_font_file(json_list_file, font_collection, subdir_collection)
            
            else :
                # load json list
                load_json_font_file(json_list_file, font_collection, subdir_collection)

            #bpy.ops.fontselector.load_fontlist()

            # load favorite list
            if os.path.isfile(preffav) and len(font_collection) > 0 :
                load_favorites()
            
            # return state to user
            print(print_statement + settings_loaded_msg)