from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, get_flashed_messages
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from functools import wraps
from flask_mail import Mail, Message
app = Flask(__name__)
app.secret_key = 'inovamagic_secret_key_2026'
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Configuración para el envío de correos
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'santiagocuellar535@gmail.com'  # <-- PON TU GMAIL PERSONAL AQUÍ
app.config['MAIL_PASSWORD'] = 'pzbpmkmooenqcnsa'# <-- PEGA AQUÍ LAS 16 LETRAS AMARILLAS SIN ESPACIOS
app.config['MAIL_DEFAULT_SENDER'] = 'santiagocuellar535@gmail.com'  # <-- VUELVE A PONER TU GMAIL PERSONAL AQUÍ

mail = Mail(app)

@app.route('/restablecer/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        flash("El enlace de recuperación ha expirado o es inválido.")
        return redirect(url_for('recuperar_password_directo'))

    if request.method == 'POST':
        nueva_password = request.form.get('password')
        hashed_password = generate_password_hash(nueva_password)
        
        # (Aquí va la lógica para actualizar tu base de datos)
        
        flash("Tu contraseña ha sido actualizada con éxito.")
        return redirect(url_for('login'))

    return render_template('restablecer.html', token=token)

# Configuration for Google OAuth
app.config['GOOGLE_CLIENT_ID'] = 'YOUR_GOOGLE_CLIENT_ID' # Placeholder
app.config['GOOGLE_CLIENT_SECRET'] = 'YOUR_GOOGLE_CLIENT_SECRET' # Placeholder
app.config['GOOGLE_DISCOVERY_URL'] = (
    'https://accounts.google.com/.well-known/openid-configuration'
)

oauth = OAuth(app)
s = URLSafeTimedSerializer(app.secret_key) # For password reset tokens

# In-memory user store for demonstration purposes
USERS = {
    "santiago@evaristogarcia.com": {
        "name": "Santiago Cuellar",
        "password": generate_password_hash("12345"), # Hashed password
        "role": "Administrador",
        "institution": "I.E. Evaristo García",
        "address": "Calle 1 # 2-3, Cali",
        "neighborhood": "Centro",
        "phone": "+57 300 1234567",
        "is_admin": True,
        "google_id": None # To store Google ID if authenticated via Google
    },
    "maria@evaristogarcia.com": {
        "name": "Maria Lopez",
        "password": generate_password_hash("password123"),
        "role": "Estudiante",
        "institution": "I.E. Evaristo García",
        "address": "Carrera 4 # 5-6, Cali",
        "neighborhood": "Versalles",
        "phone": "+57 310 9876543",
        "is_admin": False,
        "google_id": None
    }
}

# Decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash("Necesitas iniciar sesión para acceder a esta página.", "error")
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check if user is admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash("Necesitas iniciar sesión para acceder a esta página.", "error")
            return redirect(url_for('login_page'))
        user = USERS.get(session['user_email'])
        if not user or not user.get('is_admin'):
            flash("No tienes permisos de administrador para acceder a esta página.", "error")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

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

PRODUCTOS_POR_ID = {p["id"]: p for p in productos}

IVA_RATE = 0.19
ENVIO_GRATIS_DESDE = 150_000
COSTO_ENVIO = 8_900


def _init_carrito():
    if "carrito" not in session:
        session["carrito"] = {}
    return session["carrito"]


def _buscar_producto(producto_id):
    try:
        return PRODUCTOS_POR_ID.get(int(producto_id))
    except (TypeError, ValueError):
        return None


def _calcular_totales(items):
    subtotal = sum(item["precio"] * item["cantidad"] for item in items)
    envio = 0 if subtotal >= ENVIO_GRATIS_DESDE or subtotal == 0 else COSTO_ENVIO
    iva = round(subtotal * IVA_RATE)
    total = subtotal + envio + iva
    cantidad_items = sum(item["cantidad"] for item in items)
    return {
        "subtotal": subtotal,
        "envio": envio,
        "iva": iva,
        "total": total,
        "cantidad_items": cantidad_items,
        "envio_gratis": subtotal >= ENVIO_GRATIS_DESDE,
    }


def _carrito_a_lista():
    carrito = _init_carrito()
    items = []
    for pid, data in carrito.items():
        producto = _buscar_producto(pid)
        if producto:
            items.append({
                "id": producto["id"],
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "imagen": producto["imagen"],
                "categoria": producto["categoria"],
                "cantidad": data["cantidad"],
                "subtotal_linea": producto["precio"] * data["cantidad"],
            })
    return items


def _respuesta_carrito(extra=None):
    items = _carrito_a_lista()
    totales = _calcular_totales(items)
    resp = {"ok": True, "items": items, **totales}
    if extra:
        resp.update(extra)
    return resp

@app.route('/')
def index():
    carrusel_items = [productos[0], productos[5], productos[15]]
    user_email = session.get('user_email')
    usuario_logueado = USERS.get(user_email) if user_email else None
    # Check for flashed messages directly in the template context
    has_flashed_messages = bool(get_flashed_messages())

    return render_template(
        'index.html',
        productos=productos,
        carrusel=carrusel_items,
        usuario=usuario_logueado,
        current_year=datetime.now().year,
        has_flashed_messages=has_flashed_messages
    )


@app.route('/login-page')
def login_page():
    error_auth = session.pop('error_auth', None)
    success_auth = session.pop('success_auth', None)
    active_tab = session.pop('active_tab', 'login')
    return render_template('login.html', error=error_auth, success=success_auth, active_tab=active_tab)


@app.route('/login', methods=['POST'])
def login():
    correo = request.form.get('email')
    contrasena = request.form.get('password')

    user = USERS.get(correo)
    if user and check_password_hash(user["password"], contrasena):
        session['user_email'] = correo
        flash(f"Bienvenido, {user['name']}!", "success")
        return redirect(url_for('index'))
    flash("El correo o la contraseña son incorrectos. Inténtalo de nuevo.", "error")
    session['active_tab'] = 'login'
    return redirect(url_for('login_page'))


@app.route('/register', methods=['POST'])
def register():
    nombre = request.form.get('name')
    correo = request.form.get('email')
    contrasena = request.form.get('password')
    rol = request.form.get('role')
    institucion = request.form.get('institution')
    direccion = request.form.get('address')
    barrio = request.form.get('neighborhood')
    telefono = request.form.get('phone')

    if not all([nombre, correo, contrasena, rol, institucion, direccion, barrio, telefono]):
        flash("Todos los campos son obligatorios para el registro.", "error")
        session['active_tab'] = 'register'
        return redirect(url_for('login_page'))

    if correo in USERS:
        flash("Este correo electrónico ya se encuentra registrado.", "error")
        session['active_tab'] = 'register'
    else:
        hashed_password = generate_password_hash(contrasena)
        USERS[correo] = {
            "name": nombre,
            "password": hashed_password,
            "role": rol,
            "institution": institucion,
            "address": direccion,
            "neighborhood": barrio,
            "phone": telefono,
            "is_admin": False, # New registered users are not admins by default
            "google_id": None
        }
        flash("¡Cuenta creada con éxito! Ya puedes iniciar sesión.", "success")
        session['active_tab'] = 'login'

    return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    # Clear Authlib session for Google OAuth
    oauth.google.clear_session()
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for('index'))

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar_password_directo():
    if request.method == 'POST':
        correo = request.form.get('email')
        nueva_password = request.form.get('password')
        
        # Buscamos si el correo existe en tu diccionario USERS
        user = USERS.get(correo)
        
        if user:
            # Si existe, le encriptamos y actualizamos la contraseña de una
            user['password'] = generate_password_hash(nueva_password)
            flash("Tu contraseña ha sido actualizada con éxito. Ya puedes iniciar sesión.", "success")
            return redirect(url_for('login_page'))
        else:
            # Si el correo no está registrado, le avisamos
            flash("El correo electrónico no se encuentra registrado.", "error")
            return redirect(url_for('recuperar_password_directo'))
            
    return render_template('recuperar.html')

@app.route('/actualizar-password/<token>', methods=['GET', 'POST'])
def cambiar_password_final(token):
    try:
        # Verificar el token de seguridad
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        flash("El enlace de recuperación ha expirado o es inválido.")
        return redirect(url_for('recuperar_password_directo'))

    if request.method == 'POST':
        nueva_password = request.form.get('password')
        hashed_password = generate_password_hash(nueva_password)
        
        flash("Tu contraseña ha sido actualizada con éxito. Ya puedes iniciar sesión.")
        return redirect(url_for('login'))

    return render_template('restablecer.html', token=token)

# Google OAuth2 Setup
oauth.register(
    'google',
    client_id=app.config.get('GOOGLE_CLIENT_ID'),
    client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url=app.config.get('GOOGLE_DISCOVERY_URL'),
    client_kwargs={'scope': 'openid email profile'},
    # Use HTTPS in production
    redirect_uri='http://127.0.0.1:5000/authorize/google'
)

@app.route('/login-google')
def login_google():
    # Clear previous session data for Google OAuth
    session.pop('google_oauth_token', None)
    session.pop('user_email', None)
    return oauth.google.authorize_redirect(redirect_uri=url_for('authorize_google', _external=True))


@app.route('/authorize/google')
def authorize_google():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        flash(f"Error de autenticación con Google: {e}", "error")
        return redirect(url_for('login_page'))

    userinfo = token.get('userinfo')
    if userinfo:
        email = userinfo['email']
        name = userinfo['name']
        google_id = userinfo['sub']

        if email not in USERS:
            # Register new user if not exists
            USERS[email] = {
                "name": name,
                "password": None, # Google authenticated users don't have a local password
                "role": "Estudiante", # Default role for new Google users
                "institution": "No especificada",
                "address": "No especificada",
                "neighborhood": "No especificado",
                "phone": "No especificado",
                "is_admin": False,
                "google_id": google_id
            }
            flash(f"¡Bienvenido, {name}! Tu cuenta de Google ha sido vinculada.", "success")
        else:
            # Update existing user with Google ID if they haven't logged in with Google before
            if not USERS[email].get('google_id'):
                USERS[email]['google_id'] = google_id
            flash(f"Bienvenido de nuevo, {name}!", "success")

        session['user_email'] = email
        return redirect(url_for('index'))
    
    flash("No se pudo obtener la información de usuario de Google.", "error")
    return redirect(url_for('login_page'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_email = session['user_email']
    user_data = USERS.get(user_email)

    if request.method == 'POST':
        user_data['name'] = request.form.get('name')
        user_data['role'] = request.form.get('role')
        user_data['institution'] = request.form.get('institution')
        user_data['address'] = request.form.get('address')
        user_data['neighborhood'] = request.form.get('neighborhood')
        user_data['phone'] = request.form.get('phone')
        flash("Tu perfil ha sido actualizado exitosamente.", "success")
        return redirect(url_for('profile')) # Redirect to GET to show updated data

    return render_template('profile.html', user=user_data) # Need to create this template


@app.route('/admin')
@admin_required
def admin_panel():
    total_sales = 1_500_000 # Placeholder
    orders_count = 120 # Placeholder
    visits_count = 5000 # Placeholder

    # Example sales history (placeholder data)
    sales_history = [
        {"id": 1, "cliente": "Santiago Cuellar", "grado": "11°", "productos": "Pantalón, Camisa", "total": 107000},
        {"id": 2, "cliente": "Maria Lopez", "grado": "10°", "productos": "Jardinera", "total": 97500},
    ]

    # Pass all users to the admin template
    return render_template(
        'admin.html',
        ventas_totales="{:,.0f}".format(total_sales),
        stats={"pedidos_cont": orders_count, "visitas": visits_count},
        historial=sales_history,
        users=USERS # Pass the entire USERS dictionary
    )


@app.route('/carrito')
def carrito_legacy():
    return redirect(url_for('index', carrito=1))


# ── API REST del Carrito ──

@app.route('/api/carrito', methods=['GET'])
def obtener_carrito():
    return jsonify(_respuesta_carrito())


@app.route('/api/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json(silent=True) or {}
    producto_id = data.get('id')
    try:
        cantidad = int(data.get('cantidad', 1))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "mensaje": "Cantidad inválida."}), 400

    if cantidad < 1:
        return jsonify({"ok": False, "mensaje": "Cantidad inválida."}), 400

    producto = _buscar_producto(producto_id)
    if not producto:
        return jsonify({"ok": False, "mensaje": "Producto no encontrado."}), 404

    carrito = _init_carrito()
    pid = str(producto["id"])
    if pid in carrito:
        carrito[pid]["cantidad"] += cantidad
    else:
        carrito[pid] = {"cantidad": cantidad}

    session.modified = True
    return jsonify(_respuesta_carrito({
        "mensaje": f'"{producto["nombre"]}" añadido al carrito.',
    }))


@app.route('/api/carrito/actualizar', methods=['POST'])
def actualizar_carrito():
    data = request.get_json(silent=True) or {}
    producto_id = data.get('id')
    try:
        cantidad = int(data.get('cantidad', 1))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "mensaje": "Cantidad inválida."}), 400

    producto = _buscar_producto(producto_id)
    if not producto:
        return jsonify({"ok": False, "mensaje": "Producto no encontrado."}), 404

    carrito = _init_carrito()
    pid = str(producto["id"])

    if cantidad <= 0:
        carrito.pop(pid, None)
    elif pid in carrito:
        carrito[pid]["cantidad"] = cantidad
    else:
        carrito[pid] = {"cantidad": cantidad}

    session.modified = True
    return jsonify(_respuesta_carrito())


@app.route('/api/carrito/eliminar', methods=['POST'])
def eliminar_del_carrito():
    data = request.get_json(silent=True) or {}
    producto_id = data.get('id')

    if not _buscar_producto(producto_id):
        return jsonify({"ok": False, "mensaje": "Producto no encontrado."}), 404

    carrito = _init_carrito()
    carrito.pop(str(producto_id), None)
    session.modified = True

    return jsonify(_respuesta_carrito({"mensaje": "Producto eliminado del carrito."}))


@app.route('/api/carrito/vaciar', methods=['POST'])
def vaciar_carrito():
    session["carrito"] = {}
    session.modified = True
    return jsonify(_respuesta_carrito({"mensaje": "Carrito vaciado."}))


@app.route('/api/carrito/comprar', methods=['POST'])
def finalizar_compra():
    items = _carrito_a_lista()
    if not items:
        return jsonify({"ok": False, "mensaje": "Tu carrito está vacío."}), 400

    totales = _calcular_totales(items)
    ahora = datetime.now()
    numero_orden = f"INV-{ahora.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    recibo = {
        "numero_orden": numero_orden,
        "fecha": ahora.strftime("%d/%m/%Y"),
        "hora": ahora.strftime("%H:%M:%S"),
        "comprador": session.get("user_name", "Cliente Invitado"), # Use user_name from session
        "institucion": "I.E. Evaristo García",
        "tienda": "Inovamagic Store",
        "metodo_pago": "Apple Pay · Tarjeta terminada en •••• 4242",
        "estado": "Pago aprobado",
        "items": items,
        "subtotal": totales["subtotal"],
        "envio": totales["envio"],
        "iva": totales["iva"],
        "total": totales["total"],
        "cantidad_items": totales["cantidad_items"],
        "envio_gratis": totales["envio_gratis"],
        "entrega_estimada": "3 a 5 días hábiles",
    }

    session["carrito"] = {}
    session.modified = True

    return jsonify({"ok": True, "recibo": recibo})


if __name__ == '__main__':
    app.run(debug=True)
