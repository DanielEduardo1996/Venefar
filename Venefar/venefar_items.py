# -*- coding: utf-8 -*-
"""VENEFAR - Catalogo de items equipables
Todos los tipos x materiales.
"""

# ─── Materiales ──────────────────────────────────────
MATERIALES = {
    "hierro":  {"nombre": "hierro",  "multi_dano": 1.00, "multi_precio": 1.00, "multi_dur": 1.00, "multi_peso": 1.00, "color": "gris"},
    "bronce":  {"nombre": "bronce",  "multi_dano": 0.90, "multi_precio": 0.85, "multi_dur": 1.30, "multi_peso": 1.15, "color": "dorado"},
    "acero":   {"nombre": "acero",   "multi_dano": 1.30, "multi_precio": 2.20, "multi_dur": 1.50, "multi_peso": 0.90, "color": "azulado"},
    "plata":   {"nombre": "plata",   "multi_dano": 1.10, "multi_precio": 3.50, "multi_dur": 0.80, "multi_peso": 1.00, "color": "blanco"},
}


# ─── Slots ───────────────────────────────────────────
SLOTS = [
    ("cabeza",     "Cabeza"),
    ("cuello",     "Cuello"),
    ("torso",      "Torso"),
    ("hombros",    "Hombros"),
    ("manos",      "Manos"),
    ("anillo_1",   "Anillo 1"),
    ("anillo_2",   "Anillo 2"),
    ("cinturon",   "Cinturon"),
    ("piernas",    "Piernas"),
    ("pies",       "Pies"),
    ("mano_der",   "Mano derecha"),
    ("mano_izq",   "Mano izquierda"),
]

NOMBRES_SLOT = dict(SLOTS)


# ─── Tipos de armas ─────────────────────────────────
# dano_dados en formato (num_dados, caras_dado)
TIPOS_ARMAS = {
    # Dagas
    "daga":              {"nombre": "Daga",               "slot": "mano_der", "dano": (1,4), "vel": 5, "peso": 0.4, "precio": 20,  "req_fue": 5,  "dos_manos": False, "tipo": "cortante", "alcance": "corto"},
    "punal":             {"nombre": "Punal",              "slot": "mano_der", "dano": (1,5), "vel": 4, "peso": 0.5, "precio": 28,  "req_fue": 6,  "dos_manos": False, "tipo": "perforante", "alcance": "corto"},
    "daga_veneno":       {"nombre": "Daga envenenada",    "slot": "mano_der", "dano": (1,4), "vel": 5, "peso": 0.4, "precio": 45,  "req_fue": 6,  "dos_manos": False, "tipo": "perforante", "alcance": "corto", "veneno": 3},
    # Espadas
    "espada_corta":      {"nombre": "Espada corta",       "slot": "mano_der", "dano": (1,6), "vel": 4, "peso": 1.0, "precio": 60,  "req_fue": 8,  "dos_manos": False, "tipo": "cortante", "alcance": "medio"},
    "espada_larga":      {"nombre": "Espada larga",       "slot": "mano_der", "dano": (1,8), "vel": 3, "peso": 1.4, "precio": 95,  "req_fue": 11, "dos_manos": False, "tipo": "cortante", "alcance": "medio"},
    "espada_bastarda":   {"nombre": "Espada bastarda",    "slot": "mano_der", "dano": (1,8), "vel": 3, "peso": 1.6, "precio": 130, "req_fue": 12, "dos_manos": False, "tipo": "cortante", "alcance": "medio", "flexible": True},
    "estoque":           {"nombre": "Estoque",            "slot": "mano_der", "dano": (1,5), "vel": 5, "peso": 1.0, "precio": 80,  "req_fue": 9,  "dos_manos": False, "tipo": "perforante", "alcance": "medio"},
    # Hachas
    "hacha_mano":        {"nombre": "Hacha de mano",      "slot": "mano_der", "dano": (1,6), "vel": 4, "peso": 1.0, "precio": 35,  "req_fue": 8,  "dos_manos": False, "tipo": "cortante", "alcance": "corto"},
    "hacha_batalla":     {"nombre": "Hacha de batalla",   "slot": "mano_der", "dano": (1,8), "vel": 3, "peso": 1.6, "precio": 75,  "req_fue": 12, "dos_manos": False, "tipo": "cortante", "alcance": "corto"},
    "hacha_guerra":      {"nombre": "Hacha de guerra",    "slot": "mano_der", "dano": (2,6), "vel": 2, "peso": 2.5, "precio": 110, "req_fue": 14, "dos_manos": True,  "tipo": "cortante", "alcance": "medio"},
    # Mazas
    "maza":              {"nombre": "Maza",               "slot": "mano_der", "dano": (1,7), "vel": 3, "peso": 1.5, "precio": 50,  "req_fue": 10, "dos_manos": False, "tipo": "contundente", "alcance": "corto"},
    "martillo_guerra":   {"nombre": "Martillo de guerra", "slot": "mano_der", "dano": (2,6), "vel": 2, "peso": 2.8, "precio": 120, "req_fue": 15, "dos_manos": True,  "tipo": "contundente", "alcance": "medio"},
    # Lanzas
    "lanza_corta":       {"nombre": "Lanza corta",        "slot": "mano_der", "dano": (1,6), "vel": 4, "peso": 1.2, "precio": 40,  "req_fue": 8,  "dos_manos": False, "tipo": "perforante", "alcance": "medio"},
    "lanza_larga":       {"nombre": "Lanza larga",        "slot": "mano_der", "dano": (1,7), "vel": 3, "peso": 1.8, "precio": 65,  "req_fue": 10, "dos_manos": True,  "tipo": "perforante", "alcance": "largo"},
    "pica":              {"nombre": "Pica",               "slot": "mano_der", "dano": (1,8), "vel": 2, "peso": 2.5, "precio": 90,  "req_fue": 12, "dos_manos": True,  "tipo": "perforante", "alcance": "largo"},
    # Mandobles
    "mandoble":          {"nombre": "Mandoble",           "slot": "mano_der", "dano": (2,6), "vel": 2, "peso": 2.5, "precio": 140, "req_fue": 14, "dos_manos": True,  "tipo": "cortante", "alcance": "medio"},
    "montante":          {"nombre": "Montante",           "slot": "mano_der", "dano": (2,7), "vel": 2, "peso": 3.0, "precio": 180, "req_fue": 16, "dos_manos": True,  "tipo": "cortante", "alcance": "largo"},
    # Arcos
    "arco_corto":        {"nombre": "Arco corto",         "slot": "mano_der", "dano": (1,6), "vel": 3, "peso": 0.8, "precio": 45,  "req_fue": 6,  "dos_manos": True,  "tipo": "perforante", "alcance": "largo", "distancia": True},
    "arco_largo":        {"nombre": "Arco largo",         "slot": "mano_der", "dano": (1,8), "vel": 2, "peso": 1.0, "precio": 85,  "req_fue": 10, "dos_manos": True,  "tipo": "perforante", "alcance": "largo", "distancia": True},
    "arco_compuesto":    {"nombre": "Arco compuesto",     "slot": "mano_der", "dano": (1,9), "vel": 3, "peso": 1.1, "precio": 150, "req_fue": 12, "dos_manos": True,  "tipo": "perforante", "alcance": "largo", "distancia": True},
    # Ballestas
    "ballesta_ligera":   {"nombre": "Ballesta ligera",    "slot": "mano_der", "dano": (1,8), "vel": 2, "peso": 2.0, "precio": 90,  "req_fue": 8,  "dos_manos": True,  "tipo": "perforante", "alcance": "largo", "distancia": True, "recarga": 2},
    "ballesta_pesada":   {"nombre": "Ballesta pesada",    "slot": "mano_der", "dano": (2,6), "vel": 1, "peso": 3.5, "precio": 160, "req_fue": 12, "dos_manos": True,  "tipo": "perforante", "alcance": "largo", "distancia": True, "recarga": 3},
}


# ─── Tipos de armaduras/accesorios ─────────────────
TIPOS_ARMADURAS = {
    # Cascos
    "capucha_cuero":     {"nombre": "Capucha de cuero",      "slot": "cabeza",  "defensa": 2,  "peso": 0.3, "precio": 15,  "req_fue": 1},
    "casco_cuero":       {"nombre": "Casco de cuero",        "slot": "cabeza",  "defensa": 4,  "peso": 0.6, "precio": 30,  "req_fue": 3},
    "yelmo":             {"nombre": "Yelmo",                 "slot": "cabeza",  "defensa": 8,  "peso": 1.5, "precio": 60,  "req_fue": 6},
    "yelmo_completo":    {"nombre": "Yelmo completo",        "slot": "cabeza",  "defensa": 12, "peso": 2.5, "precio": 120, "req_fue": 10, "penal_vision": -2},
    "celada":            {"nombre": "Celada",                "slot": "cabeza",  "defensa": 10, "peso": 2.0, "precio": 95,  "req_fue": 8},
    # Torso
    "tunica":            {"nombre": "Tunica acolchada",      "slot": "torso",   "defensa": 2,  "peso": 1.5, "precio": 20,  "req_fue": 1},
    "gambeson":          {"nombre": "Gambeson",              "slot": "torso",   "defensa": 5,  "peso": 3.0, "precio": 55,  "req_fue": 4},
    "brigantina":        {"nombre": "Brigantina",            "slot": "torso",   "defensa": 8,  "peso": 4.5, "precio": 110, "req_fue": 7},
    "cota_malla":        {"nombre": "Cota de malla",         "slot": "torso",   "defensa": 12, "peso": 6.5, "precio": 200, "req_fue": 10},
    "coraza":            {"nombre": "Coraza",                "slot": "torso",   "defensa": 15, "peso": 8.0, "precio": 300, "req_fue": 12},
    "armadura_completa": {"nombre": "Armadura completa",     "slot": "torso",   "defensa": 20, "peso": 12.0,"precio": 500, "req_fue": 14, "penal_vel": -1},
    # Piernas
    "pantalones":        {"nombre": "Pantalones",            "slot": "piernas", "defensa": 1,  "peso": 0.8, "precio": 10,  "req_fue": 1},
    "grebas_cuero":      {"nombre": "Grebas de cuero",       "slot": "piernas", "defensa": 3,  "peso": 1.2, "precio": 25,  "req_fue": 3},
    "grebas_metal":      {"nombre": "Grebas de metal",       "slot": "piernas", "defensa": 6,  "peso": 2.5, "precio": 60,  "req_fue": 6},
    "faldon":            {"nombre": "Faldon de placas",      "slot": "piernas", "defensa": 8,  "peso": 3.5, "precio": 90,  "req_fue": 8},
    # Botas
    "zapatos":           {"nombre": "Zapatos",               "slot": "pies",    "defensa": 1,  "peso": 0.5, "precio": 8,   "req_fue": 1},
    "botas_cuero":       {"nombre": "Botas de cuero",        "slot": "pies",    "defensa": 3,  "peso": 1.0, "precio": 25,  "req_fue": 2},
    "botas_altas":       {"nombre": "Botas altas",           "slot": "pies",    "defensa": 5,  "peso": 1.5, "precio": 50,  "req_fue": 4},
    # Guantes
    "guantes_cuero":     {"nombre": "Guantes de cuero",      "slot": "manos",   "defensa": 1,  "peso": 0.3, "precio": 12,  "req_fue": 1},
    "guantes_reforzados":{"nombre": "Guantes reforzados",    "slot": "manos",   "defensa": 3,  "peso": 0.6, "precio": 30,  "req_fue": 3},
    "manoplas":          {"nombre": "Manoplas",              "slot": "manos",   "defensa": 6,  "peso": 1.2, "precio": 65,  "req_fue": 6},
    # Escudos (van al slot mano_izq)
    "rodela":            {"nombre": "Rodela",                "slot": "mano_izq", "defensa": 4,  "peso": 1.5, "precio": 35,  "req_fue": 4},
    "escudo_redondo":    {"nombre": "Escudo redondo",        "slot": "mano_izq", "defensa": 7,  "peso": 2.5, "precio": 70,  "req_fue": 6},
    "escudo_torre":      {"nombre": "Escudo de torre",       "slot": "mano_izq", "defensa": 12, "peso": 5.0, "precio": 130, "req_fue": 10},
    "paves":             {"nombre": "Paves",                 "slot": "mano_izq", "defensa": 16, "peso": 7.5, "precio": 200, "req_fue": 12, "penal_vel": -1},
    # Hombros
    "capa_sencilla":     {"nombre": "Capa sencilla",         "slot": "hombros", "defensa": 1,  "peso": 0.5, "precio": 15,  "req_fue": 1},
    "capa_capucha":      {"nombre": "Capa con capucha",      "slot": "hombros", "defensa": 2,  "peso": 0.8, "precio": 35,  "req_fue": 2},
    "manto_noble":       {"nombre": "Manto noble",           "slot": "hombros", "defensa": 3,  "peso": 1.2, "precio": 120, "req_fue": 1, "carisma": 2},
    # Cinturones
    "correa_cuero":      {"nombre": "Correa de cuero",       "slot": "cinturon", "defensa": 0, "peso": 0.2, "precio": 8,   "req_fue": 1},
    "cinturon_cuero":    {"nombre": "Cinturon de cuero grueso","slot": "cinturon","defensa": 1, "peso": 0.4, "precio": 18,  "req_fue": 2},
    "cinturon_metal":    {"nombre": "Cinturon con hebilla metal","slot": "cinturon","defensa": 2, "peso": 0.6, "precio": 40, "req_fue": 3},
    # Cuello
    "amuleto_hueso":     {"nombre": "Amuleto de hueso",      "slot": "cuello",  "defensa": 0,  "peso": 0.1, "precio": 20,  "req_fue": 1, "voluntad": 1},
    "collar_plata":      {"nombre": "Collar de plata",       "slot": "cuello",  "defensa": 0,  "peso": 0.2, "precio": 90,  "req_fue": 1, "carisma": 1},
    # Anillos
    "anillo_cobre":      {"nombre": "Anillo de cobre",       "slot": "anillo_1","defensa": 0,  "peso": 0.05, "precio": 12, "req_fue": 1},
    "anillo_plata":      {"nombre": "Anillo de plata",       "slot": "anillo_1","defensa": 0,  "peso": 0.05, "precio": 55, "req_fue": 1, "carisma": 1},
    "anillo_sello":      {"nombre": "Anillo con sello",      "slot": "anillo_1","defensa": 0,  "peso": 0.05, "precio": 120,"req_fue": 1, "reputacion": 2},
}


# ─── Funciones ───────────────────────────────────────
def es_item_equipable(item_id):
    """Comprueba si un item_id tipo 'espada_corta:acero' es equipable."""
    if not isinstance(item_id, str) or ":" not in item_id:
        return False
    tipo, material = item_id.split(":", 1)
    return tipo in TIPOS_ARMAS or tipo in TIPOS_ARMADURAS


def parsear_item_id(item_id):
    """Devuelve (tipo, material) o (None, None)."""
    if not isinstance(item_id, str) or ":" not in item_id:
        return None, None
    partes = item_id.split(":", 1)
    return partes[0], partes[1]


def obtener_item(item_id):
    """
    Dado un item_id 'espada_corta:acero', devuelve dict con todos sus stats.
    Devuelve None si no existe.
    """
    tipo, material = parsear_item_id(item_id)
    if not tipo or not material: return None
    if material not in MATERIALES: return None

    mat = MATERIALES[material]

    if tipo in TIPOS_ARMAS:
        base = TIPOS_ARMAS[tipo]
        dano_dados = base["dano"]
        dano_min = dano_dados[0]
        dano_max = dano_dados[1]
        dano_min = round(dano_min * mat["multi_dano"], 1)
        dano_max = round(dano_max * mat["multi_dano"], 1)
        return {
            "id": item_id,
            "nombre": f"{base['nombre']} de {mat['nombre']}",
            "tipo": "arma",
            "subtipo_tipo": base.get("tipo", "cortante"),
            "slot": base["slot"],
            "dano_min": dano_min,
            "dano_max": dano_max,
            "velocidad": base["vel"],
            "peso": round(base["peso"] * mat["multi_peso"], 2),
            "precio": int(base["precio"] * mat["multi_precio"]),
            "req_fuerza": base["req_fue"],
            "dos_manos": base.get("dos_manos", False),
            "alcance": base.get("alcance", "medio"),
            "distancia": base.get("distancia", False),
            "veneno": base.get("veneno", 0),
            "recarga": base.get("recarga", 0),
            "durabilidad_max": int(100 * mat["multi_dur"]),
            "durabilidad": int(100 * mat["multi_dur"]),
        }

    elif tipo in TIPOS_ARMADURAS:
        base = TIPOS_ARMADURAS[tipo]
        defensa = round(base["defensa"] * mat["multi_dano"], 1)
        return {
            "id": item_id,
            "nombre": f"{base['nombre']} de {mat['nombre']}",
            "tipo": "armadura",
            "slot": base["slot"],
            "defensa": defensa,
            "peso": round(base["peso"] * mat["multi_peso"], 2),
            "precio": int(base["precio"] * mat["multi_precio"]),
            "req_fuerza": base["req_fue"],
            "penal_vision": base.get("penal_vision", 0),
            "penal_vel": base.get("penal_vel", 0),
            "carisma": base.get("carisma", 0),
            "voluntad": base.get("voluntad", 0),
            "reputacion": base.get("reputacion", 0),
            "durabilidad_max": int(100 * mat["multi_dur"]),
            "durabilidad": int(100 * mat["multi_dur"]),
        }
    return None


def listar_items_por_slot(slot):
    """Devuelve lista de (item_id_base, nombre_base, precio_base) para un slot."""
    resultado = []
    for tipo, base in TIPOS_ARMAS.items():
        if base["slot"] == slot:
            resultado.append((tipo, base["nombre"], base["precio"]))
    for tipo, base in TIPOS_ARMADURAS.items():
        if base["slot"] == slot:
            resultado.append((tipo, base["nombre"], base["precio"]))
    return resultado


def listar_todos_items_base():
    """Devuelve lista de (tipo, nombre, categoria) de todos los items base."""
    resultado = []
    for tipo, base in TIPOS_ARMAS.items():
        resultado.append((tipo, base["nombre"], "arma"))
    for tipo, base in TIPOS_ARMADURAS.items():
        resultado.append((tipo, base["nombre"], "armadura"))
    return resultado


def generar_lista_precios():
    """
    Genera dict {item_id: precio} para todos los combos tipo:material.
    Util para el sistema de comercio.
    """
    precios = {}
    for tipo in TIPOS_ARMAS:
        for mat in MATERIALES:
            item_id = f"{tipo}:{mat}"
            item = obtener_item(item_id)
            if item:
                precios[item_id] = item["precio"]
    for tipo in TIPOS_ARMADURAS:
        for mat in MATERIALES:
            item_id = f"{tipo}:{mat}"
            item = obtener_item(item_id)
            if item:
                precios[item_id] = item["precio"]
    return precios


def calcular_stats_jugador(equipado):
    """
    Dado un dict {slot: item_id}, devuelve dict con stats totales.
    """
    stats = {
        "defensa_total": 0,
        "dano_min": 0,
        "dano_max": 0,
        "peso_total": 0,
        "penal_vision": 0,
        "penal_vel": 0,
        "carisma": 0,
        "voluntad": 0,
        "reputacion": 0,
    }
    for slot, item_id in equipado.items():
        if not item_id: continue
        item = obtener_item(item_id)
        if not item: continue
        stats["peso_total"] += item.get("peso", 0)
        if item["tipo"] == "arma":
            if item["dano_min"] > stats["dano_min"] or stats["dano_min"] == 0:
                stats["dano_min"] = item["dano_min"]
                stats["dano_max"] = item["dano_max"]
        elif item["tipo"] == "armadura":
            stats["defensa_total"] += item["defensa"]
            stats["penal_vision"] += item.get("penal_vision", 0)
            stats["penal_vel"] += item.get("penal_vel", 0)
            stats["carisma"] += item.get("carisma", 0)
            stats["voluntad"] += item.get("voluntad", 0)
            stats["reputacion"] += item.get("reputacion", 0)
    return stats