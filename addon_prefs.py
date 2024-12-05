import bpy
import os


# TODO Custom paths


class FONTSELECTOR_PF_addon_prefs(bpy.types.AddonPreferences) :
    bl_idname = __package__
    
    preferences_folder: bpy.props.StringProperty(
        name = "Preferences folder",
        default = os.path.join(
            os.path.join(
                bpy.utils.resource_path("USER"),
                "datafiles"
            ),
            "font_selector"
        ),
        description="Where Font Selector store configuration files",
        subtype="DIR_PATH",
    )
    debug : bpy.props.BoolProperty(
        name = "Debug",
    )
    viewport_popover : bpy.props.BoolProperty(
        name = "3D Viewport Popover",
        default = True,
    )
    properties_panel : bpy.props.BoolProperty(
        name = "Font Properties Panel",
    )
    sequencer_popover : bpy.props.BoolProperty(
        name = "Sequencer Popover",
        default = True,
    )
    sequencer_panel : bpy.props.BoolProperty(
        name = "Sequencer Properties Panel",
    )
    popup_operator : bpy.props.BoolProperty(
        name = "Pop Up Operator",
    )


    def draw(self, context) :
        layout = self.layout
        
        row = layout.row()
        row.prop(self, "preferences_folder", text="Preferences")
        sub = row.row()
        sub.alignment = "RIGHT"
        sub.prop(self, "debug")
        
        box = layout.box()
        box.label(text="UI")
        col = box.column(align=True)
        col.prop(self, "viewport_popover")
        col.prop(self, "properties_panel")
        col.separator()
        col.prop(self, "sequencer_popover")
        col.prop(self, "sequencer_panel")
        col.separator()
        col.prop(self, "popup_operator")
        

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PF_addon_prefs)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PF_addon_prefs)
