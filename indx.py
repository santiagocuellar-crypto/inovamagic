from flask import Flask, render_template, jsonify, request, abort

app = Flask(__name__)

# Configuración Global de la Institución
configuracion = {
    "colegio": "Institución Educativa Evaristo García",
    "nequi_numero": "3123456789",
    "whatsapp_admin": "573123456789"
}

# 📦 Catálogo completo de Insumos Escolares (18 Productos)
catalogo_productos = [
    # --- CATEGORÍA: UNIFORMES ---
    {
        "id": "1", "nombre": "Camibuso Diario Uniforme", "precio": 35000, "precio_f": "35.000", 
        "img": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500", "cat": "uniformes", 
        "prov": "Confecciones Evaristo", "stock": 12, "tallas": ["S", "M", "L", "XL"],
        "criterio": "Más Vendido 🔥", "descripcion": "Camibuso oficial de diario para la Institución Educativa Evaristo García. Tela piqué de alta resistencia, fresca y garantizada para el uso diario estudiantil."
    },
    {
        "id": "2", "nombre": "Chaqueta de la Institución", "precio": 65000, "precio_f": "65.000", 
        "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500", "cat": "uniformes", 
        "prov": "Confecciones Evaristo", "stock": 5, "tallas": ["M", "L"],
        "descripcion": "Chaqueta oficial del uniforme de gala y educación física. Forro térmico interno, bolsillos con cremallera y escudo bordado de alta definición."
    },
    {
        "id": "3", "nombre": "Sudadera de Educación Física", "precio": 40000, "precio_f": "40.000", 
        "img": "https://images.unsplash.com/photo-1483721310020-03333e577078?w=500", "cat": "uniformes", 
        "prov": "Textiles del Valle", "stock": 8, "tallas": ["S", "M", "L"],
        "descripcion": "Pantalón de sudadera cómodo y elástico para las clases de educación física y eventos deportivos de la institución."
    },

    # --- CATEGORÍA: ESCOLAR ---
    {
        "id": "4", "nombre": "Cuaderno Cuadriculado 100 Hojas", "precio": 4500, "precio_f": "4.500", 
        "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=500", "cat": "escolar", 
        "prov": "Distribuidora Cali", "stock": 50,
        "criterio": "Mejor Descuento 🏷️", "descripcion": "Cuaderno cosido de 100 hojas cuadriculadas con pasta semirrígida protectora. Ideal para matemáticas, física y dibujo técnico."
    },
    {
        "id": "5", "nombre": "Caja de Colores x24 Lapiceros", "precio": 18000, "precio_f": "18.000", 
        "img": "https://images.unsplash.com/photo-1519751138087-5bf79df62d5b?w=500", "cat": "escolar", 
        "prov": "Librería del Centro", "stock": 15,
        "descripcion": "Caja de colores premium con 24 tonos vivos. Minas suaves y resistentes a los impactos, perfectos para las clases de artes."
    },
    {
        "id": "6", "nombre": "Morral Escolar Ergonómico", "precio": 75000, "precio_f": "75.000", 
        "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500", "cat": "escolar", 
        "prov": "Totto Mayorista", "stock": 6,
        "descripcion": "Morral ultra resistente con compartimento acolchado para tablet o portátil, bolsillos laterales para botellas de agua y costuras reforzadas."
    },
    {
        "id": "7", "nombre": "Kit Escolar Completo", "precio": 3500, "precio_f": "3.500", 
        "img": "https://images.unsplash.com/photo-1568252542512-9fe8fe9c87bb?w=500", "cat": "escolar", 
        "prov": "Distribuidora Cali", "stock": 100,
        "descripcion": "El combo infaltable para el día a día. Incluye dos lápices negros No.2, un borrador de nata de alta limpieza y un sacapuntas con depósito."
    },

    # --- CATEGORÍA: BELLEZA ---
    {
        "id": "8", "nombre": "Brillo Labial Humectante", "precio": 6000, "precio_f": "6.000", 
        "img": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=500", "cat": "belleza", 
        "prov": "Variedades Express", "stock": 2, "especialidades": ["Fresa", "Menta", "Vainilla"],
        "criterio": "Más Viral ✨", "descripcion": "Brillo mágico e hidratante de larga duración. Perfecto para llevar en la cartuchera y mantener los labios protegidos del clima."
    },
    {
        "id": "9", "nombre": "Loción Corporal Refrescante", "precio": 15000, "precio_f": "15.000", 
        "img": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500", "cat": "belleza", 
        "prov": "Variedades Express", "stock": 7, "especialidades": ["Lavanda", "Frutos Rojos"],
        "descripcion": "Splash refrescante ideal para usar después de la clase de educación física y mantener un aroma limpio durante toda la jornada escolar."
    },
    {
        "id": "10", "nombre": "Gel Antibacterial Portátil", "precio": 2500, "precio_f": "2.500", 
        "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500", "cat": "belleza", 
        "prov": "Salud Total", "stock": 45,
        "descripcion": "Gel desinfectante con aloe vera que elimina el 99.9% de las bacterias sin resecar las manos. Viene con gancho para colgar en el morral."
    },

    # --- CATEGORÍA: TÉCNICOS ---
    {
        "id": "11", "nombre": "Kit Reglas Técnicas", "precio": 12000, "precio_f": "12.000", 
        "img": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=500", "cat": "construccion", 
        "prov": "Librería del Centro", "stock": 8, "especialidades": ["Sistemas", "Dibujo"],
        "criterio": "Top Recomendado ⭐", "descripcion": "Juego geométrico profesional que incluye escuadras de 45° y 60°, regla de 30cm y transportador. Indispensable para las modalidades técnicas."
    },
    {
        "id": "12", "nombre": "Bata Blanca para Laboratorio", "precio": 28000, "precio_f": "28.000", 
        "img": "https://images.unsplash.com/photo-1581092921461-eab62e97a780?w=500", "cat": "construccion", 
        "prov": "Dotaciones Cali", "stock": 14, "tallas": ["S", "M", "L"],
        "descripcion": "Bata manga larga antifluido obligatoria para las prácticas de laboratorio de química, física y talleres técnicos."
    },
    {
        "id": "13", "nombre": "Multímetro Digital Escolar", "precio": 35000, "precio_f": "35.000", 
        "img": "https://images.unsplash.com/photo-1517420164441-f549a180f24a?w=500", "cat": "construccion", 
        "prov": "Tecno-Insumos", "stock": 4, "especialidades": ["Electricidad", "Sistemas"],
        "descripcion": "Herramienta de medición electrónica compacta. Ideal para estudiantes de la especialidad técnica en electricidad y mantenimiento de sistemas."
    },
    {
        "id": "14", "nombre": "Calibrador Pie de Rey", "precio": 9000, "precio_f": "9.000", 
        "img": "https://images.unsplash.com/photo-1503694978374-8a2fa6e6963a?w=500", "cat": "construccion", 
        "prov": "Tecno-Insumos", "stock": 10, "especialidades": ["Mecánica", "Dibujo"],
        "descripcion": "Instrumento de precisión para medir dimensiones internas, externas y profundidades en proyectos de diseño técnico."
    },

    # --- CATEGORÍA: DEPORTES ---
    {
        "id": "15", "nombre": "Balón de Microfútbol Profesional", "precio": 48000, "precio_f": "48.000", 
        "img": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500", "cat": "deportes", 
        "prov": "Deportes Cali", "stock": 3,
        "criterio": "Últimas Unidades 🚨", "descripcion": "Balón oficial con bote controlado ideal para las canchas de la institución. Cuero sintético cosido de alta duración."
    },
    {
        "id": "16", "nombre": "Termo de Agua Deportivo", "precio": 12000, "precio_f": "12.000", 
        "img": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500", "cat": "deportes", 
        "prov": "Deportes Cali", "stock": 25,
        "descripcion": "Caramañola plástica libre de BPA con boquilla de seguridad. Mantiene tu hidratación al máximo durante los recreos o torneos del colegio."
    },
    {
        "id": "17", "nombre": "Cuerda para Saltar Velocidad", "precio": 8500, "precio_f": "8.500", 
        "img": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=500", "cat": "deportes", 
        "prov": "Fitness Club", "stock": 15,
        "descripcion": "Cuerda de velocidad ajustable con mangos ligeros, ideal para entrenamientos físicos y mejorar la coordinación."
    },
    {
        "id": "18", "nombre": "Gorra Institucional Deportiva", "precio": 16000, "precio_f": "16.000", 
        "img": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=500", "cat": "deportes", 
        "prov": "Textiles del Valle", "stock": 9,
        "descripcion": "Gorra con visera curva y ajuste regulable. Ideal para protegerse del sol de Cali durante las actividades físicas al aire libre."
    }
]

ventas_reales = 450000
meta_financiera = 2000000

@app.route('/')
def home():
    productos_carrusel = [p for p in catalogo_productos if "criterio" in p][:5]
    return render_template(
        'index.html', 
        catalogo=catalogo_productos, 
        carrusel=productos_carrusel,
        config=configuracion,
        ventas_reales=ventas_reales,
        meta=meta_financiera
    )

# 🚨 CAMBIO DE SEGURIDAD: Obligamos a Flask a que acepte el ID con string estricto
@app.route('/producto/<string:id>')
def detalle_producto(id):
    # Forzamos la comparación limpia eliminando espacios raros
    producto = next((p for p in catalogo_productos if str(p["id"]) == str(id).strip()), None)
    if not producto:
        abort(404)
    return render_template('producto.html', p=producto, config=configuracion, ventas_reales=ventas_reales, meta=meta_financiera)

@app.route('/api/registrar-venta', methods=['POST'])
def registrar_venta():
    global ventas_reales
    data = request.get_json()
    total_pedido = data.get('total', 0)
    ventas_reales += total_pedido
    return jsonify({"nuevas_ventas": ventas_reales})

if __name__ == '__main__':
    app.run(debug=True)