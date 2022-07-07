# Image Processing Instructions

For each still image:

1.  Export image from DICOM viewer as jpg or png
2.  Open exported image in Photoshop
3.  Covert layer to Smart Object
4.  Copy Smart Object Layer
5.  Paste Smart Object Layer into Main Photoshop file
6.  Save Photoshop file
7.  Turn on the topmost "Label" layer to ensure clearance
8.  Select the move tool (4-way arrow icon)
9.  Check the box on the top toolbar for "Show Transformation Controls"
10. Scale, rotate, and move the image, click checkmark to accept changes
11. From the "Create a new fill or adjustment layer" tool on the layers
    palette toolbar, choose "Curves"
12. Use a preset, manual points, and/or set the whitepoint and blackpoint
13. If touchup is needed, create a new layer above the image, and use
    0% hardness brushes 50-300px to paint black over unwanted features.
14. Alt-drag (copy) a new black background layer from the original
    black background layer at the bottom.
15. Select all the layers for a single image, then click the folder
    icon on the layers palette toolbar to put the layers into a new group
16. Double-click the group and rename it with a unique name and file
    extension, such as "lizard_iguana_04.png"
17. Collapse the layer group and hide it
18. Save

In the Main Photoshop file, as long as the menu item "File:Generate:Image Assets"
is checked, Photoshop will automatically export a png/jpg for every layer or layer
group named ending in ".png" or ".jpg". For the "lizard.psd" file, these assets
are put into a neighboring "lizard-assets" folder. These can be copied into the
"media/all" directory of the VetRFID directory.
