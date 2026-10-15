# -*- coding: utf-8 -*-
"""
VENEFAR - Modulo Descripciones
Motor que compone descripciones ricas a partir de piezas.
"""
import random

from descripciones.npcs import obtener_descripcion
from descripciones.fragmentos import (
    obtener_fragmento_hora,
    obtener_fragmento_clima,
    obtener_fragmento_ciudad,
)
from descripciones.ciudades import obtener_descripcion_ciudad
from descripciones.objetos import obtener_descripcion_objeto

from venefar_ui import C, linea


def describir_npc(npc, jugador, primera_vez=False, clima=None, ciudad=None):
    partes = []

    base = obtener_descripcion(npc, primera_vez=primera_vez, mood=npc.get("mood"))
    partes.append(base)

    if primera_vez or random.random() < 0.3:
        hora_txt = obtener_fragmento_hora(jugador.get("hora", 12))
        if hora_txt:
            partes.append(hora_txt)

    if clima and (primera_vez or random.random() < 0.25):
        clima_txt = obtener_fragmento_clima(clima)
        if clima_txt:
            partes.append(clima_txt)

    return "\n\n  ".join(partes)


def imprimir_descripcion_npc(npc, jugador, primera_vez=False, clima=None):
    desc = describir_npc(npc, jugador, primera_vez=primera_vez, clima=clima)
    print(f"  {C.WHITE}{desc}{C.RESET}\n")


def imprimir_descripcion_ciudad(ciudad_id, primera_vez=False):
    desc = obtener_descripcion_ciudad(ciudad_id, primera_vez=primera_vez)
    print(f"  {C.WHITE}{desc}{C.RESET}\n")


def imprimir_descripcion_objeto(nombre_objeto):
    desc = obtener_descripcion_objeto(nombre_objeto)
    print(f"  {C.WHITE}{desc}{C.RESET}\n")