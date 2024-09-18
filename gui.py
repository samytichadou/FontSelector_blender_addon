import bpy


# TODO Selected, not only active
# TODO Sequencer panel
# TODO Popover


# general GUI
def draw_fontselector_gui(layout, activedata):
    
    props = bpy.context.window_manager.fontselector_properties
    
    col = layout.column(align=True)
    
    row = col.row(align=True)
    row.prop(props, 'font_search', text="", icon='VIEWZOOM')
    row.operator("fontselector.reload_fonts", text="", icon="FILE_REFRESH")

    row = col.row()
    row.template_list("FONTSELECTOR_UL_uilist", "", props, "fonts", props, "font_index", rows = 5)


# Properties Panel GUI
class FONTSELECTOR_PT_properties_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Font Selector"
    bl_context = "data"
    bl_label = "Font Selection"
    
    @classmethod
    def poll(cls, context):
        active=bpy.context.active_object
        if active is not None:
            return active.type == 'FONT'

    def draw(self, context):
        layout = self.layout
        activedata = context.active_object.data
        draw_fontselector_gui(layout, activedata)


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PT_properties_panel)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PT_properties_panel)
