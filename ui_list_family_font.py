import bpy

from .addon_prefs import get_addon_preferences


# Font selection UI List
class FONTSELECTOR_family_uilist(bpy.types.UIList):
    
    obj = None
    strip = False
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :

        obj_props = self.obj.fontselector_object_properties
        
        # Name
        row = layout.row(align=True)
        row.label(text = item.name)

        # Multi Component
        if not self.strip and obj_props.show_multi_component and item.multi_component:
            row.operator(
                "fontselector.load_font_family",
                text="",
                icon="FONTPREVIEW",
            ).font_family_name = item.name
            # row.label(text="", icon="FONTPREVIEW")

        # Favorites
        if obj_props.show_favorite:
            if item.favorite:
                icon = 'SOLO_ON'
            else:
                icon = 'SOLO_OFF'
            row.prop(item, "favorite", text = "", icon = icon, emboss = True)


    def draw_filter(self, context, layout):

        obj_props = self.obj.fontselector_object_properties

        row = layout.row(align=True)
        row.label(text = "", icon = "FILTER")
        row.separator()
        row.prop(obj_props, "favorite_filter", text="", icon="SOLO_ON")
        row.prop(obj_props, "invert_filter", text="", icon="ARROW_LEFTRIGHT")

        row.separator()

        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.label(text = "", icon = "HIDE_OFF")
        sub.separator()
        if not self.strip:
            sub.prop(obj_props, "show_multi_component", text="", icon="FONTPREVIEW")
        sub.prop(obj_props, "show_favorite", text="", icon="SOLO_ON")

    def filter_items(self, context, data, propname):

        obj_props = self.obj.fontselector_object_properties
        families = context.window_manager.fontselector_properties.font_families
        family = families[obj_props.family_index]

        # Default return values.
        flt_flags = []
        flt_neworder = []

        helper_funcs = bpy.types.UI_UL_list

        col = getattr(data, propname)

        # Filter/Order
        if obj_props.font_search\
        or obj_props.favorite_filter\
        or obj_props.invert_filter:
            flt_flags = [self.bitflag_filter_item] * len(col)

            # Name search
            if obj_props.font_search :
                search = obj_props.font_search.lower()
                for idx, family in enumerate(col) :

                    if flt_flags[idx] != 0 :

                        chk_visible = search in family.name.lower()

                        if not chk_visible:
                            for f in family.fonts:

                                if obj_props.search_font_names and search in f.font_name.lower():
                                    chk_visible = True

                                if obj_props.search_filepath and search in f.filepath.lower():
                                    chk_visible = True

                        if not chk_visible:
                            flt_flags[idx] = 0

            # Favorites
            if obj_props.favorite_filter :
                for idx, family in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        if family.favorite == False :
                            flt_flags[idx] = 0

            # invert filtering
            if obj_props.invert_filter :
                for idx, family in enumerate(col) :
                    if flt_flags[idx] != 0 :
                        flt_flags[idx] = 0
                    else :
                        flt_flags[idx] = self.bitflag_filter_item

        return flt_flags, flt_neworder


# Font selection Object UI List
class FONTSELECTOR_UL_family_uilist_object(FONTSELECTOR_family_uilist):
    
    def __init__(self):
        self.obj = bpy.context.active_object.data
        

# Font selection Strip UI List
class FONTSELECTOR_UL_family_uilist_strip(FONTSELECTOR_family_uilist):
    
    def __init__(self):
        self.obj = bpy.context.active_sequence_strip
        self.strip = True

    
### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_UL_family_uilist_object)
    bpy.utils.register_class(FONTSELECTOR_UL_family_uilist_strip)
    
def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_UL_family_uilist_object)
    bpy.utils.unregister_class(FONTSELECTOR_UL_family_uilist_strip)
