import requests
from bs4 import BeautifulSoup
import urllib.parse

SITES_CONFIG = [
    {
        "nome": "Trabalha Brasil",
        "url_base": "https://www.trabalhabrasil.com.br/vagas-empregos/{}",
        "seletor": {"tag": "a", "class": "job__link"},
        "atributo_link": "href",
        "prefixo_url": ""
    },
    {
        "nome": "Vagas.com",
        "url_base": "https://www.vagas.com.br/vagas-de-{}",
        "seletor": {"tag": "a", "class": "link-detalhes-vaga"},
        "atributo_link": "href",
        "prefixo_url": "https://www.vagas.com.br"
    }
]

def buscar_vagas_na_web(palavra_chave: str):
    vagas_totais = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for site in SITES_CONFIG:
        print(f"Buscando em {site['nome']}...")
        
        # Ajuste específico de URL por site
        termo = palavra_chave.lower().replace(" ", "-")
        url = site['url_base'].format(termo)
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                tags = soup.find_all(site['seletor']['tag'], class_=site['seletor']['class'])
                
                for tag in tags:
                    link = tag.get(site['atributo_link'], '')
                    titulo = tag.get_text(strip=True) or tag.get('title')
                    
                    if link.startswith('/') and site['prefixo_url']:
                        link = site['prefixo_url'] + link
                        
                    if link and titulo:
                        vagas_totais.append({"titulo": titulo, "link": link})
            else:
                print(f"Status {res.status_code} em {site['nome']}")
        except Exception as e:
            print(f"Erro em {site['nome']}: {e}")

    print(f"Busca finalizada. Total: {len(vagas_totais)} vagas.")
    return vagas_totais

if __name__ == "__main__":
    # Teste com um termo mais simples para garantir o retorno
    resultado = buscar_vagas_na_web("Suporte")
    for v in resultado[:5]:
        print(f"[{v['titulo']}] -> {v['link']}")