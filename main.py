import numpy as np
import cv2
import time
from getscreen import get_screen
from keys import left, right
from imageprocessing import roi, process_img
from enemydetector import findEnemies

import Queue as Q

winlist = []

def dummyfun(x):
    return

def createControls():
    return
    cv2.namedWindow("Control",cv2.WINDOW_NORMAL)
    iLowH= 0
    iHighH = 0
    iLowS = 0
    iHighS = 0
    iLowV = 120
    iHighV = 160
    iErode = 2
    iDilate = 2
    iDP = 2
    iMDist = 23
    iParam1 = 100
    iParam2 = 20
    iMinRadius = 5
    iMaxRadius = 11

    cv2.createTrackbar('LowH', 'Control', iLowH, 179,dummyfun) # Hue(0 - 179)
    cv2.createTrackbar('HighH', 'Control', iHighH, 255,dummyfun)

    cv2.createTrackbar('LowS', 'Control', iLowS, 255,dummyfun) # Saturation(0 - 255)
    cv2.createTrackbar('HighS', 'Control', iHighS, 255,dummyfun)

    cv2.createTrackbar('LowV', 'Control', iLowV, 255,dummyfun) # Value(0 - 255)
    cv2.createTrackbar('HighV', 'Control', iHighV, 255,dummyfun)

    cv2.createTrackbar('erode', 'Control', iErode, 100, dummyfun)
    cv2.createTrackbar('dilate', 'Control', iDilate, 100, dummyfun)

    cv2.createTrackbar('dp', 'Control', iDP, 2,dummyfun)
    cv2.createTrackbar('mDist', 'Control', iMDist, 100, dummyfun)
    cv2.createTrackbar('param1','Control', iParam1, 100, dummyfun)
    cv2.createTrackbar('param2','Control', iParam2, 100, dummyfun)
    cv2.createTrackbar('minRadius','Control', iMinRadius, 300, dummyfun)
    cv2.createTrackbar('maxRadius','Control', iMaxRadius, 300, dummyfun)

def findEnemy(screen,bbox,player_x,player_y):
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
            cv2.circle(screen, (i[0], i[1]), i[2], (0, 0, 255), 2)  # draw the outer circle
            cv2.putText(screen,str(abs(int(i[0])-player_x)),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)

    return new_img_rgba, circles

def main():
    #createControls()
    last_time = time.time()
    player_x = 391
    player_y = 211
    total_enemies = 0
    last_enemy = (0,0)
    #video = cv2.VideoWriter('PythonPunchTest.avi', -1, 10, (782, 422))
    enemyQueue = Q.PriorityQueue()
    while (True):
        # 800x600 windowed mode
        try:
            printscreen, bbox = get_screen('one finger death punch')#getGameScreenLocation('one finger death punch')# np.array(ImageGrab.grab(bbox))
        except TypeError:
            cv2.destroyAllWindows()
            break

        new_printscreen,enemies = findEnemies(printscreen,bbox,player_x,player_y)

        #Debug center of screen
        #cv2.circle(printscreen,(391,211),4,(255,0,0),4)

        #Debug shows where attack range is.
        # cv2.rectangle(printscreen,(player_x-153,player_y-10),(player_x,player_y+30),(255,0,0),2)
        # cv2.rectangle(printscreen,(player_x+152,player_y-10),(player_x,player_y+30),(255,0,0),2)

        if enemies is not None:
            closest = 1000
            direction = None

            for enemy in enemies:
                dist = abs(round(int(enemy[0][0]) - player_x))
                direct = round(int(enemy[0][0])- player_x)
                if dist < closest:
                    closest = dist
                    direction = direct

            if closest is not 1000 and direction is not None:
                if closest <= 153:
                    if direction < 0:
                        left(0.1)
                    total_enemies += 1
                    if direction > 0:
                        right(0.1)
                        total_enemies += 1
                    time.sleep(0.1)


        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        #print(total_enemies)
        #cv2.imshow('window2', new_printscreen)
        #cv2.imshow('window', printscreen)
        #video.write(printscreen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            #video.release()
            break


main()
