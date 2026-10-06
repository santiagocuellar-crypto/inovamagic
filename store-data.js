import { db } from "./firebase-config.js";
import { collection, getDocs } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

try {
  const snap = await getDocs(collection(db, "products"));
  const list = snap.docs.map(d => ({ id: d.id, ...d.data() }));
  loadRemote(list);
} catch (e) {
  console.warn("No se pudieron cargar los productos.", e);
  loadRemote([]);
}