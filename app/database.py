import sqlite3
import os

os.makedirs("passageiros", exist_ok=True)
os.makedirs("embeddings", exist_ok=True)

conn = sqlite3.connect("banco.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS passageiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imagem TEXT,
        nome TEXT DEFAULT '',
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER,
        timestamp TEXT,
        local TEXT DEFAULT 'onibus_01',
        FOREIGN KEY (id) REFERENCES passageiros(id)
    )
''')

conn.commit()
