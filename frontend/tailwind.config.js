/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#142033",
        paper: "#EDEDE7",
        blueprint: "#2B5797",
        brick: "#B3441E",
        ochre: "#C08A2E",
        moss: "#3F6B4F",
        steel: "#5C728A",
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["IBM Plex Sans", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
