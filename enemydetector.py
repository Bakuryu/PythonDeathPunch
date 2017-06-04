import cv2
import numpy as np
from imageprocessing import roi, process_img

def findEnemies(screen,bbox,player_x):
    low_threshold = np.array([0, 0, 120])
    high_threshold = np.array([0, 0, 160])

    vert1 = np.array([[0, 155], [0, 120], [bbox[2] - 430, 120], [bbox[2] - 430, 155]], np.int32)
    vert2 = np.array([[411, 155], [411, 120], [bbox[2], 120], [bbox[2], 155]], np.int32)
    vertices = np.array([[vert1], [vert2]])  # Enemy vision


    enemyview = process_img(screen,low_threshold,high_threshold,vertices)

    circles = cv2.HoughCircles(enemyview,cv2.HOUGH_GRADIENT,2,23, param1=100, param2=20, minRadius=6, maxRadius=11)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(screen, (i[0], i[1]), i[2], (0, 0, 255), 1)  # draw the outer circle
            cv2.putText(screen,str(abs(int(i[0])-player_x)),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)

    return enemyview, circles