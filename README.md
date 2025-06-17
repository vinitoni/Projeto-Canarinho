# 🚌 Sistema de Reconhecimento Facial Embarcado no Ônibus

## 📄 Descrição Geral

Este sistema registra automaticamente a **entrada** e **saída** de passageiros em um ônibus por meio de **reconhecimento facial**. Ideal para uso local com Raspberry Pi ou notebooks, o sistema inclui feedback sonoro, localização geográfica (bairro e ponto fictícios), painel de controle web e banco de dados leve.

---

## ⚖️ Funcionalidades

### ✅ Reconhecimento Facial (OpenCV + face\_recognition)

* Detecção em tempo real pela câmera.
* Registro só é feito se o rosto estiver parado por pelo menos **1 segundo**.
* Verificação com base em embeddings salvos (arquivos .pkl).

### ✅ Registro Inteligente de Entrada/Saída

* Cadastro de novos passageiros com imagem + vetor facial.
* **Evita cadastros duplicados** se a pessoa já foi registrada.
* Se passageiro estiver dentro do ônibus por mais de 15s, é registrada saída.
* Se estiver fora por 15s ou mais, nova entrada é registrada.
* Ignora repetições em um intervalo de 15s.

### ✅ Sons de Feedback (via pygame)

* Som de entrada (entrada.wav).
* Som de saída (saida.wav).

### ✅ Localização Geográfica Realista + Fictícia

* Tenta pegar a cidade real via IP (ip-api.com).
* Bairro é sorteado de uma lista de bairros reais.
* Ponto é sorteado entre 1 e 50.
* Local de entrada e local de saída são **distintos**, atualizados dinamicamente.

### ✅ Painel Web (Streamlit)

* Lista com foto, nome, entrada, saída, tempo de permanência.
* **Local de entrada e local de saída** exibidos separadamente.
* Filtros por nome.
* Edição do nome.
* Exclusão de passageiros + registros.
* Botão de reset total.

---

## 📂 Estrutura de Pastas

```
codigo_reconhecimento/
├── app/
│   ├── camera.py
│   ├── utils.py
│   ├── geo.py
│   └── database.py
├── passageiros/            # Fotos salvas
├── embeddings/             # Embeddings salvos (.pkl)
├── audios/                 # entrada.wav / saida.wav
├── dashboard.py            # Painel Streamlit
├── main.py                 # Inicia reconhecimento
├── start.py                # Inicia painel
├── banco.db                # Banco SQLite
```

---

## 📈 Parâmetros de Controle

| Parâmetro                 | Valor atual   | Descrição                              |
| ------------------------- | ------------- | -------------------------------------- |
| `tempo_saida`             | `15 segundos` | Tempo mínimo para considerar saída     |
| `tempo_reentrada`         | `15 segundos` | Evita duplicar entrada                 |
| `tempo_minimo_parado`     | `1 segundo`   | Exige rosto estável antes de registrar |
| `face_distance_threshold` | `0.45`        | Precisão para reconhecimento facial    |

---

## 🚀 Como Executar o Projeto

### 1. Instalar dependências:

```bash
pip install opencv-python face_recognition pygame streamlit requests pillow
```

### 2. Rodar reconhecimento facial:

```bash
python main.py
```

### 3. Abrir o painel em outra aba:

```bash
python start.py
```

Acesse: [http://localhost:8501](http://localhost:8501)

---

## 💼 Tecnologias Usadas

* Python 3.11+
* OpenCV
* face\_recognition
* Streamlit
* SQLite3
* pygame
* requests
* Pillow (PIL)

---

**Desenvolvido por: \[Vinícius Toni]**

Projeto educacional para controle inteligente de passageiros em transporte coletivo urbano usando reconhecimento facial.
