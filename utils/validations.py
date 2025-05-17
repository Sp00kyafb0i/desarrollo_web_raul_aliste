import pymysql
import json
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, Date, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from database.db import Comuna, Actividad, Actividad_Tema, Contactar_Por, Foto, Region
import re



DB_NAME = "Tarea2"
DB_USERNAME = "root"
DB_PASSWORD = "2552"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

def validate_activity(comuna, sector, nombre, email, celular, inicio, final, descripcion):
    session = SessionLocal()
    com_bool = False
    comunas = session.query(Comuna).filter_by(nombre=comuna).all()
    for com in comunas:
        if com.nombre == comuna:
            com_bool = True
    sec_bool = (len(sector)<=100)
    nom_bool = (len(nombre)<=200 and len(nombre)>0)
    email_bool = (len(email)<=100 and len(email)>0 and bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)))
    cel_bool = (len(celular)==11)
    date_bool = (inicio < final)
    session.close()
    print(com_bool)
    print(sec_bool)
    print(nom_bool)
    print(email_bool)
    print(cel_bool)
    print(date_bool)
    return (com_bool and sec_bool and nom_bool and email_bool and cel_bool and date_bool)


def validate_tema(tema, otro):
    temas = ['música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro']
    if tema in temas:
        if tema == "otro":
            return (otro > 3 and otro <= 15)
        else:
            return True
    else:
        return False