# -*- coding: utf-8 -*-
"""VENEFAR - Generador de NPCs por Asentamiento"""
import random, json

from descripciones.generador_npcs import generar_atributos_fisicos


NOMBRES_H = [
    "Alvar", "Bruno", "Cedric", "Dario", "Edric", "Falk", "Garin", "Hakon",
    "Ivar", "Jorik", "Karl", "Loras", "Mateo", "Nestor", "Otto", "Pietro",
    "Quirce", "Ramiro", "Sigfrido", "Tomas", "Ulric", "Valerio", "Willem",
    "Ximeno", "Yago", "Zoltan", "Adso", "Beltran", "Casimiro", "Dagoberto",
    "Eneko", "Fulgencio", "Gerardo", "Hugo", "Isidro", "Justo", "Lope",
    "Mauricio", "Nuño", "Odorico", "Pelayo", "Rodrigo", "Sancho", "Teobaldo",
    "Aurelio", "Bernardo", "Cristobal", "Damian", "Eustaquio", "Fabian",
    "Gaspar", "Hernan", "Ignacio", "Jacobo", "Leandro", "Marcial", "Nicolas",
    "Onofre", "Patricio", "Rufino", "Salvador", "Timoteo", "Urbano", "Vicente",
]
NOMBRES_M = [
    "Aldonza", "Berta", "Constanza", "Dulce", "Elvira", "Frida", "Gilda",
    "Helena", "Ilduara", "Juana", "Karla", "Leocadia", "Mafalda", "Nieves",
    "Oria", "Petronila", "Quiteria", "Rosalia", "Sancha", "Teresa", "Urraca",
    "Violante", "Ximena", "Yolanda", "Zaira", "Aurora", "Beatriz", "Clara",
    "Dorotea", "Elena", "Felipa", "Gontrodo", "Hildegarda", "Isabel", "Juliana",
    "Lucia", "Magdalena", "Natividad", "Olalla", "Pilar", "Ramona", "Sabina",
    "Teodora", "Ursula", "Valentina", "Xenia", "Ysabel", "Zita", "Adela",
]

APELLIDOS_NEUTROS = [
    "de Castro", "de Ribera", "de la Torre", "del Monte", "del Rio",
    "de Solis", "de Aguilar", "de la Fuente", "de Villalba", "de Nogales",
    "de Salcedo", "de Peralta", "de Lerma", "de Zamora", "de Avila",
]
APELLIDOS_M = [
    "el Herrero", "el Carpintero", "el Panadero", "el Tuerto", "el Cojo",
    "el Rojo", "el Viejo", "el Joven", "el Zurdo", "el Gordo", "el Flaco",
    "el Manco", "el Sordo", "el Mudo", "el Sabio", "el Callado", "el Rapado",
]
APELLIDOS_F = [
    "la Herrera", "la Carpintera", "la Panadera", "la Tuerta", "la Coja",
    "la Roja", "la Vieja", "la Joven", "la Zurda", "la Gorda", "la Flaca",
    "la Manca", "la Sorda", "la Muda", "la Sabia", "la Callada", "la Rapada",
]

PASADOS = [
    "Recibio un corte profundo en el brazo durante una pelea.",
    "Perdio a un hermano en un asalto de bandidos.",
    "Fue soldado durante tres anos antes de volver.",
    "Su familia murio de fiebre hace dos inviernos.",
    "Fue acusado injustamente de un robo hace anos.",
    "Trabajo en la construccion de la catedral.",
    "Viajo una vez a la capital y no quiere volver.",
    "Tiene un hijo que se fue a la guerra y no ha vuelto.",
    "Nunca ha salido de su pueblo. Le da miedo el mundo.",
    "Su esposa lo abandono por otro.",
    "Sobrevivio a un naufragio.",
    "Tiene una deuda que no puede pagar.",
]
SUENOS = [
    "Ser rico algun dia.", "Viajar a tierras lejanas.", "Casarse y tener hijos.",
    "Vengarse de alguien.", "Dejar su oficio y dedicarse a otra cosa.",
    "Ser recordado cuando muera.", "Conocer al rey en persona.",
    "Ver el mar por primera vez.", "Aprender a leer y escribir.", "Tener una casa propia.",
]
MIEDOS = [
    "Morir solo.", "La oscuridad.", "Los bandidos.", "La peste.",
    "Que se le acabe el dinero.", "Que le descubran su pasado.", "El fuego.", "La guerra.",
]
SECRETOS = [
    "Debe dinero a alguien peligroso.", "Sabe donde hay un tesoro escondido.",
    "Tiene un amante prohibido.", "Vio algo que no debia ver.",
    "Esconde su verdadero nombre.", "Fue testigo de un crimen.",
    "Tiene un hermano que se hizo bandido.", "Vende informacion a un noble.",
    "Robo algo de la iglesia hace anos.", "Mato a alguien hace mucho tiempo.",
]
RASGOS_POSIBLES = [
    "gruñón", "hablador", "supersticioso", "desconfiado", "amable",
    "chismoso", "orgulloso", "melancolico", "avaro", "religioso",
    "callado", "curioso", "calculador", "cuidadoso", "trabajador",
    "observador", "intelectual", "viajero", "borrachin", "charlatan",
]


INVENTARIO_INICIAL = {
    "Granjero":         {"Trigo": 5, "Verduras": 5, "Herramientas": 1},
    "Ganadero":         {"Carne": 3, "Cuero crudo": 3, "Leche": 4, "Pienso": 5},
    "Pescador":         {"Pescado": 6, "Redes": 1},
    "Leñador":          {"Madera": 5, "Leña": 5, "Hachas": 1},
    "Minero":           {"Mineral": 5, "Carbón": 4, "Piedra": 5, "Picos": 1},
    "Molinero":         {"Harina": 5, "Trigo": 3},
    "Panadero":         {"Pan": 6, "Harina": 4, "Leña": 3},
    "Cervecero":        {"Cerveza": 5, "Trigo": 3, "Agua": 5},
    "Herrero":          {"Herramientas": 3, "Armas": 2, "Mineral": 5, "Carbón": 5},
    "Carpintero":       {"Muebles": 2, "Tablones": 4, "Madera": 5},
    "Sastre":           {"Ropa": 3, "Tela": 3, "Lana": 4},
    "Albañil":          {"Piedra": 5, "Madera": 3, "Herramientas": 2},
    "Tabernero":        {"Pan": 4, "Cerveza": 4, "Carne": 3},
    "Comerciante":      {"Pan": 3, "Vino": 3, "Tela": 3, "Herramientas": 2},
    "Transportista":    {"Carros": 1, "Pienso": 5, "Pan": 3},
    "Médico":           {"Remedios": 5, "Medicinas": 2, "Hierbas": 6},
    "Guardia":          {"Espadas": 1, "Pan": 2, "Cerveza": 2},
    "Administrador":    {"Pan": 3, "Vino": 3, "Tela": 2},
    "Sacerdote":        {"Bendiciones": 3, "Pan": 2, "Vino": 2},
    "Alquimista":       {"Pociones": 3, "Venenos": 2, "Hierbas": 6},
    "Escriba":          {"Documentos": 2, "Cartas": 3, "Tinta": 4, "Papel": 5},
    "Cocinero":         {"Comida cocinada": 5, "Carne": 3, "Verduras": 4},
    "Cazador":          {"Pieles": 4, "Carne": 3, "Flechas": 6, "Arcos": 1},
    "Carpintero barcos":{"Barcas": 1, "Redes": 3, "Madera": 5},
    "Vidriero":         {"Vasos": 4, "Ventanas": 2, "Arena": 5},
    "Tejedor":          {"Tela": 5, "Tapices": 2, "Lana": 5},
    "Zapatero":         {"Botas": 3, "Zapatos": 4, "Cuero": 4},
    "Sacamuelas":       {"Servicios": 1, "Instrumentos": 3},
    "Músico":           {"Instrumentos": 2, "Pan": 2, "Vino": 2},
    "Soldado":          {"Espadas": 2, "Armas": 1, "Pan": 3, "Carne": 2},
    "Ballestero":       {"Ballestas": 2, "Virotes": 8, "Madera": 4},
    "Carcelero":        {"Llaves": 2, "Cadenas": 3, "Pan": 2},
    "Barrendero":       {"Escobas": 3, "Pan": 2},
    "Mensajero":        {"Cartas": 5, "Documentos": 2, "Pan": 3},
    "Explorador":       {"Mapas": 2, "Provisiones": 4, "Flechas": 5},
    "Salinero":         {"Sal": 6, "Agua": 4},
    "Carbonero":        {"Carbón vegetal": 5, "Madera": 4, "Leña": 3},
    "Peletero":         {"Piel trabajada": 4, "Cuero": 4, "Cuero crudo": 5},
}

DISTRIBUCION_CIUDADES = {
    "capital_imperial": [
        "Administrador", "Guardia", "Guardia", "Guardia", "Soldado",
        "Carpintero", "Albañil", "Escriba", "Sacerdote", "Músico",
        "Panadero", "Cervecero", "Tabernero", "Cocinero",
        "Comerciante", "Transportista", "Médico", "Sastre", "Mensajero",
    ],
    "puerto_sal": [
        "Comerciante", "Pescador", "Pescador", "Salinero",
        "Herrero", "Carpintero barcos", "Albañil",
        "Panadero", "Cervecero", "Tabernero", "Cocinero",
        "Guardia", "Guardia", "Médico", "Transportista",
        "Peletero", "Barrendero",
    ],
    "villareal": [
        "Administrador", "Guardia", "Guardia", "Guardia", "Soldado",
        "Sastre", "Herrero", "Albañil", "Vidriero", "Tejedor",
        "Panadero", "Cervecero", "Tabernero", "Cocinero",
        "Médico", "Comerciante", "Carpintero", "Sacerdote", "Escriba",
    ],
    "santamera": [
        "Administrador", "Guardia", "Guardia", "Guardia", "Soldado",
        "Soldado", "Herrero", "Herrero", "Ballestero", "Albañil",
        "Panadero", "Tabernero", "Médico", "Comerciante",
        "Transportista", "Carcelero",
    ],
    "piedrahonda": [
        "Granjero", "Granjero", "Granjero", "Molinero", "Panadero",
        "Herrero", "Tabernero", "Guardia", "Cocinero", "Tejedor",
    ],
    "villafria": [
        "Ganadero", "Ganadero", "Ganadero", "Sastre", "Peletero",
        "Herrero", "Panadero", "Tabernero", "Guardia", "Zapatero",
    ],
    "robledal": [
        "Leñador", "Leñador", "Leñador", "Carpintero", "Carbonero",
        "Herrero", "Cazador", "Tabernero", "Guardia", "Peletero",
    ],
    "canterral": [
        "Minero", "Minero", "Minero", "Herrero", "Herrero",
        "Carbonero", "Transportista", "Tabernero", "Guardia", "Barrendero",
    ],
    "mareas": [
        "Pescador", "Pescador", "Pescador", "Salinero", "Albañil",
        "Comerciante", "Tabernero", "Guardia", "Carpintero barcos",
    ],
    "ermita_alta": [
        "Ganadero", "Ganadero", "Médico", "Leñador", "Sacerdote",
    ],
    "calas": [
        "Pescador", "Pescador", "Tabernero", "Salinero",
    ],
    "fresnillo": [
        "Granjero", "Granjero", "Molinero", "Tabernero", "Cocinero",
    ],
}

DINERO_INICIAL = {
    "Granjero": 20, "Ganadero": 25, "Pescador": 20, "Leñador": 18,
    "Minero": 22, "Molinero": 30, "Panadero": 35, "Cervecero": 40,
    "Herrero": 70, "Carpintero": 50, "Sastre": 45, "Albañil": 55,
    "Tabernero": 60, "Comerciante": 150, "Transportista": 90,
    "Médico": 80, "Guardia": 40, "Administrador": 200,
    "Sacerdote": 50, "Alquimista": 90, "Escriba": 70, "Cocinero": 55,
    "Cazador": 40, "Carpintero barcos": 80, "Vidriero": 75,
    "Tejedor": 45, "Zapatero": 50, "Sacamuelas": 60, "Músico": 35,
    "Soldado": 55, "Ballestero": 65, "Carcelero": 50, "Barrendero": 25,
    "Mensajero": 40, "Explorador": 60, "Salinero": 40, "Carbonero": 30,
    "Peletero": 55,
}

NPCS_FIJOS = [
    {"nombre": "Guzman el Herrero", "edad": 52, "sexo": "Hombre",
     "oficio": "Herrero", "ciudad": "capital_imperial",
     "rasgos": ["gruñón", "orgulloso", "trabajador"],
     "pasado": "Su padre le enseño el oficio y murio antes de verle triunfar.",
     "sueno": "Que su hijo herede el taller algun dia.",
     "miedo": "Quedarse sin hierro y no poder trabajar.",
     "secreto": None, "detalle": "Tiene las manos llenas de cicatrices de quemaduras.",
     "dinero": 80, "inventario": {"Hierro": 8, "Madera": 3, "Herramientas": 2, "Espadas": 1}},
    {"nombre": "Aldonza la Tabernera", "edad": 38, "sexo": "Mujer",
     "oficio": "Tabernero", "ciudad": "capital_imperial",
     "rasgos": ["hablador", "chismoso", "amable"],
     "pasado": "Envio una vez un cargamento de vino al sur y le pagaron con monedas falsas.",
     "sueno": "Que su taberna sea conocida en todo el reino.",
     "miedo": "La ruina.",
     "secreto": "Debe dinero al prestamista del barrio y no puede pagarlo.",
     "detalle": "Siempre lleva un panuelo rojo en el pelo.",
     "dinero": 45, "inventario": {"Vino": 6, "Pan": 4, "Cerveza": 4, "Carne": 3}},
    {"nombre": "Iñigo de Castro", "edad": 45, "sexo": "Hombre",
     "oficio": "Comerciante", "ciudad": "capital_imperial",
     "rasgos": ["calculador", "avaro", "viajero"],
     "pasado": "Viajo a tierras lejanas hace anos y volvio rico.",
     "sueno": "Retirarse en una casa junto al mar.",
     "miedo": "Perder su fortuna.",
     "secreto": "Vende informacion sobre nobles a otros nobles.",
     "detalle": "Huele a especias extranjeras.",
     "dinero": 200, "inventario": {"Hierro": 5, "Hierbas": 4, "Pan": 2, "Tela": 4}},
    {"nombre": "Urraca la Guardia", "edad": 29, "sexo": "Mujer",
     "oficio": "Guardia", "ciudad": "capital_imperial",
     "rasgos": ["desconfiado", "callado", "observador"],
     "pasado": "Su hermano fue asesinado por bandidos.",
     "sueno": "Encontrar al asesino de su hermano.",
     "miedo": "Que maten a alguien mas por su culpa.",
     "secreto": "Sabe donde se esconde un bandido.",
     "detalle": "Tiene una cicatriz profunda en el cuello.",
     "dinero": 60, "inventario": {"Espadas": 1, "Pan": 3, "Cerveza": 1}},
    {"nombre": "Elvira la Curandera", "edad": 60, "sexo": "Mujer",
     "oficio": "Médico", "ciudad": "capital_imperial",
     "rasgos": ["melancolico", "intelectual", "cuidadoso"],
     "pasado": "Perdio a su hija por una fiebre que no pudo curar.",
     "sueno": "Encontrar la cura para esa fiebre.",
     "miedo": "Que la gente deje de confiar en ella.",
     "secreto": "Cultiva hierbas que la Iglesia ha prohibido.",
     "detalle": "Tiene los ojos cansados de tanto leer y velar.",
     "dinero": 40, "inventario": {"Hierbas": 10, "Remedios": 3, "Medicinas": 2}},
]

_NOMBRES_USADOS = set()


def _nombre_unico(nombre_base):
    if nombre_base not in _NOMBRES_USADOS:
        _NOMBRES_USADOS.add(nombre_base)
        return nombre_base
    sufijos = ["II", "III", "el Mozo", "el Menor", "el Nuevo"]
    for sufijo in sufijos:
        candidato = f"{nombre_base} {sufijo}"
        if candidato not in _NOMBRES_USADOS:
            _NOMBRES_USADOS.add(candidato)
            return candidato
    n = 2
    while True:
        candidato = f"{nombre_base} ({n})"
        if candidato not in _NOMBRES_USADOS:
            _NOMBRES_USADOS.add(candidato)
            return candidato
        n += 1


def generar_npc(oficio, ciudad):
    sexo = random.choice(["H", "M"])
    nombre = random.choice(NOMBRES_H if sexo == "H" else NOMBRES_M)

    # Apellido segun sexo
    tipo_apellido = random.random()
    if tipo_apellido < 0.5:
        apellido = random.choice(APELLIDOS_NEUTROS)
    elif sexo == "H":
        apellido = random.choice(APELLIDOS_M)
    else:
        apellido = random.choice(APELLIDOS_F)

    nombre_completo = _nombre_unico(f"{nombre} {apellido}")
    edad = random.randint(18, 65)
    sexo_str = "Hombre" if sexo == "H" else "Mujer"

    n_rasgos = random.choice([2, 2, 3])
    rasgos = random.sample(RASGOS_POSIBLES, n_rasgos)
    if "gruñón" in rasgos and "amable" in rasgos: rasgos.remove("amable")
    if "callado" in rasgos and "hablador" in rasgos: rasgos.remove("hablador")

    inventario = dict(INVENTARIO_INICIAL.get(oficio, {"Pan": 1}))
    dinero = DINERO_INICIAL.get(oficio, 30) + random.randint(-10, 20)
    atributos = generar_atributos_fisicos(sexo_str, oficio)

    return {
        "nombre": nombre_completo, "edad": edad, "sexo": sexo_str,
        "oficio": oficio, "ciudad": ciudad, "rasgos": rasgos,
        "pasado": random.choice(PASADOS), "sueno": random.choice(SUENOS),
        "miedo": random.choice(MIEDOS),
        "secreto": random.choice(SECRETOS) if random.random() < 0.35 else None,
        "detalle": atributos["cicatriz"].capitalize() + ".",
        "dinero": max(10, dinero), "inventario": inventario,
        "atributos_fisicos": atributos,
    }


def generar_todos_los_npcs():
    global _NOMBRES_USADOS
    _NOMBRES_USADOS = set()
    todos = []
    for npc in NPCS_FIJOS:
        _NOMBRES_USADOS.add(npc["nombre"])
        npc_copia = dict(npc)
        npc_copia["atributos_fisicos"] = generar_atributos_fisicos(npc["sexo"], npc["oficio"])
        todos.append(npc_copia)
    for ciudad_id in DISTRIBUCION_CIUDADES.keys():
        for oficio in DISTRIBUCION_CIUDADES[ciudad_id]:
            todos.append(generar_npc(oficio, ciudad_id))
    return todos