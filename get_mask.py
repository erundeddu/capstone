#!/usr/bin/env python3 

import cv2
import numpy as np
import os

if __name__ == "__main__":
	## parameters to change
	path_img = "masks/mask_with_cylinder.bmp"  # path to image from which mask is extracted (best to use a bright image to filter out the dark borders)
	thresh = 200 # binary threshold to filter out dark borders (0-255)
	kernel_size = 11  # size of filter to perform erosion and dilation operation (kernel_size x kernel_size square)
	
	mask_folder = "masks"  # folder that contains the masks to filter out the borders of the camera in the images
	
	## script
	img_gray = cv2.imread(path_img, cv2.IMREAD_GRAYSCALE)  # open image as grayscale
	img_bw = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)[1]  # threshold grayscale image to get a binary image
	kernel = np.ones((11,11),np.uint8)  # assemble filter to perform morphological operations
	img_open = cv2.dilate(cv2.erode(img_bw, kernel), kernel)  # perform opening to polish borders 
	
	cv2.imwrite(mask_folder + "/" + "mask.bmp", img_open)  # save image

