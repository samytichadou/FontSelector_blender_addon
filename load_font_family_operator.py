import bpy

from . import properties as pr
from .addon_prefs import get_addon_preferences


class FONTSELECTOR_OT_load_font_family(bpy.types.Operator):
    """Load/Remove entire font family (Bold, Italic...)"""
    bl_idname = "fontselector.load_font_family"
    bl_label = "Load/Remove Font Family"
    bl_options = {'INTERNAL', 'UNDO'}
    
    font_name : bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return bpy.context.active_object

    def execute(self, context):
        
        debug = get_addon_preferences().debug
        
        fonts = context.window_manager.fontselector_properties.fonts
        
        active_datas = bpy.context.active_object.data
    
        target_font = fonts[self.font_name]
        
        # Change index
        active_datas.fontselector_object_properties.font_index = fonts.find(self.font_name)
        
        # Remove
        if not target_font.multi_font:
            
            try:
                default_font =  bpy.data.fonts["Bfont Regular"]
            except KeyError:
                default_font = None
                
            active_datas.font_bold = active_datas.font_italic =\
            active_datas.font_bold_italic = default_font
        
            self.report({'INFO'}, "Font family removed")
            return {'FINISHED'}
        
        # Bold
        if target_font.bold_font_name:
            bold_font = pr.get_font_datablock(
                fonts[target_font.bold_font_name],
                debug,
            )
            active_datas.font_bold = bold_font
            
        # Italic_font
        if target_font.italic_font_name:
            italic_font = pr.get_font_datablock(
                fonts[target_font.italic_font_name],
                debug,
            )
            active_datas.font_italic = italic_font
            
        # Bold Italic font
        if target_font.bold_italic_font_name:
            bold_italic_font = pr.get_font_datablock(
                fonts[target_font.bold_italic_font_name],
                debug,
            )
            active_datas.font_bold_italic = bold_italic_font
        
        self.report({'INFO'}, "Font family loaded")
            
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_load_font_family)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_load_font_family)
