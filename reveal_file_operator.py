import bpy
import platform
import os


def open_explorer(filepath):
    
    # Linux: Linux
    # Windows: Windows
    # Mac: Darwin
    osys = platform.system()
    
    if osys == "Windows":
        
        cmd = f"explorer /select {filepath}"
        
    elif osys == "Linux":
        
        cmd = 'dbus-send --session --dest=org.freedesktop.FileManager1 '
        cmd += '--type=method_call /org/freedesktop/FileManager1 '
        cmd += f'org.freedesktop.FileManager1.ShowItems array:string:"{filepath}" string:""'
        
    elif osys == "Darwin":
        
        cmd = f"open -R {filepath}"
        
    os.system(cmd)


class FONTSELECTOR_OT_reveal_file(bpy.types.Operator):
    """Reveal file in explorer"""
    bl_idname = "fontselector.reveal_file"
    bl_label = "Reveal File"
    bl_options = {'INTERNAL'}
    
    filepath : bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        # Invalid filepath
        if not os.path.isfile(self.filepath):
            self.report({'WARNING'}, "Invalid filepath")
            return {'CANCELLED'}
        
        open_explorer(self.filepath)
            
        self.report({'INFO'}, "File revealed")
            
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_reveal_file)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_reveal_file)

