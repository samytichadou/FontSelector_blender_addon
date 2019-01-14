import bpy

from .preferences import get_addon_preferences


#font list
class FontUIList(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        subdir=addon_preferences.prefs_show_subdir
        
        if item.missingfont==True:
            layout.label(icon='ERROR')
        layout.label(item.name)
        if subdir==True:
            layout.label(item.subdirectory)
        if item.favorite==True:
            layout.prop(item, "favorite", text="", icon='SOLO_ON', emboss=False, translate=False)
        else:
            layout.prop(item, "favorite", text="", icon='SOLO_OFF', emboss=False, translate=False)
            
#subdir list
class SubdirUIList(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        layout.label(item.name)