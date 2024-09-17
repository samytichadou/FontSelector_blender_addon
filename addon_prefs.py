import bpy


class FONTSELECTOR_PF_addon_prefs(bpy.types.AddonPreferences) :
    bl_idname = __package__

    def draw(self, context) :
        layout = self.layout
            

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PF_addon_prefs)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PF_addon_prefs)
