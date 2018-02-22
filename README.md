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
