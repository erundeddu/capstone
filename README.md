# Visiflex light testing
* Code to compute light intensity statistics from images captured with Basler dart camera

# How-to
* Capture the desired images using pylon Viewer while connected to Basler dart camera via USB (suggested OS: Linux)
* Copy all images to the folder /images in this package (sample images are included in this repo)
* Select one image to be used as mask in order to filter out camera borders, and copy it to the folder /masks; change the path\_img variable in get_mask.py to match the name of this image
* Generate the mask:
```
python3 get_mask.py
```
* Compute statistics for all images in the folder /images:
```
python3 test_brightness.py
```
* Statistics for all images are written under the /output folder
