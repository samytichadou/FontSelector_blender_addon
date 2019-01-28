import bpy

from .preferences import get_addon_preferences
from .update_functions import get_subdirectories_items

#font list
class FontUIList(bpy.types.UIList):

    show_subdirectory_name = bpy.props.BoolProperty(name = "Show Subdirectory", default = False)
    show_favorite_icon = bpy.props.BoolProperty(name = "Show Favorites", default = False)
    subdirectories_filter = bpy.props.EnumProperty(items = get_subdirectories_items, 
                                                name = "Subdirectories")
    favorite_filter = bpy.props.BoolProperty(name = "Favorites Filter", default = False)
    invert_filter = bpy.props.BoolProperty(name = "Invert Filter", default = False)
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        self.use_filter_show = True
        #get addon prefs
        addon_preferences = get_addon_preferences()
        show_subdir = addon_preferences.prefs_show_subdir
        active_subdir = bpy.data.window_managers['WinMan'].fontselector_sub

        if item.missingfont :
            layout.label(icon = 'ERROR')
        layout.label(item.name)
        if self.show_subdirectory_name :
            layout.label(item.subdirectory)
        if self.show_favorite_icon :
            if item.favorite :
                layout.prop(item, "favorite", text = "", icon = 'SOLO_ON', emboss = False)
            else:
                layout.prop(item, "favorite", text = "", icon='SOLO_OFF', emboss = False)

    def draw_filter(self, context, layout):
        # Nothing much to say here, it's usual UI code...

        # FILTER
        box = layout.box()
        row = box.row(align = True)

        # search classic
        row.prop(self, 'filter_name', text = '')
        # invert filtering
        row.prop(self, 'invert_filter', text = '', icon = 'ARROW_LEFTRIGHT')
        # show only favorites
        row.prop(self, 'favorite_filter', text = '', icon = 'SOLO_ON')
        # filter by subfolder
        row.prop(self, 'subdirectories_filter', text = '')

        # SORT
        box = layout.box()
        row = box.row(align = True)
        row.label('Sort')

        # sort invert
        row.prop(self, 'use_filter_sort_reverse', text = '', icon = 'ARROW_LEFTRIGHT')
        # sort by subfolder

        # VIEW
        box = layout.box()
        row = box.row(align = True)
        row.label('Display')

        # show subfolder option
        row.prop(self, 'show_subdirectory_name', text = '', icon = 'FILESEL')
        # show favorite
        row.prop(self, 'show_favorite_icon', text = '', icon = 'SOLO_OFF')

    # Called once to filter/reorder items.
    def filter_items(self, context, data, propname):
        # This function gets the collection property (as the usual tuple (data, propname)), and must return two lists:
        # * The first one is for filtering, it must contain 32bit integers were self.bitflag_filter_item marks the
        #   matching item as filtered (i.e. to be shown), and 31 other bits are free for custom needs. Here we use the
        #   first one to mark VGROUP_EMPTY.
        # * The second one is for reordering, it must return a list containing the new indices of the items (which
        #   gives us a mapping org_idx -> new_idx).
        # Please note that the default UI_UL_list defines helper functions for common tasks (see its doc for more info).
        # If you do not make filtering and/or ordering, return empty list(s) (this will be more efficient than
        # returning full lists doing nothing!).
        
        # Default return values.
        flt_flags = []
        flt_neworder = []

        helper_funcs = bpy.types.UI_UL_list

        col = getattr(data, propname)

        ### FILTERING ###

        ### TODO ### avoid if no filter flag
        flt_flags = [self.bitflag_filter_item] * len(col)

        # name search
        if self.filter_name :
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, col, "name")
        
        # subdir filtering
        if self.subdirectories_filter != 'All' :
            for idx, font in enumerate(col):
                if flt_flags[idx] != 0 :
                    if font.subdirectory != self.subdirectories_filter :
                        flt_flags[idx] = 0

        # favs filtering
        if self.favorite_filter :
            for idx, font in enumerate(col):
                if flt_flags[idx] != 0 :
                    if font.favorite ==False :
                        flt_flags[idx] = 0

        # invert filtering
        if self.invert_filter :
            for idx, font in enumerate(col):
                if flt_flags[idx] != 0 :
                    flt_flags[idx] = 0
                else :
                    flt_flags[idx] = self.bitflag_filter_item

        
        ### REORDERING ###

        return flt_flags, flt_neworder