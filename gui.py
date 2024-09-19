import bpy


# TODO Popover


# Fontselector panel
class FONTSELECTOR_panel(bpy.types.Panel):
    bl_label = "Font Selection"
    
    strip = False
    
    def draw(self, context):
        layout = self.layout
        
        if self.strip:
            active_datas = context.active_sequence_strip.fontselector_object_properties
        else:
            active_datas = context.active_object.data.fontselector_object_properties
        
        props = context.window_manager.fontselector_properties

        col = layout.column(align=True)
        
        row = col.row(align=True)
        row.prop(active_datas, "font_search", text="", icon='VIEWZOOM')
        row.operator("fontselector.reload_fonts", text="", icon="FILE_REFRESH")

        row = col.row()
        if self.strip:
            row.template_list("FONTSELECTOR_UL_uilist_strip", "", props, "fonts", active_datas, "font_index", rows = 5)
            
        else:
            row.template_list("FONTSELECTOR_UL_uilist_object", "", props, "fonts", active_datas, "font_index", rows = 5)
        
    
# Properties Panel GUI
class FONTSELECTOR_PT_properties_panel(FONTSELECTOR_panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Font Selector"
    bl_context = "data"
    bl_label = "Font Selection"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type == "FONT"
    

# Sequencer Panel GUI
class FONTSELECTOR_PT_sequencer_panel(FONTSELECTOR_panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_parent_id = "SEQUENCER_PT_effect"
    bl_category = "Strip"
    bl_label = "Font Selection"
    
    def __init__(self):
        self.strip = True
    
    @classmethod
    def poll(cls, context):
        strip = context.active_sequence_strip
        return strip.type == 'TEXT'
       

### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PT_properties_panel)
    bpy.utils.register_class(FONTSELECTOR_PT_sequencer_panel)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PT_properties_panel)
    bpy.utils.unregister_class(FONTSELECTOR_PT_sequencer_panel)
