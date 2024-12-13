### Version 3

#### V3 TO DO 
- [ ] Blender extension feedbacks
- [ ] Up and running on Blender extension

#### V3 DONE
- [x] Video tutorial
- [x] Reveal file operator does not work with windows on C:\windows\Fonts  
- [x] Update readme  
- [x] Relink error
- [x] no multi component filter if strip
- [x] Switch font op : Video strip
- [x] Switch font op : All selected objects
- [x] Load family : Store relink infos if needed (regular only)  
- [x] Load family : Apply to all selected objects  
- [x] Remove or not blender bold ital... slots if font change (mode, bool in prefs ?)  
- [x] Add help for multi font  
- [x] Remove multi_component family if not regular  
- [x] Remove blender font type if not needed  
- [x] Load family : Remove font type if not available (no regular) with modifier key ?  
- [x] Family logic  
- [x] Remove loading (and loading bar)  
- [x] Code rewrite  
- [x] Use python wheels (fonttools) to get font infos  
- [x] Reveal font in explorer operator  
- [x] Global switch font op to switch between families AND type of fonts with one button  
- [x] Improve search with individual fonts/filepath inside a family  
- [x] Operator to load a font family into specific blender font slot (bold ita...)  

### Long run
- [ ] Bug report for `INTERNAL` `bl_options` with popover (properties and INTERNAL operators)
- [ ] Fix global search menu random entries from popover  
- [ ] Export favorite fonts operator  
- [ ] Copy selected fonts in clipboard (python wheels ?)  

### Blender extension feedbacks
- [ ] There are lot of places where slashes are used like C:/Windows/Fonts. Usually we disallow this because it can cause problems on platforms, but I'm not sure here since they're platform-specific already. But you'll probably know this better than me, is it possible that user installs Windows, and therefore fonts folder on other disk? Can this be made safer with os module maybe?

- [ ] I see that add-on stores (by default) config files in datafiles folder. This is not really encouraged and can cause some problems. I will advise to use bpy.utils.extension_path_user to create safe, writeable directory specific to the add-on and store everything there. I also don't think this needs to be user preference anymore if you use this path.

- [ ] I see "Reveal File" operator which is not needed IMO. In Blender if you explore FILEPATH or DIRPATH properties alt or shift-clicking on them (icon) opens folder. I think it will be better if you use that instead, will save you some headaches.

- [ ] I would also recommend using layout.panel for creating dropdown Font Info instead of box with custom dropdown, should make UI more responsive and fast.

- [ ] Tags seem little excessive, I think "Import-Export" and "System" are enough.
