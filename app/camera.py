import cv2
import numpy as np
import face_recognition
from .utils import carregar_passageiros, salvar_novo_passageiro, registrar

def iniciar_reconhecimento():
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
                continue

            try:
                encoding = face_recognition.face_encodings(rgb_frame, [face_location])[0]
            except IndexError:
                continue

            reconhecido = False
        for pid, emb in passageiros:
            matches = face_recognition.compare_faces([emb], encoding, tolerance=0.35)
            if matches[0]:
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
