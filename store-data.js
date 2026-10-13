import { db } from "./firebase-config.js";
import { loadConfig } from "./config-data.js";
import { collection, getDocs, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// Guarda un pedido (lo llama app.js al generar el recibo). Si falla, el WhatsApp sigue funcionando.
window.saveOrder = async order => {
  try { await addDoc(collection(db, "orders"), { ...order, status: "nuevo", createdAt: serverTimestamp() }); }
  catch (e) { console.warn("No se pudo guardar el pedido.", e); }
};

await loadConfig();
try {
  const snap = await getDocs(collection(db, "products"));
  const list = snap.docs.map(d => ({ id: d.id, ...d.data() }));
  loadRemote(list);
} catch (e) {
  console.warn("No se pudieron cargar los productos.", e);
  loadRemote([]);
}