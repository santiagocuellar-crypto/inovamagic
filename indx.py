from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'inovamagic_secret_key'  # Clave segura para mantener las sesiones

# Base de datos simulada de usuarios con su preferencia de tema
usuarios = {
    "test@correo.com": {"password": "123", "theme": "light"}
}

# Lista completa de productos con imágenes reales para Inovamagic
productos = [
    {
        "id": 1,
        "nombre": "Auriculares Inalámbricos Premium",
        "precio": 180000,
        "imagen": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Audio de alta definición con cancelación de ruido activa."
    },
    {
        "id": 2,
        "nombre": "Reloj Inteligente Sport",
        "precio": 250000,
        "imagen": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Monitoreo de ritmo cardíaco, pasos y notificaciones en tiempo real."
    },
    {
        "id": 3,
        "nombre": "Camiseta Minimalista Inovamagic",
        "precio": 650000,
        "imagen": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "descripcion": "100% algodón premium con el logo exclusivo de la marca."
    },
    {
        "id": 4,
        "nombre": "Morral Ergonómico Tech",
        "precio": 140000,
        "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Compartimento acolchado para laptop y puerto de carga USB externo."
    },
    {
        "id": 5,
        "nombre": "Teclado Mecánico RGB",
        "precio": 195000,
        "imagen": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Switches Azules para una escritura rápida y retroiluminación personalizada."
    },
    {
        "id": 6,
        "nombre": "Mouse Gamer Ergonómico",
        "precio": 90000,
        "imagen": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Alta precisión con botones laterales programables."
    },
    {
        "id": 7,
        "nombre": "Termo Inteligente de Acero",
        "precio": 75000,
        "imagen": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Pantalla LED táctil que te muestra la temperatura exacta de tu bebida."
    },
    {
        "id": 8,
        "nombre": "Gorra Ajustable Streetwear",
        "precio": 45000,
        "imagen": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Estilo urbano moderno con visera curva perfecta para el diario."
    }
]

@app.route('/')
def index():
    # Detecta el tema preferido si el usuario inició sesión
    theme = "light"
    if 'usuario' in session:
        email = session['usuario']
        theme = usuarios.get(email, {}).get('theme', 'light')
    return render_template('index.html', productos=productos, theme=theme)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email in usuarios and usuarios[email]['password'] == password:
        session['usuario'] = email
        return redirect(url_for('index'))
    return "Usuario o contraseña incorrectos", 401

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return "Todos los campos son obligatorios", 400
        
    if email in usuarios:
        return "El usuario ya existe", 400
        
    # Corrección del mentor: Registro con cualquier correo electrónico válido
    usuarios[email] = {"password": password, "theme": "light"}
    session['usuario'] = email
    return redirect(url_for('index'))

@app.route('/save-theme', methods=['POST'])
def save_theme():
    # Punto 2: Guarda la persistencia del tema oscuro asociado a la cuenta del usuario
    data = request.get_json()
    theme = data.get('theme', 'light')
    
    if 'usuario' in session:
        email = session['usuario']
        if email in usuarios:
            usuarios[email]['theme'] = theme
            return jsonify({"status": "success", "theme": theme})
            
    return jsonify({"status": "guest_success", "theme": theme})

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)