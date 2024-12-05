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


# IMPORT
##################################

from . import   (
    addon_prefs,
    properties,
    load_fonts,
    ui_list_single_font,
    ui_list_family_font,
    gui,
    reload_operator,
    reveal_file_operator,
    load_font_family_operator,
    switch_font_operator,
)


# register
##################################

def register():
    properties.register()
    addon_prefs.register()
    load_fonts.register()
    ui_list_single_font.register()
    ui_list_family_font.register()
    gui.register()
    reload_operator.register()
    reveal_file_operator.register()
    load_font_family_operator.register()
    switch_font_operator.register()

def unregister():
    properties.unregister()
    addon_prefs.unregister()
    load_fonts.unregister()
    ui_list_single_font.unregister()
    ui_list_family_font.unregister()
    gui.unregister()
    reload_operator.unregister()
    reveal_file_operator.unregister()
    load_font_family_operator.unregister()
    switch_font_operator.unregister()
