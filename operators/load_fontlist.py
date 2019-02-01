import bpy
import os


from ..preferences import get_addon_preferences
from ..global_variable import json_file
from ..global_messages import refresh_msg
from ..misc_functions import absolute_path, clear_collection
from ..functions.load_json import load_json_font_file
from ..functions.load_favorites import *

from ..update_functions import update_change_font


class FontSelectorLoadFPPrefs(bpy.types.Operator):
    bl_idname = "fontselector.load_fontlist"
    bl_label = "Load Font List"
    bl_description = "Load existing Font List"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        addon_preferences = get_addon_preferences()
        prefs = absolute_path(addon_preferences.prefs_folderpath)
        json_path = os.path.join(prefs, json_file)
        return os.path.isfile(json_path)
    
    def execute(self, context):
        addon_preferences = get_addon_preferences()
        prefpath = absolute_path(addon_preferences.prefs_folderpath)
        json_path = os.path.join(prefpath, json_file)

        collection_font_list = bpy.data.window_managers['WinMan'].fontselector_list
        collection_subdir_list = bpy.data.window_managers['WinMan'].fontselector_sub

        # remove existing folder list
        clear_collection(collection_font_list)
        clear_collection(collection_subdir_list)

        # load json
        load_json_font_file(json_path, collection_font_list, collection_subdir_list)

        # load favorites
        load_favorites()

        # update font in viewport
        update_change_font(self, context)

        # toggle override prop to false
        bpy.data.window_managers['WinMan'].fontselector_override = False

        # report user
        self.report({'INFO'}, refresh_msg)
            
        return {'FINISHED'}