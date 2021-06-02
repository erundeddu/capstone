#!/usr/bin/env python3 

import cv2
import numpy as np
import os
from datetime import datetime

if __name__ == "__main__":
	
	img_folder = "images"  # folder that contains the images to be processed
	out_folder = "output"  # folder that contains the processed information
	mask_folder = "masks"  # folder that contains the masks to filter out the borders of the camera in the images
	
	now = datetime.now()  # get current date and time
	ts = now.strftime("%Y%m%d_%H%M%S")  # get timestamp as a string
	out_path = out_folder + "/" + "brightness_" + ts + ".csv"  # path of file to which processed information is saved
	
	if not os.path.isdir(out_folder):
		os.mkdir(out_folder)
	
	f = open(out_path, "w")
	f.write("img_name,mean_intensity,std_intensity\n")  # initialize file header
	f.close()
	
	mask = cv2.imread(mask_folder + "/" + "mask.bmp", 0)  # get the mask to filter out borders of the camera
	
	for i in os.listdir(img_folder):
		img_gray = cv2.imread(img_folder + "/" + i, cv2.IMREAD_GRAYSCALE)  # read each image as grayscale
		img_masked = cv2.bitwise_and(img_gray, img_gray, mask=mask)  # apply mask to filter out camera borders (these now have intensity = 0)
		img_flat = img_masked.flatten()/255  # convert the 2D image matrix into a 1D array of 0-1 entries for postprocessing
		intensity_mean = np.mean(img_flat[img_flat>0])  # calculate average intensity
		intensity_std = np.std(img_flat[img_flat>0])  # calculate standard deviation of intensity
			
		f = open(out_path, "a")  # open file to write results
		f.write(i + "," + "{:.4f}".format(intensity_mean) + "," + "{:.4f}".format(intensity_std) + "\n")  # write intensity statistics
		f.close()  # close file
		
	

