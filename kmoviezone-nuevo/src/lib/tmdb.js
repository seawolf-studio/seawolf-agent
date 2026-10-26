// Cliente TMDb — la MISMA fuente de metadatos que usa DooPlay, pero gratis y nuestro.
// La clave vive en .env como TMDB_API_KEY (nunca en el codigo ni en el repo).
const BASE = 'https://api.themoviedb.org/3';
const IMG = 'https://image.tmdb.org/t/p/w500';

export const tieneClave = () => Boolean(process.env.TMDB_API_KEY);

async function pide(path, params = {}) {
  const key = process.env.TMDB_API_KEY;
  if (!key) throw new Error('TMDB_API_KEY no configurada');
  const q = new URLSearchParams({ api_key: key, language: 'es-ES', ...params });
  const r = await fetch(`${BASE}${path}?${q}`);
  if (!r.ok) throw new Error(`TMDb ${r.status}`);
  return r.json();
}

export const poster = (p) => (p ? `${IMG}${p}` : null);

/** Busca titulos. Devuelve fichas normalizadas del riel. */
export async function buscar(consulta, pagina = 1) {
  const d = await pide('/search/multi', { query: consulta, page: pagina });
  return (d.results || []).filter(x => x.media_type === 'movie' || x.media_type === 'tv').map(map);
}

/** Populares (para la home). */
export async function populares(tipo = 'movie') {
  const d = await pide(`/${tipo}/popular`);
  return (d.results || []).map(map);
}

function map(x) {
  return {
    tmdb_id: x.id,
    tipo: x.media_type === 'tv' || x.first_air_date ? 'serie' : 'pelicula',
    nombre: x.title || x.name || '(sin titulo)',
    anio: String(x.release_date || x.first_air_date || '').slice(0, 4),
    poster: poster(x.poster_path),
    sinopsis: x.overview || '',
    puntaje: x.vote_average ?? null,
  };
}
