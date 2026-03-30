from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services import executar_varredura_vagas

def tarefa_agendada():
    print("--- Iniciando Varredura Automática ---")
    db = SessionLocal()
    try:
        resultado = executar_varredura_vagas(db)
        print(f"Resultado da automação: {resultado}")
    finally:
        db.close()
    print("--- Fim da Varredura Automática ---")

def iniciar_agendador():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tarefa_agendada, 'interval', hours=24)
    scheduler.start()