import bpy
import os

from .properties import FontFolders
from .global_variable import win_folder,mac_folder,linux_folder


addon_name = os.path.basename(os.path.dirname(__file__))

class FontSelectorAddonPrefs(bpy.types.AddonPreferences) :
    bl_idname = addon_name
    
    # UI
    row_number : bpy.props.IntProperty(
                    default = 5,
                    min = 3,
                    max = 50,
                    description = 'Number of rows by default of the Font List, also the minimum number of row'
                    )
    
    # FONT FOLDERS
    font_folders : bpy.props.CollectionProperty(type = FontFolders)
    
    # PREFS
    prefs_folderpath : bpy.props.StringProperty(
            name = "Preferences Folder Path",
            default = os.path.join(bpy.utils.user_resource('CONFIG'), "font_selector_prefs"),
            description = "Folder where Font Selector Preferences will be stored",
            subtype = "DIR_PATH"
            )

    # PROGRESS BAR
    progress_bar_color : bpy.props.FloatVectorProperty(
            name = "Progress Bar", 
            size = 3,
            min = 0.0,
            max = 1.0,
            default = [1, 1, 1],
            subtype = 'COLOR'
            )
    
    progress_bar_background_color : bpy.props.FloatVectorProperty(
            name = "Background", 
            size = 3,
            min = 0.0,
            max = 1.0,
            default = [0.2, 0.2, 0.2],
            subtype = 'COLOR'
            )

    progress_bar_size : bpy.props.IntProperty(
            name = "Progress Bar Size", 
            min = 1,
            max = 100,
            default = 10
            )

    # DEBUG
    debug_value : bpy.props.BoolProperty(
            name = "Debug Toggle", 
            default = False
            )
    
    # STARTUP BEHAVIOR
    startup_check_behavior : bpy.props.EnumProperty(
        name = "Startup Check", 
        default = 'AUTOMATIC_UPDATE',
        items = (
            ('AUTOMATIC_UPDATE', "Auto Update", "Auto Check of Font Folder on startup, if Changes, Blender will refresh the Font List"),
            ('MESSAGE_ONLY', "Message Only", "Auto Check of Font Folder on startup, if Changes, Blender will show a message"),
            ('MANUAL', "Manual", "No Startup Check, Font List has to be manually refreshed"),
            ))
            

    def draw(self, context) :
        layout = self.layout
        font_list = self.font_folders
        wm = context.window_manager
        
        temp_list = [f.folderpath for f in font_list]
        for f in wm.fontselector_defaultfolders: temp_list.append(f.folderpath)
        
        dupelist = [x for x in temp_list if temp_list.count(x) >= 2]

        col = layout.column(align = False)
        
        # default font folders
        box = col.box()
        row = box.row()
        row.label(text = wm.fontselector_os + " Default Font Folders", icon = "FILE_FOLDER")
        col2 = box.column(align=True)
        for folder in wm.fontselector_defaultfolders:
            row = col2.row()
            row.label(text = folder.folderpath)
        row = box.row()
        if context.window_manager.fontselector_isrefreshing:
            row.operator('fontselector.refresh_toggle', text = "Cancel", icon = 'CANCEL')
        else:
            row.operator('fontselector.refresh_toggle', icon = 'FILE_REFRESH')

        # font folders
        box = col.box()
        row = box.row(align = True)
        row.label(text = "Custom Font Folders", icon = 'FILE_FONT')
        if len(dupelist) > 0 :
            row.label(text = 'Dupe Warning', icon = 'ERROR')

        row = box.row(align = True)
        row.operator("fontselector.add_fp", text = "Add", icon = 'ADD')
        row.separator()
        row.operator("fontselector.save_fpprefs", text = 'Save', icon = 'DISK_DRIVE')
        row.operator("fontselector.load_fpprefs", text = 'Load', icon = 'LOOP_BACK')

        idx = 0
        for i in font_list :
            sub_box = box.box()
            row = sub_box.row()
            row.prop(i, "folderpath")
            if i.folderpath in dupelist:
                row.label(icon = 'ERROR')
            op = row.operator("fontselector.suppress_fp", text = '', icon = 'X', emboss = False)
            op.index = idx
            idx += 1
        
        # startup behavior
        box = col.box()
        row = box.row(align = True)
        row.label(icon = 'BLENDER')
        row.prop(self, 'startup_check_behavior', text = "On startup")

        # progress bar
        box = col.box()
        row = box.row(align = True)
        row.label(text = "Progress Bar", icon = 'TIME')
        row.prop(self, 'progress_bar_color', text = '')
        row.prop(self, 'progress_bar_size', text = 'Size')
        row.prop(self, 'progress_bar_background_color')
        
        # font list row
        box = col.box()
        row = box.row(align = True)
        row.label(text = 'Font list rows', icon = 'COLLAPSEMENU')
        row.prop(self, 'row_number', text = '')
        
        # extra settings
        box = col.box()
        row = box.row(align = True)
        row.label(text = "Extra Settings", icon = 'MODIFIER_ON')
        row.prop(self, 'debug_value')
        row = box.row(align = True)
        row.prop(self, 'prefs_folderpath', text = 'Preferences Path')
            

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)