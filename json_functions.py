import bpy
import json

def create_json_file(datas, path) :
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=True)

def initialize_json_datas () :
    datas = {}
    datas['size'] = []
    datas['fonts'] = []
    datas['subdirectories'] = []
    datas['filtered'] = []
    return datas

def add_fonts_json(datas, font_list) :
    #datas = {}
    #datas['font'] = []
    for font in font_list :
        datas['fonts'].append({
            "name" : font[0],
            "filepath" : font[1],
            "subdirectory" : font[2]
        })
    return datas

def add_subdirectories_json(datas, subdir_list) :
    for sub in subdir_list :
        datas['subdirectories'].append({
            "name" : sub[0],
            "filepath" : sub[1]
        })
    return datas

def add_size_json(datas, size) :
    datas['size'] = size
    
    return datas

#read json
def read_json(filepath):
    with open(filepath, "r") as read_file:
        datas = json.load(read_file)
    return datas