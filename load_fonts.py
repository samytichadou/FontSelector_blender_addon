import bpy
import os
import platform
import json
from fontTools import ttLib

from bpy.app.handlers import persistent

from .addon_prefs import get_addon_preferences


# TODO use /etc/fonts/font.conf on linux to get font dirs ?


# Font format
font_formats = [
    ".otf",
    ".ttf",
]


def get_os_folders():
    # Linux: Linux
    # Windows: Windows
    # Mac: Darwin
    osys = platform.system()
    user_path = os.path.expanduser( '~' )
    # user_path = os.environ["HOME"]
    
    print("FONTSELECTOR --- Checking OS")
    
    if osys == "Linux":
        print("FONTSELECTOR --- OS : Linux")
        
        return [
            r"/usr/share/fonts", # Debian Ubuntu
            r"/usr/local/share/fonts", # Debian Ubuntu
            r"/usr/X11R6/lib/X11/fonts", # RH
            os.path.join(user_path, r".local/share/fonts"), # Fedora
            os.path.join(user_path, r".fonts"), # Debian Ubuntu
        ]
    elif osys == "Windows":
        print("FONTSELECTOR --- OS : Windows")
        
        return [
            # r"C:\Windows\Fonts",
            os.path.join(os.environ['windir'], "fonts"), # System wide install
            os.path.join(os.environ['LOCALAPPDATA'], r"\Microsoft\Windows\Fonts"), # User install
        ]
    elif osys == "Darwin":
        print("FONTSELECTOR --- OS : Mac")
        
        return [
            os.path.join(user_path, r"/Library/Fonts/"),
            r"/Library/Fonts",
            r"/System/Library/Fonts",
            r"/System Folder/Fonts/",
            r"/Network/Library/Fonts/",
        ]
    
    print("FONTSELECTOR --- OS not supported")
    

def get_folder_size(folderpath):
    
    size = 0
    
    for file in os.listdir(folderpath):
        size += os.path.getsize(
            os.path.join(folderpath, file)
        )
            
    return size
    

def get_font_list_from_folder(folderpath):
    
    font_list = []
    
    # Invalid folder
    if not os.path.isdir(folderpath):
        print(f"FONTSELECTOR --- Invalid folder - {folderpath}")
        return font_list
    
    # Check for font files
    for root, dirs, files in os.walk(folderpath):
        
        for file in files:
        
            filename, ext = os.path.splitext(file)
            
            if ext in font_formats:
                filepath = os.path.join(root, file)
                
                font = ttLib.TTFont(filepath)
                
                font_list.append(
                    {
                        "filepath" : filepath,
                        "name" : font['name'].getDebugName(4),
                        "family" : font['name'].getDebugName(1),
                        "type" : font['name'].getDebugName(2),
                    }
                )
                
    return font_list
            

def read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset


def write_json_file(datas, path):
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=False)


def get_preferences_folder():
    folder = bpy.path.abspath(get_addon_preferences().preferences_folder)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


def get_json_filepath():
    return os.path.join(
        get_preferences_folder(),
        "fonts_datas.json",
    )


def get_existing_datas():
    filepath = get_json_filepath()
    if not os.path.isfile(filepath):
        return None
    return read_json(filepath)


def get_favorite_json_filepath():
    return os.path.join(
        get_preferences_folder(),
        "favorite_datas.json",
    )


def get_existing_favorite_datas():
    filepath = get_favorite_json_filepath()
    if not os.path.isfile(filepath):
        return {
            "favorites" : []
        }
    return read_json(filepath)


def reload_favorites():
    
    print("FONTSELECTOR --- Loading favorites")
    
    datas = get_existing_favorite_datas()
    props = bpy.context.window_manager.fontselector_properties
    
    props.no_callback = True
    
    for f in datas["favorites"]:
        
        for font in props.fonts:
            if font.name == f:
                font.favorite = True
                break
            
    props.no_callback = False
        

def refresh_fonts_json(force_refresh = False):
    
    size = 0
    folders = []
    
    for folderpath in get_os_folders():
        
        # Invalid folder
        if not os.path.isdir(folderpath):
            print(f"FONTSELECTOR --- Invalid folder - {folderpath}")
            continue
            
        size += get_folder_size(folderpath)
        folders.append(folderpath)
        
    # TODO Add custom folders
        
    datas = get_existing_datas()
    
    # Refresh
    if datas is None\
    or datas["size"] != size\
    or force_refresh:
        
        print("FONTSELECTOR --- Refreshing fonts datas")
        
        fonts = []
        
        for folderpath in folders:
            
            print(f"FONTSELECTOR --- Refreshing : {folderpath}")
            
            fonts.extend(
                get_font_list_from_folder(folderpath)
            )
        
        # Alphabetical order
        fonts.sort(key=lambda x: x['name'].lower(), reverse=False)
        
        datas = {
            "size" : size,
            "fonts" : fonts
        }
        
        # Write json file
        write_json_file(
            datas,
            get_json_filepath(),
        )
        
        return datas, True
    
    print("FONTSELECTOR --- Keeping fonts datas")
    
    return datas, False


def reload_font_collections(font_datas):
    
    print("FONTSELECTOR --- Reloading collections")
    
    props = bpy.context.window_manager.fontselector_properties.fonts
    
    props.clear()
    
    for font in font_datas["fonts"]:
        new = props.add()
        new.filepath = font["filepath"]
        new.name = font["name"]
        new.font_family = font["family"]
        new.font_type = font["type"]


def get_font_from_name(font_name):
    idx = 0
    for font in bpy.context.window_manager.fontselector_properties.fonts:
        if font.name == font_name:
            return font, idx
        idx += 1
    return None, None


def relink_font_objects():
    
    print("FONTSELECTOR --- Relinking font objects")
    
    obj_list = []
    
    # Get text curves
    for obj in bpy.data.curves:
        obj_list.append(obj)
    
    # Get text strips
    for scn in bpy.data.scenes:
        if scn.sequence_editor:
            for strip in scn.sequence_editor.sequences_all:
                if strip.type == "TEXT":
                    obj_list.append(strip)
    
    # Prevent index callback
    font_props = bpy.context.window_manager.fontselector_properties
    font_props.no_callback = True
        
    # Relink
    for obj in obj_list:
        
        props = obj.fontselector_object_properties
        
        font, index = get_font_from_name(props.font_name)
        
        # Missing font
        if font is None:
            print(f"FONTSELECTOR --- Unable to relink : {props.font_name}")
            
            props.font_index = -1
            continue
        
        # Reload old missing font
        if props.font_index == -1:
            try:
                bpy.data.fonts[font.name].filepath = font.filepath
            except KeyError:
                print(f"FONTSELECTOR --- Unable to reload : {font.filepath}")
            
        props.font_index = index
    
    font_props.no_callback = False
                    
    
@persistent
def startup_load_fonts(scene):
    
    datas, change = refresh_fonts_json()
    
    reload_font_collections(datas)
    
    relink_font_objects()
    
    reload_favorites()

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_load_fonts)

def unregister():
    bpy.app.handlers.load_post.remove(startup_load_fonts)
            
