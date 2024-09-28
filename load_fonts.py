import bpy
import os
import platform
import json
from fontTools import ttLib

from bpy.app.handlers import persistent

from .addon_prefs import get_addon_preferences


# Font format
font_formats = [
    ".otf",
    ".ttf",
]


def get_os_folders(debug):
    # Linux: Linux
    # Windows: Windows
    # Mac: Darwin
    osys = platform.system()
    user_path = os.path.expanduser( '~' )
    # user_path = os.environ["HOME"]
    
    if debug:
        print("FONTSELECTOR --- Checking OS")
    
    if osys == "Linux":
        if debug:
            print("FONTSELECTOR --- OS : Linux")
        
        return [
            r"/usr/share/fonts", # Debian Ubuntu
            r"/usr/local/share/fonts", # Debian Ubuntu
            r"/usr/X11R6/lib/X11/fonts", # RH
            os.path.join(user_path, r".local/share/fonts"), # Fedora
            os.path.join(user_path, r".fonts"), # Debian Ubuntu
        ]
    elif osys == "Windows":
        if debug:
            print("FONTSELECTOR --- OS : Windows")
        
        return [
            r"C:\Windows\Fonts",
            os.path.join(user_path, "fonts"), # System wide install
            os.path.join(user_path, r"Microsoft\Windows\Fonts"), # User install
        ]
    elif osys == "Darwin":
        if debug:
            print("FONTSELECTOR --- OS : Mac")
        
        return [
            os.path.join(user_path, r"Library/Fonts/"),
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
    

def get_font_list_from_folder(
    folderpath,
    debug,
):
    
    font_list = []
    
    # Invalid folder
    if not os.path.isdir(folderpath):
        if debug:
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


def reload_favorites(debug):
    
    if debug:
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
        

def refresh_fonts_json(
    debug,
    force_refresh = False,
):
    
    size = 0
    folders = []
    
    for folderpath in get_os_folders(debug):
        
        # Invalid folder
        if not os.path.isdir(folderpath):
            if debug:
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
            
            if debug:
                print(f"FONTSELECTOR --- Refreshing : {folderpath}")
            
            fonts.extend(
                get_font_list_from_folder(folderpath, debug)
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
    
    print("FONTSELECTOR --- No change, keeping fonts datas")
    
    return datas, False


def reload_font_collections(
    font_datas,
    debug,
):
    
    if debug:
        print("FONTSELECTOR --- Reloading collections")
    
    props = bpy.context.window_manager.fontselector_properties.fonts
    
    props.clear()
    
    for font in font_datas["fonts"]:
        
        bold = italic = bold_italic = ""
        
        # Get Bold-Italic if exists
        for f in font_datas["fonts"]:
            
            if f["family"] == font["family"]:
                if f["type"] == "Bold":
                    bold = f["name"]
                elif f["type"] == "Italic":
                    italic = f["name"]
                elif f["type"] == "Bold Italic":
                    bold_italic = f["name"]
        
        # Store Properties
        new = props.add()
        new.filepath = font["filepath"]
        new.name = font["name"]
        new.font_family = font["family"]
        new.font_type = font["type"]
        
        new.bold_font_name = bold
        new.italic_font_name = italic
        new.bold_italic_font_name = bold_italic


def get_font_from_name(font_name):
    idx = 0
    for font in bpy.context.window_manager.fontselector_properties.fonts:
        if font.name == font_name:
            return font, idx
        idx += 1
    return None, None


def relink_font_objects(debug):
    
    if debug:
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
            
            if debug:
                print(f"FONTSELECTOR --- Unable to relink : {props.font_name}")
            
            props.font_index = -1
            continue
        
        # Reload old missing font
        if props.font_index == -1:
            try:
                bpy.data.fonts[font.name].filepath = font.filepath
            except KeyError:
                if debug:
                    print(f"FONTSELECTOR --- Unable to reload : {font.filepath}")
                else:
                    pass
            
        props.font_index = index
    
    font_props.no_callback = False
                    
    
@persistent
def startup_load_fonts(scene):
    
    debug = get_addon_preferences().debug
    
    datas, change = refresh_fonts_json(debug)
    
    reload_font_collections(datas, debug)
    
    relink_font_objects(debug)
    
    reload_favorites(debug)

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_load_fonts)

def unregister():
    bpy.app.handlers.load_post.remove(startup_load_fonts)
            
