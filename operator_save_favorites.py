import bpy
import os
import csv

from .preferences import get_addon_preferences


class FontSelectorSaveFavorites(bpy.types.Operator):
    bl_idname = "fontselector.save_favorites"
    bl_label = ""
    bl_description = "Save Favorite Fonts in external Font Selector preference file"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list
        active=bpy.context.active_object
        if active is not None:
            active_type=active.type
        else:
            active_type=""
        return prefs!='' and len(fontlist)>0 and active_type=='FONT'
    
    def execute(self, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        preffav = os.path.join(prefpath, "fontselector_favorites")
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list
        favlist=[]
        dupepath=[]
        
        #check if folder exist and create it if not
        if os.path.isdir(prefpath)==False:
            os.makedirs(prefpath)
        
        #get dupepath
        for f in fontlist:
            dupepath.append(f.name)
        
        #get old favs
        if os.path.isfile(preffav)==True:
            with open(preffav, 'r', newline='') as csvfile:
                line = csv.reader(csvfile, delimiter='\n')
                for l in line:
                    favlist.append(l)
        
        if len(fontlist)!=0:
            nfile = open(preffav, "w")
            for f in fontlist:
                if f.favorite==True:
                    fpath=os.path.abspath(bpy.path.abspath(f.filepath))
                    nfile.write(f.name+" || "+fpath+' || '+os.path.basename(os.path.dirname(fpath))+"\n")
            for f2 in favlist:
                l1=str(f2).replace("[", "")
                l2=l1.replace("]", "")
                l3=l2.replace("'", "")
                l4=l3.replace('"', "")
                n=l4.split(" || ")[0]
#                p=l4.split(" || ")[1]
                if n not in dupepath:
                    nfile.write(l4+"\n")
                
            nfile.close()
                    
        return {'FINISHED'}