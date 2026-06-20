import random

# Base de datos maestra de imágenes coherentes por categoría
IMAGENES_COHERENTES = {
    "Diario Masculino": [
        "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?q=80&w=500&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?q=80&w=500&auto=format&fit=crop"
    ],
    "Diario Femenino": [
        "https://images.unsplash.com/photo-1598198414976-ddb788ec80c1?q=80&w=500&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=500&auto=format&fit=crop"
    ],
    "Educación Física": [
        "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=500&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1556906781-9a412961c28c?q=80&w=500&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1483721310020-03333e577078?q=80&w=500&auto=format&fit=crop"
    ],
    "Sistemas y Especialidad": [
        "https://images.unsplash.com/photo-1581655353564-df123a1eb820?q=80&w=500&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?q=80&w=500&auto=format&fit=crop"
    ],
    "Calzado Escolar": [
        "https://images.unsplash.com/photo-1549298916-b41d501d3772?q=80&w=500&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1608231387042-66d1773070a5?q=80&w=500&auto=format&fit=crop"
    ],
    "Accesorios": [
        "https://images.unsplash.com/photo-1582966772680-860e372bb558?q=80&w=500&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1624222247344-550fb8ef5521?q=80&w=500&auto=format&fit=crop"
    ]
}

# Componentes estructurales para fabricar las variaciones de productos
prendas_base = [
    {"nombre": "Pantalón de Diario Lino", "cat": "Diario Masculino", "precio_base": 75000},
    {"nombre": "Camisa de Diario Manga Corta", "cat": "Diario Masculino", "precio_base": 32000},
    {"nombre": "Camisa de Diario Manga Larga", "cat": "Diario Masculino", "precio_base": 38000},
    {"nombre": "Jardinera Escolar Plisada", "cat": "Diario Femenino", "precio_base": 78000},
    {"nombre": "Blusa Escolar de Diario", "cat": "Diario Femenino", "precio_base": 30000},
    {"nombre": "Sudadera Deportiva Institucional", "cat": "Educación Física", "precio_base": 55000},
    {"nombre": "Camiseta Deportiva Cuello V", "cat": "Educación Física", "precio_base": 28000},
    {"nombre": "Pantaloneta Atlética de Poliéster", "cat": "Educación Física", "precio_base": 25000},
    {"nombre": "Camiseta Polo Técnica en Sistemas", "cat": "Sistemas y Especialidad", "precio_base": 42000},
    {"nombre": "Chaqueta Rompevientos Inovamagic", "cat": "Sistemas y Especialidad", "precio_base": 115000},
    {"nombre": "Zapatos de Cuero Negro Colegial", "cat": "Calzado Escolar", "precio_base": 90000},
    {"nombre": "Tenis Blancos Deportivos Confort", "cat": "Calzado Escolar", "precio_base": 85000},
    {"nombre": "Correa Ajustable de Cuero", "cat": "Accesorios", "precio_base": 16000},
    {"nombre": "Medias Blancas Tejidas", "cat": "Accesorios", "precio_base": 8000}
]

tallas = ["Talla 12", "Talla 14", "Talla 16", "Talla S", "Talla M", "Talla L", "Talla XL"]

productos = []
id_contador = 1

# Bucle inteligente que itera hasta alcanzar exactamente los 100 productos requeridos
while len(productos) < 100:
    for prenda in prendas_base:
        if len(productos) >= 100:
            break
            
        talla_seleccionada = tallas[(id_contador - 1) % len(tallas)]
        
        # Le aplicamos una ligera variación de precio según la talla para que se vea real
        variacion_precio = ((id_contador % 3) * 2000)
        precio_final = prenda["precio_base"] + variacion_precio
        
        # Seleccionamos la imagen coherente correspondiente a su categoría
        lista_imgs = IMAGENES_COHERENTES[prenda["cat"]]
        imagen_seleccionada = lista_imgs[(id_contador - 1) % len(lista_imgs)]
        
        productos.append({
            "id": id_contador,
            "nombre": f"{prenda['nombre']} ({talla_seleccionada})",
            "descripcion": f"{prenda['nombre']} oficial para la Institución Educativa. Confeccionado en materiales de alta resistencia, ideal para el uso diario escolar.",
            "precio": precio_final,
            "imagen": imagen_seleccionada
        })
        id_contador += 1
    }
]