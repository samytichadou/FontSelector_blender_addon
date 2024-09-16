import bpy


class FONTSELECTOR_PR_properties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    filepath : bpy.props.StringProperty(
        name = "Filepath",
        )
    favorite : bpy.props.BoolProperty(
        name = "Favorite",
        )
    subdirectory : bpy.props.StringProperty(name="Subdirectory")


### REGISTER ---

def register():
    bpy.utils.register_class(FONTSELECTOR_PR_properties)
    bpy.types.WindowManager.fontselector_properties = \
        bpy.props.PointerProperty(
            type = FONTSELECTOR_PR_properties,
            name="Font Selector Properties",
        )

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PR_properties)
    del bpy.types.WindowManager.fontselector_properties
