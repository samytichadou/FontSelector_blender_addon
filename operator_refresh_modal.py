import bpy
import os
import csv

from .preferences import get_addon_preferences
from .misc_functions import create_dir, clear_collection
from .function_load_favorites import load_favorites

from .global_variable import extensions

class FontSelectorRefreshModal(bpy.types.Operator):
    bl_idname = "fontselector.refresh_modal"
    bl_label = "Refresh Font List"

    is_running = bpy.props.BoolProperty()
    font_number = bpy.props.IntProperty()
    filterlist = []
    subdir = []

    def __init__(self):
        #get addon prefs
        dlist = bpy.data.fonts
        addon_preferences = get_addon_preferences()
                
        prefpath = os.path.abspath(bpy.path.abspath(addon_preferences))
        preffilter = os.path.join(prefpath, "fontselector_filter")
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list

        #clean unused
        if len(dlist) > 0:
            bpy.ops.fontselector.remove_unused()

        #check if external folder exist and create it if not
        create_dir(prefpath)

        #clear collection
        clear_collection(fontlist)
        
        #get filters
        if os.path.isdir(prefpath) == True :
            if os.path.isfile(preffilter) == True :
                with open(preffilter, 'r', newline='') as csvfile :
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1=str(l).replace("[", "")
                        l2=l1.replace("]", "")
                        l3=l2.replace("'", "")
                        l4=l3.replace('"', "")
                        self.filterlist.append(l4)

    def modal(self, context, event):
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefpath = os.path.abspath(bpy.path.abspath(addon_preferences))
        preffav = os.path.join(prefpath, "fontselector_favorites")
        prefflist = os.path.join(prefpath, "fontselector_fontlist")
        dupelist = []

        idx = 0

        chk=0
        chk2=0

        for fp in fplist :
            path = os.path.abspath(bpy.path.abspath(fp.folderpath))
            if fp.folderpath!="" :
                if os.path.isdir(path)==True:
                    chk=1
                    nbfile=0
                    nbft=0
                    for dirpath, dirnames, files in os.walk(path):
                        for f3 in files:
                            exte=os.path.splitext(f3)[1]
                            if any(exte==ext for ext in extensions):
                                nbfile=nbfile+1
                        for f2 in os.listdir(dirpath):
                            filename, file_extension = os.path.splitext(f2)
                            if any(file_extension==ext for ext in extensions) and dirpath not in subdir:
                                self.subdir.append(dirpath)
                    for d in self.subdir:
                        for file in os.listdir(d):
                            filename, file_extension = os.path.splitext(file)
                            #mac exception for corrupted font
                            if file not in self.filterlist:
                                if any(file_extension==ext for ext in extensions):
                                    chk2=1
                                    chk3=0
                                    for font in bpy.data.fonts:
                                        fname=os.path.basename(os.path.abspath(bpy.path.abspath(font.filepath)))
                                        if os.path.join(d, file)==os.path.abspath(bpy.path.abspath(font.filepath)) or file==fname:
                                            chk3=1
                                    if chk3==0:
                                        try:
                                            nbft=nbft+1
                                            bpy.data.fonts.load(filepath=os.path.join(d, file))
                                            print(str(nbft)+"/"+str(nbfile)+" fonts treated --- "+file+" imported")
                                        except RuntimeError:
                                            nbft=nbft+1
                                            self.filterlist.append(file)
                                            print(str(nbft)+"/"+str(nbfile)+" fonts treated --- "+file+" corrupted, filtered out")
                            
        if chk==1 and chk2==1:      
            nfile = open(prefflist, "w")
            for f in bpy.data.fonts:
                chkd=0
                for d in dupelist:
                    if os.path.abspath(bpy.path.abspath(f.filepath))==d:
                        chkd=1
                if chkd==0:
                    nfpath=os.path.abspath(bpy.path.abspath(f.filepath))
                    nfile.write(f.name+" || "+nfpath+' || '+os.path.basename(os.path.dirname(nfpath))+"\n")
                    dupelist.append(nfpath)
                if f.users==0:
                    bpy.data.fonts.remove(f, do_unlink=True)
            nfile.close()
            if os.path.isfile(self.prefflist)==True:
                bpy.ops.fontselector.load_fontlist()
                info='Font Selector Warning : Font List refreshed'
                print(info)
                self.report({'INFO'}, info)
            if os.path.isfile(preffav)==True:
                load_favorites()
                
        elif chk==0:
            info = 'No valid Font Folder, check Preferences'
            self.report({'ERROR'}, info)  
            
        elif chk2==0:
            info = 'No valid Font in Folders, check Preferences'
            self.report({'ERROR'}, info)
        
        if self.font_number == idx :
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        addon_preferences = get_addon_preferences()
        freq=addon_preferences.check_frequency
        wm = context.window_manager
        self._timer = wm.event_timer_add(freq, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print("Reload Images timer ended")