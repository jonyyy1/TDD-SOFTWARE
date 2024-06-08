# FastAPI Geolocation API

## Descripción

Este proyecto implementa una API de geolocalización utilizando FastAPI. La API expone dos endpoints:

- `/get_coordinates/`: Recibe el nombre de una ciudad y devuelve sus coordenadas (latitud y longitud).
- `/get_distance/`: Recibe dos coordenadas y devuelve la distancia entre ellas.

## Requisitos

- Python 3.7+
- FastAPI
- Uvicorn
- Requests
- Geopy
- Pytest
- Locust (para pruebas de estrés)
- SonarQube (para análisis de código)

## Instalación

1. Clona este repositorio:

    ```sh
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Crea un entorno virtual y actívalo:

    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

## Uso

### Iniciar el Servidor

Para iniciar el servidor FastAPI, ejecuta:

```sh
uvicorn app:app --reload
```

El servidor se iniciará en http://127.0.0.1:8000.

Endpoints

/get_coordinates/

	•	Descripción: Devuelve las coordenadas de una ciudad.
	•	Parámetros:
	•	city_name (str): Nombre de la ciudad.
	•	Ejemplo:

```sh
curl "http://127.0.0.1:8000/get_coordinates/?city_name=New+York"
```

/get_distance/

	•	Descripción: Calcula la distancia entre dos puntos geográficos.
	•	Parámetros:
	•	lat1 (float): Latitud del primer punto.
	•	lon1 (float): Longitud del primer punto.
	•	lat2 (float): Latitud del segundo punto.
	•	lon2 (float): Longitud del segundo punto.
	•	Ejemplo:


```sh
curl "http://127.0.0.1:8000/get_distance/?lat1=0&lon1=0&lat2=1&lon2=1"
```

Pruebas

Pruebas Unitarias

Para ejecutar las pruebas unitarias, utiliza pytest:

```sh
pytest --cov=app
```

Pruebas de Estrés

Para ejecutar pruebas de estrés, instala Locust y configura el archivo locustfile.py. Luego, ejecuta:

```sh
locust
```