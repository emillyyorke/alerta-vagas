from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexão: usuario:senha@host:porta/nome_do_banco
SQLALCHEMY_DATABASE_URL = "postgresql://admin:sua_senha_segura@localhost:5432/vagas_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()