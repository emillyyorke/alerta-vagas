from sqlalchemy.orm import Session
from app import models, scraper, notifier

def executar_varredura_vagas(db: Session):
    termos_ativos = db.query(models.TermoBusca).filter(models.TermoBusca.ativo == True).all()
    
    for termo in termos_ativos:
        vagas_raspadas = scraper.buscar_vagas_na_web(termo.palavra_chave)
        vagas_novas_objetos = []

        for vaga_data in vagas_raspadas:
            vaga_existente = db.query(models.Vaga).filter(models.Vaga.link == vaga_data['link']).first()

            if not vaga_existente:
                nova_vaga = models.Vaga(
                    titulo=vaga_data['titulo'],
                    link=vaga_data['link'],
                    termo_id=termo.id
                )
                db.add(nova_vaga)
                vagas_novas_objetos.append(nova_vaga)
        
        if vagas_novas_objetos:
            db.commit()
            # Envia o e-mail para o dono do termo de busca
            notifier.enviar_alerta_vagas(termo.dono.email, vagas_novas_objetos)
            
            # Marca as vagas como notificadas no banco
            for v in vagas_novas_objetos:
                v.notificado = True
            db.commit()

    return "Processo concluído"