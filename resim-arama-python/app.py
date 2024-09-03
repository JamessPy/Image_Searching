import os
from flask import Flask, render_template, request
from imgset import ImgSet
from form import RegisterForm
from imgsearch import imageDataSerch
import cv2

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home_page():
    form = RegisterForm()
    ImgSet('upload').Run()
    return render_template("index.html", form=form)


@app.route("/upload")
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'upload/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    ImgSet('upload').Run()
    return render_template("complete.html")

@app.route("/search")
def search_page():
    return render_template("search.html")


@app.route("/search", methods=['POST'])
def search():
    target = os.path.join(APP_ROOT, 'tmp/')


    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    imageDataSerch(destination)
    return render_template("complete.html")


if __name__ == "__main__":
    app.run(port=4555, debug=True)
