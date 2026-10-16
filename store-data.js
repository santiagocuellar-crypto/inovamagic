import { db } from "./firebase-config.js";
import { loadConfig } from "./config-data.js";
import { collection, onSnapshot, addDoc, getDoc, doc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// Guarda un pedido (lo llama app.js al generar el recibo). Si falla, el WhatsApp sigue funcionando.
window.saveOrder = async order => {
  try { await addDoc(collection(db, "orders"), { ...order, status: "nuevo", createdAt: serverTimestamp() }); }
  catch (e) { console.warn("No se pudo guardar el pedido.", e); }
};

// Fotos completas de un producto: se piden solo al abrir su detalle (así la tienda carga liviana)
const photoCache = {};
window.loadPhotos = async id => {
  if (photoCache[id]) return photoCache[id];
  try { const s = await getDoc(doc(db, "productImages", id)); return (photoCache[id] = s.exists() ? (s.data().imgs || []) : []); }
  catch { return []; }
};

await loadConfig();
// Escucha en tiempo real: cuando cambia un producto, la tienda se actualiza sola, sin recargar
onSnapshot(collection(db, "products"),
  snap => loadRemote(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
  e => { console.warn("No se pudieron cargar los productos.", e); loadRemote([]); });