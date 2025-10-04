/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
      extend: {
        colors: {
          primary: '#FF6B35',
          secondary: '#F7931E',
          accent: '#C1292E',
        },
      },
    },
    plugins: [],
}