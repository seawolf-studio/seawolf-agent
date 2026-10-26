// LA MADRIGUERA — contrato del riel comun (Linea de Montaje Seawolf)
// Toda estacion lee/escribe este formato. Nada nace suelto.

/** Pieza canonica del riel. */
export function pieza(datos = {}) {
  return {
    id: datos.id ?? '',
    tipo: datos.tipo ?? 'titulo',          // titulo | temporada | episodio | fuente
    origen: datos.origen ?? 'importador',  // estacion que la produjo
    estado: datos.estado ?? 'listo',
    datos,
    senales: [],                            // eventos de consumo (vistas, favoritos...)
    historial: [],
    siguiente: datos.siguiente ?? 'publicar',
    contrato_salida: {},
  };
}

/** Una ficha de titulo normalizada (el contrato que consume el sitio publico). */
export function titulo({ tmdb_id, tipo = 'pelicula', nombre, anio, poster, sinopsis, generos = [], fuentes = [], puntaje = null }) {
  return pieza({
    id: `tmdb:${tmdb_id}`,
    tipo,
    origen: 'importador-tmdb',
    tmdb_id, tipo, nombre, anio, poster, sinopsis, generos, fuentes, puntaje,
    siguiente: 'publicar',
  });
}
