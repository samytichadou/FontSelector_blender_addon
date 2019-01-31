import bpy
import os

from .function_change_font import change_font
from .misc_functions import clear_collection

first_active_object = ""
    
#update change font
def update_change_font(self, context) :
    global first_active_object

    #check if the loop is run through the active object or other selected ones
    if first_active_object == "" :

        active = first_active_object = bpy.context.active_object
        scn = bpy.context.scene
        
        selected = []
        chkerror = 0

        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        idx = active.data.fontselector_index
        
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

#update make fake_user
def update_fake_user(self, context) :
    fontlist = bpy.data.window_managers['WinMan'].fontselector_list
    for font in fontlist :
        if font.fake_user :
            # import font
            if os.path.isfile(font.filepath) :
                chkunused = 0
                chklocal = 0

                #check for local font
                for f in bpy.data.fonts :
                    if f.filepath == font.filepath :
                        chklocal= 1
                        new_font = f
                        break

                #check unused font
                if chklocal == 0 :
                    for f in bpy.data.fonts :
                        if f.users == 0 and f.filepath != font.filepath and chkunused == 0 :
                            chkunused = 1
                            f.name = os.path.splitext(font.name)[0]
                            f.filepath = font.filepath
                            new_font = f
                            break
                
                #import font
                if chkunused == 0 and chklocal == 0 :
                    new_font = bpy.data.fonts.load(filepath=font.filepath)

            #no font file
            else:
                font.missingfont=True

            # use fake user
            new_font.use_fake_user = True
        # remove fake user
        else :
            try :
                old_font = bpy.data.fonts[font.name]
                old_font.use_fake_user = False
                # remove font
                bpy.data.fonts.remove(old_font, do_unlink=True)
            except KeyError :
                pass