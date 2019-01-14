import bpy
import os
import csv

from .preferences import get_addon_preferences


class FontSelectorLoadFavorites(bpy.types.Operator):
    bl_idname = "fontselector.load_favorites"
    bl_label = ""
    bl_description = "Load Font Favorites from external Font Selector preferences File"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        return prefs!=''
    
    def execute(self, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        preffav = os.path.join(prefpath, "fontselector_favorites")
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list
        favlist=[]
        
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
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)
                print("Font Selector Warning : Preference File does not exist, check Preference Folder path")  
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info)  
            print("Font Selector Warning : Folder does not exist, check Preference Folder path")  
            
        return {'FINISHED'}