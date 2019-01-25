import bpy
import os
import time
#import blf
import bgl

from ..misc_functions import get_all_font_files, create_dir, absolute_path, clear_collection, get_size, remove_unused_font, update_progress
from ..preferences import get_addon_preferences
from ..json_functions import *
from ..functions.load_json import load_json_font_file

from ..global_variable import json_file
from ..global_messages import *

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
    # get color and size of progress bar
    addon_preferences = get_addon_preferences()
    color_bar = addon_preferences.progress_bar_color
    bar_thickness = addon_preferences.progress_bar_size

    # Progress Bar
    width = context.area.width
    #height = context.area.height
    x = 0
    y = 0
    completion = count / total
    size = int(width * completion)
    #color_bar_back = [1.0, 1.0, 1.0, 0.1]
    #color_font = [1.0, 1.0, 1.0, 1.0]

    #draw_box(x, y, width, bar_thickness, color_bar_back)
    #draw_box(x, y, size, bar_thickness, color_bar)
    bgl.glColor4f(*color_bar)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glBegin(bgl.GL_QUADS)
    
    bgl.glVertex2f(x + size, y + bar_thickness)
    bgl.glVertex2f(x, y + bar_thickness)
    bgl.glVertex2f(x, y)
    bgl.glVertex2f(x + size, y)

    # Text
    #bgl.glColor4f(*color_font)
    #font_id = 0  # XXX, need to find out how best to get this.
    #text = "Fonts Loading"
    #xfont = width / 2 - 60
    #yfont = 10
    #blf.position(font_id, xfont, yfont, 0)
    #blf.size(font_id, 18, 72)
    #blf.draw(font_id, text)

    bgl.glEnd()

### MODAL ###

# refresh operator modal
class FontSelectorModalTest(bpy.types.Operator):
    bl_idname = "fontselector.modal_refresh"
    bl_label = "Refresh Font List Modal"


    _updating = False
    _timer = None

    font_list = []
    json_font_list = []
    subdirectories = []
    avoid_list = []
    corrupted = []
    size_total = 0
    pref_path = ""
    json_output = ""
    json_old = ""
    debug = False


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
        self.debug = addon_preferences.debug_value

        fplist = addon_preferences.font_folders
        prefpath = absolute_path(addon_preferences.prefs_folderpath)
        #data_font_list = bpy.data.fonts

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
        
        if os.path.isfile(self.json_output) :
            # turn relevant json files into old
            os.rename(self.json_output, self.json_old)

        #create subdir list

        #clean unused
        remove_unused_font()
        
        #check if external folder exist and create it if not
        create_dir(prefpath)

        self.report({'INFO'}, start_refreshing_msg) 

    def modal(self, context, event):
        global count

        # redraw area
        try:
            for area in context.screen.areas:
                #area.tag_redraw()
                #if area.type == 'VIEW_3D':
                if area.type == 'PROPERTIES':
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

                for filtered in self.avoid_list :
                    if name == filtered :
                        chk_local_dupe = 1
                        update_progress(progress_print_statement, count + 1, total)
                        if self.debug :
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
                        self.avoid_list.append(name)
                        update_progress(progress_print_statement, count + 1, total)
                        if self.debug :
                            print(str(count+1) + "/" + str(total) + " fonts treated --- " + name + " imported")
                    except RuntimeError:
                        self.avoid_list.append(name)
                        self.corrupted.append([path, subdir, name])
                        update_progress(progress_print_statement, count + 1, total)
                        if self.debug :
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
        #self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        self._handle = bpy.types.SpaceProperties.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        #bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        bpy.types.SpaceProperties.draw_handler_remove(self._handle, 'WINDOW')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        # recover old json files
        if os.path.isfile(self.json_old) :
            os.rename(self.json_old, self.json_output)

        # reset variables
        global total
        global count
        total = 0
        count = 0
        del self.font_list[:]
        del self.subdirectories[:]

        # return cancel state to user
        self.report({'INFO'}, cancel_refresh_msg)

    def finish(self, context):
        #bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        bpy.types.SpaceProperties.draw_handler_remove(self._handle, 'WINDOW')
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        collection_font_list = bpy.data.window_managers['WinMan'].fontselector_list
        collection_subdir_list = bpy.data.window_managers['WinMan'].fontselector_sub

        # initialize json
        datas = initialize_json_datas()
        # write json font list
        datas = add_fonts_json(datas, self.json_font_list)
        # write json subdir list
        datas = add_subdirectories_json(datas, self.subdirectories)
        # write json size
        datas = add_size_json(datas, self.size_total)
        # write json file
        create_json_file(datas, self.json_output)
        # delete json old files
        if os.path.isfile(self.json_old) :
            os.remove(self.json_old)

        # clean collection data
        clear_collection(collection_font_list)
        clear_collection(collection_subdir_list)

        # load new json into blender data blocks
        load_json_font_file(self.json_output, collection_font_list, collection_subdir_list)

        # reset variables
        global total
        global count
        total = 0
        count = 0
        del self.font_list[:]
        del self.subdirectories[:]

        # redraw area
        try:
            for area in context.screen.areas:
                if area.type == 'PROPERTIES':
                    area.tag_redraw()
        except AttributeError:
            pass

        # if only one subdir, select it

        # return finish state to user
        self.report({'INFO'}, refresh_msg)