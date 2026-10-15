# -*- coding: utf-8 -*-
"""
VENEFAR - Reputacion
El jugador tiene una reputacion por ciudad (-100 a +100).
"""
from venefar_ui import C
from descripciones.ciudades import obtener_nombre


# ─── Etiquetas ──────────────────────────────────────
ETIQUETAS = [
    (-100, -60, "Enemigo",     C.RED),
    (-60,  -20, "Mal visto",   C.RED),
    (-20,   20, "Neutral",     C.WHITE),
    (20,    60, "Bien visto",  C.GREEN),
    (60,   100, "Heroe local", C.CYAN),
]


def etiqueta_reputacion(valor):
    """Devuelve (texto, color) segun el valor."""
    for minimo, maximo, texto, color in ETIQUETAS:
        if minimo <= valor < maximo:
            return texto, color
    if valor >= 100:
        return "Leyenda", C.MAGENTA
    return "Neutral", C.WHITE


def multiplicador_precio_reputacion(valor):
    """
    Multiplicador de precio de COMPRA para el jugador.
    - Enemigo: +50%
    - Mal visto: +25%
    - Neutral: sin cambio
    - Bien visto: -10%
    - Heroe: -25%
    """
    if valor <= -60: return 1.50
    if valor <= -20: return 1.25
    if valor < 20:   return 1.00
    if valor < 60:   return 0.90
    return 0.75


# ─── Persistencia ───────────────────────────────────
def obtener_reputacion(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("SELECT valor FROM reputacion WHERE jugador_id=? AND ciudad=?",
              (jugador_id, ciudad))
    f = c.fetchone()
    if f is None: return 0
    return f["valor"]


def modificar_reputacion(conn, jugador_id, ciudad, delta, razon=""):
    """Suma delta al valor actual. Se limita entre -100 y +100."""
    actual = obtener_reputacion(conn, jugador_id, ciudad)
    nuevo = max(-100, min(100, actual + delta))
    if nuevo == actual:
        return actual

    c = conn.cursor()
    c.execute("""INSERT INTO reputacion (jugador_id, ciudad, valor)
                 VALUES (?, ?, ?)
                 ON CONFLICT(jugador_id, ciudad) DO UPDATE SET valor=excluded.valor""",
              (jugador_id, ciudad, nuevo))
    conn.commit()
    return nuevo


def obtener_todas(conn, jugador_id):
    """Devuelve dict {ciudad: valor}."""
    c = conn.cursor()
    c.execute("SELECT ciudad, valor FROM reputacion WHERE jugador_id=?", (jugador_id,))
    return {f["ciudad"]: f["valor"] for f in c.fetchall()}