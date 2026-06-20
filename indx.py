from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'inovamagic_secret_key_premium_2026'

# ==========================================
# BASE DE DATOS LOCAL DEL CATÁLOGO (UNIFORMES IE EVARISTO GARCÍA)
# ==========================================
PRODUCTOS_DATABASES = [
    {
        "id": 1,
        "nombre": "Uniforme de Diario - Masculino",
        "descripcion": "Camisa blanca institucional con el escudo bordado de la I.E. Evaristo García y pantalón gris clásico de lino de excelente resistencia.",
        "precio": 65000,
        "imagen": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=500&q=80"
    },
    {
        "id": 2,
        "nombre": "Uniforme de Diario - Femenino",
        "descripcion": "Blusa blanca impecable con vivos y falda a cuadros plizados reglamentaria según los lineamientos institucionales.",
        "precio": 62000,
        "imagen": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=500&q=80"
    },
    {
        "id": 3,
        "nombre": "Uniforme de Educación Física (Conjunto completo)",
        "descripcion": "Sudadera gris reforzada y camiseta blanca deportiva transpirable con franjas amarillas y verdes de la especialidad.",
        "precio": 75000,
        "imagen": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=500&q=80"
    },
    {
        "id": 4,
        "nombre": "Suéter Institucional I.E. Evaristo García",
        "descripcion": "Chaqueta de lana térmica cuello en V, color azul oscuro con el escudo del colegio de alta definición en el pecho izquierdo.",
        "precio": 45000,
        "imagen": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=500&q=80"
    },
    {
        "id": 5,
        "nombre": "Camiseta Polo Técnica - Especialidad",
        "descripcion": "Camiseta exclusiva para los estudiantes del penúltimo y último año en modalidad Técnica en Sistemas y Programación.",
        "precio": 32000,
        "imagen": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=500&q=80"
    },
    {
        "id": 6,
        "nombre": "Kit de Medias Escolares (3 Pares)",
        "descripcion": "Medias blancas de algodón de alta densidad, perfectas para usar a diario con los zapatos colegiales tradicionales.",
        "precio": 15000,
        "imagen": "https://images.unsplash.com/photo-1582966772680-860e372bb558?auto=format&fit=crop&w=500&q=80"
    }
]

# ==========================================
# RUTAS DE LA APLICACIÓN FLASK
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializar el tema de la sesión si no existe
    if 'theme' not in session:
        session['theme'] = 'light'
        
    # Si el formulario del login en el HTML hace un POST a la raíz '/'
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validación de prueba rápida (Socio, cámbiala si usas base de datos SQLite/MySQL)
        if email and len(password) >= 4:
            session['usuario'] = email
            return redirect(url_for('index'))
            
    return render_template('index.html', productos=PRODUCTOS_DATABASES, theme=session['theme'])

@app.route('/save-theme', methods=['POST'])
def save_theme():
    data = request.get_json()
    if data and 'theme' in data:
        session['theme'] = data['theme']
        return jsonify({"status": "success", "theme_saved": session['theme']}), 200
    return jsonify({"status": "error"}), 400

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

# Ejecución local en el puerto 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)