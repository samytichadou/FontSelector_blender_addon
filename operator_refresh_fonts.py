import bpy
import csv
import os

from .preferences import get_addon_preferences
from .misc_functions import create_prefs_folder


class FontSelectorRefresh(bpy.types.Operator):
    bl_idname = "fontselector.refresh"
    bl_label = "Refresh List"
    bl_description = "Refresh Available Fonts from Font Folders\nOperation can take some time, see console for progression"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        #get addon prefs
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        return len(fplist)>0 and prefs!=""
    
    def execute(self, context):
        #get addon prefs
        dlist = bpy.data.fonts
        addon_preferences = get_addon_preferences()
        fplist = addon_preferences.font_folders
        prefs = addon_preferences.prefs_folderpath
        prefpath = os.path.abspath(bpy.path.abspath(prefs))
        preffav = os.path.join(prefpath, "fontselector_favorites")
        prefflist = os.path.join(prefpath, "fontselector_fontlist")
        preffilter = os.path.join(prefpath, "fontselector_filter")
        prefsubdir = os.path.join(prefpath, "fontselector_subdir")
        fontlist=bpy.data.window_managers['WinMan'].fontselector_list
        extlist=[".otf", ".otc", ".ttf", ".ttc", ".tte", ".pfb", ".dfont", ".OTF", ".OTC", ".TTF", ".TTC", ".TTE", ".DFONT", ".PFB"]
        dupelist=[]
        subdir=[]
        filterlist=[]
        
        #get filters
        if os.path.isdir(prefpath) == True :
            if os.path.isfile(preffilter) == True :
                with open(preffilter, 'r', newline='') as csvfile :
                    line = csv.reader(csvfile, delimiter='\n')
                    for l in line:
                        l1=str(l).replace("[", "")
                        l2=l1.replace("]", "")
                        l3=l2.replace("'", "")
                        l4=l3.replace('"', "")
                        filterlist.append(l4)

        #clean unused
        if len(dlist) > 0:
            bpy.ops.fontselector.remove_unused()
        
        #check if external folder exist and create it if not
        create_prefs_folder
        
        #clear list
        if len(fontlist)>=1:
            for i in range(len(fontlist)-1,-1,-1):
                fontlist.remove(i)
        
        chk=0
        chk2=0
        for fp in fplist:
            path=os.path.abspath(bpy.path.abspath(fp.folderpath))
            if fp.folderpath!="":
                if os.path.isdir(path)==True:
                    chk=1
                    nbfile=0
                    nbft=0
                    for dirpath, dirnames, files in os.walk(path):
                        for f3 in files:
                            exte=os.path.splitext(f3)[1]
                            if any(exte==ext for ext in extlist):
                                nbfile=nbfile+1
                        for f2 in os.listdir(dirpath):
                            filename, file_extension = os.path.splitext(f2)
                            if any(file_extension==ext for ext in extlist) and dirpath not in subdir:
                                subdir.append(dirpath)
                    for d in subdir:
                        for file in os.listdir(d):
                            filename, file_extension = os.path.splitext(file)
                            #mac exception for corrupted font
                            if file not in filterlist:
                                if any(file_extension==ext for ext in extlist):
                                    chk2=1
                                    chk3=0
                                    for font in bpy.data.fonts:
                                        fname=os.path.basename(os.path.abspath(bpy.path.abspath(font.filepath)))
                                        if os.path.join(d, file)==os.path.abspath(bpy.path.abspath(font.filepath)) or file==fname:
                                            chk3=1
                                    if chk3==0:
                                        try:
                                            nbft=nbft+1
                                            bpy.data.fonts.load(filepath=os.path.join(d, file))
                                            print(str(nbft)+"/"+str(nbfile)+" fonts treated --- "+file+" imported")
                                        except RuntimeError:
                                            nbft=nbft+1
                                            filterlist.append(file)
                                            print(str(nbft)+"/"+str(nbfile)+" fonts treated --- "+file+" corrupted, filtered out")
                            
        if chk==1 and chk2==1:      
            nfile = open(prefflist, "w")
            for f in bpy.data.fonts:
                chkd=0
                for d in dupelist:
                    if os.path.abspath(bpy.path.abspath(f.filepath))==d:
                        chkd=1
                if chkd==0:
                    nfpath=os.path.abspath(bpy.path.abspath(f.filepath))
                    nfile.write(f.name+" || "+nfpath+' || '+os.path.basename(os.path.dirname(nfpath))+"\n")
                    dupelist.append(nfpath)
                if f.users==0:
                    bpy.data.fonts.remove(f, do_unlink=True)
            nfile.close()
            if os.path.isfile(prefflist)==True:
                bpy.ops.fontselector.load_fontlist()
                info='Font Selector Warning : Font List refreshed'
                print(info)
                self.report({'INFO'}, info)
            if os.path.isfile(preffav)==True:
                bpy.ops.fontselector.load_favorites()

        elif chk==0:
            info = 'No valid Font Folder, check Preferences'
            self.report({'ERROR'}, info)  
            
        elif chk2==0:
            info = 'No valid Font in Folders, check Preferences'
            self.report({'ERROR'}, info)
            
        #write filterlist
        if len(filterlist)!=0:
            if os.path.isdir(prefpath)==False:
                os.makedirs(prefpath)
            nfile2 = open(preffilter, "w")
            for f in filterlist:
                nfile2.write(f+"\n")
            nfile2.close()
            
        #write subdir list
        if len(subdir)!=0:
            if os.path.isdir(prefpath)==False:
                os.makedirs(prefpath)
            nfile3 = open(prefsubdir, "w")
            for d in subdir:
                nfile3.write(os.path.basename(d)+"\n")
            nfile3.close()
            bpy.ops.fontselector.load_fontsubs()
            
        return {'FINISHED'}