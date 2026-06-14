from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__)

# ==========================================
# 📊 CONFIGURACIÓN DE DATOS DEL PROYECTO
# ==========================================
configuracion = {
    "colegio": "I.E. Evaristo García",
    "whatsapp_admin": "573000000000",  # Tu número de WhatsApp real
    "nequi_numero": "3000000000",       # Tu número de Nequi real
    "clave_admin": "admin123"          # 🔑 Contraseña para desbloquear el panel
}

# Base de datos simulada en memoria (Caja Mayor)
ventas_totales = 450000
meta_financiera = 2000000

# Estadísticas globales iniciales de compras por modalidad para la gráfica administrativa
estadisticas_modalidades = {
    "Sistemas": 14,
    "Dibujo": 9,
    "Electricidad": 6
}

banners_carrusel = [
    {
        "id": "u1",
        "nombre": "Camibuso de Diario Oficial",
        "criterio": "Más Vendido",
        "img": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"
    },
    {
        "id": "t1",
        "nombre": "Kit de Reglas para Dibujo Técnico",
        "criterio": "Recomendado Especialidad",
        "img": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500"
    }
]

# ==========================================
# 📦 INVENTARIO COMPLETO (25 PRODUCTOS)
# ==========================================
catalogo_productos = [
    # --- UNIFORMES ---
    {"id": "1", "nombre": "Camibuso de Diario", "precio": 35000, "precio_f": "35.000", "stock": 12, "cat": "uniformes", "tallas": ["S", "M", "L", "XL"], "img": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"},
    {"id": "2", "nombre": "Pantalón de Diario Azul", "precio": 45000, "precio_f": "45.000", "stock": 5, "cat": "uniformes", "tallas": ["28", "30", "32", "34"], "img": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500"},
    {"id": "3", "nombre": "Camibuso de Educación Física", "precio": 32000, "precio_f": "32.000", "stock": 8, "cat": "uniformes", "tallas": ["S", "M", "L"], "img": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500"},
    {"id": "4", "nombre": "Sudadera de Educación Física", "precio": 48000, "precio_f": "48.000", "stock": 4, "cat": "uniformes", "tallas": ["28", "32", "S", "M"], "img": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500"},
    {"id": "5", "nombre": "Medias Blancas Escolares (Par)", "precio": 5000, "precio_f": "5.000", "stock": 30, "cat": "uniformes", "img": "https://images.unsplash.com/photo-1582966772680-860e372bb558?w=500"},
    
    # --- ESCOLAR (PAPELERÍA) ---
    {"id": "6", "nombre": "Cuaderno Cuadriculado 100H", "precio": 4500, "precio_f": "4.500", "stock": 25, "cat": "escolar", "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=500"},
    {"id": "7", "nombre": "Caja de Colores x24 Norma", "precio": 18000, "precio_f": "18.000", "stock": 14, "cat": "escolar", "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500"},
    {"id": "8", "nombre": "Morral Escolar Impermeable", "precio": 65000, "precio_f": "65.000", "stock": 6, "cat": "escolar", "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"},
    {"id": "9", "nombre": "Kit de Lapiceros (Negro, Azul, Rojo)", "precio": 3600, "precio_f": "3.600", "stock": 40, "cat": "escolar", "img": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=500"},
    {"id": "10", "nombre": "Cartuchera Organizadora Pro", "precio": 15000, "precio_f": "15.000", "stock": 12, "cat": "escolar", "img": "https://images.unsplash.com/photo-1546554137-f86b9593a222?w=500"},

    # --- BELLEZA ---
    {"id": "11", "nombre": "Brillo Labial Hidratante", "precio": 6000, "precio_f": "6.000", "stock": 19, "cat": "belleza", "img": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=500"},
    {"id": "12", "nombre": "Espejo de Bolsillo Inovamagic", "precio": 3500, "precio_f": "3.500", "stock": 15, "cat": "belleza", "img": "https://images.unsplash.com/photo-1590156546946-ce55a12a63ee?w=500"},
    {"id": "13", "nombre": "Crema de Manos Antibacterial", "precio": 8000, "precio_f": "8.000", "stock": 10, "cat": "belleza", "img": "https://images.unsplash.com/photo-1608248597481-496100c80836?w=500"},
    {"id": "14", "nombre": "Protector Solar Escolar FPS 50", "precio": 24000, "precio_f": "24.000", "stock": 7, "cat": "belleza", "img": "https://images.unsplash.com/photo-1556229174-5e42a09e45af?w=500"},
    {"id": "15", "nombre": "Bálsamo Labial de Frutas", "precio": 4000, "precio_f": "4.000", "stock": 22, "cat": "belleza", "img": "https://images.unsplash.com/photo-1617421753172-13a8080f82df?w=500"},

    # --- TÉCNICOS / CONSTRUCCIÓN ---
    {"id": "16", "nombre": "Kit Dibujo Técnico (Reglas + Portaminas)", "precio": 18000, "precio_f": "18.000", "stock": 5, "cat": "construccion", "especialidades": ["Dibujo"], "img": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=500"},
    {"id": "17", "nombre": "Multímetro Digital Escolar", "precio": 28000, "precio_f": "28.000", "stock": 3, "cat": "construccion", "especialidades": ["Electricidad", "Sistemas"], "img": "https://images.unsplash.com/photo-1517420164441-1551e2763264?w=500"},
    {"id": "18", "nombre": "Ponchadora de Cable de Red RJ45", "precio": 22000, "precio_f": "22.000", "stock": 8, "cat": "construccion", "especialidades": ["Sistemas"], "img": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500"},
    {"id": "19", "nombre": "Pelacables Automático", "precio": 32000, "precio_f": "32.000", "stock": 6, "cat": "construccion", "especialidades": ["Electricidad"], "img": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=500"},
    {"id": "20", "nombre": "Tabla de Dibujo Técnico Formato A3", "precio": 42000, "precio_f": "42.000", "stock": 4, "cat": "construccion", "especialidades": ["Dibujo"], "img": "https://images.unsplash.com/photo-1516962215378-7fa2e137ae93?w=500"},
    {"id": "21", "nombre": "Kit de Desarrollo Arduino Uno R3", "precio": 45000, "precio_f": "45.000", "stock": 5, "cat": "construccion", "especialidades": ["Sistemas", "Electricidad"], "img": "https://images.unsplash.com/photo-1553406830-ef2513670d91?w=500"},

    # --- DEPORTES ---
    {"id": "22", "nombre": "Balón de Fútbol N° 5 Golty", "precio": 55000, "precio_f": "55.000", "stock": 4, "cat": "deportes", "img": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500"},
    {"id": "23", "nombre": "Lazo para Saltar de Alta Velocidad", "precio": 12000, "precio_f": "12.000", "stock": 20, "cat": "deportes", "img": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500"},
    {"id": "24", "nombre": "Termo para Agua Deportivo 1L", "precio": 15000, "precio_f": "15.000", "stock": 11, "cat": "deportes", "img": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"},
    {"id": "25", "nombre": "Tula Deportiva Inovamagic", "precio": 9500, "precio_f": "9.500", "stock": 15, "cat": "deportes", "img": "https://images.unsplash.com/photo-1524498250428-ec03f79e5fa4?w=500"}
]

# ==========================================
# 🌐 RUTAS WEB NATIVAS
# ==========================================
@app.route('/')
def index():
    return render_template(
        'index.html', 
        config=configuracion, 
        carrusel=banners_carrusel, 
        catalogo=catalogo_productos,
        ventas_reales=ventas_totales,
        meta=meta_financiera
    )

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('.', 'sw.js')

# ==========================================
# 🔒 ENDPOINTS DE SEGURIDAD Y DATOS (API)
# ==========================================
@app.route('/api/login-admin', methods=['POST'])
def login_admin():
    """Valida la contraseña enviada desde el frontend."""
    datos = request.get_json()
    password_ingresada = datos.get('password', '')
    
    if password_ingresada == configuracion["clave_admin"]:
        return jsonify({
            "status": "success", 
            "msg": "Acceso concedido",
            "datos_grafica": estadisticas_modalidades
        })
    else:
        return jsonify({"status": "error", "msg": "Contraseña incorrecta, mano."}), 401

@app.route('/api/registrar-venta', methods=['POST'])
def registrar_venta():
    """Recibe la venta de la bolsa y suma un punto a la gráfica de la especialidad."""
    global ventas_totales
    datos = request.get_json()
    valor_compra = datos.get('total', 0)
    modalidad = datos.get('modalidad', 'Sistemas')
    
    ventas_totales += int(valor_compra)
    if modalidad in estadisticas_modalidades:
        estadisticas_modalidades[modalidad] += 1
    
    return jsonify({"status": "success", "nuevas_ventas": ventas_totales})

if __name__ == '__main__':
    app.run(debug=True, port=5000)