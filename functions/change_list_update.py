import bpy


from .change_font import change_font
from .change_font_strip import change_font_strip


# change font when change in list to relink fonts
def change_list_update() :
    wm = bpy.data.window_managers['WinMan']
    fontlist = wm.fontselector_list
    missing_list = ""

    # 3d text object
    for obj in bpy.data.objects :
        if obj.type == 'FONT' and obj.data.fontselector_font != "" :
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
                obj.data.fontselector_index = -1
                missing_list += "Object : " + obj.name

    # strip text
    for scn in bpy.data.scenes :
        seq = scn.sequence_editor.sequences_all
        for strip in seq :
            if strip.type == 'TEXT' and strip.fontselector_font != "" :

                #relink if possible
                old_font = strip.fontselector_font
                chk_font_exists = 0
                for font in fontlist :
                    if font.name == old_font :
                        strip.fontselector_index = font.index
                        change_font_strip(strip, font)
                        chk_font_exists = 1
                        break
                if chk_font_exists == 0 :
                    strip.fontselector_font_missing = True
                    # prevent automatic changes via index
                    strip.fontselector_index = len(fontlist)
                    missing_list += "Strip : " + strip.name
    
    # warning message
    if missing_list != "" :
        bpy.ops.fontselector.dialog_message('INVOKE_DEFAULT', code = 8, customstring = missing_list)