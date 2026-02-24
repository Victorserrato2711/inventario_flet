import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_USER= os.getenv("DB_USER")
DB_PASS= os.getenv("DB_PASS")
DB_HOST= os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")
DB_NAME= os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"options": "-c client_encoding=UTF8"}
)

# Crear sesión
Session = sessionmaker(bind=engine)

# Clase base para los modelos
Base = declarative_base()

def get_db():
    return Session()


# Prueba de conexión
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ Conexión exitosa a PostgreSQL")
    except Exception as e:
        print("❌ Error al conectar a PostgreSQL:", e)
