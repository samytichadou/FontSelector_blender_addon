# FontSelector - Easy font management inside Blender

**Font Selector is an addon to add font functionalities to blender.**

It allows user to **dynamically visualize available fonts** applied to a text object without the painful process of importing a font through filebrowser.

[You can see the addon in action here.](https://makertube.net/w/2sxbKKHV8QWL8p5EACGn8T)

If you like this addon, you can help me [here](https://ko-fi.com/tonton_blender) through Donation, to buy me a coffee and allow me to continue to develop free tools.

Since version 3.0 of the addon, **it is now distributed as a blender extension**, user will have to install it accordingly, or download it through Blender extension platform : https://extensions.blender.org/

### Font Selector's features :

- **Automatic detection** of the font folders according to the host OS (if some folders are missing, please report an issue)

- Support for **3D text objects** and **video text strips**

- **Dynamic browsing through fonts** without leaving the 3D view/sequencer and with direct visualisation of the font on active text object, like in any other compositing and editing software

- **Font list stored externally in cache files**, to prevent a re run on every startup. Font Selector will automatically check for new/removed fonts and update the list accordingly on every startup

- **Favorites font system :** because browsing through hundred of fonts can be slow, you can mark fonts as favorites, these favorites fonts can be easily access by turning on the favorite filter

- Font are stored in **families**, browsable quickly, user can then choose available type (Regular, Bold, Condensed...)

- **Reveal file operator** allows user to open an explorer to the selected font

- Load Font Family operator to **load all "blender specific" font types of a family in one click**. Blender handles multiple font types on a single text object with the limitation of 4 of them (Regular, Bold, Italic, Bold Italic). Font Selector, if available, allows user to set them up for the selected font family

### Disclaimer :

Font Selector, except for the Load Font Family operator, **uses only the regular font slot blender text object**, in order to be clearer to the user, and show him instantly the change. For example, **a bold font will be apply by filling the text object regular's slot**.  
Three other font slots (bold, italic, bold italic) are user by blender to mix in a single text object different font types.  
**For this specific usecase, please use the Load Font Family operator.**

**Warning :**

The "master" branch of font selector is the experimental one, to get stable version manually, download latest release from this page : https://github.com/samytichadou/FontSelector_blender_addon/releases  

### Known issues :
- On windows, `Reveal file` operator does not select specific font file. This an issue from windows explorer cli arguments.
- When using Popover panels, the F3 search menu will populate with unnamed elements from these panels. This seems to be a blender bug.
