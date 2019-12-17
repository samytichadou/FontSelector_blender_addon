import bpy

from ..global_messages import resync, desync, print_statement

# check for desync fonts
def checkDesyncFonts():
    wm = bpy.context.window_manager
    collection_font_list = wm.fontselector_list

    #font objects
    for obj in bpy.data.objects:
        if obj.type == 'FONT' and obj.data.fontselector_font != "" and obj.data.font is not None:
            if obj.data.font.name != obj.data.fontselector_font:
                #try resync
                chk_resync = 0
                for font in collection_font_list:
                    if font.name == obj.data.font.name:
                        obj.data.fontselector_index = font.index
                        print(print_statement + obj.name + resync)
                        obj.data.fontselector_font = obj.data.font.name
                        obj.data.fontselector_desync_font = False
                        chk_resync = 1
                        break
                if chk_resync == 0: 
                    print(print_statement + obj.name + desync)
                    obj.data.fontselector_desync_font = True

    #font strips
    for scn in bpy.data.scenes:
        if scn.sequence_editor.sequences_all is not None:
            seq = scn.sequence_editor.sequences_all
            for strip in seq :
                if strip.type == 'TEXT' and strip.fontselector_font != "" and strip.font is not None:
                    if strip.font.name != strip.fontselector_font:
                        #try resync
                        chk_resync = 0
                        for font in collection_font_list:
                            if font.name == strip.font.name:
                                strip.fontselector_index = font.index
                                print(print_statement + strip.name + resync)
                                strip.fontselector_font = strip.font.name
                                strip.fontselector_desync_font = False
                                chk_resync = 1
                                break
                        if chk_resync == 0: 
                            print(print_statement + strip.name + desync)
                            strip.fontselector_desync_font = True