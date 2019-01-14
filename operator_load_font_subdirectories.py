import bpy
import os
import csv

from .preferences import get_addon_preferences


class FontSelectorLoadFontSubs(bpy.types.Operator):
    bl_idname = "fontselector.load_fontsubs"
    bl_label = ""
    bl_description = "Load Font Subdirectories from external Font Selector preferences File"
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
        prefsubdir = os.path.join(prefpath, "fontselector_subdir")
        fontsub=bpy.data.window_managers['WinMan'].fontselector_sub
        
        #remove existing font subs
        if len(fontsub)>0:
            for i in range(len(fontsub)-1,-1,-1):
                fontsub.remove(i)
        
        if os.path.isdir(prefpath)==True:
            if os.path.isfile(prefsubdir)==True:
                with open(prefsubdir, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1=str(l).replace("[", "")
                        l2=l1.replace("]", "")
                        l3=l2.replace("'", "")
                        l4=l3.replace('"', "")
                        newsub=fontsub.add()
                        newsub.name=l4
            else:
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)  
                print("Font Selector Warning : Preference File does not exist, check Preference Folder path")  
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info) 
            print("Font Selector Warning : Folder does not exist, check Preference Folder path")   
            
        return {'FINISHED'}