import sqlite3
import pandas as pd
import streamlit as st

st.title("Dashboard de Passageiros - Ônibus")

conn = sqlite3.connect("banco.db")

st.subheader("👥 Registros de Passageiros")
df = pd.read_sql_query("""
    SELECT registros.id, passageiros.nome, passageiros.imagem, registros.timestamp, registros.local
    FROM registros
    JOIN passageiros ON passageiros.id = registros.id
    ORDER BY timestamp DESC
""", conn)

st.dataframe(df)

if st.checkbox("📈 Mostrar gráfico de frequência"):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    por_data = df.groupby(df['timestamp'].dt.date).count()['id']
    st.line_chart(por_data)
