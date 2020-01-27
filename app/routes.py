from flask import render_template,request, redirect, send_from_directory,send_file
from app import app

from smoothing.filter_median_size import FilterMedian
from smoothing.Noise import Noise

import os

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config["IMAGE_UPLOADS"] = "E:\[1]OfflineTugas\GPC\smoothing-gpc-with-interface\imageuploads"
app.config["IMAGE_RESULTS"] = "E:\[1]OfflineTugas\GPC\smoothing-gpc-with-interface\imageresults"
app.config["IMAGE_NOISE"] = "E:\[1]OfflineTugas\GPC\smoothing-gpc-with-interface\imagenoise"
app.config["STATIC"] = "E:\[1]OfflineTugas\GPC\smoothing-gpc-with-interface\static"


imagePath = ""
fileType = "jpg"
@app.route('/')
@app.route('/index')
def index():
     return render_template("index.html")

@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    imagePath = ""
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
        
            fileNameSplit = image.filename.split('.')
            fileType = fileNameSplit[len(fileNameSplit)-1]
            image.filename = "original_image." + fileType
            imagePath = image.filename
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            noise = Noise()
            noise.addNoise(fileType)
            
            #image.filename = "original_image.png"
            print(image.filename)
            print("Image Saved")
            
            return render_template("index.html", imagePath = image.filename)
            
    return render_template("index.html", imagePath = imagePath)

@app.route("/jquery/")
def jquery():
    return render_template("jquery.js")

@app.route("/getImageOrigin/<imageName>")
def getImageOrigin(imageName):
    return send_from_directory(
        os.path.join(
            app.config["IMAGE_UPLOADS"]
            ),imageName
    )

@app.route("/bootstrapmin/")
def bootstrapmin():
    return render_template("bootstrap.min.js")

@app.route("/bootstrapcss/")
def bootstrapcss():
    return render_template("bootstrap.css")

@app.route("/setMedian", methods=["GET", "POST"])
def setMedian():
    imageOrigin = imagePath
    FilterMedian().main(imageOrigin)
    median = FilterMedian()

    psnr = median.psnrResult()
    kernelSize = request.form.get('kernel_size')
    median.main(kernelSize)
    return render_template("index.html", imagePath = imageOrigin, 
        medianImage="result_median."+fileType, psnr = psnr)

@app.route("/getImageMedian/")
def getImageMedian():
    return send_from_directory(
        os.path.join(
            app.config["IMAGE_RESULTS"]
            ),"result_median.jpg"
    )

@app.route("/getImagePlaceholder/")
def getImagePlaceholder():
    return send_from_directory(
        os.path.join(
            app.config["STATIC"]
            ),"imageplaceholder.png"
    )

@app.route("/getImageNoise/")
def getImageNoise():
    print( os.path.join(
           app.config["IMAGE_NOISE"]
            ),"test_noise_added."+fileType
            )
    return send_from_directory(
        os.path.join(
           app.config["IMAGE_NOISE"]
            ),"test_noise_added."+fileType
    )