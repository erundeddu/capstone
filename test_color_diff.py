#!/usr/bin/env python3 

import cv2
import numpy as np
import os
from datetime import datetime


def cluster_colors(mat):
	# perform k-means clustering (k=2) on a RGB matrix, output statistics and distance between the two clusters
	z = mat.reshape((-1,3))
	z = np.float32(z)
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	K = 2
	compactness,label,center=cv2.kmeans(z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
	c1_hsv = cv2.cvtColor(np.uint8([[[center[0,0],center[0,1],center[0,2]]]]), cv2.COLOR_BGR2HSV)
	c2_hsv = cv2.cvtColor(np.uint8([[[center[1,0],center[1,1],center[1,2]]]]), cv2.COLOR_BGR2HSV)
	c1_hs = np.array([c1_hsv[0,0,1]*np.cos(c1_hsv[0,0,0]*np.pi/90), c1_hsv[0,0,1]*np.sin(c1_hsv[0,0,0]*np.pi/90)])
	c2_hs = np.array([c2_hsv[0,0,1]*np.cos(c2_hsv[0,0,0]*np.pi/90), c2_hsv[0,0,1]*np.sin(c2_hsv[0,0,0]*np.pi/90)])
	distance = ((c1_hs[0]-c2_hs[0])**2 + (c1_hs[1]-c2_hs[1])**2)**0.5  # only H and S channels used to compute distance to find a measure for color difference
	# distance = ((center[0,0]-center[1,0])**2 + (center[0,1]-center[1,1])**2 + (center[0,2]-center[1,2])**2)**0.5
	distance /= (255*2)  # normalize distance
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
		comp, cent, dst = cluster_colors(img)
		f = open(out_path, "a")  # open file to write results
		f.write(i + "," + "{:.8f}".format(dst) + "," + "{:.8f}".format(comp) + "\n")  # write results
		f.close()  # close file

