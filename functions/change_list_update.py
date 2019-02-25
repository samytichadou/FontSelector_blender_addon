import bpy


from .change_font import change_font


# change font when change in list to relink fonts
def change_list_update() :
    wm = bpy.data.window_managers['WinMan']
    fontlist = wm.fontselector_list
    missing_list = ""

    for obj in bpy.data.objects :
        if obj.type == 'FONT' :

            # relink if possible
            old_font = obj.data.fontselector_font
            chk_font_exists = 0
            for font in fontlist :
                if font.name == old_font :
                    obj.data.fontselector_index = font.index
                    change_font(obj, font)
                    chk_font_exists = 1
                    break
            if chk_font_exists == 0 :
                obj.data.fontselector_font_missing = True
                # prevent automatic changes via index
                obj.data.fontselector_index = len(fontlist)
                missing_list += obj.name
    
    # warning message
    if missing_list != "" :
        bpy.ops.fontselector.dialog_message('INVOKE_DEFAULT', code = 8, customstring = missing_list)