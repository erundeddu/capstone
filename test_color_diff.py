#!/usr/bin/env python3 

import cv2
import numpy as np
import os
from datetime import datetime


def cluster_colors(mat):
	# perform k-means clustering (k=2) on a HSV matrix, output statistics and distance between the two clusters
	z = mat.reshape((-1,3))
	z = np.float32(z)
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	K = 2
	compactness,label,center=cv2.kmeans(z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
	distance = ((center[0,0]-center[1,0])**2 + (center[0,1]-center[1,1])**2)**0.5  # only H and S channels used to compute distance to find a measure for color difference
	return compactness,center,distance
	


if __name__ == "__main__":
	cropped_folder = "cropped"  # folder that contains the images to be processed
	out_folder = "output"  # folder that contains the processed information
	
	now = datetime.now()  # get current date and time
	ts = now.strftime("%Y%m%d_%H%M%S")  # get timestamp as a string
	out_path = out_folder + "/" + "ftir_" + ts + ".csv"  # path of file to which processed information is saved
	
	# create folder to store results if not existent
	if not os.path.isdir(out_folder):
		os.mkdir(out_folder)
		
	f = open(out_path, "w")
	f.write("img_name,HS_distance,compactness\n")  # initialize file header
	f.close()
	
	for i in os.listdir(cropped_folder):
		img = cv2.imread(cropped_folder + "/" + i)  # read each image
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert to hsv space for processing
		comp, cent, dst = cluster_colors(img_hsv)
		f = open(out_path, "a")  # open file to write results
		f.write(i + "," + "{:.4f}".format(dst) + "," + "{:.4f}".format(comp) + "\n")  # write results
		f.close()  # close file

