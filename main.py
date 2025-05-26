import cv2
import os
import sqlite3
import face_recognition
import numpy as np
from datetime import datetime
import pickle

# Pastas e banco
os.makedirs("passageiros", exist_ok=True)
os.makedirs("embeddings", exist_ok=True)

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS passageiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imagem TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER,
        timestamp TEXT
    )
''')

conn.commit()

# Carregar embeddings
def carregar_passageiros():
    passageiros = []
    for arquivo in os.listdir("embeddings"):
        if arquivo.endswith(".pkl"):
            pid = int(arquivo.split(".")[0])
            with open(f"embeddings/{pid}.pkl", "rb") as f:
                encoding = pickle.load(f)
                passageiros.append((pid, encoding))
    return passageiros

# Salvar novo passageiro
def salvar_novo_passageiro(face_img, encoding):
    novo_id = len(os.listdir("embeddings")) + 1
    caminho_img = f"passageiros/{novo_id}.jpg"
    caminho_emb = f"embeddings/{novo_id}.pkl"
    cv2.imwrite(caminho_img, face_img)
    with open(caminho_emb, "wb") as f:
        pickle.dump(encoding, f)
    cursor.execute("INSERT INTO passageiros (imagem) VALUES (?)", (caminho_img,))
    cursor.execute("INSERT INTO registros (id, timestamp) VALUES (?, ?)", (novo_id, datetime.now()))
    conn.commit()
    return novo_id

# Registrar entrada
ultimos_registros = {}
def registrar(id):
    agora = datetime.now()
    ultimo = ultimos_registros.get(id)
    if not ultimo or (agora - ultimo).total_seconds() > 30:
        cursor.execute("INSERT INTO registros (id, timestamp) VALUES (?, ?)", (id, agora.strftime("%Y-%m-%d %H:%M:%S")))
        ultimos_registros[id] = agora
        conn.commit()

# Inicializar webcam com resolução baixa
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

passageiros = carregar_passageiros()
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    frame_count += 1

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_crop = frame[top:bottom, left:right]
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        if frame_count % 5 != 0:
            continue  # só processa a cada 5 frames

        try:
            encoding = face_recognition.face_encodings(rgb_frame, [face_location])[0]
        except IndexError:
            continue

        reconhecido = False
        for pid, emb in passageiros:
            distancia = np.linalg.norm(encoding - emb)
            if distancia < 0.45:  # limiar ajustável
                cv2.putText(frame, f"ID: {pid}", (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                registrar(pid)
                reconhecido = True
                break

        if not reconhecido:
            novo_id = salvar_novo_passageiro(face_crop, encoding)
            passageiros = carregar_passageiros()
            cv2.putText(frame, f"Novo ID: {novo_id}", (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    cv2.imshow("Reconhecimento Facial", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
