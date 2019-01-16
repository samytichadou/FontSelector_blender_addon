import bpy
import os
import csv

from .preferences import get_addon_preferences
from .misc_functions import absolute_path

from .global_variable import fav_list

def load_favorites():
    #get addon prefs
    addon_preferences = get_addon_preferences()
    prefs = addon_preferences.prefs_folderpath
    prefpath = absolute_path(prefs)
    preffav = os.path.join(prefpath, fav_list)
    fontlist = bpy.data.window_managers['WinMan'].fontselector_list
    favlist = []
    
    if os.path.isdir(prefpath)==True:
        if os.path.isfile(preffav)==True:
            with open(preffav, 'r', newline='') as csvfile:
                line = csv.reader(csvfile, delimiter='\n')
                for l in line:
                    l1=str(l).replace("[", "")
                    l2=l1.replace("]", "")
                    l3=l2.replace("'", "")
                    l4=l3.replace('"', "")
                    n=l4.split(" || ")[0]
                    favlist.append(n)
                for f2 in favlist:
                    for f in fontlist:
                        if f.name==f2:
                            f.favorite=True
        else:
            print("Font Selector --- Preference File does not exist")  