import bpy
import os
import shutil
from bpy_extras.io_utils import ExportHelper

from ..preferences import get_addon_preferences


class FontSelectorExportFavorites(bpy.types.Operator, ExportHelper):
    bl_idname = "fontselector.export_favorites"
    bl_label = "Export Favorites"
    bl_description = "Export Fonts marked as Favorites in a zip file"
    filename_ext = ".zip"
    filepath = bpy.props.StringProperty(default="favorite_fonts")
        
    @classmethod
    def poll(cls, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list
        chk=0
        for f in fontlist:
            if f.favorite==True:
                chk=1
        return len(fplist)>0 and prefs!="" and len(fontlist)>0 and chk==1
    
    def execute(self, context):
        return fontselector_export_favorites(self.filepath, context)
    

### Write Export Function ###
def fontselector_export_favorites(filepath, context):
    fontlist=bpy.data.window_managers['WinMan'].fontselector_list
    zippath=os.path.abspath(bpy.path.abspath(filepath))
    temp=os.path.splitext(zippath)[0]
    
    #create tempfolder
    os.makedirs(os.path.splitext(zippath)[0])
    
    #copy fonts
    for f in fontlist:
        if f.favorite==True:
            name=os.path.basename(f.filepath)
            shutil.copy2(f.filepath, os.path.join(temp, name))
            shutil.copystat(f.filepath, os.path.join(temp, name))
    shutil.make_archive(os.path.splitext(zippath)[0], 'zip', temp)
    shutil.rmtree(temp)
 
    print('Font Selector Export finished')
    return {'FINISHED'} 