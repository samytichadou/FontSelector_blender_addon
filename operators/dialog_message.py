import bpy

from ..global_messages import *

### CODES ###
# 1 = startup changes in font folder message
# 2 = error subdirectory font folder doesn't exist anymore
# 3 = saved font folders with deleted inexistent folder
# 4 = unable to save font folder, no existent one
# 5 = font installed, refreshing invitation
# 6 = persmission denied for font installation

class FontSelectorDialogMessage(bpy.types.Operator):
    bl_idname = "fontselector.dialog_message"
    bl_label = "FontSelector Dialog"
    bl_options = {'INTERNAL'}
 
    code = bpy.props.IntProperty()
    customstring = bpy.props.StringProperty()
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        # startup changes in font folder message
        if self.code == 1 :
            self.layout.label(changes_msg, icon = 'ERROR')
            self.layout.operator("fontselector.modal_refresh", icon='FILE_REFRESH')
        
        # error subdirectory font folder doesn't exist anymore
        elif self.code == 2 :
            self.layout.label(subdirectory_error, icon = 'ERROR')
            self.layout.label(changes_msg)
            self.layout.operator("fontselector.modal_refresh", icon='FILE_REFRESH')

        # saved font folders with deleted inexistent folder
        elif self.code == 3 :
            self.layout.label(fontfolder_saved)
            self.layout.label(fontfolder_deleted, icon = 'ERROR')
            for folder in self.customstring.split(", ") :
                self.layout.label(folder)

        # unable to save font folder, no existent one
        elif self.code == 4 :
            self.layout.label(fontfolder_not_saved, icon = 'ERROR')
            self.layout.label(fontfolder_deleted)
            for folder in self.customstring.split(", ") :
                self.layout.label(folder)

        # font installed, refreshing invitation
        elif self.code == 5 :
            self.layout.label(font_installed, icon = 'INFO')
            self.layout.operator("fontselector.modal_refresh", icon='FILE_REFRESH')
        
        # persmission denied for font installation
        elif self.code == 6 :
            self.layout.label(permission_denied, icon = 'ERROR')
            self.layout.label(self.customstring)