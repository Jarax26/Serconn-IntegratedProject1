/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Busca en todos los archivos .html dentro de la carpeta 'templates'
    './*/templates/**/*.html', // Esto es útil si tienes carpetas de templates dentro de cada app de Django
  ],

  theme: {
    extend: {
      colors: {
        'brand-primary': '#00c2ff',     // cyan brillante
        'brand-secondary': '#7c5dfa',    // púrpura de acento
        'brand-aux': '#3c2d7a',         // auxiliar
        'brand-text': '#0f2338',        // texto principal
        'brand-background': '#f6fbff',  // fondo
      },
      fontFamily: {
        'sans': ['Poppins', 'sans-serif'], // fuente 'Poppins'
      }
    },
  },

  plugins: [],
}