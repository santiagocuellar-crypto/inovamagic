from flask import Flask, render_template, jsonify, request
import shelve
from datetime import datetime

app = Flask(__name__)

# --- ARCHIVO DE ALMACENAMIENTO ---
def init_db():
    with shelve.open('inovamagic_storage') as db:
        if 'ventas' not in db: db['ventas'] = []
        if 'stats' not in db: db['stats'] = {"ventas_totales": 0, "pedidos_cont": 0, "visitas": 0}

init_db()

def registrar_log(tipo, accion, detalle):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("auditoria_seguridad.txt", "a", encoding="utf-8") as f:
        f.write(f"[{ahora}] [{tipo}] // {accion} -> {detalle}\n")

def money_format(value):
    return "{:,.0f}".format(value).replace(",", ".")

CUPONES = {
    "EVARISTO50": 0.50,
    "INNOVA20": 0.20,
    "SUERTE10": 0.10,
    "PROFE100": 1.00
}

@app.route('/')
def home():
    with shelve.open('inovamagic_storage', writeback=True) as db:
        db['stats']['visitas'] += 1
        v_totales = db['stats']['ventas_totales']
        
    config = {
        "colegio": "I.E. Evaristo García",
        "nequi_numero": "3043100365",
        "whatsapp_admin": "573153968920",
        "meta_financiera": 2000000 
    }

    tallas = ["S", "M", "L", "XL"]
    especialidades = ["Artes", "Sistemas", "Audio Visuales", "Deportes"]
    
    catalogo = [
        {"id": "u_diario", "cat": "uniformes", "prov": "Textiles JC", "nombre": "Uniforme de Diario Completo", "precio": 50000, "img": "https://replicate.delivery/xpbkg/92N6UfUvevT0EisO7f53vA8HlVv437qH3uM4f5uC7R1A7T5SA/output.png", "tallas": tallas},
        {"id": "u_fisica", "cat": "uniformes", "prov": "Textiles JC", "nombre": "Uniforme Educación Física", "precio": 55000, "img": "https://images.unsplash.com/photo-1556906781-9a412961c28c?w=400"},
        {"id": "u_esp", "cat": "uniformes", "prov": "Confecciones Cali", "nombre": "Uniforme Especialidad", "precio": 100000, "img": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400", "tallas": tallas, "especialidades": especialidades},
        {"id": "p_cuaderno", "cat": "escolar", "prov": "Librería Central", "nombre": "Cuaderno Institucional 100H", "precio": 6500, "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400"},
        {"id": "a_bolso", "cat": "escolar", "prov": "ImportCali", "nombre": "Maletín Reforzado Evaristo", "precio": 85000, "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400"},
        {"id": "balon_f", "cat": "deportes", "prov": "SportShop", "nombre": "Balón de Fútbol GOLTY", "precio": 45000, "img": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400"},
        {"id": "p_obra", "cat": "construccion", "prov": "Pintuco", "nombre": "Pintura de Obra (Balde)", "precio": 120000, "img": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=400"},
        {"id": "obra_blanca", "cat": "construccion", "prov": "HomeCenter", "nombre": "Kit Estuco y Obra Blanca", "precio": 150000, "img": "https://images.unsplash.com/photo-1621905235277-f45428d5ce05?w=400"},
        {"id": "maq_1", "cat": "belleza", "prov": "BeautyCali", "nombre": "Kit Maquillaje Básico", "precio": 35000, "img": "https://images.unsplash.com/photo-1522335789183-b15c77bd3353?w=400"},
        {"id": "maq_2", "cat": "belleza", "prov": "Natura", "nombre": "Crema Hidratante Suave", "precio": 22000, "img": "https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?w=400"},
        {"id": "maq_3", "cat": "belleza", "prov": "BeautyCali", "nombre": "Brillo Labial / Gloss", "precio": 12000, "img": "https://images.unsplash.com/photo-1586776977607-310e9c725c37?w=400"}
    ]

    for p in catalogo:
        p["precio_f"] = money_format(p["precio"])

    return render_template('index.html', config=config, catalogo=catalogo, ventas_reales=v_totales, meta=config["meta_financiera"])

@app.route('/api/validar-cupon', methods=['POST'])
def validar_cupon():
    codigo = request.json.get('codigo', '').upper().strip()
    if codigo in CUPONES:
        return jsonify({"valid": True, "descuento": CUPONES[codigo]})
    return jsonify({"valid": False, "descuento": 0})

@app.route('/api/registrar-venta', methods=['POST'])
def registrar_venta():
    data = request.json
    cliente = data.get('cliente')
    grado = data.get('grado')
    total = int(data.get('total'))
    productos = data.get('productos')
    
    lista_items = [f"{p['name']} ({p['d']})" for p in productos]
    
    with shelve.open('inovamagic_storage', writeback=True) as db:
        db['stats']['ventas_totales'] += total
        db['stats']['pedidos_cont'] += 1
        
        nueva_orden = {
            "id": db['stats']['pedidos_cont'],
            "cliente": cliente,
            "grado": grado,
            "productos": ", ".join(lista_items),
            "total": money_format(total),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        db['ventas'].append(nueva_orden)
        v_totales_actuales = db['stats']['ventas_totales']
        
    registrar_log("SUCCESS", "TRANSACCION_REGISTRADA", f"Orden #{db['stats']['pedidos_cont']} para {cliente}.")
    return jsonify({"status": "success", "orden_id": db['stats']['pedidos_cont'], "nuevas_ventas": v_totales_actuales})

@app.route('/api/cyber-alert', methods=['POST'])
def cyber_alert():
    return jsonify({"status": "protected"})

@app.route('/inovamagic-admin-777')
def admin():
    with shelve.open('inovamagic_storage') as db:
        v_totales = money_format(db['stats']['ventas_totales'])
        historial_ventas = db['ventas']
        estadisticas = db['stats']
    return render_template('admin.html', ventas_totales=v_totales, historial=historial_ventas, stats=estadisticas)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)