PDG Mutagen
==========================
![PDG Mutagen banner image](img/mutagen_cover.png)
*Toolset for generating and handling large Wedge variation counts in Houdini with PDG/TOPs*

<br>

## About
**PDG Mutagen** is a toolset designed to efficently and intuitively handle the often large Wedge variation counts and data amounts when working with PDG Wedging in *©SideFX Houdini*.

It includes a Python Panel Interface the "Mutagen Viewer", that allows you to do display and play back the PDG wedge variations.
* Allows to visually select a specific wedge variation that will then be selected in the PDG Graph as well.
* Right click in wedge variation to open full-size rendered image sequence in RV or File Browser.
* Mark/label wedge variations you like, save the selection.
* "Setup Mutation" Tool to generate new base wedge node containing all wedge parameters from marked wedge variations.


It also includes a "PDG Mutagen Shelf" containing utility tools.
* "Mutagen Setup" creates a PDG Graph Template with basic Wedging Setup, designed to work with the Mutagen Viewer and other Mutagen Tools.
* "Convert Takes to Wedges" converts variations you have set up in the "classical take style" to a single Wedge TOP that holds all the edited parameters. Append additional Wedge TOPs as you like to generate further variation.
* "Select Wedge Index" lets you numerically enter a target wedge index like "0_1_4_6_2" and selects it in the PDG Graph. This is handy for large wedge counts where visual selection is tedious or impossible.
* "Split IM Montage" splits ImageMagick Monatge in two separate Streams. This is handy for very large wedging setups which become unhandy in a single montage and also ImageMagick concatenation will fail.



**PDG Mutagen** is in prototype stage and for experimental use. It may contain bugs and the code is not fully cleaned up. Feel free to customize to your needs.

Compatible with *Houdini 17.5.x / Tested with 17.5.299*




Here are some animations produced with it:

* [![Volumetric fractals](img/volumes.jpg)](https://www.youtube.com/watch?v=E8n6chN2Txw)
* [![Dynamical systems](img/particles.jpg)](https://www.youtube.com/watch?v=_gdApm_QPjs)
* [![2D fractals](img/2d.jpg)](https://www.youtube.com/watch?v=__8gaEv5GAs)



<br>

## Resources
* [SideFX Pipeline PDG  - Learning Ressources](https://www.sidefx.com/learn/pipeline-pdg/)
* [Entagma PDG for Design - Learning Ressources](https://www.sidefx.com/learn/collections/pdg-for-design/)

<br>