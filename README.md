# 🚌 Projeto Canarinho – Reconhecimento Facial Embarcado

Este projeto utiliza **reconhecimento facial** em tempo real para registrar automaticamente passageiros ao entrarem em um ônibus. Ideal para rodar em dispositivos embarcados como o **Raspberry Pi**.

---

## 🎯 Objetivo

Registrar e identificar rostos de passageiros por meio da câmera embarcada, armazenando os dados localmente em um banco SQLite com os horários de entrada, além de disponibilizar um **dashboard interativo** via Streamlit para análise posterior.

---

## 📷 Funcionalidades

- 📸 Detecção facial em tempo real via webcam
- 🆕 Registro automático de novos passageiros não reconhecidos
- 🧠 Reconhecimento por similaridade com embeddings faciais
- 💾 Armazenamento local em banco de dados SQLite
- ☁️ Backup e simulação de sincronização com armazenamento em nuvem
- 📊 Dashboard em Streamlit para análise de registros
- 🧩 Estrutura modular de código
- 🪶 Leve e eficiente para rodar em **Raspberry Pi** (resolução reduzida, baixo consumo de memória)

---

## ⚙️ Como Usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/projeto-canarinho.git
   cd projeto-canarinho
````
pip install -r requirements.txt
````
````
python reconhecimento.py
````
````
streamlit run dashboard.py
