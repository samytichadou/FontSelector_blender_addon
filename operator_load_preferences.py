import bpy
import os
import csv

from .preferences import get_addon_preferences


class FontSelectorLoadFPPrefs(bpy.types.Operator):
    bl_idname = "fontselector.load_fpprefs"
    bl_label = ""
    bl_description = "Load Font Folders Paths from external Font Selector preferences File"
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
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        prefFP = os.path.join(prefpath, "fontselector_fontfolders")
        
        #remove existing folder list
        if len(fplist)>=1:
            for i in range(len(fplist)-1,-1,-1):
                fplist.remove(i)
        
        if os.path.isdir(prefpath)==True:
            if os.path.isfile(prefFP)==True:
                with open(prefFP, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1=str(l).replace("[", "")
                        l2=l1.replace("]", "")
                        l3=l2.replace("'", "")
                        l4=l3.replace('"', "")
                        newfolder=fplist.add()
                        newfolder.folderpath=l4
            else:
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)  
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info)  
            
        return {'FINISHED'}