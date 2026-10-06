import { auth, db } from "./firebase-config.js";
import { signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { collection, addDoc, getDocs, deleteDoc, doc, query, orderBy, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const $ = id => document.getElementById(id);
const say = (t, ok) => { $("msg").textContent = t; $("msg").style.color = ok ? "#1a7f37" : "#c0261c"; };
let imgData = "";

$("shop").innerHTML = Object.entries(SHOPS).map(([k, s]) => `<option value="${k}">${s.name}</option>`).join("");
$("cat").innerHTML = CATEGORIES.filter(c => c !== "Todo").map(c => `<option>${c}</option>`).join("");

// ----- Sesión -----
onAuthStateChanged(auth, user => {
  $("login").hidden = !!user;
  $("panel").hidden = !user;
  if (user) { $("who").textContent = user.email; $("uid").textContent = user.uid; loadList(); }
});
$("login").onsubmit = async e => {
  e.preventDefault();
  try { await signInWithEmailAndPassword(auth, $("email").value, $("pass").value); }
  catch { alert("Correo o contraseña incorrectos."); }
};
$("out").onclick = () => signOut(auth);

// ----- Foto: se reduce y comprime en el navegador (así cabe gratis en Firestore) -----
$("file").onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  const img = new Image();
  img.onload = () => {
    const s = Math.min(1, 700 / Math.max(img.width, img.height));
    const c = document.createElement("canvas");
    c.width = Math.round(img.width * s); c.height = Math.round(img.height * s);
    c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
    imgData = c.toDataURL("image/jpeg", 0.72);
    $("preview").src = imgData; $("preview").style.display = "block";
  };
  img.src = URL.createObjectURL(f);
};

// ----- Guardar producto -----
$("add").onsubmit = async e => {
  e.preventDefault();
  if (!imgData) return say("Elige una foto primero.");
  if (imgData.length > 900000) return say("La foto es muy pesada, prueba con otra.");
  try {
    await addDoc(collection(db, "products"), {
      shop: $("shop").value, cat: $("cat").value, name: $("name").value.trim(),
      price: Number($("price").value.replace(/\D/g, "")), img: imgData, createdAt: serverTimestamp()
    });
    say("Producto guardado.", true);
    $("add").reset(); $("preview").style.display = "none"; imgData = "";
    loadList();
  } catch { say("No se pudo guardar. Revisa que tu UID esté en las reglas de Firestore."); }
};

// ----- Lista y borrado -----
async function loadList() {
  try {
    const snap = await getDocs(query(collection(db, "products"), orderBy("createdAt", "desc")));
    $("list").innerHTML = snap.empty ? "<small>Aún no hay productos.</small>" : snap.docs.map(d => {
      const p = d.data();
      return `<div class="prow"><img src="${p.img}" alt=""><div class="t">${p.name}<br><small>${SHOPS[p.shop]?.name || p.shop} · $${p.price.toLocaleString("es-CO")}</small></div><button class="del" data-id="${d.id}">Borrar</button></div>`;
    }).join("");
  } catch { $("list").innerHTML = "<small>No se pudo cargar la lista.</small>"; }
}
$("list").onclick = async e => {
  const id = e.target.dataset.id;
  if (id && confirm("¿Borrar este producto?")) { await deleteDoc(doc(db, "products", id)); loadList(); }
};