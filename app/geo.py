import requests
import random

BAIRROS_FAKE = [
    "Água Verde", "Águas Claras", "Amizade", "Barra do Rio Cerro", "Barra do Rio Molha",
    "Boa Vista", "Braço Ribeirão Cavalo", "Centenário", "Centro", "Chico de Paulo",
    "Czerniewicz", "Estrada Nova", "Ilha da Figueira", "Jaraguá 84", "Jaraguá 99",
    "Jaraguá Esquerdo", "João Pessoa", "Nereu Ramos", "Nova Brasília", "Parque Malwee",
    "Rau", "Ribeirão Cavalo", "Rio Cerro I", "Rio Cerro II", "Rio da Luz", "Rio Molha",
    "Santa Luzia", "Santo Antônio", "São Luís", "Tifa Martins", "Tifa Monos",
    "Três Rios do Norte", "Três Rios do Sul", "Vieira", "Vila Baependi", "Vila Lalau",
    "Vila Lenzi", "Vila Nova"
]

def obter_localizacao_por_ip():
    try:
        response = requests.get("http://ip-api.com/json/").json()
        cidade = response.get("city", "Cidade Desconhecida")
    except Exception:
        cidade = "Cidade Fictícia"

    bairro = random.choice(BAIRROS_FAKE)
    ponto = random.randint(1, 50)

    return f"{bairro} - {cidade} / Ponto {ponto}"
