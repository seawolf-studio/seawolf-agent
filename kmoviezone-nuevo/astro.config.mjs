// kmoviezone-nuevo — configuracion Astro
// Estacion C (Servir) de la Linea de Montaje. Sin WordPress, sin PHP.
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://kmoviezone.net',
  output: 'static',          // estatico = inmune a la clase de fallos de PHP
  build: { format: 'directory' },
});
