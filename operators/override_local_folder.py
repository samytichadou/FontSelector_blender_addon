import bpy


from ..preferences import get_addon_preferences
from ..global_variable import json_font_folders
from ..global_messages import override_loaded_msg
from ..misc_functions import absolute_path, clear_collection, get_all_font_files

class FontSelectorOverrideFolder(bpy.types.Operator):
    bl_idname = "fontselector.override_folder"
    bl_label = "Toggle Override Folder"
    bl_description = "Use the Override Folder"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        wm = bpy.data.window_managers['WinMan']
        return wm.fontselector_folder_override != "" and not wm.fontselector_override
    
    def execute(self, context):
        collection_font_list = bpy.data.window_managers['WinMan'].fontselector_list
        collection_subdir_list = bpy.data.window_managers['WinMan'].fontselector_sub

        wm = bpy.data.window_managers['WinMan']
        override_folder = absolute_path(wm.fontselector_folder_override)

        fontpath_list, subdir_list = get_all_font_files(override_folder)

        # remove existing folder list
        clear_collection(collection_font_list)
        clear_collection(collection_subdir_list)

        # load fonts
        for font in fontpath_list :
            try :
                # load font in blender datas to get name
                datafont = bpy.data.fonts.load(filepath = font[0])
                # add to font list
                newfont = collection_font_list.add()
                newfont.name = datafont.name
                newfont.filepath = font[0]
                newfont.subdirectory = font[1]
                # delete font
                bpy.data.fonts.remove(datafont, do_unlink=True)
            except RuntimeError :
                pass

        # toggle override prop to false
        bpy.data.window_managers['WinMan'].fontselector_override = True

        # report user
        self.report({'INFO'}, override_loaded_msg)
            
        return {'FINISHED'}