# Visiflex fiducials ordered detection
* Code to detect coordinates of red LED fiducials in images captured with Basler Dart camera, and order a list of fiducials coordinates counterclockwise, starting from the fiducial at the top of the image


# How-to

* Paste the image of interest in the same folder as `main.py` and rename the image as fiducials.bmp

* Run:

```
python3 main.py
```

* The program saves the following images:

	* filtered.bmp: shows the filtering of red spots by HSV color range
	* processed.bmp: shows the ordered detected fiducials
	
* `main.py` can be rewritten as a function that returns the variable `ordered_keypoints_top` to return the list containing the counterclockwise oredered keypoints starting from the fiducial at the top of the image

