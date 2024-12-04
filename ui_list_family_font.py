import bpy

from .addon_prefs import get_addon_preferences


# Font selection UI List
class FONTSELECTOR_family_uilist(bpy.types.UIList):
    
    obj = None
    strip = False
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        
        row = layout.row(align=True)
        row.label(text = item.name)


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
