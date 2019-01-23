import bpy
import os
import time
import blf
import bgl

from ..misc_functions import get_all_font_files, create_dir, absolute_path, clear_collection, get_size
from ..preferences import get_addon_preferences
from ..global_variable import json_file
from ..json_functions import *

count = 0
total = 0

### UI ###

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
def draw_callback_px(self, context):
    bar_thickness = 30

    # Progress Bar
    width = context.area.width
    x = 0
    y = 0
    completion = count / total
    size = int(width * completion)
    color_bar_back = [1.0, 1.0, 1.0, 0.1]
    color_bar = [1.0, 1.0, 1.0, 0.3]
    color_font = [1.0, 1.0, 1.0, 1.0]

    draw_box(x, y, width, bar_thickness, color_bar_back)
    draw_box(x, y, size, bar_thickness, color_bar)

    # Text
    bgl.glColor4f(*color_font)
    font_id = 0  # XXX, need to find out how best to get this.
    text = "Fonts Loading"
    xfont = width / 2 - 60
    yfont = 10
    blf.position(font_id, xfont, yfont, 0)
    blf.size(font_id, 18, 72)
    blf.draw(font_id, text)

    bgl.glEnd()

### MODAL ###

# refresh operator modal
class FontSelectorModalTest(bpy.types.Operator):
    bl_idname = "fontselector.modal_test"
    bl_label = "Modal Test"


    _updating = False
    _timer = None

    font_list = []
    json_font_list = []
    subdirectories = []
    filter_list = []
    corrupted = []
    size_total = 0
    pref_path = ""
    json_output = ""
    json_old = ""


    @classmethod
    def poll(cls, context):
        addon_preferences = get_addon_preferences()
        fontcheck = []      
        fplist = addon_preferences.font_folders
        try :
            for f in fplist :
                absolute_folder = absolute_path(f.folderpath)
                for font in get_all_font_files(absolute_folder) :
                    fontcheck.append(font)
        except IndexError :
            pass
        return len(fontcheck)>0


    def __init__(self):

        global total

        addon_preferences = get_addon_preferences()
        self.pref_path = addon_preferences.prefs_folderpath
        self.json_output = os.path.join(addon_preferences.prefs_folderpath, json_file)
        self.json_old = os.path.join(addon_preferences.prefs_folderpath, "fontselector.old")

        fplist = addon_preferences.font_folders
        prefpath = absolute_path(addon_preferences.prefs_folderpath)
        collection_font_list = bpy.data.window_managers['WinMan'].fontselector_list
        data_font_list = bpy.data.fonts

        for folder in fplist :
            if folder.folderpath != "" :
                absolute_folder = absolute_path(folder.folderpath)
                self.size_total += get_size(absolute_folder) 
                fontpath_list, subdir_list = get_all_font_files(absolute_folder)
                for font in fontpath_list :
                    self.font_list.append(font)
                for subdir in subdir_list :
                    self.subdirectories.append(subdir)
        total = len(self.font_list)

        #get filtered font

        #create subdir list

        #clean unused
        if len(data_font_list) > 0:
            bpy.ops.fontselector.remove_unused()
        
        #check if external folder exist and create it if not
        create_dir(prefpath)
        
        #clear list
        #clear_collection(collection_font_list)      

        print("Start")

        # turn relevant json files into old
        os.rename(self.json_output, self.json_old)

    def modal(self, context, event):
        global count

        # redraw area
        try:
            for area in context.screen.areas:
                #area.tag_redraw()
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
                chk_local_dupe = 0
                path, subdir, name = self.font_list[count]

                for filtered in self.filter_list :
                    if name == filtered :
                        chk_local_dupe = 1
                        print(str(count+1) + "/" + str(total) + " fonts treated --- " + name + " filtered out")
                        break

                if chk_local_dupe == 0 :
                    try:
                        # load font in blender datas to get name
                        datafont = bpy.data.fonts.load(filepath = path)
                        # append to json font list [name, filepath, subdir]
                        self.json_font_list.append([datafont.name, path, subdir])
                        # delete font
                        bpy.data.fonts.remove(datafont, do_unlink=True)
                        # append in filter list
                        self.filter_list.append(name)
                        print(str(count+1) + "/" + str(total) + " fonts treated --- " + name + " imported")
                    except RuntimeError:
                        self.filter_list.append(name)
                        self.corrupted.append([path, subdir, name])
                        print(str(count+1) + "/" + str(total) + " fonts treated --- " + name + " corrupted, filtered out")

                #print(self.font_list[count])
                #print(str(count+1)+"/"+str(total))

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
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
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
        del self.font_list[:]

        # recover old json files
        os.rename(self.json_old, self.json_output)

    def finish(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.report({'INFO'}, "FINISHED")
        print('finished')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        # initialize json
        datas = initialize_json_datas()
        # write json font list
        datas = add_fonts_json(datas, self.json_font_list)
        # write json subdir list
        datas = add_subdirectories_json(datas, self.subdirectories)
        # write json filter list
        # write json size
        datas = add_size_json(datas, self.size_total)
        # copy json 
        # write json file
        create_json_file(datas, self.json_output)
        # delete json old files
        os.remove(self.json_old)

        global total
        global count
        total = 0
        count = 0
        del self.font_list[:]