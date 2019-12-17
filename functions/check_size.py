import bpy
import os

from .json_functions import read_json
from .misc_functions import get_size, absolute_path
from ..preferences import get_addon_preferences

from ..global_variable import json_file, win_folder, mac_folder, linux_folder

# check size change and return true or false
def check_size_changes() :

    check = True
    folder_list = []
    size = 0
    wm = bpy.context.window_manager
    addon_preferences = get_addon_preferences()
    prefpath = addon_preferences.prefs_folderpath
    json_output = os.path.join(prefpath, json_file)

    if os.path.isfile(json_output) :
        datas = read_json(json_output)

        # default folders
        if wm.fontselector_os == 'WINDOWS': default_folders = win_folder
        elif wm.fontselector_os == 'MAC': default_folders = mac_folder
        else: default_folders = linux_folder
        for fp in default_folders:
            size += get_size(fp)

        # custom folders
        for fp in addon_preferences.font_folders:
            if fp.folderpath != "" :
                size += get_size(absolute_path(fp.folderpath))

        # size check
        if size == datas['size'] :
            check = False
        else :
            check = True

    return check