import bpy

from .addon_prefs import get_addon_preferences


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


def viewport_popover_draw(self, context):
    if get_addon_preferences().properties_panel\
    and context.active_object.type == "FONT":
        self.layout.popover(panel="FONTSELECTOR_PT_viewport_popover", text="", icon="FILE_FONT")
   

# 3D viewport popover
class FONTSELECTOR_PT_viewport_popover(FONTSELECTOR_panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 10
    
    @classmethod
    def poll(cls, context):
        if get_addon_preferences().properties_panel:
            return context.active_object.type == "FONT"
        
    
# Properties Panel GUI
class FONTSELECTOR_PT_properties_panel(FONTSELECTOR_panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Font Selector"
    bl_context = "data"
    bl_label = "Font Selection"
    
    @classmethod
    def poll(cls, context):
        if get_addon_preferences().properties_panel:
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
        if get_addon_preferences().sequencer_panel:
            strip = context.active_sequence_strip
            return strip.type == 'TEXT'
       

### REGISTER ---
def register():
    bpy.types.VIEW3D_MT_editor_menus.append(viewport_popover_draw)
    bpy.utils.register_class(FONTSELECTOR_PT_viewport_popover)
    bpy.utils.register_class(FONTSELECTOR_PT_properties_panel)
    bpy.utils.register_class(FONTSELECTOR_PT_sequencer_panel)

def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(viewport_popover_draw)
    bpy.utils.unregister_class(FONTSELECTOR_PT_viewport_popover)
    bpy.utils.unregister_class(FONTSELECTOR_PT_properties_panel)
    bpy.utils.unregister_class(FONTSELECTOR_PT_sequencer_panel)
