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
    ultimo_cadastro = 0
    delay_reconhecimento = 5  # processar reconhecimento facial a cada 5 frames
    frame_count = 0

    print("[INFO] Reconhecimento iniciado. Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERRO] Falha ao capturar imagem da câmera.")
            break

        frame_count += 1
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if frame_count % delay_reconhecimento == 0:
            encodings_atual_frame = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_location, encoding in zip(face_locations, encodings_atual_frame):
                top, right, bottom, left = face_location
                face_crop = frame[top:bottom, left:right]

                reconhecido = False
                for pid, emb in passageiros:
                    distance = np.linalg.norm(encoding - emb)
                    if distance < 0.45:
                        status = registrar_entrada_saida(pid)

                        # Visual feedback
                        cor = (0, 255, 0) if status == "Entrada" else (0, 0, 255)
                        texto = f"{status} - ID: {pid}" if status != "Ignorado" else f"ID {pid} - Ignorado"
                        cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)
                        cv2.putText(frame, texto, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 2)

                        reconhecido = True
                        break

                if not reconhecido and time.time() - ultimo_cadastro > 5:
                    novo_id = salvar_novo_passageiro(face_crop, encoding)
                    passageiros = carregar_passageiros()  # Atualiza lista com novo passageiro
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 165, 255), 2)
                    cv2.putText(frame, f"Novo ID: {novo_id}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
                    ultimo_cadastro = time.time()

        else:
            # Desenha bounding boxes sem tentar reconhecer
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (100, 100, 100), 1)

        cv2.imshow("Reconhecimento Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("[INFO] Encerrando reconhecimento.")
            break

    cap.release()
    cv2.destroyAllWindows()
