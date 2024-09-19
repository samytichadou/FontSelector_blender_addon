import bpy


# Font selection UI List
class FONTSELECTOR_uilist(bpy.types.UIList):
    
    show_favorite : bpy.props.BoolProperty(name = "Show Favorites", description = "Show Favorites icon")
    favorite_filter : bpy.props.BoolProperty(name = "Favorites Filter", description = "Favorites Filter")
    invert_filter : bpy.props.BoolProperty(name = "Invert Filter", description = "Invert Filters")
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        
        row = layout.row(align=True)
        
        row.label(text = item.name)
        
        if self.show_favorite:
            if item.favorite:
                icon = 'SOLO_ON'
            else:
                icon = 'SOLO_OFF'
            row.prop(item, "favorite", text = "", icon = icon, emboss = True)
            
    def draw_filter(self, context, layout):
        
        # TODO UI
        row = layout.row(align=True)
        
        row.prop(self, "favorite_filter", text="", icon="SOLO_ON")
        row.prop(self, "invert_filter", text="", icon="ARROW_LEFTRIGHT")
        row.separator()
        row.prop(self, "show_favorite", text="", icon="SOLO_OFF")
        
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
        
        if self.filter_name or self.favorite_filter or self.invert_filter:
            flt_flags = [self.bitflag_filter_item] * len(col)
            
            # Name search
            if self.filter_name :
                search = self.filter_name.lower()
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if search not in font.name.lower()\
                        and search not in font.filepath.lower():
                            flt_flags[idx] = 0
            
            # Favorites
            if self.favorite_filter :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if font.favorite ==False :
                            flt_flags[idx] = 0
                            
            # invert filtering
            if self.invert_filter :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        flt_flags[idx] = 0
                    else :
                        flt_flags[idx] = self.bitflag_filter_item

        return flt_flags, flt_neworder


# Font selection Object UI List
class FONTSELECTOR_UL_uilist_object(FONTSELECTOR_uilist):
    
    def __init__(self):
        obj = bpy.context.active_object.data
        self.filter_name = obj.fontselector_object_properties.font_search
        

# Font selection Strip UI List
class FONTSELECTOR_UL_uilist_strip(FONTSELECTOR_uilist):
    
    def __init__(self):
        obj = bpy.context.active_sequence_strip
        self.filter_name = obj.fontselector_object_properties.font_search
    
    
### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_UL_uilist_object)
    bpy.utils.register_class(FONTSELECTOR_UL_uilist_strip)
    
def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_UL_uilist_object)
    bpy.utils.unregister_class(FONTSELECTOR_UL_uilist_strip)
