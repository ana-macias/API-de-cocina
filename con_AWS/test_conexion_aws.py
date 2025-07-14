import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión
def get_db_config():
    return {
        'host': os.getenv('AWS_DB_HOST'),
        'database': os.getenv('AWS_DB_NAME'),
        'user': os.getenv('AWS_DB_USER'),
        'password': os.getenv('AWS_DB_PASSWORD'),
        'port': os.getenv('AWS_DB_PORT', '5432'),
        'sslmode': 'require'
    }

def test_conexion():
    config = get_db_config()
    print("🔌 Intentando conectar con:")
    for k, v in config.items():
        if k != 'password':
            print(f"  {k}: {v}")
    
    try:
        conn = psycopg2.connect(**config)
        print("✅ Conexión exitosa a la base de datos AWS.")
        conn.close()
    except OperationalError as e:
        print("❌ Error de conexión:")
        print(e)

def revisar_tablas():
    conn = psycopg2.connect(**get_db_config())
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tablas = cursor.fetchall()
        print("📋 Tablas en el esquema 'public':")
        for t in tablas:
            print("  -", t[0])
    conn.close()

if __name__ == '__main__':
    test_conexion()
    revisar_tablas()
