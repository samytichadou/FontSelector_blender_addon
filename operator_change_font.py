import bpy
import os

from .preferences import get_addon_preferences


class FontSelectorChange(bpy.types.Operator):
    bl_idname = "fontselector.change"
    bl_label = ""
    bl_description = "Change Font"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        active=bpy.context.active_object
        if active is not None:
            active_type=active.type
        else:
            active_type=""
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list
        return len(fplist)>0 and len(fontlist)>0 and active_type=='FONT'
    
    def execute(self, context):
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list
        idx=bpy.context.active_object.data.fontselector_index
        name=os.path.basename(fontlist[idx].filepath)
        active=bpy.context.active_object
        
        if fontlist[idx].name=='Bfont':
            active.data.font=bpy.data.fonts['Bfont']
        else:
            if idx<len(fontlist):
                if os.path.isfile(fontlist[idx].filepath)==True:
                    chk=0
                    chk2=0
                    for f in bpy.data.fonts:
                        if f.filepath==fontlist[idx].filepath:
                            chk2=1
                            fok=f.name
                    for f in bpy.data.fonts:
                        if chk2==0:
                            if f.users==0 and f.filepath!=fontlist[idx].filepath and chk==0:
                                chk=1
                                f.name=os.path.splitext(name)[0]
                                f.filepath=fontlist[idx].filepath
                    if chk==0 and chk2==0:
                        bpy.data.fonts.load(filepath=fontlist[idx].filepath)
                        for f in bpy.data.fonts:
                            if f.filepath==fontlist[idx].filepath:
                                fok=f.name
                    elif chk==1 and chk2==0:
                        for f in bpy.data.fonts:
                            if f.filepath==fontlist[idx].filepath:
                                fok=f.name
                    active.data.font=bpy.data.fonts[fok]
                else:
                    fontlist[idx].missingfont=True
    
        return {'FINISHED'}