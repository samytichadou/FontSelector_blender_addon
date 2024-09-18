import bpy


#font list
class FONTSELECTOR_UL_uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :       

        layout.label(text = item.name)
    
    
### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_UL_uilist)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_UL_uilist)
