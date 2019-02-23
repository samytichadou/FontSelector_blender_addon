# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 3
#  of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Font Selector",
    "author": "Samy Tichadou (tonton)",
    "version": (1, 26),
    "blender": (2, 80, 0),
    "location": "Properties > Font > Font selection",
    "description": "Select Fonts directly in the property panel",
    "wiki_url": "https://github.com/samytichadou/FontSelector_blender_addon/wiki",
    "tracker_url": "https://github.com/samytichadou/FontSelector_blender_addon/issues/new",
    "category": "Properties"}

import bpy
import os
import csv
import shutil
from bpy_extras.io_utils import ExportHelper
from bpy.app.handlers import persistent


#######################################################################
### update ###
#######################################################################

# update change font
def update_change_font(self, context):
    bpy.ops.fontselector.change()


# update save favorites
def update_save_favorites(self, context):
    active = bpy.context.active_object
    if active is not None:
        if active.type == 'FONT':
            bpy.ops.fontselector.save_favorites()


# update list for favorite filter
def update_favorite_filter(self, context):
    bpy.ops.fontselector.filter_favorites()


# update list for subdir filter
def update_subdir_filter(self, context):
    bpy.ops.fontselector.filter_subdirfonts()


# update lists when toggling subdir
def update_subdir_toggle(self, context):
    active = bpy.context.active_object
    if active is not None:
        if active.type == 'FONT':
            bpy.ops.fontselector.filter_favorites()


#######################################################################
### addon collections ###
#######################################################################

# Create custom property group
class FontSelectorFontList(bpy.types.PropertyGroup):
    """name = StringProperty() """
    filepath = bpy.props.StringProperty(name="filepath")
    missingfont = bpy.props.BoolProperty(name="missingfont", default=False)
    favorite = bpy.props.BoolProperty(name="favorite", default=False, update=update_save_favorites,
                                      description="Mark/Unmark as Favorite Font")
    subdirectory = bpy.props.StringProperty(name="subdirectory")


class FontSelectorFontSubs(bpy.types.PropertyGroup):
    '''name = StringProperty() '''


class FontFolders(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    folderpath = bpy.props.StringProperty(
        name="Folder path",
        description="Folder where CatHide Presets will be stored",
        subtype="DIR_PATH",
    )


#######################################################################
### addon preferences ###
#######################################################################

class FontSelectorAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

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

    def draw(self, context):
        layout = self.layout
        list = self.font_folders
        dupelist = []

        for i in list:
            dupelist.append(i.folderpath)
        dlist = [x for x in dupelist if dupelist.count(x) >= 2]

        row = layout.row(align=True)
        row.label(icon='PREFERENCES')
        row.prop(self, 'prefs_folderpath', text='External Preferences Path')

        row = layout.row(align=True)
        row.label(text='Number of Font list rows', icon='COLLAPSEMENU')
        row.prop(self, 'row_number', text='')

        row = layout.row(align=True)
        row.label(text='Subdirectories', icon='FILE_FOLDER')
        row.prop(self, 'prefs_show_subdir', text='Show Font subdirectories')

        row = layout.row(align=True)
        row.label(text='Add Font Filter', icon='FILTER')
        row.prop(self, 'prefs_filter', text='')
        row.operator('fontselector.add_filtered', text='', icon='ADD')

        row = layout.row()
        row.label(text="Font Folders", icon='FILE_FONT')
        if len(dlist) > 0:
            row.label(text="Dupe Warning", icon='ERROR')
        row.operator("fontselector.add_fp", text="Add Font Folder", icon='ADD')
        row.operator("fontselector.save_fpprefs", text='', icon='DISK_DRIVE')
        row.operator("fontselector.load_fpprefs", text='', icon='LOOP_BACK')

        idx = -1
        for i in list:
            idx = idx + 1
            box = layout.box()
            row = box.row()
            row.prop(i, "folderpath")
            if i.folderpath in dlist:
                row.label(icon='ERROR')
            op = row.operator("fontselector.suppress_fp", text='', icon='X', emboss=False)
            op.index = idx


#######################################################################
### addon operators ###
#######################################################################

# get addon preferences
def get_addon_preferences():
    addon_preferences = bpy.context.preferences.addons[__name__].preferences
    return addon_preferences


# add filepath
class FontSelectorAddFP(bpy.types.Operator):
    bl_idname = "fontselector.add_fp"
    bl_label = ""
    bl_description = "Add Font Folder Path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders

        # Create font folder
        fplist.add()

        return {'FINISHED'}


# add filtered font
class FontSelectorAddFiltered(bpy.types.Operator):
    bl_idname = "fontselector.add_filtered"
    bl_label = ""
    bl_description = "Add Font to Filter"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        new = addon_preferences.prefs_filter
        return new != ''

    def execute(self, context):
        addon_preferences = get_addon_preferences()
        new = addon_preferences.prefs_filter
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        preffilter = os.path.join(prefpath, "fontselector_filter")

        filterlist = []

        # get filtered
        if os.path.isdir(prefpath) == True:
            if os.path.isfile(preffilter) == True:
                with open(preffilter, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1 = str(l).replace("[", "")
                        l2 = l1.replace("]", "")
                        l3 = l2.replace("'", "")
                        l4 = l3.replace('"', "")
                        filterlist.append(l4)

        # add new one
        chk = 0
        if new != "":
            for f in filterlist:
                if new == f:
                    chk = 1
            if chk == 0:
                filterlist.append(new)
            else:
                info = new + ' already in Filtered Fonts'
                self.report({'INFO'}, info)

        # create external file
        if len(filterlist) != 0 and chk == 0:
            if os.path.isdir(prefpath) == False:
                os.makedirs(prefpath)
            nfile = open(preffilter, "w")
            for f in filterlist:
                nfile.write(f + "\n")
            nfile.close()

            info = new + ' added to Filtered Fonts'
            self.report({'INFO'}, info)

            addon_preferences.prefs_filter = ""

        return {'FINISHED'}


# suppress filepath
def fontselector_suppress_fp(index):
    # get addon prefs
    addon_preferences = get_addon_preferences()
    fplist = addon_preferences.font_folders

    fplist.remove(index)
    # operator refresh fonts if list created


class FontSelectorSuppressFP(bpy.types.Operator):
    bl_idname = "fontselector.suppress_fp"
    bl_label = ""
    bl_description = "Suppress Font Filepath"
    bl_options = {'REGISTER', 'UNDO'}
    index = bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        return len(fplist) > 0

    def execute(self, context):
        fontselector_suppress_fp(self.index)
        return {'FINISHED'}


# refresh operator
class FontSelectorRefresh(bpy.types.Operator):
    bl_idname = "fontselector.refresh"
    bl_label = "Refresh List"
    bl_description = "Refresh Available Fonts from Font Folders\nOperation can take some time, see console for progression"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        return len(fplist) > 0 and prefs != ""

    def execute(self, context):
        # get addon prefs
        dlist = bpy.data.fonts
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        preffav = os.path.join(prefpath, "fontselector_favorites")
        prefflist = os.path.join(prefpath, "fontselector_fontlist")
        preffilter = os.path.join(prefpath, "fontselector_filter")
        prefsubdir = os.path.join(prefpath, "fontselector_subdir")
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        extlist = [".otf", ".otc", ".ttf", ".ttc", ".tte", ".pfb", ".dfont", ".OTF", ".OTC", ".TTF", ".TTC", ".TTE",
                   ".DFONT", ".PFB"]
        dupelist = []
        subdir = []
        filterlist = []

        # get filters
        if os.path.isdir(prefpath) == True:
            if os.path.isfile(preffilter) == True:
                with open(preffilter, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1 = str(l).replace("[", "")
                        l2 = l1.replace("]", "")
                        l3 = l2.replace("'", "")
                        l4 = l3.replace('"', "")
                        filterlist.append(l4)

        if len(dlist) > 0:
            bpy.ops.fontselector.remove_unused()

        # check if external folder exist and create it if not
        if os.path.isdir(prefpath) == False:
            os.makedirs(prefpath)

        # clear list
        if len(fontlist) >= 1:
            for i in range(len(fontlist) - 1, -1, -1):
                fontlist.remove(i)

        chk = 0
        chk2 = 0
        for fp in fplist:
            path = os.path.abspath(bpy.path.abspath(fp.folderpath))
            if fp.folderpath != "":
                if os.path.isdir(path) == True:
                    chk = 1
                    nbfile = 0
                    nbft = 0
                    for dirpath, dirnames, files in os.walk(path):
                        for f3 in files:
                            exte = os.path.splitext(f3)[1]
                            if any(exte == ext for ext in extlist):
                                nbfile = nbfile + 1
                        for f2 in os.listdir(dirpath):
                            filename, file_extension = os.path.splitext(f2)
                            if any(file_extension == ext for ext in extlist) and dirpath not in subdir:
                                subdir.append(dirpath)
                    for d in subdir:
                        for file in os.listdir(d):
                            filename, file_extension = os.path.splitext(file)
                            # mac exception for corrupted font
                            if file not in filterlist:
                                if any(file_extension == ext for ext in extlist):
                                    chk2 = 1
                                    chk3 = 0
                                    for font in bpy.data.fonts:
                                        fname = os.path.basename(os.path.abspath(bpy.path.abspath(font.filepath)))
                                        if os.path.join(d, file) == os.path.abspath(
                                                bpy.path.abspath(font.filepath)) or file == fname:
                                            chk3 = 1
                                    if chk3 == 0:
                                        try:
                                            nbft = nbft + 1
                                            bpy.data.fonts.load(filepath=os.path.join(d, file))
                                            print(str(nbft) + "/" + str(
                                                nbfile) + " fonts treated --- " + file + " imported")
                                        except RuntimeError:
                                            nbft = nbft + 1
                                            filterlist.append(file)
                                            print(str(nbft) + "/" + str(
                                                nbfile) + " fonts treated --- " + file + " corrupted, filtered out")

        if chk == 1 and chk2 == 1:
            nfile = open(prefflist, "w")
            for f in bpy.data.fonts:
                chkd = 0
                for d in dupelist:
                    if os.path.abspath(bpy.path.abspath(f.filepath)) == d:
                        chkd = 1
                if chkd == 0:
                    nfpath = os.path.abspath(bpy.path.abspath(f.filepath))
                    nfile.write(f.name + " || " + nfpath + ' || ' + os.path.basename(os.path.dirname(nfpath)) + "\n")
                    dupelist.append(nfpath)
                if f.users == 0:
                    bpy.data.fonts.remove(f, do_unlink=True)
            nfile.close()
            if os.path.isfile(prefflist) == True:
                bpy.ops.fontselector.load_fontlist()
                info = 'Font Selector Warning : Font List refreshed'
                print(info)
                self.report({'INFO'}, info)
            if os.path.isfile(preffav) == True:
                bpy.ops.fontselector.load_favorites()

        elif chk == 0:
            info = 'No valid Font Folder, check Preferences'
            self.report({'ERROR'}, info)

        elif chk2 == 0:
            info = 'No valid Font in Folders, check Preferences'
            self.report({'ERROR'}, info)

        # write filterlist
        if len(filterlist) != 0:
            if os.path.isdir(prefpath) == False:
                os.makedirs(prefpath)
            nfile2 = open(preffilter, "w")
            for f in filterlist:
                nfile2.write(f + "\n")
            nfile2.close()

        # write subdir list
        if len(subdir) != 0:
            if os.path.isdir(prefpath) == False:
                os.makedirs(prefpath)
            nfile3 = open(prefsubdir, "w")
            for d in subdir:
                nfile3.write(os.path.basename(d) + "\n")
            nfile3.close()
            bpy.ops.fontselector.load_fontsubs()

        return {'FINISHED'}


# change font operator
class FontSelectorChange(bpy.types.Operator):
    bl_idname = "fontselector.change"
    bl_label = ""
    bl_description = "Change Font"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        active = bpy.context.active_object
        if active is not None:
            active_type = active.type
        else:
            active_type = ""
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        return len(fplist) > 0 and len(fontlist) > 0 and active_type == 'FONT'

    def execute(self, context):
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        idx = bpy.context.active_object.data.fontselector_index
        name = os.path.basename(fontlist[idx].filepath)
        active = bpy.context.active_object

        if fontlist[idx].name == 'Bfont':
            active.data.font = bpy.data.fonts['Bfont']
        else:
            if idx < len(fontlist):
                if os.path.isfile(fontlist[idx].filepath) == True:
                    chk = 0
                    chk2 = 0
                    for f in bpy.data.fonts:
                        if f.filepath == fontlist[idx].filepath:
                            chk2 = 1
                            fok = f.name
                    for f in bpy.data.fonts:
                        if chk2 == 0:
                            if f.users == 0 and f.filepath != fontlist[idx].filepath and chk == 0:
                                chk = 1
                                f.name = os.path.splitext(name)[0]
                                f.filepath = fontlist[idx].filepath
                    if chk == 0 and chk2 == 0:
                        bpy.data.fonts.load(filepath=fontlist[idx].filepath)
                        for f in bpy.data.fonts:
                            if f.filepath == fontlist[idx].filepath:
                                fok = f.name
                    elif chk == 1 and chk2 == 0:
                        for f in bpy.data.fonts:
                            if f.filepath == fontlist[idx].filepath:
                                fok = f.name
                    active.data.font = bpy.data.fonts[fok]
                else:
                    fontlist[idx].missingfont = True

        return {'FINISHED'}


# remove unused fonts
class FontSelectorRemoveUnused(bpy.types.Operator):
    bl_idname = "fontselector.remove_unused"
    bl_label = "Remove unused Fonts"
    bl_description = "Remove Unused Fonts form Blend file"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        flist = bpy.data.fonts
        return len(flist) > 0

    def execute(self, context):
        flist = bpy.data.fonts
        n = 0
        for f in flist:
            if f.users == 0:
                n = n + 1
                bpy.data.fonts.remove(f, do_unlink=True)

        if n > 0:
            info = str(n) + ' unused Font(s) removed'
            self.report({'INFO'}, info)
        else:
            info = 'No unused Font to remove'
            self.report({'INFO'}, info)

        return {'FINISHED'}


# save fp prefs operator
class FontSelectorSaveFPPrefs(bpy.types.Operator):
    bl_idname = "fontselector.save_fpprefs"
    bl_label = ""
    bl_description = "Save Font Folders Paths in external Font Selector preference file"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        return len(fplist) > 0 and prefs != ''

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        prefFP = os.path.join(prefpath, "fontselector_fontfolders")
        linelist = []

        # check if folder exist and create it if not
        if os.path.isdir(prefpath) == False:
            os.makedirs(prefpath)

        chk = 0
        for fp in fplist:
            fpath = os.path.abspath(bpy.path.abspath(fp.folderpath))
            if os.path.isdir(fpath) == True:
                chk = 1
                linelist.append(fpath)

        if chk == 1:
            nfile = open(prefFP, "w")
            for l in list(set(linelist)):
                nfile.write(l + '\n')
            nfile.close()

        return {'FINISHED'}


# load fp prefs operator
class FontSelectorLoadFPPrefs(bpy.types.Operator):
    bl_idname = "fontselector.load_fpprefs"
    bl_label = ""
    bl_description = "Load Font Folders Paths from external Font Selector preferences File"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        return prefs != ''

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        pref_fp = os.path.join(prefpath, "fontselector_fontfolders")
        linelist = []

        # remove existing folder list
        if len(fplist) >= 1:
            for i in range(len(fplist) - 1, -1, -1):
                fplist.remove(i)

        if os.path.isdir(prefpath) == True:
            if os.path.isfile(pref_fp) == True:
                with open(pref_fp, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1 = str(l).replace("[", "")
                        l2 = l1.replace("]", "")
                        l3 = l2.replace("'", "")
                        l4 = l3.replace('"', "")
                        newfolder = fplist.add()
                        newfolder.folderpath = l4
            else:
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info)

        return {'FINISHED'}


# save favorite
class FontSelectorSaveFavorites(bpy.types.Operator):
    bl_idname = "fontselector.save_favorites"
    bl_label = ""
    bl_description = "Save Favorite Fonts in external Font Selector preference file"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        active = bpy.context.active_object
        if active is not None:
            active_type = active.type
        else:
            active_type = ""
        return prefs != '' and len(fontlist) > 0 and active_type == 'FONT'

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        preffav = os.path.join(prefpath, "fontselector_favorites")
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        favlist = []
        dupepath = []

        # check if folder exist and create it if not
        if os.path.isdir(prefpath) == False:
            os.makedirs(prefpath)

        # get dupepath
        for f in fontlist:
            dupepath.append(f.name)

        # get old favs
        if os.path.isfile(preffav) == True:
            with open(preffav, 'r', newline='') as csvfile:
                line = csv.reader(csvfile, delimiter='\n')
                for l in line:
                    favlist.append(l)

        if len(fontlist) != 0:
            nfile = open(preffav, "w")
            for f in fontlist:
                if f.favorite == True:
                    fpath = os.path.abspath(bpy.path.abspath(f.filepath))
                    nfile.write(f.name + " || " + fpath + ' || ' + os.path.basename(os.path.dirname(fpath)) + "\n")
            for f2 in favlist:
                l1 = str(f2).replace("[", "")
                l2 = l1.replace("]", "")
                l3 = l2.replace("'", "")
                l4 = l3.replace('"', "")
                n = l4.split(" || ")[0]
                #                p=l4.split(" || ")[1]
                if n not in dupepath:
                    nfile.write(l4 + "\n")

            nfile.close()

        return {'FINISHED'}


# load favorites
class FontSelectorLoadFavorites(bpy.types.Operator):
    bl_idname = "fontselector.load_favorites"
    bl_label = ""
    bl_description = "Load Font Favorites from external Font Selector preferences File"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        return prefs != ''

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        preffav = os.path.join(prefpath, "fontselector_favorites")
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        favlist = []

        if os.path.isdir(prefpath) == True:
            if os.path.isfile(preffav) == True:
                with open(preffav, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1 = str(l).replace("[", "")
                        l2 = l1.replace("]", "")
                        l3 = l2.replace("'", "")
                        l4 = l3.replace('"', "")
                        n = l4.split(" || ")[0]
                        p = l4.split(" || ")[1]
                        favlist.append(n)
                    for f2 in favlist:
                        for f in fontlist:
                            if f.name == f2:
                                f.favorite = True
            else:
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)
                print("Font Selector Warning : Preference File does not exist, check Preference Folder path")
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info)
            print("Font Selector Warning : Folder does not exist, check Preference Folder path")

        return {'FINISHED'}


# load font list
class FontSelectorLoadFontList(bpy.types.Operator):
    bl_idname = "fontselector.load_fontlist"
    bl_label = ""
    bl_description = "Load Font List from external Font Selector preferences File"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        return prefs != ''

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        prefflist = os.path.join(prefpath, "fontselector_fontlist")
        preffav = os.path.join(prefpath, "fontselector_favorites")
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list

        # remove existing font list
        if len(fontlist) > 0:
            for i in range(len(fontlist) - 1, -1, -1):
                fontlist.remove(i)

        if os.path.isdir(prefpath) == True:
            if os.path.isfile(prefflist) == True:
                with open(prefflist, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1 = str(l).replace("[", "")
                        l2 = l1.replace("]", "")
                        l3 = l2.replace("'", "")
                        l4 = l3.replace('"', "")
                        n = l4.split(" || ")[0]
                        p = l4.split(" || ")[1]
                        s = l4.split(" || ")[2]
                        newfont = fontlist.add()
                        newfont.name = n
                        newfont.filepath = p
                        newfont.subdirectory = s
                if os.path.isfile(preffav) == True:
                    bpy.ops.fontselector.load_favorites()
            else:
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)
                print("Font Selector Warning : Preference File does not exist, check Preference Folder path")
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info)
            print("Font Selector Warning : Folder does not exist, check Preference Folder path")

        return {'FINISHED'}


# load font subdirectories
class FontSelectorLoadFontSubs(bpy.types.Operator):
    bl_idname = "fontselector.load_fontsubs"
    bl_label = ""
    bl_description = "Load Font Subdirectories from external Font Selector preferences File"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        return prefs != ''

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        prefsubdir = os.path.join(prefpath, "fontselector_subdir")
        fontsub = bpy.data.window_managers['WinMan'].fontselector_sub

        # remove existing font subs
        if len(fontsub) > 0:
            for i in range(len(fontsub) - 1, -1, -1):
                fontsub.remove(i)

        if os.path.isdir(prefpath) == True:
            if os.path.isfile(prefsubdir) == True:
                with open(prefsubdir, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1 = str(l).replace("[", "")
                        l2 = l1.replace("]", "")
                        l3 = l2.replace("'", "")
                        l4 = l3.replace('"', "")
                        newsub = fontsub.add()
                        newsub.name = l4
            else:
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)
                print("Font Selector Warning : Preference File does not exist, check Preference Folder path")
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info)
            print("Font Selector Warning : Folder does not exist, check Preference Folder path")

        return {'FINISHED'}


# filter subdirectories fonts
class FontSelectorFilterSubdirFonts(bpy.types.Operator):
    bl_idname = "fontselector.filter_subdirfonts"
    bl_label = ""
    bl_description = "Filter Font List to show only selected subdirectory Fonts"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        if active is not None:
            active_type = active.type
        else:
            active_type = ""
        return active_type == 'FONT' and len(bpy.data.window_managers['WinMan'].fontselector_sub) != 0

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        prefflist = os.path.join(prefpath, "fontselector_fontlist")
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        active = bpy.context.active_object
        sub_idx = active.data.fontselector_sub_index
        active_subdir = bpy.data.window_managers['WinMan'].fontselector_sub[sub_idx]

        # remove existing font list
        if len(fontlist) > 0:
            for i in range(len(fontlist) - 1, -1, -1):
                fontlist.remove(i)

        if os.path.isdir(prefpath) == True:
            if os.path.isfile(prefflist) == True:
                with open(prefflist, 'r', newline='') as csvfile:
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1 = str(l).replace("[", "")
                        l2 = l1.replace("]", "")
                        l3 = l2.replace("'", "")
                        l4 = l3.replace('"', "")
                        n = l4.split(" || ")[0]
                        p = l4.split(" || ")[1]
                        s = l4.split(" || ")[2]
                        if s == active_subdir.name:
                            newfont = fontlist.add()
                            newfont.name = n
                            newfont.filepath = p
                            newfont.subdirectory = s

        bpy.ops.fontselector.load_favorites()

        return {'FINISHED'}


# filter UIlist favorites
class FontSelectorFilterFavorite(bpy.types.Operator):
    bl_idname = "fontselector.filter_favorites"
    bl_label = ""
    bl_description = "Filter Font List to show only favorites Fonts"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        if active is not None:
            active_type = active.type
        else:
            active_type = ""
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        return prefs != '' and active_type == 'FONT'

    def execute(self, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        prefflist = os.path.join(prefpath, "fontselector_fontlist")
        preffav = os.path.join(prefpath, "fontselector_favorites")
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        favtoggle = bpy.context.active_object.data.fontselector_favs
        sub_idx = bpy.context.active_object.data.fontselector_sub_index
        active_subdir = bpy.data.window_managers['WinMan'].fontselector_sub[sub_idx]
        sub = bpy.context.active_object.data.fontselector_use_sub

        if os.path.isdir(prefpath) == True:
            if os.path.isfile(prefflist) == True:
                if favtoggle == False and sub == False:
                    bpy.ops.fontselector.load_fontlist()
                elif favtoggle == False and sub == True:
                    bpy.ops.fontselector.filter_subdirfonts()
                else:
                    # remove existing font list
                    if len(fontlist) > 0:
                        for i in range(len(fontlist) - 1, -1, -1):
                            fontlist.remove(i)
                    if os.path.isfile(preffav) == True:
                        with open(preffav, 'r', newline='') as csvfile:
                            line = csv.reader(csvfile, delimiter='\n')
                            for l in line:
                                l1 = str(l).replace("[", "")
                                l2 = l1.replace("]", "")
                                l3 = l2.replace("'", "")
                                l4 = l3.replace('"', "")
                                n = l4.split(" || ")[0]
                                p = l4.split(" || ")[1]
                                s = l4.split(" || ")[2]
                                if sub == True:
                                    if s == active_subdir.name:
                                        newfont = fontlist.add()
                                        newfont.name = n
                                        newfont.filepath = p
                                        newfont.subdirectory = s
                                else:
                                    newfont = fontlist.add()
                                    newfont.name = n
                                    newfont.filepath = p
                                    newfont.subdirectory = s

                    else:
                        info = 'No Favorite Fonts'
                        self.report({'ERROR'}, info)
                        print("Font Selector Warning : No Favorite Fonts")

                if os.path.isfile(preffav) == True:
                    bpy.ops.fontselector.load_favorites()
            else:
                info = 'Preference File does not exist, check Preference Folder path'
                self.report({'ERROR'}, info)
                print("Font Selector Warning : Preference File does not exist, check Preference Folder path")
        else:
            info = 'Folder does not exist, check Preference Folder path'
            self.report({'ERROR'}, info)
            print("Font Selector Warning : Folder does not exist, check Preference Folder path")

        return {'FINISHED'}


### Export Preset  ###
class FontSelectorExportFavorites(bpy.types.Operator, ExportHelper):
    bl_idname = "fontselector.export_favorites"
    bl_label = "Export Favorites"
    bl_description = "Export Fonts marked as Favorites in a zip file"
    filename_ext = ".zip"
    filepath = bpy.props.StringProperty(default="favorite_fonts")

    @classmethod
    def poll(cls, context):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        fontlist = bpy.data.window_managers['WinMan'].fontselector_list
        chk = 0
        for f in fontlist:
            if f.favorite == True:
                chk = 1
        return len(fplist) > 0 and prefs != "" and len(fontlist) > 0 and chk == 1

    def execute(self, context):
        return fontselector_export_favorites(self.filepath, context)


### EXPORT MENU
def menu_export_favorites(self, context):
    self.layout.operator('fontselector.export_favorites', text="Favorite Fonts export", icon='FILE_FONT')


### Write Export Function ###
def fontselector_export_favorites(filepath, context):
    fontlist = bpy.data.window_managers['WinMan'].fontselector_list
    zippath = os.path.abspath(bpy.path.abspath(filepath))
    temp = os.path.splitext(zippath)[0]

    # create tempfolder
    os.makedirs(os.path.splitext(zippath)[0])

    # copy fonts
    for f in fontlist:
        if f.favorite == True:
            name = os.path.basename(f.filepath)
            shutil.copy2(f.filepath, os.path.join(temp, name))
            shutil.copystat(f.filepath, os.path.join(temp, name))
    shutil.make_archive(os.path.splitext(zippath)[0], 'zip', temp)
    shutil.rmtree(temp)

    print('Font Selector Export finished')
    return {'FINISHED'}


#######################################################################
### addon UI List ###
#######################################################################

# font list
class FontUIList(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        # get addon prefs
        addon_preferences = get_addon_preferences()
        subdir = addon_preferences.prefs_show_subdir

        if item.missingfont == True:
            layout.label(icon='ERROR')
        layout.label(text=item.name)
        if subdir == True:
            layout.label(text=item.subdirectory)
        if item.favorite == True:
            layout.prop(item, "favorite", text="", icon='SOLO_ON', emboss=False, translate=False)
        else:
            layout.prop(item, "favorite", text="", icon='SOLO_OFF', emboss=False, translate=False)


# subdir list
class SubdirUIList(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        layout.label(text=item.name)


#######################################################################
### addon GUI ###
#######################################################################

# addon panel
class FontSelectorPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Font Selector"
    bl_context = "data"
    bl_label = "Font Selection"

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        if active is not None:
            active_type = active.type
        else:
            active_type = ""
        return active_type == 'FONT'

    def draw(self, context):
        layout = self.layout
        # get addon prefs
        addon_preferences = get_addon_preferences()
        rownumber = addon_preferences.row_number
        fplist = addon_preferences.font_folders
        activedata = bpy.context.active_object.data
        fonth = bpy.data.window_managers['WinMan']

        if len(fonth.fontselector_sub) > 5:
            sub_row = 5
        else:
            sub_row = len(fonth.fontselector_sub)

        if len(fplist) == 0:
            layout.label(text="Add Font Folder in Addon Preference", icon='INFO')
        else:
            row = layout.row()
            row.operator("fontselector.refresh", icon='FILE_REFRESH')
            if fonth.fontselector_list == 0:
                row = layout.row()
                row.label(text="Refresh to get List of available Fonts", icon='INFO')
            else:
                row.operator("fontselector.remove_unused", icon='UNLINKED')
                row.prop(activedata, 'fontselector_use_sub', text='', icon='FILE_FONT')
                if activedata.fontselector_favs == True:
                    row.prop(activedata, 'fontselector_favs', text='', icon='SOLO_ON')
                elif activedata.fontselector_favs == False:
                    row.prop(activedata, 'fontselector_favs', text='', icon='SOLO_OFF')
                if len(fonth.fontselector_sub) != 0 and activedata.fontselector_use_sub == True:
                    row = layout.row()
                    row.template_list("SubdirUIList", "", fonth, "fontselector_sub", activedata,
                                      "fontselector_sub_index", rows=sub_row)
                row = layout.row()
                row.template_list("FontUIList", "", fonth, "fontselector_list", activedata, "fontselector_index",
                                  rows=rownumber)


#######################################################################
### handler ###
#######################################################################

# handler
@persistent
def fontselector_startup(scene):
    # get addon prefs
    addon_preferences = get_addon_preferences()
    prefs = addon_preferences.prefs_folderpath
    prefpath = os.path.abspath(bpy.path.abspath(prefs))
    preffav = os.path.join(prefpath, "fontselector_favorites")
    prefflist = os.path.join(prefpath, "fontselector_fontlist")
    prefsubdir = os.path.join(prefpath, "fontselector_subdir")
    fontlist = bpy.data.window_managers['WinMan'].fontselector_list

    chk = 0
    if os.path.isfile(prefflist) == True:
        chk = 1
        bpy.ops.fontselector.load_fontlist()
    if os.path.isfile(prefsubdir) == True:
        bpy.ops.fontselector.load_fontsubs()
    if os.path.isfile(preffav) == True and len(fontlist) > 0:
        bpy.ops.fontselector.load_favorites()
    if chk == 1:
        print("Font Selector settings loaded")


#######################################################################
### reg unreg ###
#######################################################################

def register():
    bpy.utils.register_class(FontFolders)
    bpy.utils.register_class(FontSelectorAddonPrefs)
    bpy.utils.register_class(FontSelectorAddFP)
    bpy.utils.register_class(FontSelectorAddFiltered)
    bpy.utils.register_class(FontSelectorSuppressFP)
    bpy.utils.register_class(FontSelectorRefresh)
    bpy.utils.register_class(FontSelectorChange)
    bpy.utils.register_class(FontSelectorRemoveUnused)
    bpy.utils.register_class(FontSelectorSaveFPPrefs)
    bpy.utils.register_class(FontSelectorLoadFPPrefs)
    bpy.utils.register_class(FontSelectorSaveFavorites)
    bpy.utils.register_class(FontSelectorLoadFavorites)
    bpy.utils.register_class(FontSelectorLoadFontList)
    bpy.utils.register_class(FontSelectorLoadFontSubs)
    bpy.utils.register_class(FontSelectorFilterSubdirFonts)
    bpy.utils.register_class(FontSelectorFilterFavorite)
    bpy.utils.register_class(FontSelectorExportFavorites)
    bpy.utils.register_class(FontUIList)
    bpy.utils.register_class(SubdirUIList)
    bpy.utils.register_class(FontSelectorPanel)
    bpy.utils.register_class(FontSelectorFontList)
    bpy.utils.register_class(FontSelectorFontSubs)
    bpy.types.WindowManager.fontselector_list = \
        bpy.props.CollectionProperty(type=FontSelectorFontList)
    bpy.types.WindowManager.fontselector_sub = \
        bpy.props.CollectionProperty(type=FontSelectorFontSubs)
    bpy.types.TextCurve.fontselector_favs = \
        bpy.props.BoolProperty(default=False, update=update_favorite_filter,
                               description="Toggle display only Favorite Fonts")
    bpy.types.TextCurve.fontselector_index = \
        bpy.props.IntProperty(update=update_change_font)
    bpy.types.TextCurve.fontselector_sub_index = \
        bpy.props.IntProperty(update=update_subdir_filter)
    bpy.types.TextCurve.fontselector_use_sub = \
        bpy.props.BoolProperty(update=update_subdir_toggle, description="Toggle display Subdirectory Mode")

    bpy.app.handlers.load_post.append(fontselector_startup)

    bpy.types.TOPBAR_MT_file_export.append(menu_export_favorites)


def unregister():
    bpy.utils.unregister_class(FontFolders)
    bpy.utils.unregister_class(FontSelectorAddonPrefs)
    bpy.utils.unregister_class(FontSelectorAddFP)
    bpy.utils.unregister_class(FontSelectorAddFiltered)
    bpy.utils.unregister_class(FontSelectorSuppressFP)
    bpy.utils.unregister_class(FontSelectorRefresh)
    bpy.utils.unregister_class(FontSelectorChange)
    bpy.utils.unregister_class(FontSelectorRemoveUnused)
    bpy.utils.unregister_class(FontSelectorSaveFPPrefs)
    bpy.utils.unregister_class(FontSelectorLoadFPPrefs)
    bpy.utils.unregister_class(FontSelectorSaveFavorites)
    bpy.utils.unregister_class(FontSelectorLoadFavorites)
    bpy.utils.unregister_class(FontSelectorLoadFontList)
    bpy.utils.unregister_class(FontSelectorLoadFontSubs)
    bpy.utils.unregister_class(FontSelectorFilterSubdirFonts)
    bpy.utils.unregister_class(FontSelectorFilterFavorite)
    bpy.utils.unregister_class(FontSelectorExportFavorites)
    bpy.utils.unregister_class(FontUIList)
    bpy.utils.unregister_class(SubdirUIList)
    bpy.utils.unregister_class(FontSelectorPanel)
    bpy.utils.unregister_class(FontSelectorFontList)
    bpy.utils.unregister_class(FontSelectorFontSubs)
    del bpy.types.WindowManager.fontselector_list
    del bpy.types.WindowManager.fontselector_sub
    del bpy.types.TextCurve.fontselector_favs
    del bpy.types.TextCurve.fontselector_index
    del bpy.types.TextCurve.fontselector_sub_index
    del bpy.types.TextCurve.fontselector_use_sub

    bpy.app.handlers.load_post.remove(fontselector_startup)

    bpy.types.TOPBAR_MT_file_export.remove(menu_export_favorites)


if __name__ == "__main__":
    register()
