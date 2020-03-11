import bpy

from bpy.types import Panel

from.preferences import get_addon_preferences

# Properties Panel GUI
class FONTSELECTOR_PT_propertiespanel(Panel):
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
        activedata = context.active_object.data
        draw_general_gui(layout, activedata)

# Sequencer Panel GUI
class FONTSELECTOR_PT_sequencerpanel(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Strip"
    bl_label = "Font Selection"
    #bl_parent_id = "SEQUENCER_PT_effect"
    #bl_options = {'DEFAULT_CLOSED'}

    @staticmethod
    def has_sequencer(context):
        return (context.space_data.type in {'SEQUENCER', 'SEQUENCER_PREVIEW'})

    @classmethod
    def poll(cls, context):
        if not cls.has_sequencer(context): return False
        try :
            strip = context.scene.sequence_editor.active_strip
            strip.name
        except AttributeError:
            return False

        return strip.type == 'TEXT'


    def draw(self, context):
        layout = self.layout
        activedata = context.scene.sequence_editor.active_strip
        draw_general_gui(layout, activedata)


# general GUI
def draw_general_gui(layout, activedata):
    layout.use_property_split = True # Active single-column layout
    
    #get addon prefs
    addon_preferences = get_addon_preferences()
    debug = addon_preferences.debug_value
    rownumber = addon_preferences.row_number
    fplist = addon_preferences.font_folders
    
    wm = bpy.context.window_manager
    
    # no list
    if len(wm.fontselector_list) == 0 :
        row = layout.row()
        row.label(text = 'Refresh to get List of available Fonts', icon = 'INFO')
        row = layout.row()
        if wm.fontselector_isrefreshing :
            row.operator('fontselector.refresh_toggle', icon = 'CANCEL')
        else :
            row.operator('fontselector.refresh_toggle', icon = 'FILE_REFRESH')

    else: 
        if activedata.fontselector_font_missing :
            row = layout.row()
            row.label(text = "Missing : " + activedata.fontselector_font, icon = "ERROR")

        if activedata.fontselector_desync_font :
            row = layout.row()
            if activedata.font is not None:
                row.label(text = "Desync Font : " + activedata.font.name, icon = "ORPHAN_DATA")
            else:
                row.label(text = "Desync Font", icon = "ORPHAN_DATA")

        # debug font
        if debug :
            box = layout.box()
            box.label(text = "DEBUG")
            row = box.row()
            row.label(text = "font : " + activedata.fontselector_font)
            row = box.row()
            row.label(text = "index : " + str(activedata.fontselector_index))
            row = box.row()
            row.label(text = "avoid : " + str(activedata.fontselector_avoid_changes))

        col = layout.column(align=True)
        row = col.row()
        row.prop(wm, 'fontselector_search', text="", icon='VIEWZOOM')

        row = col.row()
        row.template_list("FONTSELECTOR_UL_uilist", "", wm, "fontselector_list", activedata, "fontselector_index", rows = rownumber)

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=True)
        row = flow.row(align = True)
        if wm.fontselector_isrefreshing :
            row.operator('fontselector.refresh_toggle', icon = 'CANCEL')
        else :
            row.operator('fontselector.refresh_toggle', icon = 'FILE_REFRESH')
        row = flow.row(align = True)
        row.operator("fontselector.check_changes", text = "Check", icon = 'OUTLINER_OB_LIGHT')
        row = flow.row(align = True)
        row.operator("fontselector.remove_unused", text = "Clean", icon = 'UNLINKED')

# popover 3d view function
def popover_view3d_function(self, context):
    if bpy.context.active_object is not None and bpy.context.active_object.type == 'FONT':
        self.layout.popover(
                panel="FONTSELECTOR_PT_propertiespanel",
                #icon='FILE_FONT',
                text="Font",
            )