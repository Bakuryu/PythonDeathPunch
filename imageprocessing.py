import cv2
import numpy as np

def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, (255,255,255))
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(original_image, low_threshold, high_threshold,vertices):
    img_hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    img_thresholded = cv2.inRange(img_hsv,low_threshold,high_threshold)
    erode_x = 2#cv2.getTrackbarPos('erode', 'Control')
    erode_y = erode_x
    dilate_x = 2#cv2.getTrackbarPos('dilate', 'Control')
    dilate_y = dilate_x
    ekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erode_x,erode_y))
    dkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_x,dilate_y))
    cv2.erode(img_thresholded,ekernel,img_thresholded,iterations = 1)
    cv2.dilate(img_thresholded,dkernel,img_thresholded,iterations = 1)

    processed_img = roi(img_thresholded, [vertices])

    return processed_img