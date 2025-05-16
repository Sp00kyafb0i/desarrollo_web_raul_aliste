import pymysql
import json
from sqlalchemy import create_engine, Column, integer, BigInteger, String, ForeignKey, Date, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship



DB_NAME = "Tarea2"
DB_USERNAME = "root"
DB_PASSWORD = "2552"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()



####### MODELS: #######

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(integer, primary_key=True, autoincrement=True)
    comuna_id = Column(integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=False)
    dia_hora_inicio = Column(Date, nullable=False)
    dia_hora_termino = Column(Date, nullable=True)
    descripcion = Column(String(500), nullable=True)

class Actividad_Tema(Base):
    __tablename__ = 'actividad_tema'
    id = Column(integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música','deporte','ciencias','religión','política','tecnología','juegos','baile','comida','otro', name='tema_enum'))
    glosa_otro = Column(String(15), nullable=True)
    actividad_id = Column(integer, ForeignKey('actividad.id'), nullable=False)

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(integer, ForeignKey('region.id'), nullable=False)

class Contactar_Por(Base):
    __tablename__ = 'contactar_por'
    id = Column(integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp','telegram','X','instagram','tiktok','otra', name='contacto_enum'))
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(integer, ForeignKey('actividad.id'), nullable=False)

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(integer, ForeignKey('actividad.id'), nullable=False)


class Region(Base):
    __tablename__ = 'region'
    id = Column(integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)




########### FUNCTIONS #############


def get_activities(n):
    session = SessionLocal()
    if n:
        events = session.query(Actividad).limit(n).all()
    else:
        events = session.query(Actividad).all()
    session.close()
    return events

def create_activity(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    new_activity = Actividad(comuna_id=comuna_id, sector=sector, nombre=nombre, email=email, celular=celular, dia_hora_inicio=dia_hora_inicio, dia_hora_termino=dia_hora_termino, descripcion=descripcion)
    session.add(new_activity)
    session.commit
    session.close()

def create_photo(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()
    new_photo = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, actividad_id=actividad_id)
    session.add(new_photo)
    session.commit
    session.close()

def get_actividad_by_id(id):
    session = SessionLocal()
    user = session.query(Actividad).filter_by(id=id).first()
    session.close()
    return user

def get_photos(id):
    session = SessionLocal()
    photos = session.query(Foto).filter_by(actividad_id=id).all()
    fst = photos[0]
    session.close()
    return [fst, photos]

def get_photo_path_name(id):
    session = SessionLocal()
    path = session.query(Foto).filter_by(id=id).first().ruta_archivo
    name = session.query(Foto).filter_by(id=id).first().nombre_archivo
    session.close()
    return [path, name]

def get_tema(actividad_id):
    session = SessionLocal()
    tema = session.query(Actividad_Tema).filter_by(actividad_id=actividad_id).first()
    session.close()
    return tema

def get_comuna(actividad_id):
    session = SessionLocal()
    user = session.query(Actividad).filter_by(id=actividad_id).first().comuna_id
    comuna = session.query(Comuna).filter_by(id=user).first()
    session.close()
    return comuna