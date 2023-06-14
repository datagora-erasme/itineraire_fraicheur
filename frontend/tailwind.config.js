/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bgWhite: 'white',
        primary: '#D6EFF8',
        mainText: '#1F3D47',
        startGradientLegend: '#900C3F',
        endGradientLegend: '#1f8b2c'
      },
    },
  },
  plugins: [],
}

