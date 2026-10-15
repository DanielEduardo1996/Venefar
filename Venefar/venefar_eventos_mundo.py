# -*- coding: utf-8 -*-
"""
VENEFAR - Eventos del Mundo
Eventos procedurales que afectan a rutas, precios, NPCs y asentamientos.
"""
import random, json

from venefar_db import conectar


# Catálogo de eventos. Cada uno:
#   id, tipo, descripcion, duracion (dias), efecto
# efecto puede incluir:
#   precios: {producto: multiplicador}
#   ciudad_afectada: 'id' o None
#   ruta_afectada: (a, b) o None
#   mood_npcs: 'preocupado' etc (se aplica a NPCs de ciudad_afectada)
CATALOGO = [
    # ── Rutas y puentes ─────────────────────
    {
        "id": "puente_roto",
        "tipo": "ruta",
        "descripcion": "Un puente clave se ha derrumbado. Las caravanas toman una ruta mas larga.",
        "duracion": 25,
        "efectos": {
            "ruta_afectada": ("canterral", "santamera"),
            "precios": {"Mineral": 1.35, "Hierro": 1.30, "Carbon": 1.25},
        },
    },
    {
        "id": "camino_asaltado",
        "tipo": "ruta",
        "descripcion": "Bandidos controlan un tramo del camino real. Los transportistas temen pasar.",
        "duracion": 15,
        "efectos": {
            "ruta_afectada": ("capital_imperial", "robledal"),
            "precios": {"Madera": 1.25, "Tablones": 1.20},
        },
    },
    {
        "id": "tormenta_costera",
        "tipo": "clima",
        "descripcion": "Una gran tormenta azota la costa. Pocos barcos se atreven a salir.",
        "duracion": 10,
        "efectos": {
            "ciudad_afectada": "puerto_sal",
            "precios": {"Pescado": 1.40, "Sal": 1.30},
        },
    },
    # ── Cosechas y produccion ──────────────
    {
        "id": "sequia",
        "tipo": "cosecha",
        "descripcion": "La sequia arruina los campos. Los granjeros recogen la mitad de lo habitual.",
        "duracion": 30,
        "efectos": {
            "precios": {"Trigo": 1.50, "Harina": 1.40, "Pan": 1.30, "Verduras": 1.30},
        },
    },
    {
        "id": "plaga_ganado",
        "tipo": "cosecha",
        "descripcion": "Una plaga diezma los rebanos de la region.",
        "duracion": 25,
        "efectos": {
            "ciudad_afectada": "villafria",
            "precios": {"Carne": 1.45, "Cuero crudo": 1.35, "Lana": 1.30},
        },
    },
    {
        "id": "buena_cosecha",
        "tipo": "cosecha",
        "descripcion": "Una cosecha excepcional llena los graneros del reino.",
        "duracion": 20,
        "efectos": {
            "precios": {"Trigo": 0.70, "Verduras": 0.75, "Pan": 0.80},
        },
    },
    # ── Politica y guerra ──────────────────
    {
        "id": "rumor_guerra",
        "tipo": "politica",
        "descripcion": "Corre el rumor de que habra guerra con el norte. La gente se prepara.",
        "duracion": 20,
        "efectos": {
            "precios": {"Armas": 1.40, "Espadas": 1.35, "Herramientas": 1.15},
            "mood_npcs": "preocupado",
        },
    },
    {
        "id": "impuestos_altos",
        "tipo": "politica",
        "descripcion": "El rey ha subido los impuestos para pagar al ejercito.",
        "duracion": 15,
        "efectos": {
            "precios": {"Pan": 1.15, "Cerveza": 1.20, "Vino": 1.15},
            "mood_npcs": "molesto",
        },
    },
    {
        "id": "festival_real",
        "tipo": "politica",
        "descripcion": "El rey proclama un festival. Hay vino barato en todas las tabernas.",
        "duracion": 10,
        "efectos": {
            "precios": {"Vino": 0.75, "Cerveza": 0.80, "Carne": 0.90},
            "mood_npcs": "contento",
        },
    },
    # ── Minas y herreria ───────────────────
    {
        "id": "derrumbe_mina",
        "tipo": "produccion",
        "descripcion": "Un derrumbe en las minas de Canterral corta la produccion de mineral.",
        "duracion": 20,
        "efectos": {
            "ciudad_afectada": "canterral",
            "precios": {"Mineral": 1.45, "Hierro": 1.35, "Carbon": 1.25},
        },
    },
    {
        "id": "vena_rica",
        "tipo": "produccion",
        "descripcion": "Se descubre una vena de mineral especialmente rica en Canterral.",
        "duracion": 20,
        "efectos": {
            "ciudad_afectada": "canterral",
            "precios": {"Mineral": 0.70, "Hierro": 0.80},
        },
    },
    # ── Mar y pesca ────────────────────────
    {
        "id": "buena_pesca",
        "tipo": "produccion",
        "descripcion": "Los bancos de peces se acercan a la costa. Los pescadores hacen su agosto.",
        "duracion": 15,
        "efectos": {
            "ciudad_afectada": "puerto_sal",
            "precios": {"Pescado": 0.65, "Sal": 0.85},
        },
    },
    # ── Salud ──────────────────────────────
    {
        "id": "fiebre",
        "tipo": "salud",
        "descripcion": "Una fiebre recorre la region. Los medicos no dan abasto.",
        "duracion": 18,
        "efectos": {
            "precios": {"Hierbas": 1.50, "Remedios": 1.60, "Medicinas": 1.40},
            "mood_npcs": "enfermo",
        },
    },
]


def _cargar_activos(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM eventos_activos")
    activos = []
    for f in c.fetchall():
        activos.append({
            "id_db": f["id"],
            "tipo": f["tipo"],
            "dias_restantes": f["dias_restantes"],
            "datos": json.loads(f["datos"]),
        })
    return activos


def _guardar_activo(conn, tipo, dia_inicio, dias_restantes, datos):
    c = conn.cursor()
    c.execute("""INSERT INTO eventos_activos (tipo, dia_inicio, dias_restantes, datos)
                 VALUES (?, ?, ?, ?)""",
              (tipo, dia_inicio, dias_restantes, json.dumps(datos, ensure_ascii=False)))


def _limpiar_expirados(conn):
    c = conn.cursor()
    c.execute("DELETE FROM eventos_activos WHERE dias_restantes <= 0")
    conn.commit()


def modificador_precio(conn, producto):
    """Devuelve el multiplicador de precio segun eventos activos."""
    activos = _cargar_activos(conn)
    multi = 1.0
    for ev in activos:
        precios = ev["datos"].get("efectos", {}).get("precios", {})
        if producto in precios:
            multi *= precios[producto]
    return multi


def disparar_evento(conn, npcs, dia, guardar=True):
    """Con 5% de probabilidad diaria, dispara un evento del mundo."""
    if random.random() > 0.05:
        return None

    # No repetir el mismo tipo ya activo
    activos = _cargar_activos(conn)
    ids_activos = [a["datos"].get("id") for a in activos]

    candidatos = [e for e in CATALOGO if e["id"] not in ids_activos]
    if not candidatos:
        return None

    evento = random.choice(candidatos)
    duracion = evento["duracion"]

    datos = {
        "id": evento["id"],
        "nombre": evento["id"],
        "descripcion": evento["descripcion"],
        "efectos": evento["efectos"],
    }
    if guardar:
        _guardar_activo(conn, evento["tipo"], dia, duracion, datos)

    # Aplicar efecto inmediato sobre NPCs si procede
    ciudad_afectada = evento["efectos"].get("ciudad_afectada")
    mood_global = evento["efectos"].get("mood_npcs")
    for npc in npcs:
        if ciudad_afectada and npc.get("ciudad") != ciudad_afectada:
            continue
        if mood_global and random.random() < 0.5:
            npc["mood"] = mood_global
        elif random.random() < 0.3:
            npc["mood"] = random.choice(["preocupado", "molesto", "contento"])

    if guardar:
        c = conn.cursor()
        c.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)",
                  (dia, "mundo", f"EVENTO: {evento['descripcion']}"))
        conn.commit()

    return evento


def avanzar_eventos(conn):
    """Reduce dias restantes de eventos activos. Elimina los expirados."""
    c = conn.cursor()
    c.execute("UPDATE eventos_activos SET dias_restantes = dias_restantes - 1")
    conn.commit()
    _limpiar_expirados(conn)


def listar_eventos_activos(conn):
    return _cargar_activos(conn)