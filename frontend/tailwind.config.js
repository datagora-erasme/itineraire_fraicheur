/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bgWhite: 'white',
        primary: 'black',
        mainText: '#343F56'
      },
    },
  },
  plugins: [],
}

