# Visiflex light testing
* Code to compute light intensity statistics from images captured with Basler Dart camera
* Code to test FTIR contact detection from images captured with Basler Dart camera on an assembled Visiflex

# Opacity testing how-to
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

# Contact detection testing how-to
* Capture the desired images of the Visiflex cap under a concentrated external contact using pylon Viewer while connected to Basler dart camera via USB (suggested OS: Linux)
* Copy all images to the folder /ftir_images in this package (sample images are included in this repo)
* Image cropping:
```
python3 crop_ftir.py
```
* Each image in the /ftir_images folder will be displayed. Left mouse click the point on the cap area of the image corresponding to the contact point, then press 'd' to display the next image.
* All cropped images will be saved to the folder /cropped
* Analysis of cropped images:
```
python3 test_color_diff.py
```
* For each cropped image quantifies difference between contact and non contact location, results are written under the /output folder

