import cv2
import numpy as np

# high/low HSV thresholds for detection of red (need two separate low/high thresholds because hue wraps around red)
low_red_1 = np.array([175,220,50])
high_red_1 = np.array([180,255,255])
low_red_2 = np.array([0,220,50])
high_red_2 = np.array([10,255,255])

img = cv2.imread("fiducials.bmp")  # read camera image
# img = cv2.flip(img, -1)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert image to HSV

mask_1 = cv2.inRange(img_hsv, low_red_1, high_red_1)
mask_2 = cv2.inRange(img_hsv, low_red_2, high_red_2)
mask = cv2.bitwise_or(mask_1, mask_2)  # mask to filter red (overlap two masks)

color = cv2.bitwise_and(img, img, mask=mask)  # filter original image
color = cv2.resize(color, (400, 300))  # resize (reduce) image to display on monitor
img = cv2.resize(img, (400, 300))  # resize original image
cv2.imwrite("filtered.bmp", color)  # save image showing only filtered red spots

im = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)  # convert image with filtered red spots to grayscale

# Set up the blob detector with parameters.
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 5
params.maxThreshold = 255
params.filterByArea = True
params.minArea = 10
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(im)  # detect blobs in grayscale image

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
# im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

for k in keypoints:  # draw all keypoints as circles on the original image
    img = cv2.circle(img, (int(k.pt[0]), int(k.pt[1])), 5, (255,255,0),-1)

x_acc = 0  # accumulator for x coordinates
y_acc = 0  # accumulator for y coordinates
for k in keypoints:
    x_acc += k.pt[0]
    y_acc += k.pt[1]
# find the center of the fiducials circle as an average of all fiducials pose
x_center = x_acc/len(keypoints)
y_center = y_acc/len(keypoints)

ordered_keypoints = []  # list of ordered keypoints (by proximity to each other)
ordered_keypoints.append(keypoints[0].pt)  # start with the first member of keypoints
idx_used = [0]  # list including all the indices of the points used from keypoints

while len(idx_used) < len(keypoints):  # loop until every single keypoint has been arranged
    min_dst = np.inf
    candidate_idx = None
    for ii in range(len(keypoints)):  # find, among all keypoints that have not been used, the one with closest distance to the last point in ordered_keypoints
        if ii not in idx_used:
            dst = (ordered_keypoints[-1][0] - keypoints[ii].pt[0]) ** 2 + (ordered_keypoints[-1][1] - keypoints[ii].pt[1]) ** 2
            if dst < min_dst:
                min_dst = dst
                candidate_idx = ii
    idx_used.append(candidate_idx)  # update idx_used with the index of the point that was added to ordered_keypoints
    ordered_keypoints.append(keypoints[candidate_idx].pt)

# check if the sequence is clockwise or counterclockwise
pt1 = ordered_keypoints[0]  # first point
pt2 = ordered_keypoints[1]  # second point
pt3 = ordered_keypoints[-1]  # last point

is_ccw = False   # if True: sequence is counterclockwise
# compare, depending on the quadrant around the center of fiducials ring in which the first point is found, its x or y coordinate to that of the second point to determine CW or CCW
if pt1[0] > x_center and pt1[1] > y_center:  # IV quadrant
    if pt1[0] < pt2[0]:
        is_ccw = True
    elif pt1[0] > pt3[0]:
    	is_ccw = True    
elif pt1[0] > x_center and pt1[1] < y_center:  # I quadrant
    if pt1[0] > pt2[0]:
        is_ccw = True
    elif pt1[0] < pt3[0]:
    	is_ccw = True  
elif pt1[0] < x_center and pt1[1] < y_center:  # II quadrant
    if pt1[0] > pt2[0]:
        is_ccw = True
    elif pt1[0] < pt3[0]:
    	is_ccw = True
else:  # III quadrant
    if pt1[0] < pt2[0]:
        is_ccw = True
    elif pt1[0] > pt3[0]:
    	is_ccw = True 

if not is_ccw:
    ordered_keypoints.reverse()  # now ordered_keypoints must be ccw

# sort sequence of points such that index 0 corresponds to the point at the top (lowest y coord)
# find keypoint with lowest y coord
min_y_val = np.inf
top_idx = None
for ii in range(len(ordered_keypoints)):
    y_val = ordered_keypoints[ii][1]
    if y_val < min_y_val:
        min_y_val = y_val
        top_idx = ii
idx = []  # list used to reshuffle ordered_keypoints
for ii in range(len(ordered_keypoints)):
    idx.append((top_idx+ii) % len(ordered_keypoints))
ordered_keypoints_top = []  # ordered_keypoints that start from the keypoint at the top of the image
for ii in range(len(ordered_keypoints)):
    ordered_keypoints_top.append(ordered_keypoints[idx[ii]])

for ii in range(len(ordered_keypoints)):  # label all fiducials with a number to show the success of the algorithm
    img = cv2.putText(img, str(ii), (int(ordered_keypoints_top[ii][0]),int(ordered_keypoints_top[ii][1])), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255), 2)

img = cv2.circle(img, (int(x_center), int(y_center)), 2, (0,0,255), -1)  # draw the center of the fiducials ring

cv2.imwrite('processed.bmp', img)  # save processed image
