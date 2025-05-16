from flask import Flask, request, render_template, redirect, url_for, session
import hashlib
import filetype
import os
from werkzeug.utils import secure_filename
from database import db

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def main():
    data = db.get_activities(5)
    return render_template("html/index.html", data=data)




@app.route("/lista", methods=["GET"])
def lista():
    return render_template("html/lista.html", data=None)

@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    return render_template("html/estadisticas.html")


    

@app.route("/actividad/<int:id>", methods=["GET"])
def profile(id=None):
    if not id:
        return render_template("html/index.html")
    return render_template("actividad.html", id=id)


@app.route("/nueva-actividad", methods=["GET", "POST"])
def nueva():
    if request.method == "GET":
        return render_template("html/nueva-actividad.html")
    elif request.method == "POST":


        return render_template("actividad.html", id=id)

