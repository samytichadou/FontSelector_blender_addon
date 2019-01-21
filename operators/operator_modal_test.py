import bpy
import os
import time
import blf
import bgl

from ..misc_functions import get_all_font_files

path = r"C:\Windows\Fonts"
count = 0
total = 0

# draw box in open gl function
def draw_box(x, y, w, h, color):
    bgl.glColor4f(*color)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glBegin(bgl.GL_QUADS)
    
    bgl.glVertex2f(x + w, y + h)
    bgl.glVertex2f(x, y + h)
    bgl.glVertex2f(x, y)
    bgl.glVertex2f(x + w, y)
    bgl.glEnd()

# callback for loading bar in 3D view 
def draw_callback_loading(self, context): 
    bar_thickness = 30

    # Progress Bar
    width = context.area.width
    x = 0
    y = 0
    completion = count / total
    size = int(width * completion)

    draw_box(x, y, size, bar_thickness, (1.0, 1.0, 1.0, 0.15))

    # Text
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    font_id = 0  # XXX, need to find out how best to get this.
    text = "Fonts Loading"
    xfont = width / 2 - 60
    yfont = 10
    blf.position(font_id, xfont, yfont, 0)
    blf.size(font_id, 18, 72)
    blf.draw(font_id, text)

    bgl.glEnd()

# refresh operator modal
class FontSelectorModalTest(bpy.types.Operator):
    bl_idname = "fontselector.modal_test"
    bl_label = "Modal Test"

    _updating = False
    _timer = None

    font_list = []

    def __init__(self):
        global total

        for font in get_all_font_files(path) :
            self.font_list.append(font)
        total = len(self.font_list)
        print("Start")

        ### TODO ### turn relevant json files into old

    def modal(self, context, event):
        global count

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
                print(self.font_list[count])
                print(str(count+1)+"/"+str(total))
                count += 1
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
        # the arguments we pass the callback
        args = (self, context)
        self._timer = wm.event_timer_add(0.001, context.window)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_loading, args, 'WINDOW', 'POST_PIXEL')
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.report({'INFO'}, "CANCEL")
        print('cancel')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        global total
        global count
        total = 0
        count = 0
        self.font_list.clear()

        ### TODO ### recover old json files

    def finish(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.report({'INFO'}, "FINISHED")
        print('finished')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        global total
        global count
        total = 0
        count = 0
        self.font_list.clear()

        ### TODO ### delete json old files