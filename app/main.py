from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db
from app import services
from app.scheduler import iniciar_agendador
from fastapi.middleware.cors import CORSMiddleware

# Cria as tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Alerta de Vagas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Libera o acesso para o React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "mensagem": "Servidor rodando e banco conectado!"}

# --- NOVA ROTA: CADASTRO DE USUÁRIO ---
@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verifica se o e-mail já existe no banco
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado na plataforma.")
    
    # 2. Criptografa a senha (aqui vamos fazer algo simples por enquanto, mas no mundo real usaríamos a biblioteca Passlib)
    senha_falsa_hash = usuario.senha + "_hashsecreto" 
    
    # 3. Prepara o objeto para salvar no banco
    novo_usuario = models.Usuario(
        nome=usuario.nome, 
        email=usuario.email, 
        senha_hash=senha_falsa_hash
    )
    
    # 4. Salva no banco de dados
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario) # Atualiza para pegar o ID gerado pelo PostgreSQL
    
    return novo_usuario

# --- CADASTRAR TERMO DE BUSCA ---
@app.post("/usuarios/{usuario_id}/termos/", response_model=schemas.TermoBuscaResponse)
def criar_termo_para_usuario(
    usuario_id: int, 
    termo: schemas.TermoBuscaCreate, 
    db: Session = Depends(get_db)
):
    # 1. Verifica se o usuário existe no banco
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # 2. Cria o termo associado ao ID do usuário
    novo_termo = models.TermoBusca(
        palavra_chave=termo.palavra_chave,
        usuario_id=usuario_id
    )
    
    # 3. Salva no banco
    db.add(novo_termo)
    db.commit()
    db.refresh(novo_termo)
    
    return novo_termo

# --- ROTA PARA RODAR A VARREDURA MANUALMENTE ---
@app.post("/admin/varredura/")
def rodar_varredura_manual(db: Session = Depends(get_db)):
    total = services.executar_varredura_vagas(db)
    return {"status": "sucesso", "vagas_novas_encontradas": total}

@app.get("/vagas/")
def listar_vagas_do_banco(db: Session = Depends(get_db)):
    return db.query(models.Vaga).all()

# Rota para agendador
@app.on_event("startup")
def on_startup():
    iniciar_agendador()
    print("Agendador de tarefas iniciado com sucesso!")