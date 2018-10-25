import numpy as np
from PIL import Image
from PIL import ImageDraw
import os as os

folder ='D://Downloads//Subject10'

for file in os.listdir(folder):
	if file[len(file)-1] != 'b':
		image = Image.open(folder + '//' + file)
		image.save(file[0:len(file)-4] + '.jpeg')
