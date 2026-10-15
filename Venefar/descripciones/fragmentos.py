# -*- coding: utf-8 -*-
"""
VENEFAR - Fragmentos dinamicos
Piezas de texto que se combinan segun contexto (hora, clima, ciudad, etc.)
"""

FRAGMENTOS_HORA = {
    "manana": [
        "La luz de la manana entra oblicua por las ventanas.",
        "El aire fresco de la manana aun no se ha ido.",
    ],
    "tarde": [
        "El sol de la tarde calienta las paredes.",
        "La luz del mediodia cae dura sobre las calles.",
    ],
    "atardecer": [
        "El sol empieza a caer, tiñendo todo de naranja.",
        "Las sombras se alargan por las calles.",
    ],
    "noche": [
        "Solo unas pocas velas iluminan la estancia.",
        "La noche pesa sobre la ciudad como una manta oscura.",
    ],
}


FRAGMENTOS_CLIMA = {
    "despejado": [
        "El cielo esta limpio y azul.",
        "Hace un dia claro y agradable.",
    ],
    "nublado": [
        "El cielo esta cubierto de nubes grises.",
        "Un manto de nubes cubre el sol.",
    ],
    "lluvia": [
        "Se oye la lluvia golpear los tejados.",
        "El agua cae sin parar desde primera hora.",
    ],
    "tormenta": [
        "Los truenos retumban a lo lejos.",
        "Los relampagos iluminan el horizonte de vez en cuando.",
    ],
    "nieve": [
        "Todo esta cubierto de un manto blanco.",
        "El frio corta la cara.",
    ],
}


FRAGMENTOS_CIUDAD = {
    "capital_imperial": [
        "La Capital Imperial nunca duerme del todo.",
        "El castillo del rey se alza imponente sobre las colinas.",
    ],
    "puerto_sal": [
        "Huele a sal y a pescado en todas partes.",
        "Las gaviotas gritan sobre el puerto.",
    ],
    "villareal": [
        "El castillo ducal domina la ciudad desde lo alto.",
        "Se respira un aire de poder y de intrigas.",
    ],
    "piedrahonda": [
        "Es un pueblo tranquilo, de gentes sencillas.",
        "El cruce de caminos trae viajeros de todas partes.",
    ],
}


def obtener_fragmento_hora(hora):
    """Devuelve un fragmento segun la hora del dia (0-23)."""
    import random
    if 5 <= hora < 12:
        pool = FRAGMENTOS_HORA["manana"]
    elif 12 <= hora < 18:
        pool = FRAGMENTOS_HORA["tarde"]
    elif 18 <= hora < 22:
        pool = FRAGMENTOS_HORA["atardecer"]
    else:
        pool = FRAGMENTOS_HORA["noche"]
    return random.choice(pool) if pool else None


def obtener_fragmento_clima(clima):
    """Devuelve un fragmento segun el clima actual."""
    import random
    pool = FRAGMENTOS_CLIMA.get(clima, [])
    return random.choice(pool) if pool else None


def obtener_fragmento_ciudad(ciudad):
    """Devuelve un fragmento segun la ciudad actual."""
    import random
    pool = FRAGMENTOS_CIUDAD.get(ciudad, [])
    return random.choice(pool) if pool else None