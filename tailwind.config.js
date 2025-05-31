/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors') // Mengimpor colors dari Tailwind CSS

module.exports = {
  darkMode: "class", // Mode gelap diaktifkan berdasarkan class
  content: [
    "./pages/**/*.tsx",
    "./components/**/*.tsx",
    // Jika file lain terlibat, pastikan menambahkannya ke sini
    "./path/to/your/html/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        sky: colors.sky, // Mendefinisikan warna sky dari Tailwind CSS
      },
      backgroundImage: {
        check: "url('/icons/check.svg')",
        landscape: "url('/images/landscape/2.jpg')",
      },
    },
  },
  variants: {
    extend: {
      backgroundColor: ["checked"],
      borderColor: ["checked"],
      inset: ["checked"],
      zIndex: ["hover", "active"],
    },
  },
  plugins: [
    // require('tailwindcss-text-stroke')(),
  ],
};
