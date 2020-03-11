import bpy,os,platform

from ..global_variable import win_folder, mac_folder, linux_folder
from .misc_functions import clear_collection

# set default font folder
def setOs():
    wm = bpy.context.window_manager
    default_folders_list = wm.fontselector_defaultfolders

    clear_collection(default_folders_list)

    if platform.system() == "Windows": 
        wm.fontselector_os = 'WINDOWS'
        default_folder = win_folder
    elif platform.system() == "Darwin":
        wm.fontselector_os = 'MAC'
        default_folder = mac_folder
    else:
        wm.fontselector_os = 'LINUX'
        default_folder = linux_folder

    idx = 0
    for folder in default_folder:
        newfolder = default_folders_list.add()
        newfolder.name = wm.fontselector_os + "_" + str(idx)
        newfolder.folderpath = folder
        idx += 1