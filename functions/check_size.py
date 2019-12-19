import bpy
import os

from .json_functions import read_json
from .misc_functions import get_size, absolute_path
from ..preferences import get_addon_preferences
from ..global_variable import json_file


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
        for fp in wm.fontselector_defaultfolders:
            size += get_size(fp.folderpath)

        # custom folders
        for fp in addon_preferences.font_folders:
            if fp.folderpath != "" and os.path.isdir(fp.folderpath):
                size += get_size(absolute_path(fp.folderpath))

        # size check
        if size == datas['size'] :
            check = False
        else :
            check = True

    return check