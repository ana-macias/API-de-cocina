import sqlite3
from datetime import datetime

# 1.Creamos la tabla
def crear_tabla():
    conn = sqlite3.connect('consultas_cocina.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preguntas_respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 2. Guardamos una nueva pregunta y respuesta en la DB
def guardar_consulta(pregunta: str, respuesta: str):
    conn = sqlite3.connect('consultas_cocina.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO preguntas_respuestas (pregunta, respuesta)
        VALUES (?, ?)
    ''', (pregunta, respuesta))
    conn.commit()
    conn.close()
    
# 4. Generamos un historial de  preguntas y respuestas almacenadas

def obtener_historial():
    conn = sqlite3.connect('consultas_cocina.db') 
    cursor = conn.cursor()
    cursor.execute('SELECT pregunta, respuesta, fecha FROM preguntas_respuestas ORDER BY fecha DESC')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# 5. Creamos la tabla al importar este módulo
crear_tabla()