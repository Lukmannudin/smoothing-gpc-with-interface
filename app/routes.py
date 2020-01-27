from flask import render_template,request, redirect, send_from_directory,send_file
from app import app

from smoothing.filter_median_size import FilterMedian

import os

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config["IMAGE_UPLOADS"] = "/home/codelabs/ngulik/python/microblog/imageuploads"
app.config["IMAGE_RESULTS"] = "/home/codelabs/ngulik/python/microblog/imageresults"
app.config["STATIC"] = "/home/codelabs/ngulik/python/microblog/static"


imagePath = ""
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
            # image.filename = "original_image." + fileNameSplit[len(fileNameSplit)-1]
            image.filename = "original_image.png"
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
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
    imageOrigin = "original_image.png"
    FilterMedian().main(imageOrigin)
    return render_template("index.html", imagePath = imageOrigin, 
        medianImage="medianresult.png")

@app.route("/getImageMedian/")
def getImageMedian():
    return send_from_directory(
        os.path.join(
            app.config["IMAGE_RESULTS"]
            ),"medianresult.png"
    )

@app.route("/getImagePlaceholder/")
def getImagePlaceholder():
    return send_from_directory(
        os.path.join(
            app.config["STATIC"]
            ),"imageplaceholder.png"
    )