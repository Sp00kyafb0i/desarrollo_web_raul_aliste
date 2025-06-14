from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import hashlib
import filetype
import os
from werkzeug.utils import secure_filename
from database import db
from utils.validations import validate_activity, validate_tema
from datetime import datetime
import uuid


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def main():
    data = db.get_activities(5)
    return render_template("html/index.html", data=data, get_comuna=db.get_comuna, get_tema=db.get_tema, get_photos=db.get_photos)




@app.route("/lista", methods=["GET"])
def lista():
    data = db.get_activities(None)
    return render_template("html/lista.html", data=data, get_comuna=db.get_comuna, get_tema=db.get_tema, get_photos=db.get_photos)

@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    return render_template("html/estadisticas.html")


    

@app.route("/actividad/<int:id>", methods=["GET"])
def ver_actividad(id):
    actividad = db.get_actividad_by_id(id)
    return render_template("html/actividad.html", actividad=actividad, fotos = db.get_photos(id), comuna = db.get_comuna(id).nombre, tema = db.get_tema(id).tema, get_photos=db.get_photos, id=id)


@app.route("/actividad/<int:id>/comentarios", methods=["GET"])
def obtener_comentarios(id):
    comentarios = db.get_comentarios(id)
    comentarios = [{
        "nombre": c.nombre,
        "texto": c.texto,
        "fecha": c.fecha.strftime("%Y-%m-%d %H:%M:%S")
    } for c in comentarios]
    return jsonify(comentarios)

@app.route("/actividad/<int:id>/comentarios", methods=["POST"])
def agregar_comentario(id):
    data = request.get_json()
    nombre = data.get("nombre", "").strip()
    texto = data.get("texto", "").strip()

    if not (3 <= len(nombre) <= 80) or len(texto) < 5:
        return jsonify({"error": "Validación fallida"}), 400

    fecha = datetime.now()
    db.create_comentario(nombre, texto, fecha ,id)
    return jsonify({"success": True}), 200




@app.route("/nueva-actividad", methods=["GET", "POST"])
def nueva():
    if request.method == "GET":
        return render_template("html/nueva-actividad.html")
    elif request.method == "POST":


        #Actividad
        comuna = request.form.get("Comunas").replace("+", " ")
        sector = request.form.get("sector-id").replace("+", " ")
        nombre = request.form.get("name-id").replace("+", " ")
        email = request.form.get("email-id")
        celular = request.form.get("codigo-id") + request.form.get("nro-id")
        inicio = request.form.get("hora-actual-id")
        inicio = datetime.strptime(inicio, "%Y-%m-%dT%H:%M")
        final = request.form.get("hora-sgte-id")
        final = datetime.strptime(final, "%Y-%m-%dT%H:%M")
        descripcion = request.form.get("description").replace("+", " ")
        if validate_activity(comuna, sector, nombre, email, celular, inicio, final, descripcion):
            print("New activity")
            activity_id = db.create_activity(comuna, sector, nombre, email, celular, inicio, final, descripcion)
        else:
            print("Failed activity")


        #Tema
        tema = request.form.get("temas")
        otro = request.form.get("otro-id").replace("+", " ")
        print(tema)
        if validate_tema(tema, otro):
            print("New tema")
            db.create_tema(tema, otro, activity_id)
            

        #Contacto
        contacto0 = [request.form.get("whatsapp-id").replace("+", " "), "whatsapp"]
        contacto1 = [request.form.get("telegram-id").replace("+", " "), "telegram"]
        contacto2 = [request.form.get("x-id").replace("+", " "), "x"]
        contacto3 = [request.form.get("instagram-id").replace("+", " "), "instagram"]
        contacto4 = [request.form.get("tiktok-id").replace("+", " "), "tiktok"]
        contacto5 = [request.form.get("otra-id").replace("+", " "), "otra"]
        contacts = [contacto0, contacto1, contacto2, contacto3, contacto4, contacto5]
        for contact in contacts:
            if contact[0]!="" and (len(contact[0]) <= 150):
                print("New contact")
                db.create_contact(contact[0], contact[1], activity_id)


        #Foto
        file0 = request.files.get("file")
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")
        file3 = request.files.get("file3")
        file4 = request.files.get("file4")
        files = [file0, file1, file2, file3, file4]
        for file in files:
            if file:
                _filename = hashlib.sha256(
                secure_filename(file.filename).encode("utf-8")
                ).hexdigest()
                _extension = filetype.guess(file).extension
                img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"
                print("New photo")
                db.create_photo(os.path.join(app.config["UPLOAD_FOLDER"], img_filename).replace("\\", "/"), _filename, activity_id)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))


        data = db.get_activities(5)
        return redirect(url_for('ver_actividad', id=activity_id))

