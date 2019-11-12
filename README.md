# FontSelector_blender_addon

Font Selector is a simple addon to add font functionality to blender.

It allows you to dynamically visualize available fonts applied to a text object without the painful process of importing a font through filebrowser.



Here are Font Selector's features :

- Font Folders configuration : the addon allows you to setup several font folder on your computer through the addon user preferences. Sudirectories of the font folders will also be scanned for fonts. If you have uninstalled fonts on this computer, you can use them aside installed fonts, just create several font folders. You can save this configuration in an external file, in case you uninstall the addon, and want to keep track of your font folders. The external file is in a simple txt file, stored in a custom folder (by default in config folder of blender, you can change this through user preferences of the addon). This means you can load a previous font folder configuration in one click, in case you uninstalled your addon...

- Browse dynamically through fonts without leaving the 3D view and with direct visualisation of the font on active text object, like in any other compositing and editing software

- Refresh operator checks for you all available fonts in your font folders and subdirectories. It may take some time, but the result will be externally stored in your prefs folder. You don't have to do it again, except if you installed (or add) or uninstalled (or remove) fonts in your font folders

- Favorites font system : because browsing through hundred of fonts can be painful, you can mark fonts as favorites, these favorites fonts can be easily access by turning on the favorite filter !

- Export Favorites Fonts : If you have to go work somewhere else and want to bring your favorites fonts with you, go to export (under File in the Info Panel) and export them in a zip file !

- Remove unused Fonts : To work, the addon has to create an extra vector font datablock (extra font imported) and replace it when you browse from font to font. This leads to an unused datablock at the end of the day. A simple Operator allows you to remove it quickly !

- Choose the default size of the Font List (number of row) in the addon preferences. If you use only a few favorite fonts, no need for a huge panel !

- Origin directories and subdirectories of the font are stored, you can display them in the classic list, or toggle with the subdirectory Mode, organising the fonts by these directories !

- The addon now filtered the corrupted font file out, and store their name in a file in order to not try to import them again ! You can manually add some font to filter through the addon preferences !
