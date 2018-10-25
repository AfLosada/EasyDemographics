from flask import Flask, render_template, request
from watson_developer_cloud import VisualRecognitionV3
import json
import cv2
import math
import os

path = "D://Nonono//Web//images//"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)

#El metodo para llamar al api de watson con una imagen, crea un json en el directorio
def llamarWatson(direcion_vid, carpeta_vid, numer):
    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey='APIKEY'
     )
    print("se metio a llamar watson")
    #Se lee la imagen como bits y se hace el llamado al api de watson
    with open(direcion_vid, 'rb') as images_file:
        classes = visual_recognition.detect_faces(
        images_file,
        threshold='0.3',
        owners=["me"]).get_result()
    json.dumps(classes, indent=2)
    with open(carpeta_vid + 'data' + str(numer) + '.json', 'w') as outfile:
        json.dump(classes, outfile)


def contarJson(lim,carpetica):
    num = 0
    i = 1
    while(i <= lim):
        ruta = 'D://Nonono//Web//'+carpetica+'\\data'+ str(i) + '.json'
        with open(ruta) as json_data:
            d = json.load(json_data)
        num += len(d['images'][0]['faces'])
        i = i+1
    print("ruta es "+ ruta)
    print("el numero total de personas es "+str(num))
    return num

#El metodo para procesar el video, la idea es que los parametros que le entren sean
#El directorio donde se va a leer el video
#El nombre del archivo de video
#El nombre de la carpeta donde se va a guardar el video
def procesar_video(dir, video, carpeta):
    cap = cv2.VideoCapture(dir+video)
    print("se metio a procesar video")
    frameRate = cap.get(5) #frame rate
    frameRate2 = math.ceil(cap.get(5))
    print("frame rate es"+ str(frameRate2))
   ##cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    ##lim = cap.get(cv2.CAP_PROP_POS_MSEC)
    totFrames = cap.get(7) #frames totales del video
    print("total de frames es " + str(totFrames))
    segtot = totFrames/frameRate2
    intervalo = 4;
    lim = segtot/intervalo
    print("paso el get raro")
    x=1
    if(os.path.exists(carpeta) == False):
        os.mkdir(carpeta)
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate*4) == 0):
            filename = "./" + carpeta + "/" +  str(int(x)) + ".jpg"
            x+=1
            cv2.imwrite(filename, frame)
            #Este metodo guarda un archivo json para cada imagen, la idea es procesarlo despues
            llamarWatson(direcion_vid = filename, carpeta_vid =  carpeta + '/', numer = int(x)-1)
    cap.release()
    print ("Done!")
    print (lim)
    return lim

#Pagina principal
@app.route('/temp')
def home():
    return render_template("index.html")
#Pagina secundaria
@app.route('/procesar')
def about():
    return render_template("info.html")
#Pagina secundaria
@app.route('/')
def info():
    return render_template("index.html")

#Se llama aca cuando se sube el video, el cual lo guarda
@app.route("/procesar/",methods=["POST"])
def upload():
    #Todo este pedazo guarda la imagen
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    x= 0
    for file in request.files.getlist("file"):
        x+=1
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        #Despues de guardar el video, lo que se hace es procesar el video, separandolo en mini imagenes y
        #Usando el api de watson
        carpetica = 'Uploads\\' + (filename[0:len(filename)-4] + str(x))
        print(carpetica)
        lim = procesar_video(dir = (path), video = filename, carpeta = 'Uploads/' + (filename[0:len(filename)-4] + str(x)))
        print("supuestamente proceso")
        num = contarJson(lim = lim, carpetica = carpetica)
    return render_template("info.html", numeroPersonas = num, nombreVideo = (filename[0:len(filename)-4]) + str(x))

if __name__ == '__main__':
    app.run(debug=True)