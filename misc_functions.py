import bpy
import os

from .preferences import get_addon_preferences

from .global_variable import extensions

# suppress filepath
def fontselector_suppress_fp(index) :
    #get addon prefs
    addon_preferences = get_addon_preferences()
    fplist = addon_preferences.font_folders
    
    fplist.remove(index)
    #operator refresh fonts if list created

# export menu
def menu_export_favorites(self, context) :
    self.layout.operator('fontselector.export_favorites', text="Favorite Fonts export", icon='FILE_FONT')

# clear collection
def clear_collection(collection) :
        if len(collection)>=1:
            for i in range(len(collection)-1,-1,-1):
                collection.remove(i)

# absolute path
def absolute_path(path) :
        apath = os.path.abspath(bpy.path.abspath(path))
        return apath

# get size of folder and subdir in bytes
def get_size(folderpath) :
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folderpath):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# create directory if doesn't exist
def create_dir(dir_path) :
        if os.path.isdir(dir_path) == False :
                os.makedirs(dir_path)

# remove unused font datablocks
def remove_unused_font() :
        removed_fonts_count = 0
        for f in bpy.data.fonts :
            if f.users == 0 :
                removed_fonts_count += 1
                bpy.data.fonts.remove(f, do_unlink=True)
        return removed_fonts_count

# get all font files in dir and subdir
def get_all_font_files(base_dir) :
        font_files = []
        for (root, directories, filenames) in os.walk(base_dir) :
                for file in filenames :
                        extension = os.path.splitext(file)[1]
                        if any(extension == ext for ext in extensions) :
                                font_files.append(os.path.join(root, file))
        return font_files