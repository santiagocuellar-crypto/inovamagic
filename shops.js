// ====== CONFIGURACIÓN (edita aquí) ======
const DELIVERY_FEE = 5000; // domicilio, se cobra una vez por local
// true = tus productos reales + los de ejemplo juntos. Ponlo en false antes de compartir la tienda.
const SHOW_DEMO = true;
const CATEGORIES = ["Todo", "Ropa", "Calzado", "Accesorios", "Juegos"];

// Cada local: whatsapp (con 57 + número, sin +) y payUrl (enlace de pago: Wompi, Bre-B, etc.)
const SHOPS = {
  moda:  { name: "Distribuciones Cuellar",    whatsapp: "573153968920S", payUrl: "https://www.nequi.com.co" },
  pasos: { name: "Pasos Urbanos", whatsapp: "573153968920", payUrl: "https://www.bancolombia.com" },
  juego: { name: "Juegos Mágicos", whatsapp: "573153968920", payUrl: "https://www.nequi.com.co" },
};