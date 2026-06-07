from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# CONFIGURACIÓN GLOBAL DEL PROYECTO DE GRADO
config_proyecto = {
    "colegio": "Institución Educativa Evaristo García",
    "nequi_numero": "3123456789",  # Pon aquí tu número real de Nequi
    "whatsapp_admin": "573123456789" # Tu número de WhatsApp con el 57 adelante
}

# CATÁLOGO COMPLETO DE INSUMOS (Para que cargue en la cuadrícula responsive)
catalogo_productos = [
    {"id": "1", "nombre": "Uniforme de Diario Completo", "precio": 45000, "precio_f": "45.000", "cat": "uniformes", "prov": "Confecciones Evaristo", "stock": 5, "tallas": ["S", "M", "L", "XL"]},
    {"id": "2", "nombre": "Cuaderno Cuadriculado 100 Hojas", "precio": 5500, "precio_f": "5.500", "cat": "escolar", "prov": "Norma", "stock": 20},
    {"id": "3", "nombre": "Sudadera de Educación Física", "precio": 38000, "precio_f": "38.000", "cat": "uniformes", "prov": "Confecciones Evaristo", "stock": 2, "tallas": ["S", "M", "L"]},
    {"id": "4", "nombre": "Kit de Pinturas y Pinceles", "precio": 12000, "precio_f": "12.000", "cat": "construccion", "prov": "Artes Cali", "stock": 10, "especialidades": ["Sistemas", "Dibujo", "Electricidad"]},
    {"id": "5", "nombre": "Balón de Fútbol Profesional", "precio": 60000, "precio_f": "60.000", "cat": "deportes", "prov": "Golty", "stock": 4},
    {"id": "6", "nombre": "Brillo Labial / Protector", "precio": 3500, "precio_f": "3.500", "cat": "belleza", "prov": "Cosméticos SAS", "stock": 15}
]

# Variables de simulación de base de datos
ventas_totales = 180000  # Dinero simulado en Caja Mayor para la barra
meta_financiera = 2000000

@app.route('/')
def home():
    # Enviamos exactamente las variables que el index.html premium necesita
    return render_template(
        'index.html', 
        config=config_proyecto, 
        catalogo=catalogo_productos, 
        ventas_reales=ventas_totales, 
        meta=meta_financiera
    )

@app.route('/api/validar-cupon',     methods=['POST'])
def validar_cupon():
    data = request.get_json() or {}
    codigo = data.get('codigo', '').upper()
    cupones = {"EVARISTO50": 0.50, "INNOVA20": 0.20, "SUERTE10": 0.10, "PROFE100": 1.0}
    
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

@app.route('/api/cyber-alert', methods=['POST'])
def cyber_alert():
    return jsonify({"status": "Ataque mitigado exitosamente por Innovalogic Shield"})

if __name__ == '__main__':
    app.run(debug=True)