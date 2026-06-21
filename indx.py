from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# La clave secreta es obligatoria en Flask para poder usar sesiones cifradas
app.secret_key = 'inovamagic_secret_key_2026' 

# Credenciales de prueba fijas para la sustentación
USUARIO_TEST = "santiago@evaristogarcia.com"
CLAVE_TEST = "12345"

# Tu base de datos de 20 productos
productos = [
    {"id": 1, "categoria": "diario-masculino", "nombre": "Pantalón de Diario Lino (Talla 14)", "descripcion": "Pantalón gris de lino institucional para hombre. Confección clásica, tela resistente y cómoda.", "precio": 75000, "imagen": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?q=80&w=500&auto=format&fit=crop"},
    {"id": 2, "categoria": "diario-masculino", "nombre": "Pantalón de Diario Lino (Talla S)", "descripcion": "Pantalón gris de lino institucional talla adulto S. Corte elegante y excelente caída.", "precio": 79000, "imagen": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?q=80&w=500&auto=format&fit=crop"},
    {"id": 3, "categoria": "diario-masculino", "nombre": "Camisa de Diario Manga Corta (Talla 14)", "descripcion": "Camisa blanca institucional en lino/algodón. Fresca, cómoda y fácil de planchar.", "precio": 32000, "imagen": "https://images.unsplash.com/photo-1603252109303-2751441dd157?q=80&w=500&auto=format&fit=crop"},
    {"id": 4, "categoria": "diario-masculino", "nombre": "Camisa de Diario Manga Corta (Talla S)", "descripcion": "Camisa blanca formal de diario para las tallas superiores del plantel.", "precio": 36000, "imagen": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=500&auto=format&fit=crop"},
    {"id": 5, "categoria": "diario-masculino", "nombre": "Camisa de Diario Manga Corta (Talla M)", "descripcion": "Camisa de diario blanca confeccionada con telas premium de dacrón.", "precio": 36000, "imagen": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?q=80&w=500&auto=format&fit=crop"},
    {"id": 6, "categoria": "diario-femenino", "nombre": "Jardinera Escolar Plisada (Talla 14)", "descripcion": "Jardinera oficial a cuadros verdes y grises. Pliegues firmes de alta calidad y tirantas ajustables.", "precio": 78000, "imagen": "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=500&auto=format&fit=crop"},
    {"id": 7, "categoria": "diario-femenino", "nombre": "Jardinera Escolar Plisada (Talla S)", "descripcion": "Jardinera a cuadros institucional, talle alto y costuras de seguridad de alta resistencia.", "precio": 82000, "imagen": "https://images.unsplash.com/photo-1598198414976-ddb788ec80c1?q=80&w=500&auto=format&fit=crop"},
    {"id": 8, "categoria": "diario-femenino", "nombre": "Blusa Escolar de Diario (Talla 14)", "descripcion": "Blusa blanca formal de diario femenina, fácil lavado y secado rápido.", "precio": 30000, "imagen": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=500&auto=format&fit=crop"},
    {"id": 9, "categoria": "diario-femenino", "nombre": "Blusa Escolar de Diario (Talla 16)", "descripcion": "Blusa blanca con botones ocultos y entalle perfecto institucional.", "precio": 32000, "imagen": "https://images.unsplash.com/photo-1598555880561-159855588056?q=80&w=500&auto=format&fit=crop"},
    {"id": 10, "categoria": "diario-femenino", "nombre": "Blusa Escolar de Diario (Talla M)", "descripcion": "Blusa blanca oficial de dama en dacrón de alta calidad.", "precio": 34000, "imagen": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=500&auto=format&fit=crop"},
    {"id": 11, "categoria": "educacion-fisica", "nombre": "Sudadera Deportiva (Talla 14)", "descripcion": "Pantalón de sudadera azul turquesa institucional con franjas laterales, pretina elástica y cordón ajustable.", "precio": 55000, "imagen": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=500&auto=format&fit=crop"},
    {"id": 12, "categoria": "educacion-fisica", "nombre": "Sudadera Deportiva (Talla S)", "descripcion": "Pantalón deportivo institucional, tela impermeable ligera de alta duración bota recta.", "precio": 59000, "imagen": "https://images.unsplash.com/photo-1556906781-9a412961c28c?q=80&w=500&auto=format&fit=crop"},
    {"id": 13, "categoria": "educacion-fisica", "nombre": "Camiseta Deportiva Cuello V (Talla 14)", "descripcion": "Camiseta deportiva fresca de algodón peinado, absorbe la humedad eficientemente.", "precio": 28000, "imagen": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=500&auto=format&fit=crop"},
    {"id": 14, "categoria": "educacion-fisica", "nombre": "Camiseta Deportiva Cuello V (Talla 16)", "descripcion": "Camiseta institucional para educación física, tela ligera anti-transpirante.", "precio": 30000, "imagen": "https://images.unsplash.com/photo-1483721310020-03333e577078?q=80&w=500&auto=format&fit=crop"},
    {"id": 15, "categoria": "educacion-fisica", "nombre": "Camiseta Deportiva Cuello V (Talla M)", "descripcion": "Camiseta oficial cuello en V con tejido microperforado de alta ventilación.", "precio": 32000, "imagen": "https://images.unsplash.com/photo-1506152983158-b4a74a01c721?q=80&w=500&auto=format&fit=crop"},
    {"id": 16, "categoria": "sistemas", "nombre": "Camiseta Polo Técnica Sistemas (Talla S)", "descripcion": "Camiseta tipo Polo exclusiva azul oscuro con bordados técnicos de la Especialidad de Sistemas.", "precio": 44000, "imagen": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?q=80&w=500&auto=format&fit=crop"},
    {"id": 17, "categoria": "sistemas", "nombre": "Camiseta Polo Técnica Sistemas (Talla M)", "descripcion": "Polo técnico en algodón piqué de alta gama, color azul noche institucional.", "precio": 44000, "imagen": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?q=80&w=500&auto=format&fit=crop"},
    {"id": 18, "categoria": "accesorios", "nombre": "Chaqueta Rompevientos Inovamagic (Talla M)", "descripcion": "Chaqueta impermeable de la promoción escolar con capota oculta, cierres de seguridad y logo bordado.", "precio": 115000, "imagen": "https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=500&auto=format&fit=crop"},
    {"id": 19, "categoria": "accesorios", "nombre": "Correa Ajustable de Cuero", "descripcion": "Correa de cuero negro formal con hebilla metálica de alta sujeción para uniforme de diario.", "precio": 16000, "imagen": "https://images.unsplash.com/photo-1624222247344-550fb8ef5521?q=80&w=500&auto=format&fit=crop"},
    {"id": 20, "categoria": "accesorios", "nombre": "Medias Blancas Tejidas", "descripcion": "Par de medias escolares blancas de caña alta, elástico suave que no marca la piel.", "precio": 8000, "imagen": "https://images.unsplash.com/photo-1582966772680-860e372bb558?q=80&w=500&auto=format&fit=crop"}
]

@app.route('/')
def index():
    carrusel_items = [productos[0], productos[5], productos[15]]
    # Mandamos el estado de la sesión y los errores si existen
    usuario_logueado = session.get('usuario')
    error_auth = session.pop('error_auth', None)
    return render_template('index.html', productos=productos, carrusel=carrusel_items, usuario=usuario_logueado, error=error_auth)

@app.route('/login', methods=['POST'])
def login():
    correo = request.form.get('email')
    contrasena = request.form.get('password')
    
    # Validación lógica de credenciales
    if correo == USUARIO_TEST and contrasena == CLAVE_TEST:
        session['usuario'] = "Santiago Cuellar"  # Guarda el usuario en la sesión
    else:
        session['error_auth'] = "Correo o contraseña incorrectos"
        
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Destruye la sesión del usuario
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)