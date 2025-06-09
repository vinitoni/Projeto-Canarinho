import subprocess

# Iniciar reconhecimento facial
subprocess.Popen(["python", "main.py"])

# Iniciar o Streamlit dashboard
subprocess.call(["streamlit", "run", "dashboard.py"])
