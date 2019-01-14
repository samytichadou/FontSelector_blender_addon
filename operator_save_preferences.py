import bpy
import os

from .preferences import get_addon_preferences


class FontSelectorSaveFPPrefs(bpy.types.Operator):
    bl_idname = "fontselector.save_fpprefs"
    bl_label = ""
    bl_description = "Save Font Folders Paths in external Font Selector preference file"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        return len(fplist)>0 and prefs!=''
    
    def execute(self, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        prefFP = os.path.join(prefpath, "fontselector_fontfolders")
        linelist=[]
        
        #check if folder exist and create it if not
        if os.path.isdir(prefpath)==False:
            os.makedirs(prefpath)

        chk=0
        for fp in fplist:
            fpath=os.path.abspath(bpy.path.abspath(fp.folderpath))
            if os.path.isdir(fpath)==True:
                chk=1
                linelist.append(fpath)
                
        if chk==1:
            nfile = open(prefFP, "w")
            for l in list(set(linelist)):
                nfile.write(l+'\n')
            nfile.close()
                    
        return {'FINISHED'}