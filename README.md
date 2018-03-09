# SSLD-images
Collects images from the Swedish Sign Language dictionary (http://teckensprakslexikon.su.se) and outputs a composite image.

Requires Python3 with packages `PIL` and `bs4`, and that Wget and ImageMagick are installed.

Run the script from the command line with
```
python3 get_ssld_images.py {signID}
```
for the default setting creating a side-by-side concatenation of the images of the sign.

![side-by-side image](https://github.com/borstell/SSLD-images/blob/master/00003_side-by-side.jpg)

For a semi-transparent overlay, run:
```
python3 get_ssld_images.py {signID} -overlay
```
NB: `-o` works as a shorthand for `-overlay`.

![overlay image](https://github.com/borstell/SSLD-images/blob/master/00003_overlay.jpg)

SignIDs can be given in the full five-digit format (e.g., `00001`) or without zero-fillers (e.g., `1`).
Multiple signIDs can be entered at once, by separating them with a comma "," – for example:
```
python3 get_ssld_images.py 00001,00002,00003
```

## Update 2018-03-09:
Some entries in the Swedish Sign Language dictionary have more than two images for the signs (usually due to being compounds with several movement parts). In the updated version, this is handled as follows:

If there are three images for the entry, the default option renders a side-by-side image in which each individual image has been cropped to 60% of its original width.

![side-by-side image](https://github.com/borstell/SSLD-images/blob/master/11955_side-by-side.jpg)

And the overlay option renders a regular overlay but in two steps (first merging images 1 and 2, then the output merged with image 3):

![overlay image](https://github.com/borstell/SSLD-images/blob/master/11955_overlay.jpg)

If there are four images for the entry, the default option renders a 2x2 image, left to right, top-down.

![side-by-side image](https://github.com/borstell/SSLD-images/blob/master/09979_side-by-side.jpg)

And the overlay option renders two overlays (images 1+2 and images 3+4) that are then positioned side-by-side.

![overlay image](https://github.com/borstell/SSLD-images/blob/master/09979_overlay.jpg)
