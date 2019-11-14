import bpy

# check for desync fonts
def checkDesyncFonts():
    desync_text_list = []
    desync_strip_list = []
    
    #font objects
    for obj in bpy.data.objects:
        if obj.type == 'FONT' and obj.data.fontselector_font != "":
            if obj.data.font.name != obj.data.fontselector_font:
                obj.data.fontselector_desync_font = True
                obj.data.fontselector_index = -1
                desync_text_list.append(obj)

    #font strips
    for obj in bpy.data.objects:
        if obj.type == 'FONT' and obj.data.fontselector_font != "":
            if obj.data.font.name != obj.data.fontselector_font:
                obj.data.fontselector_desync_font = True
                obj.data.fontselector_index = -1
                desync_strip_list.append(obj)

    return desync_text_list, desync_strip_list