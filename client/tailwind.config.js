module.exports = {
  purge: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
    fontFamily: {
      Montserrat: ["Montserrat", "sans-serif"],
    },
  },
  variants: {
    extend: {
      transitionDuration: ["hover", "focus", "active"],
      transitionTimingFunction: ["hover", "focus"],
      backgroundColor: ["active"],
    },
  },
  plugins: [],
};
