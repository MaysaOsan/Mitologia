from sqlmodel import create_engine, SQLModel, Session
from models.seres import Ser
import os

#Datos de sesión
db_user: str = "quevedo"
db_password: str =  "1234"
db_server: str = "fastapi-db"  #preuba .2 localhost
db_port: int = 5432        #3306  cuando teniamos sql
db_name: str = "seriesdb"  

#Conexión a la base de datos
#DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"   Para MySQL
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("DB_URL", DATABASE_URL),echo=True)

def get_session():
    with Session(engine) as session: #creamos una sesión
        yield session #sirve para que el contexto de la sesión se cierre

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Ser(id=1, nombre="Cronos", raza="titan",titulo="Titan del Tiempo", esDios=False, fechaDeCreacion="2024-1-18"))
        session.add(Ser(id=2, nombre="Gaia", raza="titan", titulo="Titanide de la Tierra", esDios= False, fechaDeCreacion="2024-11-12"))
        session.add(Ser(id=3, nombre="Zeus", raza="dios", titulo="Dios del cielo, el trueno y el rayo", esDios=True, fechaDeCreacion="2024-1-18"))
        session.add(Ser(id=4, nombre="Aquiles", raza="Semidios", titulo="guerrero de Troya", esDios=False, fechaDeCreacion="2025-3-5"))
        session.commit()
        #session.refesh_all() #actualiza los datos en la base de datos



## O pudo ser:
# session.add.all(losSeres)
#losSeres: list[Ser] = [
#    Ser(id=1, nombre="Cronos", raza="titan",titulo="Titan del Tiempo", esDios=False, fechaDeCreacion=date(2024,1,18)),
#    Ser(id=2, nombre="Gaia", raza="titan", titulo="Titanide de la Tierra", esDios= False, fechaDeCreacion=date(2024,11,12)),
#    Ser(id=3, nombre="Zeus", raza="dios", titulo="Dios del cielo, el trueno y el rayo", esDios=True, fechaDeCreacion=date(2024,1,18)),
#    Ser(id=4, nombre="Aquiles", raza="Semidios", titulo="guerrero de Troya", esDios=False, fechaDeCreacion=date(2025,3,5))
#]