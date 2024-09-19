import bpy


# TODO Popover


# general GUI
def draw_fontselector_gui(layout, active_datas):
    
    props = bpy.context.window_manager.fontselector_properties
    
    col = layout.column(align=True)
    
    row = col.row(align=True)
    row.prop(props, 'font_search', text="", icon='VIEWZOOM')
    row.operator("fontselector.reload_fonts", text="", icon="FILE_REFRESH")

    row = col.row()
    row.template_list("FONTSELECTOR_UL_uilist", "", props, "fonts", active_datas, "font_index", rows = 5)

    
# Properties Panel GUI
class FONTSELECTOR_PT_properties_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Font Selector"
    bl_context = "data"
    bl_label = "Font Selection"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type == "FONT"
    
    def draw(self, context):
        layout = self.layout
        active_datas = context.active_object.data.fontselector_object_properties
        draw_fontselector_gui(layout, active_datas)


# Sequencer Panel GUI
class FONTSELECTOR_PT_sequencer_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_parent_id = "SEQUENCER_PT_effect"
    bl_category = "Strip"
    bl_label = "Font Selection"
    
    @classmethod
    def poll(cls, context):
        strip = context.active_sequence_strip
        return strip.type == 'TEXT'
    
    def draw(self, context):
        layout = self.layout
        active_datas = context.active_sequence_strip.fontselector_object_properties
        draw_fontselector_gui(layout, active_datas)
        

### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PT_properties_panel)
    bpy.utils.register_class(FONTSELECTOR_PT_sequencer_panel)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PT_properties_panel)
    bpy.utils.unregister_class(FONTSELECTOR_PT_sequencer_panel)
