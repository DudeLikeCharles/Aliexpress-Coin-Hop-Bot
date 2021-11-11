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
while True:
    im_array = find_white(screenshot())
    if len(im_array) > 0:
        print("Found white pixels")
        for pixel in im_array:
            device.touch(pixel[0],pixel[1],"DOWN_AND_UP")
            time.sleep(0.1)
    device.shell('input touchscreen swipe 500 500 500 500 '+str(gap))
    time.sleep(2.5)

