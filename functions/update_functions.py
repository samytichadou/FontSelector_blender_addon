import bpy
import os

from .change_font import change_font
from .misc_functions import clear_collection

first_active_object = ""
    
#update change font
def update_change_font(self, context) :
    global first_active_object

    #check if the loop is run through the active object or other selected ones
    if first_active_object == "" :

        active = first_active_object = bpy.context.active_object
        scn = bpy.context.scene
        wm = bpy.data.window_managers['WinMan']
        
        selected = []
        chkerror = 0

        fontlist = wm.fontselector_list
        idx = active.data.fontselector_index

        ### OLD OVERRIDE ###
        #if wm.fontselector_override :
        #    idx = active.data.fontselector_override_index
        #else :
        #    idx = active.data.fontselector_index
        
        #error handling for not updated list
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
            #regular change of font
            else :
                for obj in selected :
                    #check if font is already changed
                    if font != obj.data.font :
                        ### OLD OVERRIDE ###
                        #if wm.fontselector_override :
                        #    obj.data.fontselector_override_index = idx
                        #else :
                        #    obj.data.fontselector_index = idx
                        obj.data.fontselector_index = idx
                        change_font(obj, font)

        #reset global variable                        
        first_active_object = ""
 
#update save favorites
def update_save_favorites(self, context) :
    active = bpy.context.active_object
    if active is not None :
        if active.type == 'FONT' :
            bpy.ops.fontselector.save_favorites()

#get subdirectories item for enum property
def get_subdirectories_items(self, context) :
    subdir_list = []
    subdir_list.append(("All", "All", "All available Fonts"))
    for sub in bpy.data.window_managers['WinMan'].fontselector_sub :
        subdir_list.append((sub.name, sub.name, sub.filepath))
    return subdir_list

#get name of override folder
def update_change_folder_override(self, context) :
    wm = bpy.data.window_managers['WinMan']
    folder_path = wm.fontselector_folder_override
    wm.fontselector_foldername_override = os.path.basename(os.path.dirname(folder_path))