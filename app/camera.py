import cv2
import numpy as np
import face_recognition
import time
from .utils import carregar_passageiros, salvar_novo_passageiro, registrar_entrada_saida

def iniciar_reconhecimento():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    passageiros = carregar_passageiros()
    frame_count = 0
    ultimo_cadastro = 0

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
                continue

            try:
                encoding = face_recognition.face_encodings(rgb_frame, [face_location])[0]
            except IndexError:
                continue

            reconhecido = False
            for pid, emb in passageiros:
                distance = np.linalg.norm(encoding - emb)
                if distance < 0.45:
                    status = registrar_entrada_saida(pid)

                    if status != "Ignorado":
                        cor = (0, 255, 0) if status == "Entrada" else (0, 0, 255)
                        cv2.putText(frame, f"{status} - ID: {pid}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)
                    else:
                        cv2.putText(frame, f"ID {pid} - Ignorado", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)

                    reconhecido = True
                    break

            if not reconhecido and time.time() - ultimo_cadastro > 5:
                novo_id = salvar_novo_passageiro(face_crop, encoding)
                passageiros = carregar_passageiros()
                cv2.putText(frame, f"Novo ID: {novo_id}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
                ultimo_cadastro = time.time()

        cv2.imshow("Reconhecimento Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
