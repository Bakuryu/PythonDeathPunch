import cv2
import numpy as np
from imageprocessing import roi, process_img


def findEnemies(screen,bbox,player_x,player_y):
    low_threshold = np.array([0, 0, 120])
    high_threshold = np.array([0, 0, 160])

    # low_threshold = np.array([cv2.getTrackbarPos('LowH', 'Control'), cv2.getTrackbarPos('LowS', 'Control'),
    #                           cv2.getTrackbarPos('LowV', 'Control')])
    # high_threshold = np.array([cv2.getTrackbarPos('HighH', 'Control'), cv2.getTrackbarPos('HighS', 'Control'),
    #                            cv2.getTrackbarPos('HighV', 'Control')])

    vertices = np.array([[0, 155], [0, 120], [bbox[2], 120], [bbox[2], 155]], np.int32) #Enemy vision

    new_img_rgba = process_img(screen,low_threshold,high_threshold,vertices)
    new_img_rgba = roi(new_img_rgba,[vertices])
    new_img_rgba = cv2.GaussianBlur(new_img_rgba,(9,9), 2,2)

    dp = cv2.getTrackbarPos('dp','Control')
    mDist = cv2.getTrackbarPos('mDist','Control')
    para1 = cv2.getTrackbarPos('param1', 'Control')
    para2 = cv2.getTrackbarPos('param2','Control')
    minRad = cv2.getTrackbarPos('minRadius', 'Control')
    maxRad = cv2.getTrackbarPos('maxRadius', 'Control')
    #circles = cv2.HoughCircles(new_img_rgba,cv2.HOUGH_GRADIENT,dp,mDist, param1=para1, param2=para2, minRadius=minRad, maxRadius=maxRad)
    circles = cv2.HoughCircles(new_img_rgba,cv2.HOUGH_GRADIENT,2,23, param1=100, param2=20, minRadius=6, maxRadius=11)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(screen, (i[0], i[1]), i[2], (0, 0, 255), 1.5)  # draw the outer circle
            cv2.putText(screen,str(abs(int(i[0])-player_x)),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)

    return new_img_rgba, circles