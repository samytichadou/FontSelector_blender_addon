import bpy
import os
import platform
import json

from bpy.app.handlers import persistent

from .addon_prefs import get_addon_preferences


# TODO If list changed, relink fonts


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
    if osys == "Linux":
        return [
            r"/usr/share/fonts", # Debian Ubuntu
            r"/usr/X11R6/lib/X11/fonts", # RH
            os.path.join(os.environ['HOME'], r".local/share/fonts"), # Fedora
            os.path.join(os.environ['HOME'], ".fonts"), # Debian Ubuntu
        ]
    elif osys == "Windows":
        return [
            # r"C:\Windows\Fonts",
            os.path.join(os.environ['windir'], "fonts"), # System wide install
            os.path.join(os.environ['LOCALAPPDATA'], r"\Microsoft\Windows\Fonts"), # User install
        ]
    elif osys == "Darwin":
        return [
            r"/Library/Fonts",
            r"/System/Library/Fonts",
        ]
    

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
                
                font_list.append(
                    {
                        "filepath" : os.path.join(root, file),
                        # TODO Read properly font file content to retrieve name...
                        "name" : filename,
                        "family" : "family",
                        "type" : "type",
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
        fonts.sort(key=lambda x: x['name'], reverse=False)      
        
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

    
@persistent
def startup_load_fonts(scene):
    
    datas = refresh_fonts_json()[0]
    
    reload_font_collections(datas)

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_load_fonts)

def unregister():
    bpy.app.handlers.load_post.remove(startup_load_fonts)
            
