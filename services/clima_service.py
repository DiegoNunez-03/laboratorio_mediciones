# services/clima_service.py
"""
Servicio de integración con la API de Open-Meteo.

Flujo típico:
1) geocodificar_ciudad("Buenos Aires") -> lat, lon, país, etc.
2) obtener_clima_actual(lat, lon) -> temperatura, humedad, presión, etc.

Estas funciones NO acceden a la base de datos. Solo hablan con la API
y devuelven diccionarios listos para que los use el servicio de mediciones.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# -----------------------------
# Excepciones específicas
# -----------------------------


class CiudadNoEncontrada(Exception):
    """Se lanza cuando la API de geocoding no encuentra la ciudad pedida."""
    pass


class ErrorAPIClima(Exception):
    """Se lanza cuando hay algún problema al consultar la API de clima."""
    pass


# -----------------------------
# Modelos de datos (opcionales, pero prolijos)
# -----------------------------


@dataclass
class CiudadGeo:
    nombre: str
    pais: str
    codigo_pais: str
    latitud: float
    longitud: float


@dataclass
class ClimaActual:
    temperatura: float               # °C
    humedad_relativa: Optional[float]  # %
    sensacion_termica: Optional[float]  # °C
    presion: Optional[float]           # hPa aprox
    velocidad_viento: Optional[float]  # km/h aprox
    descripcion: str                   # texto en castellano


# -----------------------------
# Geocoding: ciudad -> coordenadas
# -----------------------------


def geocodificar_ciudad(nombre_ciudad: str) -> CiudadGeo:
    """
    Usa la API de geocoding de Open-Meteo para transformar un nombre de ciudad
    en coordenadas (lat/lon) + país.

    :param nombre_ciudad: Nombre tal como lo ingresa el usuario ("Buenos Aires").
    :return: CiudadGeo con nombre normalizado, país, código de país y coordenadas.
    :raises CiudadNoEncontrada: si la API no devuelve resultados.
    :raises ErrorAPIClima: si hay un problema de red o de respuesta.
    """
    params = {
        "name": nombre_ciudad,
        "count": 1,        # solo queremos el mejor resultado
        "language": "es",
        "format": "json",
    }

    try:
        resp = requests.get(GEOCODING_URL, params=params, timeout=10)
    except requests.RequestException as exc:
        raise ErrorAPIClima(f"Error de red al consultar geocoding: {exc}") from exc

    if resp.status_code != 200:
        raise ErrorAPIClima(
            f"Error en geocoding (status {resp.status_code}): {resp.text}"
        )

    data = resp.json()

    results = data.get("results") or []
    if not results:
        raise CiudadNoEncontrada(f"No se encontró la ciudad '{nombre_ciudad}'.")

    r0 = results[0]

    return CiudadGeo(
        nombre=r0.get("name", nombre_ciudad),
        pais=r0.get("country", ""),
        codigo_pais=r0.get("country_code", ""),
        latitud=float(r0["latitude"]),
        longitud=float(r0["longitude"]),
    )


# -----------------------------
# Clima actual: coordenadas -> valores meteorológicos
# -----------------------------


def obtener_clima_actual(latitud: float, longitud: float) -> ClimaActual:
    """
    Consulta Open-Meteo para obtener el clima actual en una posición dada.

    :param latitud: Latitud en grados decimales.
    :param longitud: Longitud en grados decimales.
    :return: ClimaActual con temperatura, humedad, presión, etc.
    :raises ErrorAPIClima: si hay problemas con la API.
    """
    params = {
        "latitude": latitud,
        "longitude": longitud,
        # Pedimos solo las variables que necesitamos
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "pressure_msl,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "timezone": "auto",
    }

    try:
        resp = requests.get(WEATHER_URL, params=params, timeout=10)
    except requests.RequestException as exc:
        raise ErrorAPIClima(f"Error de red al consultar clima: {exc}") from exc

    if resp.status_code != 200:
        raise ErrorAPIClima(
            f"Error en clima (status {resp.status_code}): {resp.text}"
        )

    data = resp.json()
    current: Dict[str, Any] = data.get("current") or {}

    temperatura = current.get("temperature_2m")
    humedad = current.get("relative_humidity_2m")
    sensacion = current.get("apparent_temperature")
    presion = current.get("pressure_msl")
    viento = current.get("wind_speed_10m")
    weather_code = current.get("weather_code")

    descripcion = describir_weather_code(weather_code)

    return ClimaActual(
        temperatura=float(temperatura) if temperatura is not None else 0.0,
        humedad_relativa=float(humedad) if humedad is not None else None,
        sensacion_termica=float(sensacion) if sensacion is not None else None,
        presion=float(presion) if presion is not None else None,
        velocidad_viento=float(viento) if viento is not None else None,
        descripcion=descripcion,
    )


# -----------------------------
# Traducción de weather_code a texto
# -----------------------------


def describir_weather_code(code: Optional[int]) -> str:
    """
    Traduce el weather_code de Open-Meteo a una descripción simple en castellano.
    Mapeo simplificado suficiente para un TP.
    """
    if code is None:
        return "Sin datos"

    mapping = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna",
        55: "Llovizna intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        71: "Nieve ligera",
        73: "Nieve moderada",
        75: "Nieve intensa",
        80: "Chaparrones ligeros",
        81: "Chaparrones moderados",
        82: "Chaparrones fuertes",
        95: "Tormenta",
        96: "Tormenta con granizo",
        99: "Tormenta fuerte con granizo",
    }

    return mapping.get(code, f"Código de tiempo {code}")
