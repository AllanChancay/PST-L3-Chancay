# Lab 3 Estructura de un backend

Código base del curso para leer, ejecutar y modificar a mano, sin IA.
Hardware de referencia: NodeMCU ESP8266, DHT11 y LED RGB de cátodo común.
Este proyecto es una propuesta de material base para acompañar la guía.

## Backend en Windows
Desde backend, en una terminal Command Prompt de VS Code:
```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger: http://127.0.0.1:8000/docs
En macOS/Linux: python3 -m venv .venv y usar .venv/bin/python.
Los cinco endpoints base están en app/routes.py. La lista guarda como máximo
100 lecturas en memoria y se pierde al reiniciar. Ejecutar un solo proceso.
POST /lecturas retorna HTTP 201 con {"lectura": {...}, "led": "apagado"}.
PUT /led acepta rojo, verde, azul o apagado. No hay autenticación:
utilizar únicamente en la red de laboratorio autorizada.

## Firmware
Abrir firmware con PlatformIO IDE en VS Code. Copiar include/config.example.h
a include/config.h y completar WiFi, URL con IPv4 del PC e identificador.
Build, Upload y Monitor a 115200 baudios. El ESP envía cada 5 segundos y aplica
el color devuelto por POST /lecturas; PUT /led se refleja en el próximo envío.
Conexiones y pruebas: ver guía. Las dependencias se descargan la primera vez.
No publicar config.h, contraseñas ni tokens.

## Reto
Implementar GET /lecturas/promedio?n=3 a mano; no se incluye la solución.
Devolver cantidad, temperatura_promedio y humedad_promedio (dos decimales).
Validar n de 1 a 100; sin lecturas responder 404; si hay menos de n, usar todas.

## Antes de la sesión
El docente debe probar el firmware en el hardware real y la red del aula,
precargar las herramientas y validar las dependencias en los equipos.
La guía destina 105 minutos a trabajar con el entorno ya preparado.

# Validación
GET /salud, http://127.0.0.1:8000/salud, 200, 200

GET /lecturas, http://127.0.0.1:8000/lecturas, 200, 200

GET /led, http://127.0.0.1:8000/led, 200, 200

PUT /led, http://127.0.0.1:8000/led, 200, 200

POST /lecturas, http://127.0.0.1:8000/lecturas, 201, 201

GET /lecturas, http://127.0.0.1:8000/lecturas, 200, 200

GET /led, http://127.0.0.1:8000/led, 200, 200

## Errores:
POST con humedad igual a 150:
POST /lecturas, http://127.0.0.1:8000/lecturas, 200, 422

PUT /led con {"color":"amarillo"}. 
PUT /led, http://127.0.0.1:8000/led, 200, 422

## Datos del Estudiante
Nombre: Chancay Chiriguaya Allan y Cayambe Sinche Anthony Joel 

Objetivo: Identificar la estructura de un backend, comprender las rutas, modelos, servicios y almacenamiento, ejecutar la API localmente, probar endpoints desde Swagger y agregar una nueva ruta superando el reto propuesto.

## Respuestas a las Preguntas
*1. ¿Qué función recibe el JSON y cuál lo guarda?*
La que recibe la petición es `post_lectura` en `routes.py`, y la que guarda los datos es `guardar_lectura` en `services.py`.

*2. ¿Qué archivo cambiarías para añadir una URL?**
El archivo `routes.py`.

*3. ¿Qué ocurre con las lecturas y el color cuando se reinicia la API? ¿Por qué?*
Se borran y el color vuelve a su estado inicial ("apagado"). Esto ocurre porque el almacenamiento (`store.py`) mantiene los datos en la memoria RAM del proceso, no en una base de datos persistente.

*4. ¿Por qué una petición con JSON bien escrito puede devolver 422? Indica qué archivo define esa validación.*
Porque los valores rompen las reglas de negocio (ej. enviar humedad de 150 cuando el máximo es 100). Estas validaciones lógicas se definen en los modelos Pydantic dentro de `schemas.py`.

*5. Explica el recorrido completo de una lectura: ESP8266, ruta, modelo, servicio, almacenamiento y respuesta. ¿En qué momento cambia el LED?*
El ESP8266 envía el POST -> `routes.py` recibe la petición -> `schemas.py` valida la estructura -> `services.py` ejecuta la lógica -> `store.py` añade el dato a la lista en memoria. El LED cambia en el hardware físicamente solo después de que el ESP8266 lee y procesa la respuesta devuelta por la API.