from flask import render_template,request, redirect, send_from_directory,send_file
from app import app

from FilterMedianSize import FilterMedianSize
from FilterMeanSize import FilterMeanSize
from FilterMinSize import FilterMinSize

from Noise import Noise

import os

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['BASE_URL'] = "/home/codelabs/ngulik/python/smoothing-gpc-with-interface/"

app.config["IMAGE_UPLOADS"] = app.config['BASE_URL']+"imageuploads"
app.config["IMAGE_RESULTS"] = app.config['BASE_URL']+"imageresults"
app.config["IMAGE_NOISE"] = app.config['BASE_URL']+"imagenoise"
app.config["STATIC"] = app.config['BASE_URL']+"static"


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
            image.filename = "original_image." + "jpg"
            imagePath = image.filename
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            noise = Noise()
            noise.addNoise("jpg")
            
            # image.filename = "original_image.png"
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
    median = FilterMedianSize(app.config['BASE_URL'])

    imagePath = checkImageOrigin()

    meanImage = checkImageMean()
    minImage = checkImageMin()

    kernelSize = request.form.get('kernel_size')
    median.main(kernelSize)
    psnr = median.psnrResult()
    return render_template("index.html", imagePath = imagePath, 
        medianImage="result_median."+fileType, psnr = psnr,
        meanImage = meanImage, minImage = minImage
        )

@app.route("/setMean", methods=["GET", "POST"])
def setMean():
    imagePath = checkImageOrigin()

    medianImage = checkImageMedian()
    minImage = checkImageMin()

    print(minImage)

    mean = FilterMeanSize(app.config['BASE_URL'])
    mean.main()
    psnr = mean.psnrResult()
    return render_template("index.html", imagePath = imagePath, 
        meanImage="result_mean."+fileType, psnr2 = psnr,
        medianImage = medianImage, minImage = minImage
        )

@app.route("/setMin", methods=["GET", "POST"])
def setMin():
    imagePath = checkImageOrigin()
    min = FilterMinSize(app.config['BASE_URL'])
    min.main()

    medianImage = checkImageMedian()
    meanImage = checkImageMean()

    psnr = min.psnrResult()
    return render_template("index.html", imagePath = imagePath, 
        minImage="result_min."+fileType, psnr3 = psnr,
        medianImage = medianImage, meanImage = meanImage
        )


@app.route("/getImageMedian/")
def getImageMedian():
    return send_from_directory(
        os.path.join(
            app.config["IMAGE_RESULTS"]
            ),"result_median.jpg"
    )

@app.route("/getImageMean/")
def getImageMean():
    return send_from_directory(
        os.path.join(
            app.config["IMAGE_RESULTS"]
            ),"result_mean.jpg"
    )

@app.route("/getImageMin/")
def getImageMin():
    return send_from_directory(
        os.path.join(
            app.config["IMAGE_RESULTS"]
            ),"result_min.jpg"
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


def checkImageOrigin():
    if os.path.isfile(app.config['BASE_URL']+"original_image.jpg"):
        return "original_image.jpg"
    else:
        return ""

def checkImageNoise():
    if os.path.isfile(app.config["IMAGE_NOISE"]+"test_noise_added.jpg"):
        return True
    else:
        return False

def checkImageMedian():
    if os.path.isfile(app.config["IMAGE_RESULTS"]+"result_median.jpg"):
        return True
    else:
        return False

def checkImageMean():
    if os.path.isfile(app.config["IMAGE_RESULTS"]+"result_mean.jpg"):
        return True
    else:
        return False

def checkImageMin():

    print("bab2:"+os.path)
    if send_from_directory(os.path.join(app.config["IMAGE_RESULTS"]),"result_median.jpg"):
        return True
    else:
        return False