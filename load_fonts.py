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
    

def get_folder_size(start_path):
    
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    return total_size
    

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


def reorder_dict_key(
    dict,
    key,
    specific_order = [],
):

    # Alphabetical order
    s = sorted(dict, key=lambda x: x[key])

    if not specific_order:
        return s

    # Specific order
    new_list = []
    for font in s:
        if font[key] not in specific_order:
            new_list.append(font)
            s.remove(font)

    data = {x[key]: x for x in s}
    for i in reversed(range(len(specific_order))):
        try:
            new_list.insert(0, data[specific_order[i]])
        except KeyError:
            pass

    return new_list


def get_font_families_from_folder(
    datas,
    folderpath,
    debug,
):
    
    # Invalid folder
    if not os.path.isdir(folderpath):
        if debug:
            print(f"FONTSELECTOR --- Invalid folder - {folderpath}")
        return datas
    
    # Check for font files
    for root, dirs, files in os.walk(folderpath):
        
        for file in files:
        
            filename, ext = os.path.splitext(file)
            
            if ext in font_formats:

                filepath = os.path.join(root, file)
                font = ttLib.TTFont(filepath)
                family = font['name'].getDebugName(1)
                
                font_datas = {
                    "filepath" : filepath,
                    "name" : font['name'].getDebugName(4),
                    "type" : font['name'].getDebugName(2),
                }
                
                try:
                    
                    f = datas["families"][family]

                    if debug:
                        print(f"FONTSELECTOR --- Font family found : {family}")
                        print(f"FONTSELECTOR --- Adding font : {font_datas['name']}")

                    
                    chk_dupe = False
                    for font in f:
                        if font["type"] == font_datas["type"]:
                            chk_dupe = True
                            if debug:
                                print(f"FONTSELECTOR --- Similar Fonts : {font['filepath']} - {filepath}")
                            break
                    
                    if not chk_dupe:
                        f.append(font_datas)
                        
                except KeyError:
                    
                    datas["families"][family] = [
                        font_datas,
                    ]

    return datas


def refresh_font_families_json(
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

    datas = get_existing_families_datas()

    # Refresh
    if datas is None\
    or datas["size"] != size\
    or force_refresh:

        print("FONTSELECTOR --- Refreshing families datas")

        datas = {
            "size" : size,
            "families" : {}
        }

        for folderpath in folders:

            if debug:
                print(f"FONTSELECTOR --- Refreshing : {folderpath}")

            datas = get_font_families_from_folder(
                datas,
                folderpath,
                debug,
            )

        # Alphabetical order
        datas["families"] = dict(sorted(datas["families"].items(), key=lambda item: item[0].lower()))

        # Sort fonts inside families
        for fam in datas["families"]:
            new_list = reorder_dict_key(
                datas["families"][fam],
                "type",
                ["Regular", "Bold", "Italic", "Bold Italic"],
            )
            datas["families"][fam] = new_list

        # Write json file
        fam_json = os.path.join(
            get_preferences_folder(),
            "families_datas.json",
        )
        write_json_file(
            datas,
            fam_json,
        )

        return datas, True

    print("FONTSELECTOR --- No change, keeping families datas")

    return datas, False


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

def get_families_json_filepath():
    return os.path.join(
        get_preferences_folder(),
        "families_datas.json",
    )


def get_existing_datas():
    filepath = get_json_filepath()
    if not os.path.isfile(filepath):
        return None
    return read_json(filepath)

def get_existing_families_datas():
    filepath = get_families_json_filepath()
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
        
        for family in props.font_families:
            if family.name == f:
                family.favorite = True
                break
            
    props.no_callback = False
        

def reload_font_families_collections(
    font_datas,
    debug,
):

    if debug:
        print("FONTSELECTOR --- Reloading families collections")

    props = bpy.context.window_manager.fontselector_properties.font_families

    props.clear()

    for family in font_datas["families"]:

        new_family = props.add()
        new_family.name = family

        multi_component = -1

        for font in font_datas["families"][family]:
            new_font = new_family.fonts.add()
            new_font.name = font["type"]
            new_font.filepath = font["filepath"]
            new_font.font_name = font["name"]

            if font["type"] in ["Regular", "Bold", "Italic", "Bold Italic"]:
                multi_component += 1

            if multi_component > 0:
                new_family.multi_component = True


def get_family_index_from_name(family_name):

    idx = 0
    for family in bpy.context.window_manager.fontselector_properties.font_families:
        if family.name == family_name:
            return idx
        idx += 1

    return None


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
    # font_props.no_callback = True
        
    # Relink
    for obj in obj_list:
        
        props = obj.fontselector_object_properties
        
        index = get_family_index_from_name(props.relink_family_name)
        
        # Missing family
        if index is None:
            
            if debug:
                print(f"FONTSELECTOR --- Unable to relink : {props.relink_family_name} - {props.relink_type_name}")
            
            props.family_index = -1
            continue
            
        # Relink
        props.family_index = index

        try:
            props.family_types = props.relink_type_name
        except TypeError:
            if debug:
                print(f"FONTSELECTOR --- Unable to relink : {props.relink_family_name} - {props.relink_type_name}")
            props.family_index = -1
    
    # font_props.no_callback = False
                    
    
@persistent
def startup_load_fonts(scene):
    
    debug = get_addon_preferences().debug

    # Reload families
    datas, change = refresh_font_families_json(debug)
    reload_font_families_collections(datas, debug)

    # Relink
    relink_font_objects(debug)

    # Reload favorites
    reload_favorites(debug)

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_load_fonts)

def unregister():
    bpy.app.handlers.load_post.remove(startup_load_fonts)
            
