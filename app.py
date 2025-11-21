from flask import Flask, request, jsonify
from flask_cors import CORS
from services.mediciones_service import (
    registrar_medicion_desde_api,
    listar_mediciones,
    CiudadNoEncontrada,
    ErrorAPIClima,
)

app = Flask(__name__)
CORS(app)

@app.route("/api/mediciones", methods=["POST"])
def crear_medicion():
    """
    Endpoint que recibe SOLO el nombre de la ciudad en JSON:
    {
        "ciudad": "Buenos Aires"
    }

    Usa la API de Open-Meteo para obtener clima actual y registrar
    la medición en la base de datos.
    """

    data = request.get_json(silent=True) or {}
    ciudad = data.get("ciudad")

    if not ciudad:
        return jsonify({
            "error": "Faltan datos obligatorios",
            "detalle": "Se requiere el campo 'ciudad'."
        }), 400

    try:
        resultado = registrar_medicion_desde_api(ciudad)

    except CiudadNoEncontrada as e:
        # La API de geocoding no encontró esa ciudad
        return jsonify({
            "error": "Ciudad no encontrada",
            "detalle": str(e),
        }), 404

    except ErrorAPIClima as e:
        # Problemas al hablar con la API de clima
        return jsonify({
            "error": "Error al consultar la API de clima",
            "detalle": str(e),
        }), 502

    except Exception as e:
        # Cualquier otro problema interno (BD, lógica, etc.)
        return jsonify({
            "error": "No se pudo registrar la medición",
            "detalle": str(e),
        }), 500

    # Todo OK
    return jsonify(resultado), 201


@app.route("/api/mediciones", methods=["GET"])
def obtener_mediciones():
    """
    Devuelve la lista de todas las mediciones registradas.
    """
    try:
        mediciones = listar_mediciones()
    except Exception as e:
        return jsonify({
            "error": "No se pudieron obtener las mediciones",
            "detalle": str(e),
        }), 500

    return jsonify(mediciones), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
