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

st.markdown("## 📋 Histórico de Entradas e Saídas")

# Leitura dos registros com locais separados
df = pd.read_sql_query("""
    SELECT registros.rowid AS registro_id, registros.id, passageiros.nome, passageiros.imagem, 
           registros.entrada, registros.saida, registros.local_entrada, registros.local_saida
    FROM registros 
    JOIN passageiros ON passageiros.id = registros.id 
    ORDER BY registros.entrada DESC
""", conn)

# Filtros
with st.sidebar:
    st.header("🔍 Filtros")
    filtro_nome = st.text_input("Filtrar por nome")
    if filtro_nome:
        df = df[df["nome"].str.contains(filtro_nome, case=False, na=False)]
    st.header("⚙️ Administração")

    if st.button("🧹 Limpar TODOS os dados"):
        st.warning("Você está prestes a deletar TODOS os dados. Essa ação é irreversível!")
        if st.button("🚨 Confirmar exclusão TOTAL"):
            cursor.execute("DELETE FROM registros")
            cursor.execute("DELETE FROM passageiros")
            conn.commit()
            for pasta in ["passageiros", "embeddings"]:
                for arquivo in os.listdir(pasta):
                    os.remove(os.path.join(pasta, arquivo))
            st.success("Todos os dados foram apagados com sucesso. Recarregue a página.")

# Mostrar registros
for _, row in df.iterrows():
    entrada = row['entrada']
    saida = row['saida']
    nome = row['nome'] or "Sem nome"
    permanencia = "---"

    if entrada and saida:
        dt_entrada = pd.to_datetime(entrada)
        dt_saida = pd.to_datetime(saida)
        permanencia = str(dt_saida - dt_entrada)
    elif entrada and not saida:
        permanencia = "Ainda no ônibus"

    with st.expander(f"🧍 ID {row['id']} - {nome} ({entrada})"):
        cols = st.columns([1, 2])
        with cols[0]:
            if os.path.exists(row["imagem"]):
                st.image(Image.open(row["imagem"]), width=150)
            else:
                st.warning("Imagem não encontrada.")
        with cols[1]:
            st.markdown(f"**🕒 Entrada:** {entrada or '---'}")
            st.markdown(f"**📍 Local de Entrada:** {row['local_entrada'] or '---'}")
            st.markdown(f"**🚪 Saída:** {saida or '---'}")
            st.markdown(f"**📍 Local de Saída:** {row['local_saida'] or '---'}")
            st.markdown(f"**⏳ Permanência:** {permanencia}")

            novo_nome = st.text_input("Editar nome", value=nome, key=f"nome_{row['registro_id']}")
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
