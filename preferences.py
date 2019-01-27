import bpy
import os

from .properties import FontFolders

addon_name = os.path.basename(os.path.dirname(__file__))

class FontSelectorAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    row_number = bpy.props.IntProperty(
                    default=5,
                    min=3,
                    max=50,
                    description='Number of rows by default of the Font List, also the minimum number of row'
                    )
    
    font_folders = bpy.props.CollectionProperty(type=FontFolders)
    
    prefs_folderpath = bpy.props.StringProperty(
            name="Preferences Folder Path",
            default=os.path.join(bpy.utils.user_resource('CONFIG'), "font_selector_prefs"),
            description="Folder where Font Selector Preferences will be stored",
            subtype="DIR_PATH",
            )
            
    prefs_filter = bpy.props.StringProperty(
            name="Filtered Font",
            default='',
            description="Font to filter",
            )
            
    prefs_show_subdir = bpy.props.BoolProperty(
            name="Show Font Subdirectory",
            default=False,
            description="If enabled, Font subdirectory will be shown in the Font list",
            )

    # progress bar
    progress_bar_color = bpy.props.FloatVectorProperty(
            name = "Progress Bar Color", 
            size = 4,
            min=0.0,
            max=1.0,
            default=[1, 1, 1, 1],
            subtype='COLOR'
            )

    progress_bar_size = bpy.props.IntProperty(
            name = "Progress Bar Size", 
            min=1,
            max=100,
            default=10
            )

    # debug
    debug_value = bpy.props.BoolProperty(
            name = "Debug Toggle", 
            default = False
            )
    
    # handler behavior
    startup_check_behavior = bpy.props.EnumProperty(
        name = "Startup Check", 
        default = 'AUTOMATIC_UPDATE',
        items=(
            ('AUTOMATIC_UPDATE', "Auto Update", "Auto Check of Font Folder on startup, if Changes, Blender will refresh the Font List"),
            ('MESSAGE_ONLY', "Message Only", "Auto Check of Font Folder on startup, if Changes, Blender will show a message"),
            ('MANUAL', "Manual", "No Startup Check, Font List has to be manually refreshed"),
            ))
            
    def draw(self, context):
        layout = self.layout
        list=self.font_folders
        dupelist=[]
        
        for i in list:
            dupelist.append(i.folderpath)
        dlist=[x for x in dupelist if dupelist.count(x) >= 2]
                
        row=layout.row(align=True)
        row.label(icon='SCRIPTWIN')
        row.prop(self, 'prefs_folderpath', text='External Preferences Path')

        row=layout.row(align=True)
        row.label("Startup")
        row.prop(self, 'startup_check_behavior')

        row=layout.row(align=True)
        row.label("Progress Bar")
        row.prop(self, 'progress_bar_color', text='')
        row.prop(self, 'progress_bar_size')

        row=layout.row(align=True)
        row.label("Development")
        row.prop(self, 'debug_value')
        
        row=layout.row(align=True)
        row.label('Number of Font list rows', icon='COLLAPSEMENU')
        row.prop(self, 'row_number', text='')
        
        row=layout.row(align=True)
        row.label('Subdirectories', icon='FILESEL')
        row.prop(self, 'prefs_show_subdir', text='Show Font subdirectories')
        
        row=layout.row(align=True)
        row.label('Add Font Filter', icon='FILTER')
        row.prop(self, 'prefs_filter', text='')
        row.operator('fontselector.add_filtered', text='', icon='ZOOMIN')
        
        row=layout.row()
        row.label("Font Folders", icon='FILE_FONT')
        if len(dlist)>0:
            row.label('Dupe Warning', icon='ERROR')
        row.operator("fontselector.add_fp", text="Add Font Folder", icon='ZOOMIN')
        row.operator("fontselector.save_fpprefs", text='', icon='DISK_DRIVE')
        row.operator("fontselector.load_fpprefs", text='', icon='LOAD_FACTORY')
        
        idx=-1
        for i in list:
            idx=idx+1
            box=layout.box()
            row=box.row()
            row.prop(i, "folderpath")
            if i.folderpath in dlist:
                row.label(icon='ERROR')
            op=row.operator("fontselector.suppress_fp", text='', icon='X', emboss=False)
            op.index=idx
            

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.user_preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)