from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'inovamagic_secret_key'

usuarios = {
    "test@correo.com": {"password": "123", "theme": "light"}
}

# 8 Productos reales con imágenes cargadas desde internet
productos = [
    {
        "id": 1,
        "nombre": "Auriculares Premium",
        "precio": 180000,
        "imagen": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Audio HD con cancelación de ruido activa."
    },
    {
        "id": 2,
        "nombre": "Reloj Inteligente Sport",
        "precio": 250000,
        "imagen": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Monitoreo de ritmo cardíaco y notificaciones."
    },
    {
        "id": 3,
        "nombre": "Camiseta Inovamagic",
        "precio": 65000,
        "imagen": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "descripcion": "100% algodón premium con logo exclusivo."
    },
    {
        "id": 4,
        "nombre": "Morral Tech Ergonómico",
        "precio": 140000,
        "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&auto=format&fit=crop&q=60",
        "descripcion": "Compartimento acolchado para laptop y puerto USB."
    }
]

@app.route('/')
def index():
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
    
    usuarios[email] = {"password": password, "theme": "light"}
    session['usuario'] = email
    return redirect(url_for('index'))

@app.route('/save-theme', methods=['POST'])
def save_theme():
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