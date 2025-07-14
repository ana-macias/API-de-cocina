import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión AWS RDS
def get_db_config():
    return {
        'host': os.getenv('AWS_DB_HOST'),
        'database': os.getenv('AWS_DB_NAME'),
        'user': os.getenv('AWS_DB_USER'),
        'password': os.getenv('AWS_DB_PASSWORD'),
        'port': os.getenv('AWS_DB_PORT', '5432'),
        'sslmode': 'require'  # Recomendado para AWS RDS
    }

# Función para obtener conexión
def get_aws_connection():
    try:
        conn = psycopg2.connect(**get_db_config())
        return conn
    except OperationalError as e:
        print(f"Error al conectar a PostgreSQL en AWS: {e}")
        return None

# Crear tabla (si no existe)
def crear_tabla_aws():
    conn = get_aws_connection()
    if conn is None:
        print("❌ No se pudo conectar para crear la tabla.")
        return False
    
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preguntas_respuestas (
                    id SERIAL PRIMARY KEY,
                    pregunta TEXT NOT NULL,
                    respuesta TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("✅ Tabla 'preguntas_respuestas' verificada/creada.")
            return True
    except Exception as e:
        print(f"Error al crear tabla en AWS: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

# Guardar consulta en AWS RDS
def guardar_consulta_aws(pregunta: str, respuesta: str):
    conn = get_aws_connection()
    if conn is None:
        return False
    
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO preguntas_respuestas (pregunta, respuesta)
                VALUES (%s, %s)
                RETURNING id
            ''', (pregunta, respuesta))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error al guardar consulta en AWS: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

# Obtener historial desde AWS RDS
def obtener_historial_aws(limite=50):
    conn = get_aws_connection()
    if conn is None:
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT pregunta, respuesta, fecha 
                FROM preguntas_respuestas 
                ORDER BY fecha DESC
                LIMIT %s
            ''', (limite,))
            
            resultados = cursor.fetchall()
            return [{
                'pregunta': row[0],
                'respuesta': row[1],
                'fecha': row[2].isoformat() if row[2] else None
            } for row in resultados]
    except Exception as e:
        print(f"Error al obtener historial de AWS: {e}")
        return []
    finally:
        if conn:
            conn.close()


