import bpy

    
#update change font
def update_change_font(self, context):
    bpy.ops.fontselector.change()
    
#update save favorites
def update_save_favorites(self, context):
    active=bpy.context.active_object
    if active is not None:
        if active.type=='FONT':
            bpy.ops.fontselector.save_favorites()
    
#update list for favorite filter
def update_favorite_filter(self, context):
    bpy.ops.fontselector.filter_favorites()
    
#update list for subdir filter
def update_subdir_filter(self, context):
    bpy.ops.fontselector.filter_subdirfonts()
    
#update lists when toggling subdir
def update_subdir_toggle(self, context):
    active=bpy.context.active_object
    if active is not None:
        if active.type=='FONT':
            bpy.ops.fontselector.filter_favorites()