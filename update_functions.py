import bpy
import os

from .function_change_font import change_font
    
#update change font
def update_change_font(self, context):
    scn = bpy.context.scene
    active = bpy.context.active_object
    selected = []
    chkerror = 0

    fontlist = bpy.data.window_managers['WinMan'].fontselector_list
    idx = active.data.fontselector_index
    
    try :
        font = fontlist[idx]
    except IndexError :
        chkerror = 1

    if chkerror == 0 :
        #get selected
        for obj in scn.objects :
            if obj.select == True and obj.type == 'FONT' :
                selected.append(obj)
        
        #blender font exception
        if fontlist[idx].name == 'Bfont' :
            for obj in selected :
                obj.data.font = bpy.data.fonts['Bfont']
        else :
            for obj in selected :
                change_font(obj, font)
    
#update save favorites
def update_save_favorites(self, context):
    active=bpy.context.active_object
    if active is not None:
        if active.type=='FONT':
            bpy.ops.fontselector.save_favorites()
    
#update list for favorite filter
def update_favorite_filter(self, context):
    bpy.ops.fontselector.filter_favorites()
    
#update list for subdir filter
def update_subdir_filter(self, context):
    bpy.ops.fontselector.filter_subdirfonts()
    
#update lists when toggling subdir
def update_subdir_toggle(self, context):
    active=bpy.context.active_object
    if active is not None:
        if active.type=='FONT':
            bpy.ops.fontselector.filter_favorites()