import bpy
import os
import time
import blf
import bgl

from .misc_functions import get_all_font_files

path = r"C:\Windows\Fonts"

def draw_callback_loading(self, context): 
    print("drawing")
    font_id = 0  # XXX, need to find out how best to get this.

    # draw some text
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, "Loading Test")

class FontSelectorModalTest(bpy.types.Operator):
    bl_idname = "fontselector.modal_test"
    bl_label = "Modal Test"

    _updating = False
    _timer = None

    font_list = []
    total = 0
    count = 0

    def __init__(self):
        for font in get_all_font_files(path) :
            self.font_list.append(font)
        self.total = len(self.font_list)
        print("Start")

    def modal(self, context, event):
        ### TODO ### Change le space view pour mettre dans la barre d'info
        # redraw info area
        try:
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        except AttributeError:
            pass

        # handle cancelling
        if event.type in {'ESC'} :
            self.cancel(context)
            return {'CANCELLED'}

        # do calculations
        elif event.type == 'TIMER' and not self._updating :
            try :
                self._updating = True   
                #font treatment
                print(self.font_list[self.count])
                print(str(self.count+1)+"/"+str(self.total))
                self.count += 1

                self._updating = False
                return {'PASS_THROUGH'}
            except IndexError :
                self.finish(context)
                return {'FINISHED'}
        
        # continue
        else :
            return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        # the arguments we pass the the callback
        args = (self, context)
        ### TODO ### Change le space view pour mettre dans la barre d'info
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_loading, args, 'WINDOW', 'POST_PIXEL')
        self._timer = wm.event_timer_add(0.01, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self.report({'INFO'}, "CANCEL")
        print('cancel')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def finish(self, context):
        self.report({'INFO'}, "FINISHED")
        print('finished')