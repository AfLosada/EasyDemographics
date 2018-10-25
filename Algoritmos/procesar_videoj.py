import cv2
import math
import os
dir = "D://PMC//Web//images//"
videoFile = dir + "video1.mp4"
nombreCarpeta = "aaaaa"

cap = cv2.VideoCapture(videoFile)
frameRate = cap.get(5) #frame rate
print(frameRate)
totFrames = cap.get(7) #frames totales del video
x=1
if(os.path.exists(nombreCarpeta) == False):
        os.mkdir(carpeta)
while(cap.isOpened()):
   	frameId = cap.get(1) #current frame number
   	ret, frame = cap.read()
   	if (ret != True):
   	    break
   	if (frameId % math.floor(frameRate + 1) == 0):
   		filename = "./" + nombreCarpeta + "/" +  str(int(x)) + ".jpg"
   		x+=1
   		cv2.imwrite(filename, frame)
cap.release()
print ("Done!")