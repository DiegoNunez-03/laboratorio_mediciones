# 🧪 Laboratorio de Clasificación de Temperatura – TP2  
**Algoritmos & Datos – Nuñez Diego | Guari Ezequiel**

Este proyecto implementa un laboratorio interactivo para **clasificar temperaturas**, consultar el clima real de ciudades de Argentina mediante API, y registrar automáticamente cada medición en una base de datos **PostgreSQL**.  
Incluye backend en **Flask**, integración con la API de clima **Open-Meteo**, y frontend dinámico en **HTML, CSS y JS**.

---

## 📌 Funcionalidades principales

### ✔️ 1. Búsqueda de temperatura por ciudad
- Autocompletado de ciudades.
- Consulta a Open-Meteo → temperatura, humedad, presión, viento y descripción.
- Clasificación automática según rangos:
  - **MUY_FRIO**, **FRIO**, **TEMPLADO**, **CALUROSO**, **MUY_CALUROSO**
- Registro automático en la base de datos.

### ✔️ 2. Historial de mediciones
- Se muestran **todas** las mediciones registradas.
- Ordenadas de lo más reciente → a lo más antiguo.
- Cada fila incluye:
  - Ciudad
  - Temperatura
  - Categoría
  - Fecha/hora de registro

### ✔️ 3. Detalle completo de cada medición
Al seleccionar una ciudad, se muestran:
- Temperatura actual  
- Categoría  
- Humedad  
- Sensación térmica  
- Presión  
- Velocidad del viento  
- Descripción del clima  

Todo integrado en la interfaz moderna estilo “panel de laboratorio”.

---

## 🧱 Tecnologías utilizadas

| Componente | Tecnología |
|-----------|------------|
| Backend | Python + Flask |
| Acceso a BD | psycopg2-binary |
| Base de datos | PostgreSQL |
| API externa | Open-Meteo Weather API |
| Frontend | HTML, CSS, JavaScript |
| Comunicación | JSON + CORS |

---

## 📦 Instalación y ejecución

> **Requisito**: tener instalado Python 3.10+ y PostgreSQL.

### 🔹 1. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate   # Linux

🔹 2. Instalar dependencias
    pip install -r requirements.txt

🔹 3. Crear la base de datos
    CREATE DATABASE tp2_mediciones;

🔹 4. Ejecutar el backend
    python app.py
    El servidor quedará escuchando en: 
    http://localhost:5001/api/mediciones

🔹 4. Ejecutar el frontend
    index.html


📁 Estructura del proyecto
/tp2
 ├── app.py
 ├── requirements.txt
 ├── /repositories
 ├── /services
 ├── /db
 ├── index.html
 ├── style.css
 └── app.js

 



