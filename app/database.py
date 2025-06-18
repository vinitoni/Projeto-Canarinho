import sqlite3
import os

os.makedirs("passageiros", exist_ok=True)
os.makedirs("embeddings", exist_ok=True)

# Conexão com o banco
conn = sqlite3.connect("banco.db", check_same_thread=False)
cursor = conn.cursor()

#Passageiros
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passageiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imagem TEXT,
        nome TEXT DEFAULT '',
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute("PRAGMA table_info(registros)")
colunas = [col[1] for col in cursor.fetchall()]

if "registros" in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")]:
    if "local_entrada" not in colunas:
        cursor.execute("ALTER TABLE registros ADD COLUMN local_entrada TEXT DEFAULT 'ônibus'")
    if "local_saida" not in colunas:
        cursor.execute("ALTER TABLE registros ADD COLUMN local_saida TEXT")
else:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER,
            entrada TEXT,
            saida TEXT,
            local_entrada TEXT DEFAULT 'ônibus',
            local_saida TEXT,
            FOREIGN KEY (id) REFERENCES passageiros(id)
        )
    ''')

conn.commit()
