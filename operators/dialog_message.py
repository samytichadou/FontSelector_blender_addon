import bpy

from ..global_messages import *

### CODES ###
# 1 = startup changes in font folder message

class FontSelectorDialogMessage(bpy.types.Operator):
    bl_idname = "fontselector.dialog_message"
    bl_label = "FontSelector Dialog"
    bl_options = {'INTERNAL'}
 
    code = bpy.props.IntProperty()
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        # startup changes in font folder message
        if self.code == 1 :
            self.layout.label(changes_msg, icon = 'ERROR')
            self.layout.operator("fontselector.modal_refresh", icon='FILE_REFRESH')