import bpy
import os


class FONTSELECTOR_PF_addon_prefs(bpy.types.AddonPreferences) :
    bl_idname = __package__
    
    preferences_folder: bpy.props.StringProperty(
        name="Font Selector Preferences folder",
        default=os.path.join(
            os.path.join(
                bpy.utils.resource_path("USER"),
                "datafiles"
            ),
            "font_selector"
        ),
        description="Where Font Selector store global preferences",
        subtype="DIR_PATH",
    )


    def draw(self, context) :
        layout = self.layout
        
        layout.prop(self, "preferences_folder", text = "Preference Folder")
        

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PF_addon_prefs)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PF_addon_prefs)
