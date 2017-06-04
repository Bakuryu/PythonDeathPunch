import cv2
import time
from getscreen import get_screen
from keys import left, right
from enemydetector import findEnemies

winlist = []

def main():
    last_time = time.time()
    player_x = 391
    player_y = 211
    #total_enemies = 0
    #video = cv2.VideoWriter('PythonPunchTest.avi', -1, 10, (782, 422))
    while (True):
        try:
            printscreen, bbox = get_screen('one finger death punch')#getGameScreenLocation('one finger death punch')# np.array(ImageGrab.grab(bbox))
        except TypeError:
            cv2.destroyAllWindows()
            break

        enemyview,enemies = findEnemies(printscreen,bbox,player_x)

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
                        left(0.2)
                    if direction > 0:
                        right(0.2)
                    time.sleep(0.08)


        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        #cv2.imshow('Enemy Threshold', enemyview)
        #cv2.imshow('window', printscreen)
        #video.write(printscreen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            #video.release()
            break


main()
