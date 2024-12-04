import bpy

from .addon_prefs import get_addon_preferences


# Font selection UI List
class FONTSELECTOR_uilist(bpy.types.UIList):
    
    obj = None
    strip = False
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        
        row = layout.row(align=True)
            
        row.label(text = item.name)
            
        # Multi font families
        if not self.strip\
        and self.obj.fontselector_object_properties.show_multi_font:
            
            if get_addon_preferences().no_font_family_load:
                if item.multi_font:
                    icon = "FONTPREVIEW"
                else:
                    icon = "REMOVE"
                row.operator(
                    "fontselector.load_font_family",
                    text ="",
                    icon = icon,
                ).font_name = item.name
            elif item.multi_font:
                row.label(text ="", icon = "FONTPREVIEW")
        
        # Favorites
        if self.obj.fontselector_object_properties.show_favorite:
            if item.favorite:
                icon = 'SOLO_ON'
            else:
                icon = 'SOLO_OFF'
            row.prop(item, "favorite", text = "", icon = icon, emboss = True)


    def draw_filter(self, context, layout):
        
        obj_props = self.obj.fontselector_object_properties
            
        row = layout.row(align=True)
        row.label(text = "", icon = "FILTER")
        row.prop(obj_props, "favorite_filter", text="", icon="SOLO_ON")
        if not self.strip:
            row.prop(obj_props, "multi_font_filter", text="", icon="FONTPREVIEW")
        row.separator()
        row.prop(obj_props, "invert_filter", text="", icon="ARROW_LEFTRIGHT")
        
        row.separator()
        
        if not self.strip:
            sub = row.row(align=True)
            sub.alignment = "CENTER"
            sub.label(text = "", icon = "GHOST_ENABLED")
            sub.prop(obj_props, "multi_font_component_hide", text="", icon="FONT_DATA")
        
        row.separator()
        
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.label(text = "", icon = "HIDE_OFF")
        sub.prop(obj_props, "show_favorite", text="", icon="SOLO_ON")
        if not self.strip:
            sub.prop(obj_props, "show_multi_font", text="", icon="FONTPREVIEW")
        
        
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
        
        obj_props = self.obj.fontselector_object_properties
        
        # Default return values.
        flt_flags = []
        flt_neworder = []

        helper_funcs = bpy.types.UI_UL_list
        
        col = getattr(data, propname)
        
        if obj_props.font_search\
        or obj_props.favorite_filter\
        or obj_props.multi_font_filter\
        or obj_props.invert_filter\
        or obj_props.multi_font_component_hide:
            flt_flags = [self.bitflag_filter_item] * len(col)
            
            # Name search
            if obj_props.font_search :
                search = obj_props.font_search.lower()
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if search not in font.name.lower()\
                        and search not in font.filepath.lower():
                            flt_flags[idx] = 0
            
            # Favorites
            if obj_props.favorite_filter :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if font.favorite == False :
                            flt_flags[idx] = 0
                            
            # Multi font
            if not self.strip:
                if obj_props.multi_font_filter:
                    for idx, font in enumerate(col) :
                        if flt_flags[idx] != 0 :
                            if font.multi_font == False:
                                flt_flags[idx] = 0
                                
                if obj_props.multi_font_component_hide:
                    for idx, font in enumerate(col) :
                        if flt_flags[idx] != 0 :
                            if font.multi_font_component:
                                flt_flags[idx] = 0
                            
            # invert filtering
            if obj_props.invert_filter :
                for idx, font in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        flt_flags[idx] = 0
                    else :
                        flt_flags[idx] = self.bitflag_filter_item

        return flt_flags, flt_neworder


# Font selection Object UI List
class FONTSELECTOR_UL_uilist_object(FONTSELECTOR_uilist):
    
    def __init__(self):
        self.obj = bpy.context.active_object.data
        

# Font selection Strip UI List
class FONTSELECTOR_UL_uilist_strip(FONTSELECTOR_uilist):
    
    def __init__(self):
        self.obj = bpy.context.active_sequence_strip
        self.strip = True

    
### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_UL_uilist_object)
    bpy.utils.register_class(FONTSELECTOR_UL_uilist_strip)
    
def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_UL_uilist_object)
    bpy.utils.unregister_class(FONTSELECTOR_UL_uilist_strip)
