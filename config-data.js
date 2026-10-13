// Lee los locales y categorías guardados en Firebase y los pone en SHOPS y CATEGORIES (de shops.js).
// Si en Firebase todavía no hay locales, se quedan los de shops.js como respaldo.
import { db } from "./firebase-config.js";
import { collection, getDocs, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

export async function loadConfig() {
  try {
    const [sh, ct] = await Promise.all([getDocs(collection(db, "shops")), getDoc(doc(db, "settings", "categories"))]);
    if (!sh.empty) {
      Object.keys(SHOPS).forEach(k => delete SHOPS[k]);
      sh.docs.forEach(d => { SHOPS[d.id] = d.data(); });
    }
    if (ct.exists() && Array.isArray(ct.data().list)) CATEGORIES.splice(0, CATEGORIES.length, "Todo", ...ct.data().list);
    return { imported: !sh.empty };
  } catch (e) {
    console.warn("No se pudo leer la configuración; se usan los datos de shops.js.", e);
    return { imported: false };
  }
}