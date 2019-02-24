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
        #get addon prefs
        addon_preferences = get_addon_preferences()
        rownumber = addon_preferences.row_number
        fplist = addon_preferences.font_folders
        activedata = bpy.context.active_object.data
        wm = bpy.data.window_managers['WinMan']
        
        if len(fplist)==0:
            layout.label(text = 'Add Font Folder in Addon Preference', icon = 'INFO')
        else:
            row = layout.row(align = True)
            row.operator("fontselector.modal_refresh", text = "", icon = 'FILE_REFRESH')
            if wm.fontselector_list == 0 :
                row = layout.row()
                row.label(text = 'Refresh to get List of available Fonts', icon = 'INFO')
            else: 
                row.operator("fontselector.check_changes", text = '', icon = 'OUTLINER_OB_LIGHT')
                row.separator()
                row.operator("fontselector.remove_unused", text = "", icon = 'UNLINKED')

                ### OLD OVERRIDE ###
                #row.separator()
                #row.prop(wm, 'fontselector_folder_override', text = '', icon = 'FILESEL', icon_only = True)
                #if activedata.fontselector_override :
                #    row.operator('fontselector.load_fontlist', text = '', icon ='CANCEL')
                #else :
                #    row.operator('fontselector.override_folder', text = '', icon ='HAND')
                #row.label(text = wm.fontselector_foldername_override)
                row = layout.row()
                row.template_list("FontUIList", "", wm, "fontselector_list", activedata, "fontselector_index", rows = rownumber)

                ### OLD OVERRIDE ###
                #if not activedata.fontselector_override :
                #    row.template_list("FontUIList", "", wm, "fontselector_list", activedata, "fontselector_index", rows = rownumber)
                #else :
                #    row.label(text = 'Folder Override', icon = 'INFO')
                #    row.separator()
                #    row.operator('fontselector.install_font', text = '', icon = 'FILE_FONT')
                #    row = layout.row()
                #    row.template_list("FontUIList", "", wm, "fontselector_list", activedata, "fontselector_override_index", rows = rownumber)