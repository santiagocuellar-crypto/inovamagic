from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# CONFIGURACIÓN GLOBAL DEL PROYECTO DE GRADO
config_proyecto = {
    "colegio": "Institución Educativa Evaristo García",
    "nequi_numero": "3123456789",  # Pon tu número real de Nequi
    "whatsapp_admin": "573123456789" # Tu número de WhatsApp administrador
}

# CATÁLOGO DE PRODUCTOS - IMÁGENES GENÉRICAS DE ALTA VELOCIDAD PARA EL CELULAR
catalogo_productos = [
    {"id": "1", "nombre": "Uniforme de Diario Completo", "precio": 45000, "precio_f": "45.000", "cat": "uniformes", "prov": "Confecciones Evaristo", "stock": 5, "tallas": ["S", "M", "L", "XL"], "img": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400"},
    {"id": "2", "nombre": "Cuaderno Cuadriculado 100 H", "precio": 5500, "precio_f": "5.500", "cat": "escolar", "prov": "Norma", "stock": 20, "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400"},
    {"id": "3", "nombre": "Sudadera Educación Física", "precio": 38000, "precio_f": "38.000", "cat": "uniformes", "prov": "Confecciones Evaristo", "stock": 2, "tallas": ["S", "M", "L"], "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400"},
    {"id": "4", "nombre": "Kit de Pinturas y Pinceles", "precio": 12000, "precio_f": "12.000", "cat": "construccion", "prov": "Artes Cali", "stock": 10, "especialidades": ["Sistemas", "Dibujo", "Electricidad"], "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400"},
    {"id": "5", "nombre": "Balón de Fútbol Golty", "precio": 60000, "precio_f": "60.000", "cat": "deportes", "prov": "Golty", "stock": 4, "img": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=400"},
    {"id": "6", "nombre": "Brillo Labial Hidratante", "precio": 3500, "precio_f": "3.500", "cat": "belleza", "prov": "Cosméticos SAS", "stock": 15, "img": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400"}
]

ventas_totales = 240000  
meta_financiera = 2000000

@app.route('/')
def home():
    return render_template(
        'index.html', 
        config=config_proyecto, 
        catalogo=catalogo_productos, 
        ventas_reales=ventas_totales, 
        meta=meta_financiera
    )

@app.route('/api/validar-cupon', methods=['POST'])
def validar_cupon():
    data = request.get_json() or {}
    codigo = data.get('codigo', '').upper()
    cupones = {"EVARISTO50": 0.50, "INNOVA20": 0.20, "SUERTE10": 0.10}
    if codigo in cupones:
        return jsonify({"valid": True, "descuento": cupones[codigo]})
    return jsonify({"valid": False, "descuento": 0})

@app.route('/api/registrar-venta', methods=['POST'])
def registrar_venta():
    global ventas_totales
    data = request.get_json() or {}
    valor_pagado = int(data.get('total', 0))
    ventas_totales += valor_pagado
    return jsonify({"success": True, "nuevas_ventas": ventas_totales})

if __name__ == '__main__':
    app.run(debug=True)