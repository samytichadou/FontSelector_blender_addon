import bpy
import os
from bpy.app.handlers import persistent

from .preferences import get_addon_preferences
from .global_variable import fav_list, font_list, subdir_list, size_file
from .misc_functions import get_size, absolute_path

@persistent
def fontselector_startup(scene):
    addon_preferences = get_addon_preferences()
    fplist = addon_preferences.font_folders
    prefpath = absolute_path(addon_preferences.prefs_folderpath)
    #get prefs files
    preffav = os.path.join(prefpath, fav_list)
    prefflist = os.path.join(prefpath, font_list)
    prefsubdir = os.path.join(prefpath, subdir_list)

    fontlist=bpy.data.window_managers['WinMan'].fontselector_list

    #check preference path exist
    if os.path.isdir(prefpath) :

        #check font list
        if os.path.isfile(prefflist) :

            #check if refreshing font list is needed
            for file in os.listdir(prefpath) :
                if size_file in file :
                    assumed_size = int(file.split(size_file)[1])                 
                    #get real size
                    size_total = 0
                    for fp in fplist :
                        if fp.folderpath != "" :
                            path = absolute_path(fp.folderpath)
                            size_total += get_size(path)
                    #do something if size changed
                    if size_total != assumed_size :
                        print("Font Selector --- Changes in Font Folders, refresh needed")
                    break
            
            #load files
            bpy.ops.fontselector.load_fontlist()
            if os.path.isfile(prefsubdir) :
                bpy.ops.fontselector.load_fontsubs()
            if os.path.isfile(preffav) and len(fontlist) > 0 :
                bpy.ops.fontselector.load_favorites()
            print("Font Selector --- Settings loaded")

            