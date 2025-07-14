import requests
import json

API_BASE_URL = "http://localhost:5000"

# 1. Test para la ruta raíz
def test_main_endpoint():
    response = requests.get(f"{API_BASE_URL}/")
    assert response.status_code == 200, f"Error: Status code {response.status_code}"
    assert "cocina" in response.text.lower(), "La API no menciona 'cocina' en la ruta raíz"

# 2. Prueba una pregunta válida sobre cocina
def test_pregunta_valida():    
    pregunta = "Cómo hacer una salsa bechamel"
    response = requests.get(f"{API_BASE_URL}/pront/{pregunta}")
    assert response.status_code == 200, f"Error: Status code {response.status_code}"
    data = json.loads(response.text)
    assert "respuesta" in data, "La respuesta no contiene el campo 'respuesta'"
    assert "bechamel" in data["respuesta"].lower(), "La respuesta no menciona 'bechamel'"
    print("✅ test_pregunta_valida: Pasó")

# 3. Prueba que preguntas no relacionadas a cocina sean rechazadas
def test_pregunta_invalida():
    pregunta = "Cómo programar en Python"
    response = requests.get(f"{API_BASE_URL}/pront/{pregunta}")
    assert response.status_code == 400, f"Se esperaba error 400, pero se obtuvo {response.status_code}"
    data = json.loads(response.text)
    assert "error" in data, "La respuesta de error no contiene el campo 'error'"
    assert "cocina" in data["error"].lower(), "El mensaje de error no menciona 'cocina'"
    print("✅ test_pregunta_invalida: Pasó")

# 4. Haz una consulta primero y verifica el historial   
def test_historial():
    requests.get(f"{API_BASE_URL}/pront/Cómo%20freír%20un%20huevo")
    response = requests.get(f"{API_BASE_URL}/historial")
    assert response.status_code == 200
    historial = response.json()["historial"]
    assert isinstance(historial, list)
    assert any("huevo" in str(item).lower() for item in historial)
    print("✅ test_historial: Pasó")

# 4.Llamamos directamente a las funciones de test
if __name__ == "__main__":
    test_main_endpoint()
    test_pregunta_valida()
    test_pregunta_invalida()
    test_historial()
    print("✅ ¡Todos los tests pasaron!")
