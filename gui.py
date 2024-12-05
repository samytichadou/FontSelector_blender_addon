import bpy

from .addon_prefs import get_addon_preferences


# TODO Fix search menu errors
# TODO Add help for multi font 


def draw_font_infos(container, active, context):
    
    debug = get_addon_preferences().debug
    
    fonts = context.window_manager.fontselector_properties.fonts
    font = fonts[active.font_index]
    
    row = container.row(align=True)
    if active.show_font_infos:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    row.prop(
        active,
        "show_font_infos",
        text = "",
        icon = icon,
        emboss = False,
    )
    row.label(text = "Font Infos")
    
    if active.show_font_infos:
    
        split = container.split(factor=0.2)
        col = split.column(align=True)
        col2 = split.column(align=True)
        col2.alignment = "RIGHT"
        
        col.label(text = "Name")
        col2.label(text = font.name)

        col.label(text = "Family")
        col2.label(text = font.font_family)

        col.label(text = "Type")
        col2.label(text = font.font_type)
        
        if debug:
            col.label(text = "Multi Font")
            col2.label(text = str(font.multi_font))
        
            col.label(text = "Component")
            col2.label(text = str(font.multi_font_component))

        col.label(text = "Path")
        op = col2.operator(
            "fontselector.reveal_file",
            text = font.filepath,
            icon = "FILEBROWSER",
        )
        op.filepath = font.filepath
        
        if font.bold_font_name:
            filepath = fonts[font.bold_font_name].filepath
            col.label(text = "Bold")
            op = col2.operator(
                "fontselector.reveal_file",
                text = filepath,
                icon = "FILEBROWSER",
            )
            op.filepath = filepath
        
        if font.italic_font_name:
            filepath = fonts[font.italic_font_name].filepath
            col.label(text = "Italic")
            op = col2.operator(
                "fontselector.reveal_file",
                text = filepath,
                icon = "FILEBROWSER",
            )
            op.filepath = filepath
        
        if font.bold_italic_font_name:
            filepath = fonts[font.bold_italic_font_name].filepath
            col.label(text = "Bold Italic")
            op = col2.operator(
                "fontselector.reveal_file",
                text = filepath,
                icon = "FILEBROWSER",
            )
            op.filepath = filepath
    

### Fontselector common panel UI ###
def draw_font_selector(self, context):

    layout = self.layout

    if self.strip:
        active_datas = context.active_sequence_strip.fontselector_object_properties
    else:
        active_datas = context.active_object.data.fontselector_object_properties

    props = context.window_manager.fontselector_properties

    single = get_addon_preferences().single_font_mode
    
    # Single font mode
    if single:

        # No available font
        if not props.fonts:
            row = layout.row(align=True)
            row.label(text = "No Fonts, please reload", icon = "INFO")
            row.operator("fontselector.reload_fonts", text="", icon="FILE_REFRESH")
            return

        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(active_datas, "font_search", text="", icon='VIEWZOOM')
        row.operator("fontselector.reload_fonts", text="", icon="FILE_REFRESH")

        row = col.row()
        if self.strip:
            uilist = "FONTSELECTOR_UL_uilist_strip"
        else:
            uilist = "FONTSELECTOR_UL_uilist_object"
        row.template_list(
            uilist,
            "",
            props,
            "fonts",
            active_datas,
            "font_index",
            rows = 5,
        )

        # Font infos
        if active_datas.font_index >=0\
        and active_datas.font_index < len(props.fonts):
            box = col.box()
            draw_font_infos(
                box,
                active_datas,
                context,
            )

    # Family font mode
    else:

        # No available family
        if not props.font_families:
            row = layout.row(align=True)
            row.label(text = "No Fonts, please reload", icon = "INFO")
            row.operator("fontselector.reload_fonts", text="", icon="FILE_REFRESH")
            return

        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(active_datas, "font_search", text="", icon='VIEWZOOM')

        row.separator()

        row.operator(
            "fontselector.switch_font",
            text = "",
            icon = "TRIA_LEFT",
        ).previous = True
        row.operator(
            "fontselector.switch_font",
            text = "",
            icon = "TRIA_RIGHT",
        ).previous = False

        row.separator()
        row.operator(
            "fontselector.reload_fonts",
            text="",
            icon="FILE_REFRESH",
        )

        row = col.row()
        if self.strip:
            uilist = "FONTSELECTOR_UL_family_uilist_strip"
        else:
            uilist = "FONTSELECTOR_UL_family_uilist_object"
        row.template_list(
            uilist,
            "",
            props,
            "font_families",
            active_datas,
            "family_index",
            rows = 5,
        )

        row = col.row()
        row.prop(active_datas, "family_types", text = "")
        # font_nb = len(props.font_families[active_datas.family_index].fonts)
        # if font_nb <= 4:
        #     row.prop(active_datas, "family_types", expand = True)
        # else:


class FONTSELECTOR_panel(bpy.types.Panel):
    bl_label = "Font Selection"
    
    strip = False
    
    def draw(self, context):
        
        draw_font_selector(self, context)

   
### 3D Viewport ###

def poll_viewport(context):
    active = context.active_object
    if active is not None:
        return context.active_object.type == "FONT"
    return False
        
# 3D Viewport popover
def viewport_popover_draw(self, context):
    if get_addon_preferences().viewport_popover\
    and poll_viewport(context):
        self.layout.separator()
        self.layout.popover(panel="FONTSELECTOR_PT_viewport_popover", text="", icon="FILE_FONT")
        
class FONTSELECTOR_PT_viewport_popover(FONTSELECTOR_panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 14
    
    @classmethod
    def poll(cls, context):
        if get_addon_preferences().viewport_popover:
            return poll_viewport(context)
        
    
# Properties Panel GUI
class FONTSELECTOR_PT_properties_panel(FONTSELECTOR_panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Font Selector"
    bl_context = "data"
    bl_label = "Font Selection"
    
    @classmethod
    def poll(cls, context):
        if get_addon_preferences().properties_panel:
            return poll_viewport(context)


### Sequencer ###

def poll_sequencer(context):
    active = context.active_sequence_strip
    if active is not None:
        return active.type == 'TEXT'
    return False

# Sequencer popover
def sequencer_popover_draw(self, context):
    if get_addon_preferences().sequencer_popover\
    and poll_sequencer(context):
        self.layout.popover(panel="FONTSELECTOR_PT_sequencer_popover", text="", icon="FILE_FONT")
        
class FONTSELECTOR_PT_sequencer_popover(FONTSELECTOR_panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 14
    
    strip = True
    
    @classmethod
    def poll(cls, context):
        if get_addon_preferences().sequencer_popover:
            return poll_sequencer(context)

# Sequencer Panel GUI
class FONTSELECTOR_PT_sequencer_panel(FONTSELECTOR_panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_parent_id = "SEQUENCER_PT_effect"
    bl_category = "Strip"
    bl_label = "Font Selection"
    
    strip = True
    
    @classmethod
    def poll(cls, context):
        if get_addon_preferences().sequencer_panel:
            return poll_sequencer(context)


### Popup Operator ###
class FONTSELECTOR_OT_popup(bpy.types.Operator):
    bl_idname = "fontselector.popup"
    bl_label = "Font Selection"

    strip = False
    
    @classmethod
    def poll(cls, context):
        if not get_addon_preferences().popup_operator:
            return False
        if (
            context.area.type == "SEQUENCE_EDITOR"\
            and poll_sequencer(context)
        ) or poll_viewport(context):
            return True

    def invoke(self, context, event):
        if context.area.type == "SEQUENCE_EDITOR":
            self.strip = True
        return context.window_manager.invoke_props_dialog(self, width=300)
 
    def draw(self, context):
        draw_font_selector(self, context)

    def execute(self, context):
        return {'FINISHED'}

        
### REGISTER ---
def register():
    bpy.types.VIEW3D_MT_editor_menus.append(viewport_popover_draw)
    bpy.utils.register_class(FONTSELECTOR_PT_viewport_popover)
    bpy.utils.register_class(FONTSELECTOR_PT_properties_panel)
    
    bpy.types.SEQUENCER_MT_editor_menus.append(sequencer_popover_draw)
    bpy.utils.register_class(FONTSELECTOR_PT_sequencer_popover)
    bpy.utils.register_class(FONTSELECTOR_PT_sequencer_panel)
    bpy.utils.register_class(FONTSELECTOR_OT_popup)

def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(viewport_popover_draw)
    bpy.utils.unregister_class(FONTSELECTOR_PT_viewport_popover)
    bpy.utils.unregister_class(FONTSELECTOR_PT_properties_panel)
    
    bpy.types.SEQUENCER_MT_editor_menus.remove(sequencer_popover_draw)
    bpy.utils.unregister_class(FONTSELECTOR_PT_sequencer_popover)
    bpy.utils.unregister_class(FONTSELECTOR_PT_sequencer_panel)
    bpy.utils.unregister_class(FONTSELECTOR_OT_popup)
