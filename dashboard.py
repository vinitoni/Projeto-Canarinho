import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import os

# Conexão com banco
conn = sqlite3.connect("banco.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(page_title="Painel de Passageiros", layout="wide")
st.title("🚌 Dashboard – Reconhecimento Facial no Ônibus")

st.markdown("### 📋 Histórico de Registros")
df = pd.read_sql_query("""
    SELECT registros.rowid AS registro_id, registros.id, passageiros.nome, passageiros.imagem, 
           registros.timestamp, registros.local 
    FROM registros 
    JOIN passageiros ON passageiros.id = registros.id 
    ORDER BY timestamp DESC
""", conn)

# Filtros
with st.sidebar:
    st.header("🔍 Filtros")
    filtro_nome = st.text_input("Filtrar por nome")
    if filtro_nome:
        df = df[df["nome"].str.contains(filtro_nome, case=False, na=False)]

# Mostrar registros
for i, row in df.iterrows():
    with st.expander(f"📌 ID {row['id']} - {row['nome'] or 'Sem nome'} ({row['timestamp']})"):
        cols = st.columns([1, 2])
        with cols[0]:
            if os.path.exists(row["imagem"]):
                st.image(Image.open(row["imagem"]), width=150)
            else:
                st.warning("Imagem não encontrada.")
        with cols[1]:
            novo_nome = st.text_input("Editar nome", value=row["nome"], key=f"nome_{row['registro_id']}")
            if st.button("Salvar", key=f"salvar_{row['registro_id']}"):
                cursor.execute("UPDATE passageiros SET nome = ? WHERE id = ?", (novo_nome, row["id"]))
                conn.commit()
                st.success("Nome atualizado!")

            if st.button("🗑️ Deletar passageiro", key=f"del_{row['registro_id']}"):
                cursor.execute("DELETE FROM passageiros WHERE id = ?", (row["id"],))
                cursor.execute("DELETE FROM registros WHERE id = ?", (row["id"],))
                conn.commit()
                img_path = row["imagem"]
                emb_path = img_path.replace("passageiros", "embeddings").replace(".jpg", ".pkl")
                for path in [img_path, emb_path]:
                    if os.path.exists(path):
                        os.remove(path)
                st.warning("Passageiro excluído. Recarregue a página.")
