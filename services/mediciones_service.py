# services/mediciones_service.py

from repositories.ciudad_repository import (
    obtener_ciudad_por_nombre,
    crear_ciudad,
)

from repositories.mediciones_repository import (
    obtener_rango_por_temperatura,
    insertar_medicion,
    obtener_todas_las_mediciones,
)

from services.clima_service import (
    geocodificar_ciudad,
    obtener_clima_actual,
    CiudadNoEncontrada,
    ErrorAPIClima,
)


def registrar_medicion(
    nombre_ciudad: str,
    provincia: str,
    pais: str,
    temperatura: int,
    humedad: str,
    sensacion_termica: str,
    presion: str,
    velocidad_viento: str,
    descripcion: str,
):
    """
    Flujo base:
    - busca o crea ciudad
    - determina el rango según la temperatura
    - inserta la medición
    - devuelve un resumen de lo ocurrido
    """

    # 1) Ciudad: buscar o crear
    ciudad = obtener_ciudad_por_nombre(nombre_ciudad)
    if ciudad is None:
        id_ciudad = crear_ciudad(nombre_ciudad, provincia, pais)
        ciudad = {
            "id_ciudad": id_ciudad,
            "nombre": nombre_ciudad,
            "provincia": provincia,
            "pais": pais,
        }
    else:
        id_ciudad = ciudad["id_ciudad"]

    # 2) Rango: según temperatura
    rango = obtener_rango_por_temperatura(temperatura)
    if rango is None:
        raise ValueError(
            f"No se encontró un rango de temperatura válido para {temperatura}°C"
        )

    id_rango = rango["id_rango"]

    # 3) Insertar medición
    id_medicion = insertar_medicion(
        id_ciudad=id_ciudad,
        id_rango=id_rango,
        temperatura=temperatura,
        humedad=humedad,
        sensacion_termica=sensacion_termica,
        presion=presion,
        velocidad_viento=velocidad_viento,
        descripcion=descripcion,
    )

    # 4) Devolver resumen
    return {
        "id_medicion": id_medicion,
        "ciudad": ciudad,
        "rango": rango,
        "temperatura": temperatura,
        "humedad": humedad,
        "sensacion_termica": sensacion_termica,
        "presion": presion,
        "velocidad_viento": velocidad_viento,
        "descripcion": descripcion,
    }


def registrar_medicion_desde_api(nombre_ciudad: str):
    """
    Versión automática:
    - Recibe SOLO el nombre de la ciudad (como lo escribe el usuario).
    - Usa la API de Open-Meteo para geocodificar (lat/lon) y obtener clima actual.
    - Llama a registrar_medicion con todos los datos rellenados.
    """

    # 1) Geocodificar ciudad -> lat/lon + país
    ciudad_geo = geocodificar_ciudad(nombre_ciudad)

    # Provincia: no la tenemos, ponemos algo genérico
    provincia = "Desconocida"
    # País: priorizamos código ISO, si no el nombre completo
    pais = ciudad_geo.codigo_pais or ciudad_geo.pais or "N/A"

    # 2) Obtener clima actual en esas coordenadas
    clima = obtener_clima_actual(ciudad_geo.latitud, ciudad_geo.longitud)

    # Redondeamos los valores numéricos a algo razonable
    temperatura = int(round(clima.temperatura))

    if clima.humedad_relativa is not None:
        humedad = str(int(round(clima.humedad_relativa)))
    else:
        humedad = "0"

    if clima.sensacion_termica is not None:
        sensacion_termica = str(int(round(clima.sensacion_termica)))
    else:
        sensacion_termica = str(temperatura)

    if clima.presion is not None:
        presion = str(int(round(clima.presion)))
    else:
        presion = "0"

    if clima.velocidad_viento is not None:
        velocidad_viento = str(int(round(clima.velocidad_viento)))
    else:
        velocidad_viento = "0"

    descripcion = clima.descripcion

    # 3) Reusar el flujo base que inserta en la BD
    resultado = registrar_medicion(
        nombre_ciudad=ciudad_geo.nombre,
        provincia=provincia,
        pais=pais,
        temperatura=temperatura,
        humedad=humedad,
        sensacion_termica=sensacion_termica,
        presion=presion,
        velocidad_viento=velocidad_viento,
        descripcion=descripcion,
    )

    # Podríamos anexar coords si querés, pero para el TP no es obligatorio
    resultado["ciudad_geo"] = {
        "latitud": ciudad_geo.latitud,
        "longitud": ciudad_geo.longitud,
        "codigo_pais": ciudad_geo.codigo_pais,
    }

    return resultado


def listar_mediciones():
    """
    Devuelve la lista de mediciones ya registradas.
    Ahora mismo solo delega en el repositorio, pero si mañana
    querés agregar lógica (filtros, orden, etc.), va acá.
    """
    return obtener_todas_las_mediciones()


# Reexportamos las excepciones de clima para que app.py pueda capturarlas
__all__ = [
    "registrar_medicion",
    "registrar_medicion_desde_api",
    "CiudadNoEncontrada",
    "ErrorAPIClima",
    "listar_mediciones",
]
