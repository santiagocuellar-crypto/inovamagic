// Imágenes de ejemplo: ilustraciones que coinciden con el producto (type + color).
// Cuando tengas fotos reales, cambia img por "img/jean-azul.jpg" (carpeta img/) o por la URL de Firebase.
const SHAPES = {
  pants: c => `<path d="M62 30H138L150 172H108L100 84L92 172H50Z" fill="${c}"/><path d="M62 30H138V44H62Z" fill="#000" opacity=".15"/><path d="M100 44V84" stroke="#000" opacity=".2" stroke-width="2"/><path d="M70 62Q80 74 90 62" stroke="#fff" opacity=".5" fill="none" stroke-width="2"/>`,
  shirt: c => `<path d="M72 32L100 46L128 32L168 66L146 92L136 82V172H64V82L54 92L32 66Z" fill="${c}"/><path d="M72 32Q100 62 128 32" fill="#000" opacity=".12"/>`,
  sneaker: c => `<path d="M28 132V104Q62 100 82 78L102 94Q134 98 172 116Q178 138 166 146H34Q28 142 28 132Z" fill="${c}" stroke="#bbb" stroke-width="2"/><rect x="28" y="142" width="146" height="14" rx="7" fill="#e5e5ea" stroke="#bbb"/><path d="M92 90L110 108M102 84L120 102" stroke="#999" stroke-width="3"/>`,
  sandal: c => `<ellipse cx="100" cy="124" rx="74" ry="26" fill="#e9d8c4"/><path d="M52 118Q100 70 148 118" fill="none" stroke="${c}" stroke-width="16" stroke-linecap="round"/><path d="M70 130Q100 100 130 130" fill="none" stroke="${c}" stroke-width="12" stroke-linecap="round"/>`,
  cap: c => `<path d="M40 118Q40 56 100 56Q160 56 160 118Z" fill="${c}"/><path d="M150 112Q192 114 196 128Q160 128 118 120Z" fill="${c}"/><path d="M150 112Q192 114 196 128Q160 128 118 120Z" fill="#000" opacity=".2"/><circle cx="100" cy="58" r="5" fill="${c}" stroke="#fff" stroke-opacity=".4"/>`,
  bag: c => `<path d="M72 88Q72 36 100 36Q128 36 128 88" fill="none" stroke="${c}" stroke-width="9"/><rect x="46" y="84" width="108" height="86" rx="14" fill="${c}"/><rect x="46" y="84" width="108" height="26" rx="14" fill="#000" opacity=".12"/><circle cx="100" cy="112" r="6" fill="#fff" opacity=".7"/>`,
  puzzle: c => `<g><rect x="40" y="40" width="58" height="58" rx="6" fill="#ff6b6b"/><circle cx="98" cy="69" r="10" fill="#ff6b6b"/><rect x="102" y="40" width="58" height="58" rx="6" fill="#4dabf7"/><rect x="40" y="102" width="58" height="58" rx="6" fill="#ffd43b"/><circle cx="69" cy="102" r="10" fill="#ffd43b"/><rect x="102" y="102" width="58" height="58" rx="6" fill="#51cf66"/><circle cx="102" cy="131" r="10" fill="#51cf66"/></g>`,
  board: c => `<rect x="34" y="52" width="132" height="100" rx="10" fill="#f4a261"/><g stroke="#fff" stroke-width="2" opacity=".7"><path d="M78 52V152M122 52V152M34 85H166M34 118H166"/></g><rect x="52" y="64" width="18" height="18" rx="3" fill="#fff"/><circle cx="58" cy="70" r="2" fill="#333"/><circle cx="64" cy="76" r="2" fill="#333"/><circle cx="144" cy="134" r="9" fill="#e63946"/><circle cx="100" cy="100" r="9" fill="#457b9d"/>`,
};
const art = (type, color) => "data:image/svg+xml;charset=utf-8," + encodeURIComponent(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbfbfd"/><stop offset="1" stop-color="#e8e8ed"/></linearGradient></defs><rect width="200" height="200" fill="url(#g)"/><g transform="translate(100 100) scale(.74) translate(-100 -100)">${SHAPES[type](color)}</g></svg>`);

let PRODUCTS = [
  { id: 1, shop: "moda",  cat: "Ropa",       name: "Blusa de lino beige",  price: 45000,  img: art("shirt", "#e4d5bd") },
  { id: 2, shop: "moda",  cat: "Ropa",       name: "Jean azul",            price: 89000,  img: art("pants", "#3b6fb6") },
  { id: 3, shop: "moda",  cat: "Accesorios", name: "Bolso de mano café",   price: 62000,  img: art("bag", "#8b5a3c") },
  { id: 4, shop: "pasos", cat: "Calzado",    name: "Tenis blancos",        price: 120000, img: art("sneaker", "#ffffff") },
  { id: 5, shop: "pasos", cat: "Calzado",    name: "Sandalias de cuero",   price: 78000,  img: art("sandal", "#a9744f") },
  { id: 6, shop: "pasos", cat: "Accesorios", name: "Gorra negra",          price: 28000,  img: art("cap", "#222222") },
  { id: 7, shop: "juego", cat: "Juegos",     name: "Rompecabezas 500 pzs", price: 35000,  img: art("puzzle", "") },
  { id: 8, shop: "juego", cat: "Juegos",     name: "Juego de mesa",        price: 54000,  img: art("board", "") },
];

// Productos reales guardados en Firestore (los carga store-data.js). SHOW_DEMO (en shops.js) decide si se mezclan con los de ejemplo.
const DEMO = PRODUCTS.slice(); // productos de ejemplo
function loadRemote(list) {
  const real = list.filter(p => SHOPS[p.shop]);
  PRODUCTS = SHOW_DEMO ? [...real, ...DEMO] : real; // primero los reales
  cart = Object.fromEntries(Object.entries(cart).filter(([id]) => PRODUCTS.some(p => String(p.id) === id)));
  if (!CATEGORIES.includes(cat)) cat = "Todo";
  save(); renderCats(); renderGrid(); renderCart();
}

// ====== ESTADO ======
let cat = "Todo", query = "";
let cart = JSON.parse(localStorage.getItem("cart") || "{}"); // {id: cantidad}
const $ = id => document.getElementById(id);
const money = n => "$" + n.toLocaleString("es-CO");
const save = () => localStorage.setItem("cart", JSON.stringify(cart));

// ====== CATÁLOGO ======
function renderCats() {
  $("cats").innerHTML = CATEGORIES.map(c => `<button class="${c === cat ? "on" : ""}" data-c="${c}">${c}</button>`).join("");
}
function renderGrid() {
  const q = query.toLowerCase();
  const list = PRODUCTS.filter(p => (cat === "Todo" || p.cat === cat) &&
    (p.name + SHOPS[p.shop].name).toLowerCase().includes(q));
  $("title").textContent = cat === "Todo" ? "Todo en un solo lugar" : cat;
  $("grid").innerHTML = list.length ? list.map(p => `
    <article class="card">
      <img src="${p.img}" alt="${p.name}" width="400" height="400" loading="lazy" decoding="async">
      <div class="info">
        <span class="shop">${SHOPS[p.shop].name}</span>
        <span class="name">${p.name}</span>
        <span class="price">${money(p.price)}</span>
        <button data-add="${p.id}">Agregar</button>
      </div>
    </article>`).join("") : `<p class="empty">No encontramos productos con esa búsqueda.</p>`;
  observeCards();
}

// ====== CARRITO ======
const items = () => Object.entries(cart).map(([id, q]) => ({ ...PRODUCTS.find(p => p.id == id), q }));
function groupByShop(list) {
  const g = {};
  list.forEach(i => (g[i.shop] = g[i.shop] || []).push(i));
  return g;
}
function updateCount() { $("count").textContent = Object.values(cart).reduce((a, b) => a + b, 0); }
function openDrawer(show) { $("drawer").hidden = $("shade").hidden = !show; }

function renderCart() {
  updateCount();
  $("drawerTitle").textContent = "Tu carrito";
  const list = items();
  if (!list.length) { $("drawerBody").innerHTML = `<p class="empty">Tu carrito está vacío. Agrega algo del catálogo.</p>`; return; }
  const groups = groupByShop(list);
  const sub = list.reduce((a, i) => a + i.price * i.q, 0);
  $("drawerBody").innerHTML = Object.entries(groups).map(([s, arr]) => `
    <div class="group"><h3>${SHOPS[s].name}</h3>
    ${arr.map(i => `<div class="line"><img src="${i.img}" alt=""><div class="t">${i.name}<br>${money(i.price)}</div>
      <div class="qty"><button data-dec="${i.id}">−</button>${i.q}<button data-inc="${i.id}">+</button></div></div>`).join("")}
    </div>`).join("") + `
    <div class="row total"><span>Subtotal</span><span>${money(sub)}</span></div>
    <form id="checkout">
      <label>Nombre</label><input type="text" id="cName" required>
      <label>Celular</label><input type="tel" id="cPhone" required>
      <label>Entrega</label>
      <select id="cMode"><option value="domicilio">Domicilio (+${money(DELIVERY_FEE)} por local)</option><option value="recogida">Recoger en el local (sin costo)</option></select>
      <div id="addrBox"><label>Dirección</label><input type="text" id="cAddr"></div>
      <button class="primary" type="submit">Generar recibo</button>
    </form>`;
  const toggle = () => $("addrBox").hidden = $("cMode").value === "recogida";
  $("cMode").onchange = toggle;
  $("checkout").onsubmit = e => { e.preventDefault(); renderReceipt(); };
}

// ====== RECIBO (un recibo por proveedor) ======
function renderReceipt() {
  const c = { name: $("cName").value, phone: $("cPhone").value, mode: $("cMode").value, addr: $("cAddr").value };
  const groups = groupByShop(items());
  const num = "IM-" + Date.now().toString().slice(-6);
  let html = "";
  Object.entries(groups).forEach(([s, arr]) => {
    const shop = SHOPS[s];
    const sub = arr.reduce((a, i) => a + i.price * i.q, 0);
    const fee = c.mode === "domicilio" ? DELIVERY_FEE : 0;
    const total = sub + fee;
    if (window.saveOrder) window.saveOrder({ num, shop: s, subtotal: sub, fee, total,
      items: arr.map(i => ({ id: String(i.id), name: i.name, price: i.price, q: i.q })),
      customer: { name: c.name, phone: c.phone, mode: c.mode, addr: c.mode === "domicilio" ? c.addr : "" } });
    const msg = `Hola ${shop.name}, nuevo pedido ${num} (Inovamagic)\n` +
      arr.map(i => `• ${i.q} x ${i.name} - ${money(i.price * i.q)}`).join("\n") +
      `\nSubtotal: ${money(sub)}\nDomicilio: ${money(fee)}\nTotal: ${money(total)}\n` +
      `Cliente: ${c.name} - ${c.phone}\n` +
      (c.mode === "domicilio" ? `Entrega a: ${c.addr}` : "Recoge en el local");
    html += `<div class="receipt"><h3>${shop.name}</h3><small>Pedido ${num}</small>
      ${arr.map(i => `<div class="row"><span>${i.q} × ${i.name}</span><span>${money(i.price * i.q)}</span></div>`).join("")}
      <div class="row"><span>Domicilio</span><span>${money(fee)}</span></div>
      <div class="row total"><span>Total</span><span>${money(total)}</span></div>
      ${shop.payUrl ? `<a class="primary" href="${shop.payUrl}" target="_blank" rel="noopener">Pagar ${money(total)}</a>` : `<p><small>El pago se acuerda con el local por WhatsApp.</small></p>`}
      <a class="secondary" href="https://wa.me/${shop.whatsapp}?text=${encodeURIComponent(msg)}" target="_blank" rel="noopener">Enviar pedido a ${shop.name}</a>
    </div>`;
  });
  $("drawerTitle").textContent = "Tu recibo";
  $("drawerBody").innerHTML = html + `<button class="secondary" id="done">Terminar y vaciar carrito</button>`;
  $("done").onclick = () => { cart = {}; save(); renderCart(); openDrawer(false); };
}

// ====== EFECTO DE DESVANECIDO AL HACER SCROLL ======
// Las tarjetas aparecen al entrar y se desvanecen al salir (arriba, bajo el encabezado, o abajo).
let io;
function observeCards() {
  const cards = document.querySelectorAll(".card");
  if (!("IntersectionObserver" in window)) { cards.forEach(c => c.classList.add("in")); return; }
  if (io) io.disconnect();
  io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle("in", e.isIntersecting)),
    { rootMargin: "-12% 0px -6% 0px", threshold: 0 });
  cards.forEach(c => io.observe(c));
}
// El título grande se desvanece y sube suavemente al bajar; el encabezado se vuelve más transparente.
let ticking = false;
window.addEventListener("scroll", () => {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    const p = Math.min(window.scrollY / 220, 1);
    $("title").style.opacity = 1 - p;
    $("title").style.transform = `translateY(${-24 * p}px)`;
    document.querySelector(".top").classList.toggle("scrolled", window.scrollY > 10);
    ticking = false;
  });
}, { passive: true });

// ====== EVENTOS ======
document.addEventListener("click", e => {
  const t = e.target;
  if (t.dataset.c) { cat = t.dataset.c; renderCats(); renderGrid(); }
  if (t.dataset.add) { cart[t.dataset.add] = (cart[t.dataset.add] || 0) + 1; save(); renderCart(); openDrawer(true); }
  if (t.dataset.inc) { cart[t.dataset.inc]++; save(); renderCart(); }
  if (t.dataset.dec) { if (--cart[t.dataset.dec] <= 0) delete cart[t.dataset.dec]; save(); renderCart(); }
});
let timer; // espera 150 ms al escribir para no redibujar en cada letra
$("search").oninput = e => { clearTimeout(timer); timer = setTimeout(() => { query = e.target.value; renderGrid(); }, 150); };
$("openCart").onclick = () => { renderCart(); openDrawer(true); };
$("closeCart").onclick = $("shade").onclick = () => openDrawer(false);

renderCats(); renderGrid(); updateCount();