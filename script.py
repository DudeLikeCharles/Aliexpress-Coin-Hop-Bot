from ppadb.client import Client
from PIL import Image
import numpy 
import time
adb = Client(host='127.0.0.1',port=5037)
print(adb.devices())
if len (adb.devices()) == 0:
    print("No devices found")
    exit(1)
device=devices[0]

#create an array from an screenshot
def get_array(image):
    return numpy.array(image.getdata(),
                      dtype=numpy.uint8).reshape(image.size[1],
                                                 image.size[0],
                                                 3)
#position of white pixels in an array
def get_positions(array):
    positions = []
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if (array[i][j][0] == 255 and array[i][j][1] == 255 and array[i][j][2] == 255):
                positions.append((i,j))
    return positions
#longest distance between two white pixels
def get_longest_distance(positions):
    longest_distance = 0
    for i in range(len(positions)):
        for j in range(i+1,len(positions)):
            distance = abs(positions[i][0]-positions[j][0])+abs(positions[i][1]-positions[j][1])
            if distance > longest_distance:
                longest_distance = distance
    return longest_distance

while True:
    image = device.screencap()
    with open("screen.png", "wb") as f:
        f.write(image)
    image = Image.open("Screen.png")
    positions = get_positions(get_array(image))
    pya =get_longest_distance(positions)
    print(pya)


    device.shell('input touchscreen swipe 500 500 500 500 '+str(gap))
    time.sleep(2.5)

