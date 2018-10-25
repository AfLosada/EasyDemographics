import json
import numpy as np
import cv2
import math
from PIL import Image
from PIL import ImageDraw
from pprint import pprint
from watson_developer_cloud import VisualRecognitionV3


def colorea(imagen, center, radius, color, thickness, lineType, shift):
	cv2.circle(images_file, center, radius, color, thickness, lineType, shift)

#Acá se pone el apikey para conectarse con watson
#IMPORTANTE
#Cuando hagamos las pruebas es mejor no probar llamando a Watson porque los usos que tenemos son limitados

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='APIKEY')
#Se lee la imágen como bits y se hace el llamado al api de watson
with open('.//Imagenes//critica.jpg', 'rb') as images_file:
    	classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
        owners=["me"]).get_result()
print(json.dumps(classes, indent=2))
with open('data.json', 'w') as outfile:
   	json.dump(classes, outfile)