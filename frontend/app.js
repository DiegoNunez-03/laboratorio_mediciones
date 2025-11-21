// =======================================
// Configuración de API
// =======================================
const API_BASE_URL = "http://localhost:5001";
const API_MEDICIONES_URL = `${API_BASE_URL}/api/mediciones`;

// =======================================
// Referencias a elementos del DOM
// =======================================

// Buscador de ciudades
const ciudadInput       = document.getElementById("ciudadInput");
const autocompleteList  = document.getElementById("autocompleteList");
const btnBuscarCiudad   = document.getElementById("btnBuscarCiudad");
const errorCiudad       = document.getElementById("errorCiudad");
const historialCiudades = document.getElementById("historialCiudades");

// Panel “Temperatura por ciudad”
const tempCiudadValor  = document.getElementById("tempCiudadValor");
const tempCiudadNombre = document.getElementById("tempCiudadNombre");
const detallesCiudadLista = document.getElementById("detallesCiudadLista");

// Panel de control manual
const tempInput     = document.getElementById("tempInput");
const btnClasificar = document.getElementById("btnClasificar");
const mensajeError  = document.getElementById("mensajeError");

// Monitor de resultados generales
const monitorTempValue = document.getElementById("monitorTempValue");
const categoriaOutput  = document.getElementById("categoriaOutput");
const statusFill       = document.getElementById("statusFill");

// Tabla de historial
const tbodyResultados = document.getElementById("tbodyResultados");

// =======================================
// Autocomplete de ciudades (lista simple)
// =======================================
const CIUDADES_ARG = [
  "Buenos Aires",
  "Córdoba",
  "Rosario",
  "Mendoza",
  "La Plata",
  "Mar del Plata",
  "Bahía Blanca",
  "Tucumán",
  "Neuquén",
  "Bariloche",
  "Ushuaia",
  "Salta",
  "Santa Fe",
  "Corrientes",
  "Posadas"
];

function limpiarAutocomplete() {
  if (!autocompleteList) return;
  autocompleteList.innerHTML = "";
}

function mostrarAutocomplete(coincidencias) {
  limpiarAutocomplete();
  if (!autocompleteList || coincidencias.length === 0) return;

  coincidencias.forEach(ciudad => {
    const li = document.createElement("li");
    li.textContent = ciudad;
    li.classList.add("autocomplete-item");
    li.addEventListener("click", () => {
      ciudadInput.value = ciudad;
      limpiarAutocomplete();
    });
    autocompleteList.appendChild(li);
  });
}

if (ciudadInput) {
  ciudadInput.addEventListener("input", () => {
    const texto = ciudadInput.value.trim().toLowerCase();
    if (!texto) {
      limpiarAutocomplete();
      return;
    }

    const coincidencias = CIUDADES_ARG.filter(c =>
      c.toLowerCase().startsWith(texto)
    );

    mostrarAutocomplete(coincidencias);
  });

  // Cerrar lista al salir del input (pequeño delay para permitir click)
  ciudadInput.addEventListener("blur", () => {
    setTimeout(limpiarAutocomplete, 200);
  });
}

// =======================================
// Clasificación de temperatura (algoritmo)
// =======================================

function clasificarTemperatura(temp) {
  if (temp < 0) return "MUY_FRIO";
  if (temp < 10) return "FRIO";
  if (temp < 20) return "TEMPLADO";
  if (temp < 30) return "CALUROSO";
  return "MUY_CALUROSO";
}

// Normaliza temp a un 0-100 para la barra (rango arbitrario [-10, 40])
function normalizarTempParaBarra(temp) {
  const min = -10;
  const max = 40;
  let valor = ((temp - min) / (max - min)) * 100;
  if (valor < 0) valor = 0;
  if (valor > 100) valor = 100;
  return valor;
}

// Cambia el texto, dataset y clases visuales de la chip
function actualizarChipCategoria(el, categoria) {
  if (!el) return;

  // Texto
  el.textContent = categoria || "Sin datos";

  // Atributo data-level
  el.dataset.level = categoria || "";

  // Limpiar clases visuales previas
  el.classList.remove("lab-chip--cold", "lab-chip--warm", "lab-chip--hot");

  if (!categoria) return;

  if (categoria === "MUY_FRIO" || categoria === "FRIO") {
    el.classList.add("lab-chip--cold");
  } else if (categoria === "CALUROSO") {
    el.classList.add("lab-chip--warm");
  } else if (categoria === "MUY_CALUROSO") {
    el.classList.add("lab-chip--hot");
  }
  // TEMPLADO queda con el estilo base
}

// =======================================
// Helpers para ciudad / datos
// =======================================

function extraerNombreCiudad(data, fallback) {
  if (!data) return fallback || "—";

  if (typeof data.ciudad === "string") {
    return data.ciudad;
  }
  if (data.ciudad && typeof data.ciudad === "object") {
    if (typeof data.ciudad.nombre === "string") return data.ciudad.nombre;
    if (typeof data.ciudad.name === "string") return data.ciudad.name;
  }
  if (typeof data.ciudad_nombre === "string") return data.ciudad_nombre;
  if (typeof data.nombre_ciudad === "string") return data.nombre_ciudad;

  return fallback || "—";
}

// =======================================
// Historial (tabla)
// =======================================

// function agregarFilaHistorial(temperatura, categoria, fechaHoraTexto, ciudadLabel) {
//   if (!tbodyResultados) return;

//   const tr = document.createElement("tr");

//   const tdCiudad = document.createElement("td");
//   tdCiudad.textContent = ciudadLabel || "—";

//   const tdTemp = document.createElement("td");
//   tdTemp.textContent = temperatura !== null && temperatura !== undefined
//     ? temperatura
//     : "--";

//   const tdCat = document.createElement("td");
//   tdCat.textContent = categoria || "Sin datos";

//   const tdFecha = document.createElement("td");
//   tdFecha.textContent = fechaHoraTexto || new Date().toLocaleString("es-AR");

//   tr.appendChild(tdCiudad);
//   tr.appendChild(tdTemp);
//   tr.appendChild(tdCat);
//   tr.appendChild(tdFecha);

//   tbodyResultados.appendChild(tr);
// }

function agregarFilaHistorial(temperatura, categoria, fechaHoraTexto, ciudadLabel, alInicio = false) {
    if (!tbodyResultados) return;
  
    const tr = document.createElement("tr");
  
    const tdCiudad = document.createElement("td");
    tdCiudad.textContent = ciudadLabel || "—";
  
    const tdTemp = document.createElement("td");
    tdTemp.textContent = temperatura !== null && temperatura !== undefined
      ? temperatura
      : "--";
  
    const tdCat = document.createElement("td");
    tdCat.textContent = categoria || "Sin datos";
  
    const tdFecha = document.createElement("td");
    tdFecha.textContent = fechaHoraTexto || new Date().toLocaleString("es-AR");
  
    tr.appendChild(tdCiudad);
    tr.appendChild(tdTemp);
    tr.appendChild(tdCat);
    tr.appendChild(tdFecha);
  
    // 👇 si alInicio es true, la insertamos ARRIBA
    if (alInicio && tbodyResultados.firstChild) {
      tbodyResultados.insertBefore(tr, tbodyResultados.firstChild);
    } else {
      tbodyResultados.appendChild(tr);
    }
  }
  

// =======================================
// Funciones de integración con backend
// =======================================

// GET /api/mediciones  -> carga historial desde la base
async function cargarHistorialDesdeAPI() {
  try {
    const resp = await fetch(API_MEDICIONES_URL);
    if (!resp.ok) {
      console.warn("No se pudo obtener historial desde la API:", resp.status);
      return;
    }

    const datos = await resp.json();
    if (!Array.isArray(datos)) return;

    datos.forEach(med => {
      const temp = med.temperatura;
      const cat  = med.categoria || clasificarTemperatura(temp);
      const fecha = med.fecha_medicion || med.fecha || null;
      const fechaTxt = fecha
        ? new Date(fecha).toLocaleString("es-AR")
        : new Date().toLocaleString("es-AR");

      const nombreCiudad = extraerNombreCiudad(med, "—");

      agregarFilaHistorial(temp, cat, fechaTxt, nombreCiudad, false);
    });

  } catch (error) {
    console.error("Error al cargar historial desde API:", error);
  }
}

// POST /api/mediciones  -> crea medición a partir de ciudad
async function consultarCiudadEnAPI(nombreCiudad) {
  if (!nombreCiudad) return null;

  try {
    const resp = await fetch(API_MEDICIONES_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ ciudad: nombreCiudad })
    });

    if (!resp.ok) {
      let msg = `Error HTTP: ${resp.status}`;
      try {
        const errData = await resp.json();
        if (errData && errData.error) {
          msg += ` - ${errData.error}`;
        }
      } catch (_) {}
      throw new Error(msg);
    }

    const data = await resp.json();
    return data;

  } catch (error) {
    console.error("Error al consultar ciudad en API:", error);
    throw error;
  }
}

// =======================================
// Manejadores de eventos
// =======================================

// Panel de control: clasificación manual
if (btnClasificar) {
  btnClasificar.addEventListener("click", () => {
    if (mensajeError) mensajeError.textContent = "";

    const valor = parseFloat(tempInput.value);
    if (isNaN(valor)) {
      if (mensajeError) {
        mensajeError.textContent = "Por favor, ingresá un valor numérico.";
      }
      return;
    }

    const categoria = clasificarTemperatura(valor);

    // Actualizar monitor general (Resultados de laboratorio)
    if (monitorTempValue) monitorTempValue.textContent = valor.toString();
    actualizarChipCategoria(categoriaOutput, categoria);

    // Actualizar barra
    if (statusFill) {
      const porcentaje = normalizarTempParaBarra(valor);
      statusFill.style.width = `${porcentaje}%`;
    }

    // Agregar al historial (sin ciudad asociada)
    const fechaTxt = new Date().toLocaleString("es-AR");
    agregarFilaHistorial(valor, categoria, fechaTxt, "—");
  });
}

// Buscador de ciudades
if (btnBuscarCiudad) {
  btnBuscarCiudad.addEventListener("click", async () => {
    if (errorCiudad) errorCiudad.textContent = "";

    const ciudad = ciudadInput.value.trim();
    if (!ciudad) {
      if (errorCiudad) {
        errorCiudad.textContent = "Ingresá una ciudad antes de buscar.";
      }
      return;
    }

    try {
      const data = await consultarCiudadEnAPI(ciudad);

      if (!data) {
        if (errorCiudad) {
          errorCiudad.textContent = "No se pudo obtener datos de la ciudad.";
        }
        return;
      }

      const temp = data.temperatura;
      const categoria = data.categoria || clasificarTemperatura(temp);
      const fecha = data.fecha_medicion || data.fecha || new Date().toISOString();
      const fechaTxt = new Date(fecha).toLocaleString("es-AR");

      const nombreCiudad = extraerNombreCiudad(data, ciudad);

      // Actualizar panel “Temperatura por ciudad”
      if (typeof temp === "number") {
        tempCiudadValor.textContent = temp.toFixed(1);
      } else {
        tempCiudadValor.textContent = "--";
      }
      actualizarChipCategoria(tempCiudadNombre, categoria);

      // Detalle completo de medición
      if (detallesCiudadLista) {
        detallesCiudadLista.innerHTML = "";

        const campos = [
          ["Ciudad", nombreCiudad],
          ["Temperatura", temp !== undefined ? `${temp} °C` : null],
          ["Temp. mínima", data.temp_min ?? data.temp_minima],
          ["Temp. máxima", data.temp_max ?? data.temp_maxima],
          ["Humedad", data.humedad !== undefined ? `${data.humedad} %` : null],
          ["Presión", data.presion],
          ["Sensación térmica", data.sensacion ?? data.sensacion_termica],
          ["Fecha medición", fechaTxt]
        ];

        campos.forEach(([label, valor]) => {
          if (valor === undefined || valor === null) return;
          const li = document.createElement("li");
          li.textContent = `${label}: ${valor}`;
          detallesCiudadLista.appendChild(li);
        });
      }

      // Agregar a historial de ciudades buscadas (texto legible, sin [object Object])
      if (historialCiudades) {
        const li = document.createElement("li");
        li.textContent = `${nombreCiudad} – ${temp} °C (${categoria})`;
        historialCiudades.prepend(li);
      }

      // Agregar también al historial general (tabla)
      agregarFilaHistorial(temp, categoria, fechaTxt, nombreCiudad, true);

    } catch (error) {
      if (errorCiudad) {
        errorCiudad.textContent = "Error consultando la API. Revisá la consola.";
      }
    }
  });
}

// =======================================
// Inicialización
// =======================================

document.addEventListener("DOMContentLoaded", () => {
  cargarHistorialDesdeAPI();
});

