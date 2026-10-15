# -*- coding: utf-8 -*-
"""
VENEFAR - Modulo Jugador
Estado, persistencia y evolucion del personaje del jugador.
"""
import os, json

from venefar_ui import titulo, narrar, pausa, limpiar, menu_flechas, C


# Cosas que aparecen como "objeto" en la creacion pero NO son objetos reales.
# Se filtran del inventario para que no aparezcan como items.
PSEUDO_OBJETOS = {
    "Cicatriz visible",
    "Recuerdo del amor perdido",
    "El objeto del descubrimiento",
    "Un objeto de esa persona",
    "Un recuerdo del amor perdido",
    "El recuerdo de quien perdiste",
    "Esa persona, en algún lugar, sigue viva",
    "Esa persona, en algún lugar de Venefar",
    "Alguien que te debe algo",
    "El recuerdo de algo",
}


def filtrar_inventario(inventario):
    """Quita pseudo-objetos del inventario."""
    limpio = []
    for item in inventario:
        if item in PSEUDO_OBJETOS:
            continue
        limpio.append(item)
    return limpio


def cargar_jugador(conn, identificador):
    c = conn.cursor()
    c.execute("SELECT * FROM jugador WHERE identificador=?", (identificador,))
    f = c.fetchone()
    if not f: return None

    claves = f.keys()
    ciudad = f["ciudad"] if "ciudad" in claves else "capital_imperial"
    ciudades_vistas = json.loads(f["ciudades_vistas"]) if "ciudades_vistas" in claves else []

    inv_crudo = json.loads(f["inventario"])
    inv_limpio = filtrar_inventario(inv_crudo)

    return {
        "identificador": f["identificador"],
        "nombre": f["nombre"],
        "dinero": f["dinero"],
        "inventario": inv_limpio,
        "hambre": f["hambre"],
        "sed": f["sed"],
        "cansancio": f["cansancio"],
        "salud": f["salud"],
        "energia": f["energia"],
        "hora": f["hora"],
        "ciudad": ciudad,
        "ciudades_vistas": ciudades_vistas,
    }


def guardar_jugador(conn, jugador):
    c = conn.cursor()
    # Filtrar por si acaso antes de guardar
    inv = filtrar_inventario(jugador["inventario"])
    c.execute("""INSERT OR REPLACE INTO jugador
        (identificador, nombre, dinero, inventario, hambre, sed, cansancio, salud, energia, hora, ciudad, ciudades_vistas)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (jugador["identificador"], jugador["nombre"], jugador["dinero"],
         json.dumps(inv, ensure_ascii=False),
         jugador["hambre"], jugador["sed"], jugador["cansancio"],
         jugador["salud"], jugador["energia"], jugador["hora"],
         jugador.get("ciudad", "capital_imperial"),
         json.dumps(jugador.get("ciudades_vistas", []), ensure_ascii=False)))
    conn.commit()


def avanzar_estado_jugador(jugador, dias):
    for _ in range(dias):
        jugador["hambre"] = max(0, jugador["hambre"] - 25)
        jugador["sed"] = max(0, jugador["sed"] - 30)
        jugador["cansancio"] = min(100, jugador["cansancio"] + 50)
        jugador["energia"] = max(0, jugador["energia"] - 25)

        if jugador["hambre"] <= 30 and jugador["dinero"] >= 2:
            jugador["dinero"] -= 2
            jugador["hambre"] = min(100, jugador["hambre"] + 55)

        if jugador["sed"] <= 25 and jugador["dinero"] >= 1:
            jugador["dinero"] -= 1
            jugador["sed"] = min(100, jugador["sed"] + 60)

        jugador["energia"] = min(100, jugador["energia"] + 60)
        jugador["cansancio"] = max(0, jugador["cansancio"] - 25)

        if jugador["hambre"] < 15:
            jugador["salud"] = max(0, jugador["salud"] - 5)
        if jugador["sed"] < 15:
            jugador["salud"] = max(0, jugador["salud"] - 5)
        if jugador["cansancio"] > 85:
            jugador["energia"] = max(0, jugador["energia"] - 10)
        if jugador["hambre"] > 60 and jugador["sed"] > 60 and jugador["energia"] > 60:
            jugador["salud"] = min(100, jugador["salud"] + 1)


def listar_personajes():
    if not os.path.exists("partidas"): return []
    return [f for f in os.listdir("partidas") if f.endswith(".json")]


def cargar_personaje_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def elegir_personaje(conn):
    personajes = listar_personajes()
    if not personajes:
        limpiar(); titulo("NO HAY PERSONAJES")
        narrar("Crea uno primero con venefar_creacion.py.")
        pausa(); return None

    def contexto():
        titulo("ELIGE TU PERSONAJE")
        print(f"{C.DIM}Si ya jugaste con el, se cargara tu progreso.{C.RESET}")

    items = [(p.replace('.json', ''), "") for p in personajes]
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
    nombre_archivo = personajes[idx]
    identificador = nombre_archivo.replace('.json', '')
    datos_json = cargar_personaje_json(os.path.join("partidas", nombre_archivo))
    nombre_display = datos_json["nombre"]

    existente = cargar_jugador(conn, identificador)
    if existente:
        return existente

    # Nuevo jugador: cargar inventario desde JSON y filtrar pseudo-objetos
    inv_json = list(datos_json.get("inventario", []))
    inv_limpio = filtrar_inventario(inv_json)

    jugador = {
        "identificador": identificador,
        "nombre": nombre_display,
        "historia": datos_json.get("historia", ""),
        "dinero": datos_json.get("dinero", 0),
        "inventario": inv_limpio,
        "hora": 8,
        "hambre": 100,
        "sed": 100,
        "cansancio": 0,
        "salud": 100,
        "energia": 100,
        "ciudad": "capital_imperial",
        "ciudades_vistas": [],
    }
    guardar_jugador(conn, jugador)
    return jugador