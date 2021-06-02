#!/usr/bin/env python3 

import cv2
import numpy as np
import os
from datetime import datetime


def get_square(event,x,y,flags,param):
	# callback to crop image given mouse input
	global ix,iy,drawing,img_resize,l,img_crop,start_point,end_point  # reference global variables during callback
	
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True  # enable drawing when the button is released
		ix,iy = x,y  # update last pressed x and y coords
		
	elif event == cv2.EVENT_LBUTTONUP:
		if drawing:
			start_point = (int(ix-0.5*l),int(iy-0.5*l))
			end_point = (int(ix+0.5*l),int(iy+0.5*l))
			color = (255,0,0)
			img_crop = cv2.rectangle(img_resize, start_point, end_point, color)  # save a cropped image in global var
			drawing = False


if __name__ == "__main__":
	drawing = False  # true if mouse is pressed
	ix,iy = -1,-1  # last pressed x and y coords

	img_folder = "images_ftir"  # folder that contains the images to be processed
	out_folder = "output"  # folder that contains the processed information
	cropped_folder = "cropped"
	
	l = 70  # length of square side around contact point
	
	img_crop = None  # stores image to be cropped in loop
	start_point,end_point = None,None  # store start and end points for cropping
	
	# make folders if not existent
	if not os.path.isdir(out_folder):
		os.mkdir(out_folder)
		
	if not os.path.isdir(cropped_folder):
		os.mkdir(cropped_folder)
	
	for i in os.listdir(img_folder):
		img = cv2.imread(img_folder + "/" + i)  # read each image
		scale_percent = 50 # percent of original size
		# resize image to fit on laptop screen
		width = int(img.shape[1] * scale_percent / 100)
		height = int(img.shape[0] * scale_percent / 100)
		dim = (width, height)
		img_resize = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
		cv2.namedWindow('image')
		cv2.setMouseCallback('image', get_square)  # bind mouse callback to function get_square
		while(1):
			cv2.imshow('image',img_resize)
			k = cv2.waitKey(1) & 0xFF  # keep showing the image until d is pressed (d=next image)
			if k == ord('d'):
				cv2.imwrite(cropped_folder + "/" + i, img_crop[start_point[1]+1:end_point[1],start_point[0]+1:end_point[0]])
				break
				
		cv2.destroyAllWindows()
	
		
