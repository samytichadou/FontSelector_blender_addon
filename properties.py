import bpy
    
    
class FONTSELECTOR_PR_fonts_properties(bpy.types.PropertyGroup):
    
    filepath : bpy.props.StringProperty(
        name = "Filepath",
        )
    favorite : bpy.props.BoolProperty(
        name = "Favorite",
        )
    font_family : bpy.props.StringProperty(
        name = "Font Family",
        )
    font_type : bpy.props.StringProperty(
        name = "Font Type",
        )


class FONTSELECTOR_PR_properties(bpy.types.PropertyGroup):

    font_index : bpy.props.IntProperty()
    font_search : bpy.props.StringProperty()
    
    fonts : bpy.props.CollectionProperty(
        type=FONTSELECTOR_PR_fonts_properties,
        )

### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_PR_fonts_properties)
    bpy.utils.register_class(FONTSELECTOR_PR_properties)
    bpy.types.WindowManager.fontselector_properties = \
        bpy.props.PointerProperty(
            type = FONTSELECTOR_PR_properties,
            name="Font Selector Properties",
        )

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_PR_fonts_properties)
    bpy.utils.unregister_class(FONTSELECTOR_PR_properties)
    del bpy.types.WindowManager.fontselector_properties
