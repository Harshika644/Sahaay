/* ---------- ALERT TICKER ---------- */
const alerts = [
  "🚨 Air‑raid alert issued for Jammu (seek shelter)",
  "🚌 Humanitarian corridor open 14:00‑18:00 Imphal ➜ Dimapur",
  "⏰ Night curfew (22:00‑05:00) imposed in Srinagar",
  "📵 Mobile data suspended in border districts of Punjab"
];
document.querySelector(".ticker-track").innerHTML =
  alerts.map(a => `<span>${a}</span>`).join("  |  ");

/* ---------- CAROUSEL ---------- */
const slides = document.querySelector(".slides");
const dots   = [...document.querySelectorAll(".dot")];
const total  = dots.length;
let index    = 0;

function updateCarousel() {
  slides.style.transform = `translateX(-${index * 100}%)`;
  dots.forEach((d, i) => d.classList.toggle("active", i === index));
}

document.querySelector(".left" ).onclick = () => { index = (index - 1 + total) % total; updateCarousel(); };
document.querySelector(".right").onclick = () => { index = (index + 1) % total;        updateCarousel(); };
dots.forEach((d, i) => d.onclick = () => { index = i; updateCarousel(); });

setInterval(() => { index = (index + 1) % total; updateCarousel(); }, 7000);

updateCarousel(); // initial position

