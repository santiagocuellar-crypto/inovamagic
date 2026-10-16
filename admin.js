import { auth, db, firebaseConfig } from "./firebase-config.js";
import { loadConfig } from "./config-data.js";
import { initializeApp, deleteApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { collection, onSnapshot, addDoc, getDocs, getDoc, setDoc, deleteDoc, updateDoc, doc, query, where, orderBy, limit, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const $ = id => document.getElementById(id);
const say = (t, ok) => { $("msg").textContent = t; $("msg").style.color = ok ? "#1a7f37" : "#c0261c"; };
// Los textos que escriben los clientes se "escapan" antes de mostrarlos
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const shopName = k => SHOPS[k]?.name || k;
const byDate = (a, b) => (b.data().createdAt?.seconds || 0) - (a.data().createdAt?.seconds || 0);
let imgData = "";
let myShop = null; // null = dueño (ve todo). Si no, es la clave del local del proveedor.

let imported = false; // true cuando los locales ya están guardados en Firebase
const shopOptions = keys => keys.map(k => `<option value="${esc(k)}">${esc(shopName(k))}</option>`).join("");

function setupRole() {
  $("shop").innerHTML = shopOptions(myShop ? [myShop] : Object.keys(SHOPS));
  $("pShop").innerHTML = shopOptions(Object.keys(SHOPS));
  $("provForm").hidden = $("newProv").hidden = $("provBox").hidden = !!myShop; // solo el dueño maneja proveedores
  $("nShop").innerHTML = shopOptions(Object.keys(SHOPS));
  $("cat").innerHTML = CATEGORIES.filter(c => c !== "Todo").map(c => `<option>${esc(c)}</option>`).join("");
  $("shopsBox").hidden = $("catsBox").hidden = !!myShop;
  if (!myShop) { loadProviders(); renderShops(); renderCatList(); }
  $("delDone").hidden = !!myShop;   // y solo el dueño borra pedidos
  $("ptitle").textContent = myShop ? "Panel · " + shopName(myShop) : "Panel Inovamagic";
}

// ----- Sesión -----
// Averigua quién entró: proveedor (tiene local asignado), dueño, o cuenta sin local
async function detectRole(user) {
  try {
    const p = await getDoc(doc(db, "providers", user.uid));
    if (p.exists()) return { kind: "provider", shop: p.data().shop };
  } catch (e) { return { kind: "error", e }; }
  try { await getDocs(query(collection(db, "providers"), limit(1))); return { kind: "owner" }; } // solo el dueño puede listar
  catch { return { kind: "none" }; }
}

onAuthStateChanged(auth, async user => {
  $("login").hidden = !!user;
  $("panel").hidden = true;
  $("norole").hidden = true;
  if (!user) { if (unsubOrders) unsubOrders(); return; }
  const r = await detectRole(user);
  if (r.kind === "none" || r.kind === "error") {
    $("email2").textContent = user.email; $("uid2").textContent = user.uid;
    $("roleErr").textContent = r.kind === "error" ? "No se pudo verificar la cuenta (" + (r.e.code || r.e.message) + "). ¿Publicaste las reglas nuevas en Firebase?" : "";
    $("norole").hidden = false;
    return;
  }
  imported = (await loadConfig()).imported;
  myShop = r.kind === "provider" ? r.shop : null;
  $("who").textContent = user.email; $("uid").textContent = user.uid;
  $("panel").hidden = false;
  setupRole(); loadList(); loadOrders(); watchOrders();
});
$("login").onsubmit = async e => {
  e.preventDefault();
  try { await signInWithEmailAndPassword(auth, $("email").value, $("pass").value); }
  catch { alert("Correo o contraseña incorrectos."); }
};
$("out").onclick = $("out2").onclick = () => signOut(auth);

// ----- Fotos: se reducen y comprimen en el navegador (así caben gratis en Firestore) -----
let photos = [], thumb = ""; // photos = versiones grandes; thumb = miniatura de la primera (es la que carga la tienda)
const shrink = (file, max, q) => new Promise((ok, fail) => {
  const img = new Image();
  img.onload = () => {
    const s = Math.min(1, max / Math.max(img.width, img.height));
    const c = document.createElement("canvas");
    c.width = Math.round(img.width * s); c.height = Math.round(img.height * s);
    c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
    URL.revokeObjectURL(img.src); ok(c.toDataURL("image/jpeg", q));
  };
  img.onerror = fail; img.src = URL.createObjectURL(file);
});
$("file").onchange = async e => {
  const files = [...e.target.files].slice(0, 4);
  if (!files.length) return;
  try {
    photos = await Promise.all(files.map(f => shrink(f, 900, 0.72)));
    thumb = await shrink(files[0], 400, 0.7);
    $("previews").innerHTML = photos.map(s => `<img src="${s}" alt="">`).join("");
  } catch { say("No se pudo leer alguna de las fotos."); }
};

// ----- Guardar producto -----
const list = t => t.split(",").map(x => x.trim()).filter(Boolean).slice(0, 20);
let editingId = null; // id del producto que se está editando (null = producto nuevo)
const prodCache = {};
$("add").onsubmit = async e => {
  e.preventDefault();
  if (!editingId && !photos.length) return say("Elige al menos una foto.");
  if (photos.join("").length > 900000) return say("Las fotos pesan mucho: usa menos fotos o más livianas.");
  const data = {
    shop: myShop || $("shop").value, cat: $("cat").value, name: $("name").value.trim(),
    price: Number($("price").value.replace(/\D/g, "")),
    desc: $("desc").value.trim().slice(0, 600), sizes: list($("sizes").value), colors: list($("colors").value)
  };
  if (photos.length) data.img = thumb; // si no eligió fotos nuevas, se conservan las anteriores
  try {
    let id = editingId;
    if (id) await updateDoc(doc(db, "products", id), data);
    else id = (await addDoc(collection(db, "products"), { ...data, createdAt: serverTimestamp() })).id;
    if (photos.length) await setDoc(doc(db, "productImages", id), { imgs: photos });
    say(editingId ? "Cambios guardados." : "Producto guardado.", true);
    endEdit(); loadList();
  } catch { say("No se pudo guardar. Revisa las reglas de Firestore."); }
};

function startEdit(id) {
  const p = prodCache[id]; if (!p) return;
  editingId = id; photos = []; thumb = "";
  if (!myShop) $("shop").value = p.shop;
  $("cat").value = p.cat; $("name").value = p.name; $("price").value = p.price;
  $("desc").value = p.desc || ""; $("sizes").value = (p.sizes || []).join(", "); $("colors").value = (p.colors || []).join(", ");
  $("file").value = ""; $("previews").innerHTML = `<img src="${p.img}" alt="">`;
  $("addTitle").textContent = "Editar producto"; $("saveBtn").textContent = "Guardar cambios"; $("cancelEdit").hidden = false;
  $("add").scrollIntoView({ behavior: "smooth" });
}
function endEdit() {
  editingId = null; photos = []; thumb = ""; $("add").reset(); $("previews").innerHTML = "";
  $("addTitle").textContent = "Nuevo producto"; $("saveBtn").textContent = "Guardar producto"; $("cancelEdit").hidden = true;
}
$("cancelEdit").onclick = endEdit;
$("list").addEventListener("click", e => { if (e.target.dataset.pedit) startEdit(e.target.dataset.pedit); });

// ----- Lista y borrado de productos -----
async function loadList() {
  try {
    const q = myShop ? query(collection(db, "products"), where("shop", "==", myShop))
                     : query(collection(db, "products"), orderBy("createdAt", "desc"));
    const docs = (await getDocs(q)).docs.sort(byDate);
    docs.forEach(d => { prodCache[d.id] = d.data(); });
    $("list").innerHTML = !docs.length ? "<small>Aún no hay productos.</small>" : docs.map(d => {
      const p = d.data();
      return `<div class="prow"><img src="${esc(p.img)}" alt=""><div class="t">${esc(p.name)}<br><small>${esc(shopName(p.shop))} · $${Number(p.price).toLocaleString("es-CO")}${p.soldOut ? " · <b>AGOTADO</b>" : ""}</small></div><button class="del" style="background:rgba(120,120,128,.14);color:inherit" data-pedit="${d.id}">Editar</button><button class="del" style="background:rgba(120,120,128,.14);color:inherit" data-psold="${d.id}" data-state="${p.soldOut ? 1 : 0}">${p.soldOut ? "Disponible" : "Agotado"}</button><button class="del" data-id="${d.id}">Borrar</button></div>`;
    }).join("");
  } catch (e) { console.error(e); $("list").innerHTML = `<small>No se pudo cargar la lista.<br><b>Motivo: ${esc(e.code || "")} ${esc(e.message || e)}</b></small>`; }
}
$("list").onclick = async e => {
  const id = e.target.dataset.id;
  if (id && confirm("¿Borrar este producto?")) { try { try { await deleteDoc(doc(db, "productImages", id)); } catch {} await deleteDoc(doc(db, "products", id)); } catch { say("No se pudo borrar."); } loadList(); }
};

// ----- Pedidos -----
const STATES = ["nuevo", "en preparación", "entregado"];
async function loadOrders() {
  try {
    const q = myShop ? query(collection(db, "orders"), where("shop", "==", myShop), limit(50))
                     : query(collection(db, "orders"), orderBy("createdAt", "desc"), limit(30));
    const docs = (await getDocs(q)).docs.sort(byDate);
    $("orders").innerHTML = !docs.length ? "<small>Aún no hay pedidos.</small>" : docs.map(d => {
      const o = d.data(), c = o.customer || {};
      const when = o.createdAt?.toDate ? o.createdAt.toDate().toLocaleString("es-CO") : "";
      return `<div class="order"><b>${esc(o.num)} · ${esc(shopName(o.shop))}</b><br><small>${esc(when)}</small>
        <div>${(o.items || []).map(i => `${esc(i.q)} × ${esc(i.name)}${i.size || i.color ? " (" + [i.size, i.color].filter(Boolean).map(esc).join(", ") + ")" : ""}`).join("<br>")}</div>
        <div><small>${esc(c.name)} · ${esc(c.phone)} · ${c.mode === "domicilio" ? "Domicilio: " + esc(c.addr) : "Recoge en el local"}</small></div>
        <b>Total $${Number(o.total).toLocaleString("es-CO")}</b><br>
        <select data-oid="${d.id}">${STATES.map(s => `<option ${s === o.status ? "selected" : ""}>${s}</option>`).join("")}</select>
        ${myShop ? "" : `<button class="del" data-del="${d.id}" style="margin-left:8px">Borrar</button>`}</div>`;
    }).join("");
  } catch (e) { console.error(e); $("orders").innerHTML = `<small>No se pudieron cargar los pedidos.<br><b>Motivo: ${esc(e.code || "")} ${esc(e.message || e)}</b></small>`; }
}
$("orders").onchange = async e => {
  const id = e.target.dataset.oid;
  if (id) { try { await updateDoc(doc(db, "orders", id), { status: e.target.value }); } catch { say("No se pudo cambiar el estado."); } }
};

// ----- Asignar proveedor (solo dueño): une el UID de un usuario con un local -----
$("provForm").onsubmit = async e => {
  e.preventDefault();
  try {
    await setDoc(doc(db, "providers", $("pUid").value.trim()), { shop: $("pShop").value });
    say("Proveedor asignado.", true); $("provForm").reset(); loadProviders();
  } catch { say("No se pudo asignar. ¿Publicaste las reglas nuevas?"); }
};

// ----- Borrar pedidos (solo dueño) -----
$("orders").onclick = async e => {
  const id = e.target.dataset.del;
  if (id && confirm("¿Borrar este pedido? No se puede recuperar.")) {
    try { await deleteDoc(doc(db, "orders", id)); } catch { say("No se pudo borrar el pedido."); }
    loadOrders();
  }
};
$("delDone").onclick = async () => {
  if (!confirm("¿Borrar TODOS los pedidos en estado 'entregado'? No se puede recuperar.")) return;
  try {
    const snap = await getDocs(query(collection(db, "orders"), where("status", "==", "entregado")));
    await Promise.all(snap.docs.map(d => deleteDoc(d.ref)));
    say(`Se borraron ${snap.size} pedidos entregados.`, true);
  } catch { say("No se pudieron borrar los pedidos."); }
  loadOrders();
};

// ----- Crear proveedor (solo dueño): crea su cuenta y le asigna el local en un paso -----
// Se usa una segunda conexión a Firebase para que TU sesión no se cierre al crear la cuenta.
$("newProv").onsubmit = async e => {
  e.preventDefault();
  const email = $("nEmail").value.trim(), pass = $("nPass").value, shop = $("nShop").value;
  let secApp, uid;
  try {
    secApp = initializeApp(firebaseConfig, "sec-" + Date.now());
    const secAuth = getAuth(secApp);
    uid = (await createUserWithEmailAndPassword(secAuth, email, pass)).user.uid;
    await signOut(secAuth);
  } catch (err) {
    const m = { "auth/email-already-in-use": "Ese correo ya tiene cuenta. Usa «Asignar una cuenta que ya existe» con su UID.",
      "auth/weak-password": "La contraseña es muy corta (mínimo 6 caracteres).", "auth/invalid-email": "El correo no es válido.",
      "auth/operation-not-allowed": "El acceso por correo y contraseña no está activado en Firebase." };
    say(m[err.code] || "No se pudo crear la cuenta: " + (err.code || err.message));
    if (secApp) deleteApp(secApp);
    return;
  }
  deleteApp(secApp);
  try {
    await setDoc(doc(db, "providers", uid), { shop, email });
    say(`Listo: ${email} ya puede entrar al panel de ${shopName(shop)}.`, true);
    $("newProv").reset(); loadProviders();
  } catch { say("La cuenta se creó, pero no se pudo asignar el local. Su UID es: " + uid + ". ¿Publicaste las reglas nuevas?"); }
};

// ----- Lista de proveedores asignados -----
async function loadProviders() {
  try {
    const snap = await getDocs(collection(db, "providers"));
    $("provList").innerHTML = snap.empty ? "<small>Aún no hay proveedores asignados.</small>" : snap.docs.map(d => {
      const p = d.data();
      return `<div class="prow"><div class="t">${esc(p.email || "(sin correo)")}<br><small>${esc(shopName(p.shop))}<br>UID: ${esc(d.id)}</small></div><button class="del" data-puid="${esc(d.id)}">Quitar</button></div>`;
    }).join("");
  } catch (e) { $("provList").innerHTML = `<small>No se pudo cargar. ${esc(e.code || "")}</small>`; }
}
$("provList").onclick = async e => {
  const id = e.target.dataset.puid;
  if (id && confirm("¿Quitar a este proveedor? Su cuenta seguirá existiendo, pero ya no verá ningún local.")) {
    try { await deleteDoc(doc(db, "providers", id)); } catch { say("No se pudo quitar."); }
    loadProviders();
  }
};

// ===== Locales y categorías (solo dueño) =====
const slug = s => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
async function refreshAll() { imported = (await loadConfig()).imported; setupRole(); loadList(); }
const needImport = () => { say("Primero toca «Importar los locales y categorías actuales»."); };

function renderShops() {
  $("importShops").hidden = imported;
  $("shopList").innerHTML = (imported ? "" : "<small>Estos son los locales de shops.js. Impórtalos para poder editarlos aquí.</small>") +
    Object.entries(SHOPS).map(([k, s]) => `<div class="prow"><div class="t">${esc(s.name)}<br><small>${esc(s.whatsapp)}${s.payUrl ? " · con enlace de pago" : ""}</small></div>
      ${imported ? `<button class="del" style="background:rgba(120,120,128,.14);color:inherit" data-sedit="${esc(k)}">Editar</button><button class="del" data-sdel="${esc(k)}">Quitar</button>` : ""}</div>`).join("");
}
function resetShopForm() {
  $("shopForm").reset(); $("sKey").value = "";
  $("shopFormTitle").textContent = "Agregar local"; $("sCancel").hidden = true;
}
$("sCancel").onclick = resetShopForm;

$("importShops").onclick = async () => {
  try {
    await Promise.all(Object.entries(SHOPS).map(([k, s]) => setDoc(doc(db, "shops", k), { name: s.name, whatsapp: s.whatsapp, payUrl: s.payUrl || "" })));
    await setDoc(doc(db, "settings", "categories"), { list: CATEGORIES.filter(c => c !== "Todo") });
    say("Importado. Ya puedes agregar y editar locales y categorías desde aquí.", true); refreshAll();
  } catch { say("No se pudo importar. ¿Publicaste las reglas nuevas?"); }
};

$("shopForm").onsubmit = async e => {
  e.preventDefault();
  if (!imported) return needImport();
  const editing = $("sKey").value, name = $("sName").value.trim(), key = editing || slug(name);
  if (!key) return say("Escribe un nombre válido.");
  if (!editing && SHOPS[key]) return say("Ya existe un local con ese nombre.");
  try {
    await setDoc(doc(db, "shops", key), { name, whatsapp: $("sWa").value.replace(/\D/g, ""), payUrl: $("sPay").value.trim() });
    say("Local guardado.", true); resetShopForm(); refreshAll();
  } catch { say("No se pudo guardar el local. ¿Publicaste las reglas nuevas?"); }
};

$("shopList").onclick = async e => {
  const ek = e.target.dataset.sedit, dk = e.target.dataset.sdel;
  if (ek) {
    const s = SHOPS[ek];
    $("sKey").value = ek; $("sName").value = s.name; $("sWa").value = s.whatsapp; $("sPay").value = s.payUrl || "";
    $("shopFormTitle").textContent = "Editar local"; $("sCancel").hidden = false;
    $("shopForm").scrollIntoView({ behavior: "smooth" });
  }
  if (dk) {
    try {
      const used = async c => !(await getDocs(query(collection(db, c), where("shop", "==", dk), limit(1)))).empty;
      if (await used("products") || await used("providers")) return say("Ese local aún tiene productos o un proveedor asignado. Bórralos primero.");
      if (confirm("¿Quitar este local?")) { await deleteDoc(doc(db, "shops", dk)); refreshAll(); }
    } catch { say("No se pudo quitar el local."); }
  }
};

function renderCatList() {
  $("catList").innerHTML = CATEGORIES.filter(c => c !== "Todo").map(c =>
    `<div class="prow"><div class="t">${esc(c)}</div>${imported ? `<button class="del" data-cdel="${esc(c)}">Quitar</button>` : ""}</div>`).join("");
}
const saveCats = list => setDoc(doc(db, "settings", "categories"), { list });
$("catForm").onsubmit = async e => {
  e.preventDefault();
  if (!imported) return needImport();
  const name = $("newCat").value.trim(), cur = CATEGORIES.filter(c => c !== "Todo");
  if (cur.some(c => c.toLowerCase() === name.toLowerCase())) return say("Esa categoría ya existe.");
  try { await saveCats([...cur, name]); say("Categoría agregada.", true); $("catForm").reset(); refreshAll(); }
  catch { say("No se pudo guardar. ¿Publicaste las reglas nuevas?"); }
};
$("catList").onclick = async e => {
  const c = e.target.dataset.cdel;
  if (c && confirm(`¿Quitar la categoría "${c}"? Los productos que la tengan seguirán en la tienda, pero ya no saldrán en ese filtro.`)) {
    try { await saveCats(CATEGORIES.filter(x => x !== "Todo" && x !== c)); refreshAll(); } catch { say("No se pudo quitar."); }
  }
};

// ----- Marcar un producto como agotado / disponible -----
$("list").addEventListener("click", async e => {
  const id = e.target.dataset.psold;
  if (!id) return;
  try { await updateDoc(doc(db, "products", id), { soldOut: e.target.dataset.state !== "1" }); }
  catch { say("No se pudo cambiar el estado del producto."); }
  loadList();
});

// ----- Pedidos en tiempo real: aparecen solos y suena un aviso, sin recargar -----
let unsubOrders, firstSnap = true;
function beep() {
  try {
    const c = new (window.AudioContext || window.webkitAudioContext)(), o = c.createOscillator(), g = c.createGain();
    o.connect(g); g.connect(c.destination); o.frequency.value = 880; g.gain.value = 0.15; o.start();
    setTimeout(() => { o.stop(); c.close(); }, 250);
  } catch {}
}
function watchOrders() {
  if (unsubOrders) unsubOrders();
  firstSnap = true;
  const q = myShop ? query(collection(db, "orders"), where("shop", "==", myShop), limit(50))
                   : query(collection(db, "orders"), orderBy("createdAt", "desc"), limit(30));
  unsubOrders = onSnapshot(q, snap => {
    if (snap.metadata.fromCache) return;
    if (firstSnap) { firstSnap = false; return; }
    loadOrders();
    if (snap.docChanges().some(c => c.type === "added")) { beep(); say("Llegó un pedido nuevo.", true); }
  }, () => {});
}