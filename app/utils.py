import os
import pickle
import cv2
from datetime import datetime
from .database import conn, cursor

def carregar_passageiros():
    passageiros = []
    for arquivo in os.listdir("embeddings"):
        if arquivo.endswith(".pkl"):
            pid = int(arquivo.split(".")[0])
            with open(f"embeddings/{pid}.pkl", "rb") as f:
                encoding = pickle.load(f)
                passageiros.append((pid, encoding))
    return passageiros

def salvar_novo_passageiro(face_img, encoding):
    cursor.execute("INSERT INTO passageiros (imagem) VALUES (?)", ("temporario.jpg",))
    novo_id = cursor.lastrowid
    caminho_img = f"passageiros/{novo_id}.jpg"
    caminho_emb = f"embeddings/{novo_id}.pkl"
    cv2.imwrite(caminho_img, face_img)
    with open(caminho_emb, "wb") as f:
        pickle.dump(encoding, f)
    cursor.execute("UPDATE passageiros SET imagem = ? WHERE id = ?", (caminho_img, novo_id))
    cursor.execute("INSERT INTO registros (id, timestamp) VALUES (?, ?)", (novo_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    return novo_id

ultimos_registros = {}

def registrar(id):
    agora = datetime.now()
    ultimo = ultimos_registros.get(id)
    if not ultimo or (agora - ultimo).total_seconds() > 30:
        cursor.execute("INSERT INTO registros (id, timestamp) VALUES (?, ?)", (id, agora.strftime("%Y-%m-%d %H:%M:%S")))
        ultimos_registros[id] = agora
        conn.commit()
