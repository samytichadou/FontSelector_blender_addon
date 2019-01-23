import bpy

from ..json_functions import read_json

def load_json_font_file(json_file, font_collection, subdir_collection) :
    datas = read_json(json_file)

    # load fonts
    for font in datas['fonts'] :
        newfont = font_collection.add()
        newfont.name = font['name']
        newfont.filepath = font['filepath']
        newfont.subdirectory = font['subdirectory']

    # load subdirs
    for subdir in datas['subdirectories'] : 
        newsubdir = subdir_collection.add()
        newsubdir.name = subdir['name']
        newsubdir.filepath = subdir['filepath']