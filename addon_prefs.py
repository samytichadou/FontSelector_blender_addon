import bpy
import os

# --- 1. DATENSTRUKTUR FÜR EINEN ORDNER ---
class FONTSELECTOR_PG_custom_folder(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        name="Path",
        description="Zusätzlicher Ordner, der beim Font-Scan berücksichtigt wird",
        subtype="DIR_PATH",
        default="",
    )

# --- 2. OPERATOR: ORDNER HINZUFÜGEN ---
class FONTSELECTOR_OT_add_folder(bpy.types.Operator):
    bl_idname = "fontselector.add_folder"
    bl_label = "Add Font Folder"
    bl_description = "Fügt einen neuen Ordner-Pfad hinzu"
    
    def execute(self, context):
        get_addon_preferences().custom_font_folders.add()
        return {'FINISHED'}

# --- 3. OPERATOR: ORDNER ENTFERNEN ---
class FONTSELECTOR_OT_remove_folder(bpy.types.Operator):
    bl_idname = "fontselector.remove_folder"
    bl_label = "Remove Font Folder"
    bl_description = "Entfernt diesen Ordner-Pfad"
    
    index: bpy.props.IntProperty() # Speichert, welcher Ordner gelöscht werden soll
    
    def execute(self, context):
        get_addon_preferences().custom_font_folders.remove(self.index)
        return {'FINISHED'}


# --- 4. DEINE ANGEPASSTEN PREFERENCES ---
class FONTSELECTOR_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    # HIER: Die neue CollectionProperty nutzt unsere PropertyGroup von oben
    custom_font_folders: bpy.props.CollectionProperty(
        type=FONTSELECTOR_PG_custom_folder
    )
    
    preferences_folder: bpy.props.StringProperty(
        name = "Preferences folder",
        default = bpy.utils.extension_path_user(str(__package__)),
        description="Where Font Selector store configuration files",
        subtype="DIR_PATH",
    )
    debug : bpy.props.BoolProperty(
        name = "Debug",
    )
    viewport_popover : bpy.props.BoolProperty(
        name = "3D Viewport Popover",
    )
    properties_panel : bpy.props.BoolProperty(
        name = "Font Properties Panel",
        default = True,
    )
    sequencer_popover : bpy.props.BoolProperty(
        name = "Sequencer Popover",
    )
    sequencer_panel : bpy.props.BoolProperty(
        name = "Sequencer Properties Panel",
        default = True,
    )
    popup_operator : bpy.props.BoolProperty(
        name = "Pop Up Operator",
    )

    def draw(self, context):
        layout = self.layout
        
        # --- UI für die Custom Folders ---
        box = layout.box()
        box.label(text="Custom Font Folders:", icon='FILE_FOLDER')
        
        # Alle gespeicherten Ordner auflisten
        for i, folder in enumerate(self.custom_font_folders):
            row = box.row()
            row.prop(folder, "path", text="")
            # X-Button zum Löschen der jeweiligen Zeile
            op = row.operator("fontselector.remove_folder", text="", icon='X')
            op.index = i
            
        # Plus-Button zum Hinzufügen einer neuen Zeile
        box.operator("fontselector.add_folder", text="Add Folder", icon='ADD')
        # ---------------------------------
        
        layout.separator()
        
        row = layout.row()
        row.prop(self, "preferences_folder", text="Preferences")
        sub = row.row()
        sub.alignment = "RIGHT"
        sub.prop(self, "debug")
        
        box_ui = layout.box()
        box_ui.label(text="UI")
        col = box_ui.column(align=True)
        col.prop(self, "viewport_popover")
        col.prop(self, "properties_panel")
        col.separator()
        col.prop(self, "sequencer_popover")
        col.prop(self, "sequencer_panel")
        col.separator()
        col.prop(self, "popup_operator")
        

def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)

# Alle Klassen müssen registriert werden (Reihenfolge ist wichtig!)
classes = (
    FONTSELECTOR_PG_custom_folder,
    FONTSELECTOR_OT_add_folder,
    FONTSELECTOR_OT_remove_folder,
    FONTSELECTOR_PF_addon_prefs,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
