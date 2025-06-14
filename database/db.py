import pymysql
import json
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship



DB_NAME = "tarea2"
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=False)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=True)
    descripcion = Column(String(500), nullable=True)

class Actividad_Tema(Base):
    __tablename__ = 'actividad_tema'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música','deporte','ciencias','religión','política','tecnología','juegos','baile','comida','otro', name='tema_enum'))
    glosa_otro = Column(String(15), nullable=True)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

class Contactar_Por(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp','telegram','X','instagram','tiktok','otra', name='contacto_enum'))
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)


class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(DateTime, nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)




########### FUNCTIONS #############
def create_comentario(nombre, texto, fecha, actividad_id):
    session = SessionLocal()
    new_comment = Comentario(nombre=nombre, texto=texto, fecha=fecha, actividad_id=actividad_id)
    session.add(new_comment)
    session.commit()
    session.close()

def get_comentarios(id_actividad):
    session = SessionLocal()
    comentarios = session.query(Comentario).filter_by(actividad_id=id_actividad).all()
    session.close()
    return comentarios


def create_contact(text, type, activity_id):
    session = SessionLocal()
    new_contact = Contactar_Por(nombre = type, identificador=text, actividad_id=activity_id)
    session.add(new_contact)
    session.commit()
    session.close()



def create_tema(tema, otro, activity_id):
    session = SessionLocal()
    new_tema = Actividad_Tema(tema=tema, glosa_otro = otro, actividad_id=activity_id)
    session.add(new_tema)
    session.commit()
    session.close()

def get_activities(n):
    session = SessionLocal()
    if n:
        events = session.query(Actividad).limit(n).all()
    else:
        events = session.query(Actividad).all()
    session.close()
    return events

def create_activity(comuna_nombre, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    comuna_id = session.query(Comuna).filter_by(nombre=comuna_nombre).first().id
    new_activity = Actividad(comuna_id=comuna_id, sector=sector, nombre=nombre, email=email, celular=celular, dia_hora_inicio=dia_hora_inicio, dia_hora_termino=dia_hora_termino, descripcion=descripcion)
    
    session.add(new_activity)
    session.commit()
    id = int(new_activity.id)
    session.close()
    
    return id

def create_photo(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()
    new_photo = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, actividad_id=actividad_id)
    session.add(new_photo)
    session.commit()
    session.close()

def get_actividad_by_id(id):
    session = SessionLocal()
    user = session.query(Actividad).filter_by(id=id).first()
    session.close()
    return user

def get_photos(id):
    session = SessionLocal()
    photos = session.query(Foto).filter_by(actividad_id=id).all()
    if photos:
        fst = photos[0]
        session.close()
        return [fst, photos]
    session.close()
    return

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




def estadisticas_por_dia():
    actividades = get_activities(None)  # obtener todas
    conteo = {}
    for act in actividades:
        dia = act.dia_hora_inicio.date()
        if dia not in conteo:
            conteo[dia] = 0
        conteo[dia] += 1
    return [{"dia": str(k), "cantidad": v} for k, v in sorted(conteo.items())]


def estadisticas_por_tipo():
    actividades = get_activities(None)
    conteo = {}
    for act in actividades:
        tema = get_tema(act.id)
        if tema.tema not in conteo:
            conteo[tema.tema] = 0
        conteo[tema.tema] += 1
    return [{"tipo": k, "cantidad": v} for k, v in conteo.items()]



def estadisticas_por_franja():
    actividades = get_activities(None)
    franjas = {
        "mañana": {},
        "mediodía": {},
        "tarde": {}
    }
    meses_set = set()

    for act in actividades:
        mes = act.dia_hora_inicio.strftime("%Y-%m")
        hora = act.dia_hora_inicio.hour
        if hora < 12:
            franja = "mañana"
        elif hora < 14:
            franja = "mediodía"
        else:
            franja = "tarde"

        if mes not in franjas[franja]:
            franjas[franja][mes] = 0
        franjas[franja][mes] += 1
        meses_set.add(mes)

    meses = sorted(meses_set)
    return {
        "meses": meses,
        "manana": [franjas["mañana"].get(m, 0) for m in meses],
        "mediodia": [franjas["mediodía"].get(m, 0) for m in meses],
        "tarde": [franjas["tarde"].get(m, 0) for m in meses],
    }

