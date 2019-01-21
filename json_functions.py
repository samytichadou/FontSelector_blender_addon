import bpy
import json

def create_clip_json(path, data) :
    with open(path, "w") as write_file :
        json.dump(data, write_file)

def format_strip_infos(font) :
    datas = {
        "fonts": [{
            "name": font.name,
            "filepath": font.filepath,
        }]
    }
    return datas

#read json
def read_json(filepath):
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    return data