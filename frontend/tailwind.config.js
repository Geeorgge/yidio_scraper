/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      backgroundImage: {
      'dark-gradient': 'linear-gradient(to right, #24243e, #302b63, #0f0c29)',
      },
    },
  },
  plugins: [],
}