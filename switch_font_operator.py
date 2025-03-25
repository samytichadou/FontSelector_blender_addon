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
        if context.area.type == "SEQUENCE_EDITOR":
            return context.active_strip
        else:
            return context.active_object

    def execute(self, context):

        debug = get_addon_preferences().debug

        families = context.window_manager.fontselector_properties.font_families

        # 3D Object or Video strip
        if context.area.type == "SEQUENCE_EDITOR":
            active_object_props = context.active_strip.fontselector_object_properties
        else:
            active_object_props = context.active_object.data.fontselector_object_properties

        family = families[active_object_props.family_index]
        current_type = active_object_props.family_types
        available_types = get_enum_values(
            active_object_props,
            "family_types",
        )

        # Switch active object, selected objects will follow automatically
        # Next
        if not self.previous:

            # End of available types
            if available_types.index(current_type) >= len(available_types) - 1:
                # Set family
                if active_object_props.family_index == len(families)-1:
                    # Last family, set first family
                    active_object_props.family_index = 0
                else:
                    # Set next family
                    active_object_props.family_index += 1

            # Next type
            else:
                next_type = available_types[available_types.index(current_type)+1]
                active_object_props.family_types = next_type

        # Previous
        else:

            # End of available types
            if available_types.index(current_type) == 0:
                # Set family
                if active_object_props.family_index == 0:
                    # First family, set last family
                    active_object_props.family_index = len(families)-1
                else:
                    # Set previous family
                    active_object_props.family_index -= 1
                # Set last type
                available_types = get_enum_values(
                    active_object_props,
                    "family_types",
                )
                previous_type = available_types[len(available_types)-1]
                active_object_props.family_types = previous_type


            # Next type
            else:
                # Set previous type
                previous_type = available_types[available_types.index(current_type)-1]
                active_object_props.family_types = previous_type

        if debug:
            print("FONT SELECTOR --- Font switched")

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(FONTSELECTOR_OT_switch_font)

def unregister():
    bpy.utils.unregister_class(FONTSELECTOR_OT_switch_font)
