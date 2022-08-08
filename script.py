from ppadb.client import Client
from PIL import Image
import numpy
import time
import cv2

#get touple array and return 2 rectangles with the largest y value
def get_largest_y(rect):
    largest_y = 2000000
    largest_y_rect = []
    pya=0
    for i in range(len(rect)):
        if rect[i][1] < largest_y:
            largest_y = rect[i][1]
            largest_y_rect = rect[i]
            pya=i
    rect.pop(pya)
    return largest_y_rect
#function that detects objects in pictures and draws a rectangle around them
def detect_objects(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #create touple list with 4 values
    rect = ([])
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    ret, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        #store x,y,w,h in a list

        if w>60 and h>60 and w<300 and h<300 and y>310:
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
            rect.append([x,y,w,h])

    #save image with rectangles
    cv2.imwrite('image.png', image)
    return find_distance(get_largest_y(rect), get_largest_y(rect))
# x distance between two rectangles

def find_distance(rect1, rect2):
    print(rect1)
    print(rect2)
    if(rect2[2]>600):
        rect2[2]=rect2[2]-200
    if(rect1[2]>600):
        rect1[2]=rect1[2]-200
    x1 = rect1[0]+rect1[2]/2
    x2 = rect2[0]+rect2[2]/2
    distance=0
    distance = distance +abs(x1 - x2)
    print(distance)
    return distance
#find the distance between two contours
#connect to device
client = Client(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
devices = client.devices()
device = devices[0]
print(f'Connected to {device}')
while True:
#perform swipe +



    #use cv to detect object
    #get screenshot
    screenshot = device.screencap()
    #save screenshot
    with open("screenshot.png", "wb") as f:
        f.write(screenshot)
    #convert to numpy array
    img = Image.open("screenshot.png")
    #save image from detect objects
    #create numpy array
    img_np = numpy.array(img)
    pya=detect_objects(img_np)
    pya=round(pya*1.05)
    if(pya==72):
        device.shell('input  tap 602 1500 500 500 200')
        time.sleep(1.5)
        for i in range(4):
            device.shell('input  tap 635 2080 500 500 200')
            time.sleep(2)
            device.shell('input  tap 559 1563 500 500 200')
            time.sleep(2)
            device.shell('input  tap 70 125 500 500 200')
            time.sleep(1)
        time.sleep(2)
        device.shell('input  swipe 500 500 500 500 '+str(pya))
        time.sleep(2)
        device.shell('input  tap 602 1500 500 500 200')
        time.sleep(2)
        continue
        print("tu")
    pya=max(pya,330)
    if(pya<400):
        pya=pya+30
    print("Distance :"+str(pya))
    #save img1 as a png
    time.sleep(0.5)

    device.shell('input  swipe 500 500 500 500 '+str(pya))
    time.sleep(2)
