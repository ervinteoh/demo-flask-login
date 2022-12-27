const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./src/templates/**/*.{html,jinja}", "./js/**/*.js"],
  theme: {
    screens: {
      'sm': '576px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1400px',
    },
    fontFamily: {
      sans: ['"Inter"', 'sans-serif']
    },
    container: {
      center: true,
    },
    fontSize: {
      'xs': '.75rem',
      'sm': '.875rem',
      'base': '1rem',
      'lg': '1.25rem',
      'xl': '1.5rem',
      '2xl': '1.875rem',
      '3xl': '2rem',
      '4xl': '2.125rem',
      '5xl': '2.5rem',
      '6xl': '3rem',
      '7xl': '4rem',
      '8xl': '5rem',
      '9xl': '6rem',
    },
    extend: {
      colors: {
        primary: {
          ...colors.orange,
          '900': '#522214'
        },
        neutral: {
          ...colors.gray,
          '900': '#0F131A',
        },
        black: '#07090D',
        white: '#FBFDFE',
      }
    },
  },
  plugins: [],
};
