import bpy


class FontSelectorRemoveUnused(bpy.types.Operator):
    bl_idname = "fontselector.remove_unused"
    bl_label = "Remove unused Fonts"
    bl_description = "Remove Unused Fonts form Blend file"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        flist=bpy.data.fonts
        return len(flist)>0
    
    def execute(self, context):
        flist=bpy.data.fonts
        n=0
        for f in flist:
            if f.users==0:
                n=n+1
                bpy.data.fonts.remove(f, do_unlink=True)
        
        if n>0:
            info = str(n)+' unused Font(s) removed'
            self.report({'INFO'}, info)  
        else:
            info = 'No unused Font to remove'
            self.report({'INFO'}, info)      
            
        return {'FINISHED'}