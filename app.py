from dataclasses import dataclass
import cv2 as cv
import numpy as np
import mss as mss
import mouse 

@dataclass
class Point:
    x: int
    y: int

def main() -> int:
    clickList = []          # List of blocks to click
    previous = Point(0, 0)  # Previouse block clicked

    size = 155              # Size in pixels of block in game
    bounding_box = {'top': 256, 'left': 660, 'width': size*4, 'height': size*4} # Top and left are coordinates of top left pixel of blocks
    sct = mss.mss()                                                             # Screen taker 

    while True:
        # Grabs a screen in given array and converts it to np array
        sct_img = sct.grab(bounding_box)
        screen = np.array(sct_img)
        #cv.imshow('screen', screen)

        # Checks for blue pixel which indicates end of the game (if commented you can only disable the program by going in task manager and ending task)
        #blueCheck = screen[22, 400]
        #if blueCheck[0] == 255 and blueCheck[1] == 143 and blueCheck[2] == 23:
            #cv.circle(screen, (400, 22), 1, (0,255,0))
        #    break

        # Loops over 4 by 4 grid
        for y in range(1, 5):
            for x in range(1, 5):
                # Finds a pixel for given block
                p = Point(int((size * x) - (size/2)), int((size * y) - (size/2)))

                # Checks the value of a given pixel if a pixel is black and is not a same pixel a previous pixel goes to check if this block is already on the list
                # if not adds it to list of blocks to click
                vals = screen[p.y, p.x]
                if vals[0] == 0 and vals[1] == 0 and vals[2] == 0 and previous.x != x and previous.y != y:
                    if not checkForDuplicats(Point(x, y), clickList):
                        clickList.append(Point(x, y))
                        print(y)

        # Shows all the blocks to click in consol and in the image itself
        for i in clickList:
            print(f"x: {i.x} i y: {i.y}")
            cv.circle(screen, (int((size * i.x) - (size/2)), int((size * i.y) - (size/2))), 25, (0,255,0))

        # Adds delay
        cv.waitKey(30)

        # If theres something to click calculates where to click in pixels, moves mouse there and click removing block from list and making it previous block
        if len(clickList) > 0:
            x = int((size * clickList[0].x) - (size/2)) + bounding_box.get('left')
            y = int((size * clickList[0].y) - (size/2)) + bounding_box.get('top')
            mouse.move(x, y, True, 0)
            mouse.click()
            previous = clickList[0]
            clickList.pop(0)

        # If theres nothing to click wait a bit for block to spawn in game and makes previous 0,0 point so there isnt one
        if len(clickList) <= 0:
            cv.waitKey(60)
            previous = Point(0,0)


        #print(len(clickList))
        #print(clickList)

        # Shows a ss that was taken
        cv.imshow('screenager', screen)

        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()
    cv.waitKey(0)
    return 0

# Checks for duplitaces in a Point value and Point list
def checkForDuplicats(p, list) -> bool:
    for i in range(len(list)):
        if p.x == list[i].x and p.y == list[i].y:
            return True

    return False

if __name__ == "__main__":
    main()