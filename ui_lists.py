import bpy

from .preferences import get_addon_preferences
from .update_functions import get_subdirectories_items

#font list
class FontUIList(bpy.types.UIList):

    show_subdirectory_name = bpy.props.BoolProperty(name = "Show Subdirectories", description = "Show Subdirectories")
    show_favorite_icon = bpy.props.BoolProperty(name = "Show Favorites", description = "Show Favorites")
    show_fake_user = bpy.props.BoolProperty(name = "Show Fake User", description = "Show Fake User")

    subdirectories_filter = bpy.props.EnumProperty(items = get_subdirectories_items, 
                                                name = "Subdirectories",
                                                description = "Display only specific Subdirectories")
    favorite_filter = bpy.props.BoolProperty(name = "Favorites Filter", description = "Show Only Favorites")
    invert_filter = bpy.props.BoolProperty(name = "Invert Filter", description = "Invert Filter")
    fake_user_filter = bpy.props.BoolProperty(name = "Fake User Filter", description = "Fake User Filter")

    subdirectories_sorting = bpy.props.BoolProperty(name = "Sort by Subdirectories", description = "Sort by Subdirectories")
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        #self.use_filter_show = True
        wm = bpy.data.window_managers['WinMan']

        row = layout.row(align = True)

        if item.missingfont :
            row.label(icon = 'ERROR')
        row.label(item.name)
        if self.show_subdirectory_name :
            row.label(item.subdirectory)
        if self.show_favorite_icon and not wm.fontselector_override :
            icon = 'SOLO_ON' if item.favorite else 'SOLO_OFF'
            row.prop(item, "favorite", text = "", icon = icon, emboss = True)
        if self.show_fake_user :
            row.prop(item, "fake_user", text = "", icon = 'FONT_DATA', emboss = True)

    def draw_filter(self, context, layout):

        wm = bpy.data.window_managers['WinMan']

        # FILTER
        box = layout.box()
        row = box.row(align = True)
        row.label(icon = 'VIEWZOOM')
        row.separator()

        # search classic
        row.prop(self, 'filter_name', text = '')
        row.separator()
        # filter by subfolder
        #row.prop(self, 'subdirectories_filter', text = '')
        row.prop(wm, 'fontselector_subdirectories', text = '')
        row.operator('fontselector.open_subdirectory', text = '', icon = 'FILE_FOLDER')
        row.separator()
        if not wm.fontselector_override :
            # show only favorites
            row.prop(self, 'favorite_filter', text = '', icon = 'SOLO_ON')
        # show only fake user
        row.prop(self, 'fake_user_filter', text = '', icon = 'FONT_DATA')
        # invert filtering
        row.prop(self, 'invert_filter', text = '', icon = 'ARROW_LEFTRIGHT')

        # SORT
        box = layout.box()
        row = box.row(align = True)
        row.label(icon = 'SORTSIZE')
        row.separator()
        
        # sort by subfolder
        row.prop(self, 'subdirectories_sorting', text = '', icon = 'FILESEL')
        # sort invert
        row.prop(self, 'use_filter_sort_reverse', text = '', icon = 'ARROW_LEFTRIGHT')

        # VIEW
        row.separator()
        row.label(icon = 'RESTRICT_VIEW_OFF')
        row.separator()

        # show subfolder option
        row.prop(self, 'show_subdirectory_name', text = '', icon = 'FILESEL')
        if not wm.fontselector_override :
            # show favorite
            row.prop(self, 'show_favorite_icon', text = '', icon = 'SOLO_OFF')
        # show fake user
        row.prop(self, 'show_fake_user', text = '', icon = 'FONT_DATA')
        

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

        subdirectories_filter = bpy.data.window_managers['WinMan'].fontselector_subdirectories
        wm = bpy.data.window_managers['WinMan']
        
        ### FILTERING ###

        if self.filter_name or subdirectories_filter != "All" or self.favorite_filter or self.invert_filter or self.fake_user_filter :
            flt_flags = [self.bitflag_filter_item] * len(col)

            # name search
            if self.filter_name :
                #flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, col, "name", flags=None, reverse=False)
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if self.filter_name.lower() not in font.name.lower() :
                            flt_flags[idx] = 0
            # subdir filtering
            if subdirectories_filter != 'All' :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if font.subdirectory != subdirectories_filter :
                            flt_flags[idx] = 0

            # favs filtering
            if self.favorite_filter and not wm.fontselector_override :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if font.favorite ==False :
                            flt_flags[idx] = 0
            
            # fake user filtering
            if self.fake_user_filter :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if font.fake_user ==False :
                            flt_flags[idx] = 0

            # invert filtering
            if self.invert_filter :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        flt_flags[idx] = 0
                    else :
                        flt_flags[idx] = self.bitflag_filter_item

        ### REORDERING ###
        if self.subdirectories_sorting :
            _sort = [(idx, font) for idx, font in enumerate(col)]
            flt_neworder = helper_funcs.sort_items_helper(_sort, key=lambda font: font[1].subdirectory)

        return flt_flags, flt_neworder