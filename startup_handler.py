import bpy
import os
from bpy.app.handlers import persistent

from .preferences import get_addon_preferences


@persistent
def fontselector_startup(scene):
    #get addon prefs
    addon_preferences = get_addon_preferences()
    prefs = addon_preferences.prefs_folderpath
    prefpath = os.path.abspath(bpy.path.abspath(prefs))
    preffav = os.path.join(prefpath, "fontselector_favorites")
    prefflist = os.path.join(prefpath, "fontselector_fontlist")
    prefsubdir = os.path.join(prefpath, "fontselector_subdir")
    fontlist=bpy.data.window_managers['WinMan'].fontselector_list
    
    chk=0
    if os.path.isfile(prefflist)==True:
        chk=1
        bpy.ops.fontselector.load_fontlist()
    if os.path.isfile(prefsubdir)==True:
        bpy.ops.fontselector.load_fontsubs()
    if os.path.isfile(preffav)==True and len(fontlist)>0:
        bpy.ops.fontselector.load_favorites()
    if chk==1:
        print("Font Selector settings loaded")