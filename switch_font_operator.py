import bpy

from .addon_prefs import get_addon_preferences


def get_enum_values(object, identifier):
    # Hacky way
    try:
        setattr(object, identifier, "")
    except Exception as e:
        return str(e).split("'")[1::2]

    return []


class FONTSELECTOR_OT_switch_font(bpy.types.Operator):
    """Switch to next/previous font, even in the same family)"""
    bl_idname = "fontselector.switch_font"
    bl_label = "Switch Font"
    bl_options = {'INTERNAL', 'UNDO'}

    previous : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        debug = get_addon_preferences().debug

        families = context.window_manager.fontselector_properties.font_families

        object_props = bpy.context.active_object.data.fontselector_object_properties
        # TODO Active datas from strip if needed
        # TODO Multiple selected objects

        family = families[object_props.family_index]
        current_type = object_props.family_types
        available_types = get_enum_values(
            object_props,
            "family_types",
        )

        # DEBUG
        print()
        print(family)
        print(current_type)
        print(available_types)
        print()
        print(available_types.index(current_type))
        print(len(available_types))
        print()

        # Switch

        # Next
        if not self.previous:

            # End of available types
            if available_types.index(current_type) >= len(available_types) - 1:
                # Set family
                if object_props.family_index == len(families)-1:
                    # Last family, set first family
                    object_props.family_index = 0
                else:
                    # Set next family
                    object_props.family_index += 1

            # Next type
            else:
                next_type = available_types[available_types.index(current_type)+1]
                object_props.family_types = next_type

        # Previous
        else:

            # End of available types
            if available_types.index(current_type) == 0:
                # Set family
                if object_props.family_index == 0:
                    # First family, set last family
                    object_props.family_index = len(families)-1
                else:
                    # Set previous family
                    object_props.family_index -= 1
                # Set last type
                available_types = get_enum_values(
                    object_props,
                    "family_types",
                )
                previous_type = available_types[len(available_types)-1]
                object_props.family_types = previous_type


            # Next type
            else:
                # Set previous type
                previous_type = available_types[available_types.index(current_type)-1]
                object_props.family_types = previous_type



        self.report({'INFO'}, "Font switched")

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_switch_font)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_switch_font)
