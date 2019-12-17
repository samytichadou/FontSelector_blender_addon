import bpy,os,platform


# set default font folder
def setOs():
    wm = bpy.context.window_manager
    if platform.system() == "Windows": 
        wm.fontselector_os = 'WINDOWS'
    elif platform.system() == "Darwin":
        wm.fontselector_os = 'MAC'
    else:
        wm.fontselector_os = 'LINUX'