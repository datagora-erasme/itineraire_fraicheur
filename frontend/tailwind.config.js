/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bgWhite: '#F8F9F9',
        bgGray: '#EEEEEE',
        primary: '#D6EFF8',
        mainText: '#000000',
        ligneModale: "#BDBDBD",
        startGradientLegend: '#900C3F',
        endGradientLegend: '#1f8b2c'
      },
    },
  },
  plugins: [],
}

