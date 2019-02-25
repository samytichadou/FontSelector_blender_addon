import bpy

from.preferences import get_addon_preferences

class FontSelectorPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Font Selector"
    bl_context = "data"
    bl_label = "Font Selection"
    
    @classmethod
    def poll(cls, context):
        active=bpy.context.active_object
        if active is not None:
            active_type=active.type
        else:
            active_type=""
        return active_type=='FONT'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        
        #get addon prefs
        addon_preferences = get_addon_preferences()
        rownumber = addon_preferences.row_number
        fplist = addon_preferences.font_folders
        activedata = bpy.context.active_object.data
        wm = bpy.data.window_managers['WinMan']
        
        # no font folder
        if len(fplist)==0:
            layout.label(text = 'Add Font Folder in Addon Preference', icon = 'INFO')

        else:
            row = layout.row(align = True)
            row.operator("fontselector.modal_refresh", text = "", icon = 'FILE_REFRESH')

            # no list
            if len(wm.fontselector_list) == 0 :
                row = layout.row()
                row.label(text = 'Refresh to get List of available Fonts', icon = 'INFO')

            else: 
                row.operator("fontselector.check_changes", text = '', icon = 'OUTLINER_OB_LIGHT')
                row.separator()
                row.operator("fontselector.remove_unused", text = "", icon = 'UNLINKED')
                if activedata.fontselector_font_missing :
                    row.separator()
                    row.label(text = "Missing : " + activedata.fontselector_font, icon = "ERROR")

                row = layout.row()
                row.template_list("FontUIList", "", wm, "fontselector_list", activedata, "fontselector_index", rows = rownumber)