from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__)

# ==========================================
# 📊 CONFIGURACIÓN DE DATOS DEL PROYECTO
# ==========================================
configuracion = {
    "colegio": "I.E. Evaristo García",
    "whatsapp_admin": "573000000000",  # Cambialo por tu número real de WhatsApp
    "nequi_numero": "3000000000"       # Cambialo por tu número real de Nequi
}

# Base de datos ficticia de las ventas acumuladas del colegio
ventas_totales = 450000
meta_financiera = 2000000

# Carrusel de promociones destacadas
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
# 📦 CATÁLOGO COMPLETO DE PRODUCTOS (TODAS LAS CATEGORÍAS)
# ==========================================
catalogo_productos = [
    # --- UNIFORMES ---
    {
        "id": "1",
        "nombre": "Camibuso de Diario",
        "precio": 35000,
        "precio_f": "35.000",
        "stock": 12,
        "cat": "uniformes",
        "tallas": ["S", "M", "L", "XL"],
        "img": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"
    },
    {
        "id": "2",
        "nombre": "Pantalón de Diario Azul",
        "precio": 45000,
        "precio_f": "45.000",
        "stock": 2,
        "cat": "uniformes",
        "tallas": ["28", "30", "32", "34"],
        "img": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500"
    },
    {
        "id": "3",
        "nombre": "Camibuso de Educación Física",
        "precio": 32000,
        "precio_f": "32.000",
        "stock": 8,
        "cat": "uniformes",
        "tallas": ["S", "M", "L"],
        "img": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500"
    },
    
    # --- ESCOLAR ---
    {
        "id": "4",
        "nombre": "Cuaderno Cuadriculado 100H",
        "precio": 4500,
        "precio_f": "4.500",
        "stock": 25,
        "cat": "escolar",
        "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=500"
    },
    {
        "id": "5",
        "nombre": "Caja de Colores x24 Norma",
        "precio": 18000,
        "precio_f": "18.000",
        "stock": 14,
        "cat": "escolar",
        "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500"
    },
    {
        "id": "6",
        "nombre": "Morral Escolar Impermeable",
        "precio": 65000,
        "precio_f": "65.000",
        "stock": 4,
        "cat": "escolar",
        "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"
    },

    # --- BELLEZA ---
    {
        "id": "7",
        "nombre": "Brillo Labial Hidratante",
        "precio": 6000,
        "precio_f": "6.000",
        "stock": 19,
        "cat": "belleza",
        "img": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=500"
    },
    {
        "id": "8",
        "nombre": "Espejo de Bolsillo Inovamagic",
        "precio": 3500,
        "precio_f": "3.500",
        "stock": 15,
        "cat": "belleza",
        "img": "https://images.unsplash.com/photo-1590156546946-ce55a12a63ee?w=500"
    },
    {
        "id": "9",
        "nombre": "Crema de Manos Antibacterial",
        "precio": 8000,
        "precio_f": "8.000",
        "stock": 3,
        "cat": "belleza",
        "img": "https://images.unsplash.com/photo-1608248597481-496100c80836?w=500"
    },

    # --- TÉCNICOS / CONSTRUCCIÓN ---
    {
        "id": "10",
        "nombre": "Kit Dibujo Técnico (Reglas + Portaminas)",
        "precio": 18000,
        "precio_f": "18.000",
        "stock": 5,
        "cat": "construccion",
        "especialidades": ["Dibujo"],
        "img": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=500"
    },
    {
        "id": "11",
        "nombre": "Multímetro Digital Escolar",
        "precio": 28000,
        "precio_f": "28.000",
        "stock": 3,
        "cat": "construccion",
        "especialidades": ["Electricidad", "Sistemas"],
        "img": "https://images.unsplash.com/photo-1517420164441-1551e2763264?w=500"
    },
    {
        "id": "12",
        "nombre": "Ponchadora de Cable de Red RJ45",
        "precio": 22000,
        "precio_f": "22.000",
        "stock": 8,
        "cat": "construccion",
        "especialidades": ["Sistemas"],
        "img": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500"
    },
    {
        "id": "13",
        "nombre": "Pelacables Automático Industrial",
        "precio": 32000,
        "precio_f": "32.000",
        "stock": 6,
        "cat": "construccion",
        "especialidades": ["Electricidad"],
        "img": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=500"
    },

    # --- DEPORTES ---
    {
        "id": "14",
        "nombre": "Balón de Fútbol N° 5 Golty",
        "precio": 55000,
        "precio_f": "55.000",
        "stock": 4,
        "cat": "deportes",
        "img": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500"
    },
    {
        "id": "15",
        "nombre": "Lazo para Saltar de Alta Velocidad",
        "precio": 12000,
        "precio_f": "12.000",
        "stock": 20,
        "cat": "deportes",
        "img": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500"
    },
    {
        "id": "16",
        "nombre": "Termo para Agua Deportivo 1L",
        "precio": 15000,
        "precio_f": "15.000",
        "stock": 11,
        "cat": "deportes",
        "img": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
    }
]

# ==========================================
# 🌐 RUTAS DE LA PLATAFORMA WEB
# ==========================================

@app.route('/')
def index():
    """Ruta principal que renderiza la tienda e-commerce."""
    return render_template(
        'index.html', 
        config=configuracion, 
        carrusel=banners_carrusel, 
        catalogo=catalogo_productos,
        ventas_reales=ventas_totales,
        meta=meta_financiera
    )

@app.route('/producto/<id_producto>')
def ver_producto(id_producto):
    """Ruta dinámica por si en el futuro quieres meterle una vista detallada a cada insumo."""
    producto = next((p for p in catalogo_productos if p["id"] == id_producto), None)
    if producto:
        return f"<h3>Detalle de {producto['nombre']} - Inovamagic Core</h3><p>Precio: ${producto['precio_f']}</p>"
    return "Producto no encontrado, mano.", 404

# ==========================================
# 📲 RUTAS EXCLUSIVAS PARA LA DESCARGA (PWA)
# ==========================================

@app.route('/manifest.json')
def serve_manifest():
    """Sirve el archivo de configuración de la app para Android/iOS/PC."""
    return send_from_directory('.', 'manifest.json')

@app.route('/sw.js')
def serve_sw():
    """Sirve el Service Worker que permite que la app corra en segundo plano."""
    return send_from_directory('.', 'sw.js')

# ==========================================
# 📊 API EN TIEMPO REAL (CAJA MAYOR Y GRÁFICAS)
# ==========================================

@app.route('/api/registrar-venta', methods=['POST'])
def registrar_venta():
    """Recibe el valor de la compra y actualiza la barra de presupuesto en vivo."""
    global ventas_totales
    datos = request.get_json()
    valor_compra = datos.get('total', 0)
    
    ventas_totales += int(valor_compra)
    
    return jsonify({
        "status": "success",
        "nuevas_ventas": ventas_totales
    })

# ==========================================
# 🚀 ARRANQUE DEL SERVIDOR LOCAL
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)