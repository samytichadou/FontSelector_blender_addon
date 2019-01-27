'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {  
 "name": "Font Selector",  
 "author": "Samy Tichadou (tonton)",  
 "version": (2, 0),  
 "blender": (2, 7, 9),  
 "location": "Properties > Font > Font selection",  
 "description": "Select Fonts directly in the property panel",  
  "wiki_url": "https://github.com/samytichadou/FontSelector_blender_addon/wiki",  
 "tracker_url": "https://github.com/samytichadou/FontSelector_blender_addon/issues/new",  
 "category": "Properties"}


import bpy


# load and reload submodules
##################################

import importlib
from . import developer_utils

importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())


# IMPORT SPECIFICS
##################################


from .misc_functions import menu_export_favorites
from .startup_handler import fontselector_startup
from .properties import *
from .update_functions import update_favorite_filter, update_change_font, update_subdir_toggle


# register
##################################

import traceback

def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()
         
    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

    ### PROPS ###

    bpy.types.WindowManager.fontselector_list = \
        bpy.props.CollectionProperty(type = FontSelectorFontList)
    bpy.types.WindowManager.fontselector_sub = \
        bpy.props.CollectionProperty(type = FontSelectorFontSubs)
    bpy.types.TextCurve.fontselector_favs = \
        bpy.props.BoolProperty(default = False, update = update_favorite_filter,
                                description = "Toggle display only Favorite Fonts")
    bpy.types.TextCurve.fontselector_index = \
        bpy.props.IntProperty(update = update_change_font)
    bpy.types.TextCurve.fontselector_sub_index = \
        bpy.props.IntProperty()
    bpy.types.TextCurve.fontselector_use_sub = \
        bpy.props.BoolProperty(update = update_subdir_toggle, description = "Toggle display Subdirectory Mode")
    
    ### HANDLER ###

    bpy.app.handlers.load_post.append(fontselector_startup)
    
    ### EXPORT MENU ###

    bpy.types.INFO_MT_file_export.append(menu_export_favorites)

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))

    ### PROPS ###

    del bpy.types.WindowManager.fontselector_list
    del bpy.types.WindowManager.fontselector_sub
    del bpy.types.TextCurve.fontselector_favs
    del bpy.types.TextCurve.fontselector_index
    del bpy.types.TextCurve.fontselector_sub_index
    del bpy.types.TextCurve.fontselector_use_sub
    
    ### HANDLER

    bpy.app.handlers.load_post.remove(fontselector_startup)
    
    ### EXPORT MENU ###

    bpy.types.INFO_MT_file_export.remove(menu_export_favorites)