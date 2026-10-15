# -*- coding: utf-8 -*-
"""VENEFAR - Modulo Mundo"""
import random

from venefar_npc import guardar_todos, guardar_recuerdo  # noqa
from venefar_economia import simular_dia_economico
from venefar_jugador import avanzar_estado_jugador, guardar_jugador


POOL_EVENTOS_CLIMA = [
    "Amanecio nublado. Los animos estan bajos.",
    "El sol brilla con fuerza. La gente trabaja animada.",
    "Llovio toda la manana. Las calles estan vacias.",
    "Hace un frio inesperado. La gente se queda en casa.",
    "El viento sopla fuerte. Se oyen historias de barcos perdidos.",
]
POOL_EVENTOS_SOCIAL = [
    "Una boda se celebro en la plaza. Hubo vino para todos.",
    "Hubo una discusion en la taberna. Nada grave.",
    "Un joven del barrio se alisto en el ejercito.",
    "Dos vecinos se reconciliaron tras anos de enemistad.",
    "Un nino nacio en la casa del panadero. Buena nueva.",
    "Un anciano murio en su casa. Fue enterrado al atardecer.",
]
POOL_EVENTOS_POLITICA = [
    "Corre el rumor de que el rey ha enfermado.",
    "El duque de Leon envio emisarios a la capital.",
    "El obispo predico un sermon encendido contra los nobles.",
    "La guardia reforzo las puertas. Algo se avecina.",
    "Se dice que el heredero ha sido visto con una plebeya.",
]


DIAS_POR_MES = 30
MESES_POR_ANIO = 12
DIAS_POR_ANIO = DIAS_POR_MES * MESES_POR_ANIO
ESTACIONES = ["Primavera", "Verano", "Otoño", "Invierno"]


def _desglosar_dia(dia):
    anio = (dia - 1) // DIAS_POR_ANIO + 1
    dia_del_anio = (dia - 1) % DIAS_POR_ANIO + 1
    mes = (dia_del_anio - 1) // DIAS_POR_MES + 1
    dia_del_mes = (dia_del_anio - 1) % DIAS_POR_MES + 1
    return anio, mes, dia_del_mes


def formatear_fecha(dia):
    anio, mes, dia_mes = _desglosar_dia(dia)
    return f"Dia {dia_mes} de Mes {mes}, Año {anio} d.C."


def formatear_fecha_corta(dia):
    anio, mes, dia_mes = _desglosar_dia(dia)
    return f"Mes {mes}, Dia {dia_mes}"


def obtener_estacion(dia):
    anio, mes, dia_mes = _desglosar_dia(dia)
    return ESTACIONES[(mes - 1) // 3]


def actualizar_estacion_mundo(conn, mundo):
    nueva = obtener_estacion(mundo["dia"])
    if mundo.get("estacion") != nueva:
        mundo["estacion"] = nueva
        c = conn.cursor()
        c.execute("UPDATE mundo SET estacion=? WHERE id=1", (nueva,))
        conn.commit()
        return True
    return False


def generar_evento_social(conn, npcs, dia, guardar=True):
    tipo = random.choice(["clima", "social", "politica"])
    pools = {"clima": POOL_EVENTOS_CLIMA, "social": POOL_EVENTOS_SOCIAL, "politica": POOL_EVENTOS_POLITICA}
    desc = random.choice(pools[tipo])
    if guardar:
        c = conn.cursor()
        c.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)", (dia, tipo, desc))
    for npc in npcs:
        if tipo == "clima" and random.random() < 0.3:
            npc["mood"] = random.choice(["cansado", "preocupado", "neutral"])
        elif tipo == "politica" and random.random() < 0.3:
            npc["mood"] = "preocupado"


def avanzar_un_dia(conn, npcs, mundo, jugador, guardar=True):
    from venefar_eventos_mundo import disparar_evento, avanzar_eventos
    from venefar_jugador_acciones import auto_venta_emergencia
    from venefar_negocios import procesar_negocios_dia
    from venefar_caravanas import procesar_caravanas_dia
    from venefar_bancos import procesar_interes_diario
    from venefar_guarniciones import procesar_guarniciones_dia

    mundo["dia"] += 1
    dia = mundo["dia"]
    for npc in npcs:
        npc["dias_sin_hablar"] += 1
        if random.random() < 0.25:
            npc["mood"] = random.choice(["neutral", "contento", "cansado", "preocupado", "animado"])

    # Simulacion economica (produccion + consumo + compras entre NPCs)
    simular_dia_economico(conn, npcs, dia, guardar=False)
    # Guarniciones (con npcs para actualizar memoria)
    procesar_guarniciones_dia(conn, npcs, dia)
    # Eventos
    generar_evento_social(conn, npcs, dia, guardar=guardar)
    disparar_evento(conn, npcs, dia, guardar=guardar)
    avanzar_eventos(conn)
    avanzar_estado_jugador(jugador, 1)
    # Sistemas del jugador
    procesar_negocios_dia(conn, jugador, dia)
    procesar_caravanas_dia(conn, jugador, dia)
    procesar_interes_diario(conn, jugador, dia)

    if jugador.get("hambre", 100) < 15 and jugador.get("dinero", 0) < 3:
        auto_venta_emergencia(conn, jugador, npcs)

    if guardar:
        guardar_todos(conn, npcs)
        guardar_jugador(conn, jugador)
        c = conn.cursor()
        c.execute("UPDATE mundo SET dia=? WHERE id=1", (dia,))
        actualizar_estacion_mundo(conn, mundo)
        c.execute("DELETE FROM frases_usadas WHERE dia < ?", (dia - 60,))
        conn.commit()