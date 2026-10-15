# -*- coding: utf-8 -*-
"""VENEFAR - Descripciones de NPCs.
Usa atributos fisicos unicos generados al crear el NPC.
"""
import random, json

from descripciones.generador_npcs import (
    construir_descripcion_larga,
    construir_descripcion_breve,
)


# Descripciones fijas para los 5 originales (por si quieres mantener las escritas a mano)
DESCRIPCIONES_FIJAS = {
    "Guzman el Herrero": {
        "larga": ("Guzman es un hombre ancho, de espaldas curtidas por decadas frente a la fragua. "
                  "Su delantal de cuero esta tan gastado que apenas recuerda su color original, y sus "
                  "brazos, gruesos como troncos, estan cubiertos de pequenas quemaduras antiguas. "
                  "Huele a carbon, a sudor y a hierro caliente."),
        "breve": "Guzman sigue en la fragua, el delantal gastado, las manos curtidas.",
    },
    "Aldonza la Tabernera": {
        "larga": ("Aldonza es una mujer de mediana edad, de figura menuda y movimientos rapidos. "
                  "Lleva el pelo recogido bajo un panuelo rojo que parece parte de ella. Tiene los "
                  "ojos vivos, siempre mirando a un lado y a otro, y una sonrisa facil que no siempre "
                  "llega a los ojos."),
        "breve": "Aldonza limpia una jarra detras del mostrador, el panuelo rojo en el pelo.",
    },
    "Iñigo de Castro": {
        "larga": ("Iñigo es un hombre delgado, de mediana edad, con la piel curtida de quien ha "
                  "pasado mucho tiempo al sol. Viste ropas finas pero practicas, y lleva un anillo "
                  "de plata en la mano derecha. Huele a especias extranjeras y a cuero."),
        "breve": "Iñigo revisa unas cuentas detras del mostrador, con su anillo de plata.",
    },
    "Urraca la Guardia": {
        "larga": ("Urraca es una mujer joven pero endurecida, de cuerpo atletico y porte marcial. "
                  "Lleva una cota de cuero reforzado y una espada al cinturon. Tiene una cicatriz "
                  "profunda en el cuello, ya curada. Su pelo, corto y oscuro, esta recogido."),
        "breve": "Urraca te observa en silencio, la mano cerca de la espada.",
    },
    "Elvira la Curandera": {
        "larga": ("Elvira es una mujer mayor, de pelo blanco recogido en un moño sencillo. Su rostro "
                  "esta surcado por arrugas finas. Viste ropas oscuras y practicas, con un delantal "
                  "manchado de hierbas y tinturas. Huele a tomillo y a romero."),
        "breve": "Elvira muele hierbas en un mortero, sin dejar de mirarte.",
    },
}


FRAGMENTOS_MOOD = {
    "cansado":   ["Hoy tiene los ojos mas hundidos de lo normal.", "Bosteza sin disimular."],
    "preocupado":["El ceño fruncido no se le va desde que has entrado.", "Parece distraido."],
    "contento":  ["Hoy tiene mejor cara que otras veces.", "Silba bajito mientras trabaja."],
    "molesto":   ["Esta de mal humor. Se le nota.", "Refunfuna entre dientes."],
    "borracho":  ["Huele a vino desde lejos.", "Tiene los ojos brillantes y la risa facil."],
    "animado":   ["Esta inusualmente hablador.", "Hoy parece tener ganas de conversar."],
    "enfermo":   ["Tiene mal color.", "Tose de vez en cuando."],
    "neutral":   [],
}


def _parsear_atributos(npc):
    """Devuelve el dict de atributos fisicos del NPC."""
    af = npc.get("atributos_fisicos")
    if isinstance(af, dict):
        return af
    if isinstance(af, str):
        try:
            return json.loads(af)
        except Exception:
            return {}
    return {}


def obtener_descripcion(npc, primera_vez=False, mood=None):
    """
    Devuelve la descripcion del NPC.
    Si es uno de los 5 fijos, usa la escrita a mano.
    Si no, construye una unica a partir de sus atributos fisicos.
    """
    datos_fijos = DESCRIPCIONES_FIJAS.get(npc["nombre"])
    if datos_fijos:
        lineas = []
        if primera_vez:
            lineas.append(datos_fijos["larga"])
        else:
            lineas.append(datos_fijos["breve"])
        if mood and mood in FRAGMENTOS_MOOD:
            frags = FRAGMENTOS_MOOD[mood]
            if frags and (primera_vez or random.random() < 0.5):
                lineas.append(random.choice(frags))
        return "\n\n  ".join(lineas)

    # Procedural con atributos unicos
    atributos = _parsear_atributos(npc)
    if not atributos:
        # Fallback si no hay atributos (no deberia pasar con BD nueva)
        return f"{npc['nombre']} es un {npc['oficio'].lower()} de {npc['edad']} anos."

    lineas = []
    if primera_vez:
        lineas.append(construir_descripcion_larga(
            npc["nombre"], npc["edad"], npc["sexo"], npc["oficio"], atributos))
    else:
        lineas.append(construir_descripcion_breve(
            npc["nombre"], npc["oficio"], atributos))

    # Añadir fragmento de mood
    if mood and mood in FRAGMENTOS_MOOD:
        frags = FRAGMENTOS_MOOD[mood]
        if frags and (primera_vez or random.random() < 0.5):
            lineas.append(random.choice(frags))

    return "\n\n  ".join(lineas)


def _fragmento_por_mood(npc, mood):
    frags = FRAGMENTOS_MOOD.get(mood, [])
    return random.choice(frags) if frags else None