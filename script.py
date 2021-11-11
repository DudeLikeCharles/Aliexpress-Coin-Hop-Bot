from ppadb.client import Client
from PIL import Image
import numpy 
import time
adb = Client(host='127.0.0.1',port=5037)
devices = adb.devices()
if len (adb.devices()) == 0:
    print("No devices found")
    exit(1)
device=devices[0]
#create a deque that puts the biggest elements at the front and the smallest at the back

#create an array from a screenshot
def screenshot():
    im = Image.open(device.screencap())
    im_array = numpy.array(im)
    return im_array
#find all the white pixels and return their positions
def find_white(im_array):
    white_pixels = []
    for y in range(0,im_array.shape[0]):
        for x in range(0,im_array.shape[1]):
            if im_array[y][x][0] == 255 and im_array[y][x][1] == 255 and im_array[y][x][2] == 255:
                white_pixels.append((x,y))
    return white_pixels
#find longest distance in white pixels pair of x and y
def find_longest(white_pixels):
    longest = 0
    for i in range(0,len(white_pixels)):
        for j in range(i+1,len(white_pixels)):
            x_distance = abs(white_pixels[i][0] - white_pixels[j][0])
            y_distance = abs(white_pixels[i][1] - white_pixels[j][1])
            if x_distance > y_distance:
                distance = x_distance
            else:
                distance = y_distance
            if distance > longest:
                longest = distance
    return longest

while True:
    im_array = find_white(screenshot())
    if len(im_array) > 0:
        print("Found white pixels")
        for pixel in im_array:
            device.touch(pixel[0],pixel[1],"DOWN_AND_UP")
            time.sleep(0.1)
    device.shell('input touchscreen swipe 500 500 500 500 '+str(gap))
    time.sleep(2.5)

