# 🚌 Projeto Canarinho – Reconhecimento Facial Embarcado

Este projeto utiliza **reconhecimento facial** em tempo real para registrar automaticamente passageiros ao entrarem em um ônibus. Ideal para rodar em dispositivos embarcados como o **Raspberry Pi**.

## 🎯 Objetivo

Registrar e identificar rostos de passageiros por meio da câmera embarcada, armazenando os dados localmente em um banco SQLite com os horários de entrada e um histórico de imagens e embeddings.

---

## 📷 Funcionalidades

- Detecção facial em tempo real via webcam.
- Registro automático de novos passageiros não reconhecidos.
- Identificação por similaridade facial com histórico local.
- Armazenamento em banco de dados SQLite.
- Design leve para rodar em **Raspberry Pi** (baixa resolução, pouca RAM).

---

## ⚙️ Requisitos

### ✅ Bibliotecas Python

Instale com:

```bash
pip install -r requirements.txt


````
Ou manualmente:

pip install opencv-python face-recognition numpy
