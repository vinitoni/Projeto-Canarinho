import cv2
import numpy as np
import face_recognition
import time
from datetime import datetime
import pygame
from .utils import carregar_passageiros, salvar_novo_passageiro, registrar_entrada_saida
from .geo import obter_localizacao_por_ip

pygame.mixer.init()
som_entrada = pygame.mixer.Sound("audios/entrada.wav")
som_saida = pygame.mixer.Sound("audios/saida.wav")

ultimo_registro_por_id = {}
faces_estaveis = {}

def iniciar_reconhecimento():
    print("Iniciando reconhecimento facial no ônibus...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    passageiros = carregar_passageiros()
    frame_count = 0
    ultimo_cadastro = 0
    tempo_saida = 0.25 * 60
    tempo_reentrada = 15
    tempo_minimo_parado = 1.0

    mensagem_exibida = ""
    tempo_mensagem = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        frame_count += 1
        agora = time.time()

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_crop = frame[top:bottom, left:right]
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            centro_atual = ((left + right) // 2, (top + bottom) // 2)
            parado = False

            if 'ultima_posicao' in faces_estaveis:
                ultima_posicao = faces_estaveis['ultima_posicao']
                tempo_inicial = faces_estaveis['tempo_inicial']
                distancia = np.linalg.norm(np.array(centro_atual) - np.array(ultima_posicao))
                if distancia < 15:
                    if agora - tempo_inicial >= tempo_minimo_parado:
                        parado = True
                else:
                    faces_estaveis['ultima_posicao'] = centro_atual
                    faces_estaveis['tempo_inicial'] = agora
            else:
                faces_estaveis['ultima_posicao'] = centro_atual
                faces_estaveis['tempo_inicial'] = agora

            if not parado:
                mensagem_exibida = "AGUARDE PARADO PARA RECONHECIMENTO"
                tempo_mensagem = agora
                continue

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
                    status = registrar_entrada_saida(
                        pid,
                        tempo_saida=tempo_saida,
                        tempo_reentrada=tempo_reentrada,
                        cache=ultimo_registro_por_id,
                        local=obter_localizacao_por_ip()
                    )

                    if status == "Entrada":
                        som_entrada.play()
                        mensagem_exibida = f"ENTRADA CONFIRMADA - ID {pid}"
                        tempo_mensagem = agora
                    elif status == "Saída":
                        som_saida.play()
                        mensagem_exibida = f"SAIDA REGISTRADA - ID {pid}"
                        tempo_mensagem = agora
                    else:
                        mensagem_exibida = f"ID {pid} - IGNORADO"
                        tempo_mensagem = agora

                    reconhecido = True
                    break

            if not reconhecido and agora - ultimo_cadastro > 5:
                novo_id = salvar_novo_passageiro(face_crop, encoding, local=obter_localizacao_por_ip())
                passageiros = carregar_passageiros()
                ultimo_registro_por_id[novo_id] = datetime.now()
                som_entrada.play()
                mensagem_exibida = f"USUARIO CADASTRADO - ID {novo_id}"
                tempo_mensagem = agora
                ultimo_cadastro = agora

        if mensagem_exibida and (time.time() - tempo_mensagem) < 2:
            cv2.rectangle(frame, (10, 10), (310, 50), (0, 0, 0), -1)
            cv2.putText(
                frame,
                mensagem_exibida.upper(),
                (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

        cv2.imshow("Reconhecimento Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
