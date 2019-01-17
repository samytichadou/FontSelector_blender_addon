import bpy
import os
import time

from .misc_functions import get_all_font_files

path = r"C:\Windows\Fonts"

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
        if event.type in {'ESC'} :
            self.cancel(context)
            return {'CANCELLED'}

        elif event.type == 'TIMER' and not self._updating :
            try :
                self._updating = True   
                #font treatment
                print(self.font_list[self.count])
                self.report({'INFO'}, str(self.count+1)+"/"+str(self.total))
                self.count += 1

                self._updating = False
                return {'PASS_THROUGH'}
            except IndexError :
                self.finish(context)
                return {'FINISHED'}
        else :
            return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
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