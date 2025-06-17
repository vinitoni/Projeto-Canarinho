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

def salvar_novo_passageiro(face_img, encoding, local="ônibus"):
    cursor.execute("INSERT INTO passageiros (imagem) VALUES (?)", ("temporario.jpg",))
    novo_id = cursor.lastrowid
    caminho_img = f"passageiros/{novo_id}.jpg"
    caminho_emb = f"embeddings/{novo_id}.pkl"
    cv2.imwrite(caminho_img, face_img)
    with open(caminho_emb, "wb") as f:
        pickle.dump(encoding, f)
    cursor.execute("UPDATE passageiros SET imagem = ? WHERE id = ?", (caminho_img, novo_id))
    cursor.execute(
        "INSERT INTO registros (id, entrada, local) VALUES (?, ?, ?)", 
        (novo_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), local)
    )
    conn.commit()
    return novo_id

def registrar_entrada_saida(id, tempo_saida=15*60, tempo_reentrada=10, local="ônibus", cache=None):
    agora = datetime.now()
    agora_str = agora.strftime("%Y-%m-%d %H:%M:%S")

    if cache is not None:
        ultimo = cache.get(id)
        if ultimo and (agora - ultimo).total_seconds() < tempo_reentrada:
            return "Ignorado"

    cursor.execute("SELECT entrada, saida FROM registros WHERE id = ? ORDER BY rowid DESC LIMIT 1", (id,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO registros (id, entrada, local) VALUES (?, ?, ?)", (id, agora_str, local))
        conn.commit()
        if cache is not None:
            cache[id] = agora
        return "Entrada"

    entrada_str, saida_str = row

    if entrada_str and not saida_str:
        entrada_dt = datetime.strptime(entrada_str, "%Y-%m-%d %H:%M:%S")
        if (agora - entrada_dt).total_seconds() > tempo_saida:
            cursor.execute("UPDATE registros SET saida = ? WHERE id = ? AND entrada = ?", (agora_str, id, entrada_str))
            conn.commit()
            if cache is not None:
                cache[id] = agora
            return "Saída"
        else:
            return "Ignorado"

    elif entrada_str and saida_str:
        cursor.execute("INSERT INTO registros (id, entrada, local) VALUES (?, ?, ?)", (id, agora_str, local))
        conn.commit()
        if cache is not None:
            cache[id] = agora
        return "Entrada"

    return "Ignorado"
