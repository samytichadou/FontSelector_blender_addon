import bpy
import os
import platform

from bpy.app.handlers import persistent


# Font format
font_formats = [
    ".otf",
    ".ttf",
]


def get_os_folders():
    # Linux: Linux
    # Mac: Darwin
    # Windows: Windows
    os = platform.system()
    if os == "Linux":
        return [
            r"/usr/share/fonts",
        ]
    elif os == "Windows":
        return [
            r"C:\Windows\Fonts",
        ]
    elif os == "Darwin":
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
    
    for root, dirs, files in os.walk(folderpath):
        
        for file in files:
        
            ext = os.path.splitext(file)[1]
            
            if ext in font_formats:
                
                font_list.append(os.path.join(root, file))
                
    return font_list
            

def refresh_font_folder(folderpath):
    
    # TODO Check if size has changed
    folder_size = get_folder_size(folderpath)
    
    if True :
        font_list = get_font_list_from_folder(folderpath)
        
    # TODO Store new file and list in json
        
    print(folder_size)
    print(font_list)
    

@persistent
def startup_load_fonts(scene):
    
    print("FONTSELECTOR --- Loading fonts")
    
    for folderpath in get_os_folders():
        
        print(f"FONTSELECTOR --- Loading : {folderpath}")
        refresh_font_folder(folderpath)

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_load_fonts)

def unregister():
    bpy.app.handlers.load_post.remove(startup_load_fonts)
            
