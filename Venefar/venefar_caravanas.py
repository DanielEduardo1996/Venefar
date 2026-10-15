# -*- coding: utf-8 -*-
"""VENEFAR - Caravanas"""
import json, random
from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from descripciones.ciudades import obtener_nombre
from venefar_economia import precio_actual
from venefar_mapa import RUTAS, conexiones_de, NIVELES_PELIGRO
from venefar_inventario import menu_inventario_agrupado, nombre_bonito_item


def listar_caravanas(conn, jugador_id):
    c = conn.cursor()
    c.execute("SELECT * FROM caravanas WHERE jugador_id=? ORDER BY id DESC", (jugador_id,))
    return [dict(r) for r in c.fetchall()]


def coste_caravana(dias):
    return 20 + dias * 5


def menu_enviar_caravana(conn, jugador, mundo):
    ciudad = jugador.get("ciudad", "capital_imperial")
    conexiones = conexiones_de(ciudad)
    if not conexiones:
        limpiar(); titulo("ENVIAR CARAVANA")
        narrar("Desde aqui no salen caravanas.")
        pausa(); return

    if not jugador["inventario"]:
        limpiar(); titulo("ENVIAR CARAVANA")
        narrar("No tienes nada en el inventario para enviar.")
        pausa(); return

    def contexto_dest():
        titulo("ENVIAR CARAVANA · DESTINO")
        print(f"  Origen: {C.BOLD}{obtener_nombre(ciudad)}{C.RESET}")

    items = []
    destinos = []
    for dest_id, (dias, peligro) in conexiones.items():
        nivel, _ = NIVELES_PELIGRO[peligro]
        coste = coste_caravana(dias)
        items.append((obtener_nombre(dest_id), f"{dias} dias · {coste} monedas · {nivel}"))
        destinos.append((dest_id, dias, peligro))
    idx = menu_flechas(items, contexto_fn=contexto_dest, permitir_cancelar=True)
    if idx == -1: return
    destino_id, dias, peligro = destinos[idx]

    # Elegir objeto con NOMBRES BONITOS y agrupados
    def contexto_obj():
        titulo(f"ENVIAR A {obtener_nombre(destino_id).upper()} · ELIGE OBJETO")
        print(f"  Tu dinero: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
    idx2 = menu_inventario_agrupado(jugador["inventario"],
                                     contexto_fn=contexto_obj,
                                     permitir_cancelar=True)
    if idx2 == -1: return

    item = jugador["inventario"][idx2]
    prod = item.split("x ", 1)[1] if "x " in item else item
    cant_disp = 1
    if "x " in item:
        try: cant_disp = int(item.split("x ", 1)[0])
        except Exception: cant_disp = 1

    precio_destino = precio_actual(conn, prod, ciudad=destino_id)
    precio_origen = precio_actual(conn, prod, ciudad=ciudad)

    limpiar(); titulo(f"CARAVANA A {obtener_nombre(destino_id).upper()}")
    print(f"  Producto: {nombre_bonito_item(prod)}")
    print(f"  Disponibles: {cant_disp}")
    print(f"  Precio aqui ({obtener_nombre(ciudad)}): {C.YELLOW}{precio_origen}{C.RESET}")
    print(f"  Precio destino ({obtener_nombre(destino_id)}): {C.GREEN}{precio_destino}{C.RESET}")
    coste = coste_caravana(dias)
    print(f"  Coste de la caravana: {C.RED}{coste}{C.RESET} monedas")
    print(f"  Riesgo de asalto: {NIVELES_PELIGRO[peligro][0]}")
    print()

    if jugador["dinero"] < coste:
        narrar(f"{C.RED}No tienes dinero para pagar la caravana.")
        pausa(); return

    print(f"  ¿Cuantas unidades envias? (max {cant_disp})")
    cant = pedir_numero(cant_disp)

    ingreso_estimado = int(cant * precio_destino * 0.85)

    def contexto_confirmar():
        titulo("CONFIRMAR ENVIO")
        print(f"  {C.BOLD}Producto:{C.RESET}    {nombre_bonito_item(prod)}")
        print(f"  {C.BOLD}Cantidad:{C.RESET}    {cant}")
        print(f"  {C.BOLD}Destino:{C.RESET}     {obtener_nombre(destino_id)}")
        print(f"  {C.BOLD}Coste envio:{C.RESET} {C.RED}{coste}{C.RESET} monedas")
        print(f"  {C.BOLD}Ingreso estimado:{C.RESET} {C.GREEN}{ingreso_estimado}{C.RESET} monedas")
        print()
        print(f"  {C.DIM}El ingreso es estimado. Si hay asalto, perderas todo.{C.RESET}")
        print()
        print(f"  {C.DIM}¿Confirmas el envio?{C.RESET}")

    if menu_flechas([("Confirmar envio", ""), ("Cancelar", "")],
                     contexto_fn=contexto_confirmar, permitir_cancelar=False) == 1:
        return

    if cant >= cant_disp:
        jugador["inventario"].pop(idx2)
    else:
        jugador["inventario"][idx2] = f"{cant_disp - cant}x {prod}"
    jugador["dinero"] -= coste

    dia_salida = mundo["dia"]
    dia_llegada = dia_salida + dias

    c = conn.cursor()
    c.execute("""INSERT INTO caravanas
        (jugador_id, ciudad_origen, ciudad_destino, contenido, coste,
         dia_salida, dia_llegada, estado, ingreso_estimado)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'en_camino', ?)""",
        (jugador["identificador"], ciudad, destino_id,
         json.dumps({prod: cant}), coste, dia_salida, dia_llegada,
         ingreso_estimado))
    conn.commit()

    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)

    limpiar(); titulo("CARAVANA ENVIADA")
    narrar(f"Una caravana parte hacia {obtener_nombre(destino_id)}.")
    narrar(f"Llegara en {dias} dias. Ingreso estimado: {ingreso_estimado} monedas.")
    pausa()


def menu_caravanas(conn, jugador, mundo):
    while True:
        activas = [c for c in listar_caravanas(conn, jugador["identificador"])
                   if c["estado"] == "en_camino"]

        def contexto():
            titulo("CARAVANAS")
            if activas:
                print(f"  {len(activas)} caravana(s) en camino.")
            else:
                print(f"  {C.DIM}No tienes caravanas en camino.{C.RESET}")

        items = [
            ("Enviar nueva caravana", ""),
            ("Ver caravanas en camino", ""),
            ("Volver", ""),
        ]
        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        if idx == 0:
            menu_enviar_caravana(conn, jugador, mundo)
        elif idx == 1:
            _ver_caravanas(conn, jugador, mundo)
        elif idx == 2:
            return


def _ver_caravanas(conn, jugador, mundo):
    limpiar(); titulo("MIS CARAVANAS")
    activas = [c for c in listar_caravanas(conn, jugador["identificador"])
               if c["estado"] == "en_camino"]
    if not activas:
        narrar("No tienes caravanas activas.")
        pausa(); return
    dia_actual = mundo["dia"]
    for c in activas:
        cont = json.loads(c["contenido"])
        desc = ", ".join(f"{nombre_bonito_item(k)} x{v}" for k, v in cont.items())
        dias_restantes = max(0, c["dia_llegada"] - dia_actual)
        print(f"  {C.CYAN}{obtener_nombre(c['ciudad_origen'])} → {obtener_nombre(c['ciudad_destino'])}{C.RESET}")
        print(f"    Contenido: {desc}")
        print(f"    Llega en {dias_restantes} dias.")
        print(f"    Ingreso estimado: {c['ingreso_estimado']} monedas.")
        print()
    pausa()


def procesar_caravanas_dia(conn, jugador, dia):
    jugador_id = jugador["identificador"]
    activas = [c for c in listar_caravanas(conn, jugador_id)
               if c["estado"] == "en_camino"]
    for c in activas:
        if c["dia_llegada"] > dia: continue
        peligro = 1
        for r in RUTAS:
            a, b, _, p = r
            if (a == c["ciudad_origen"] and b == c["ciudad_destino"]) or \
               (b == c["ciudad_origen"] and a == c["ciudad_destino"]):
                peligro = p
                break
        prob_asalto = [0.05, 0.15, 0.30, 0.50][peligro]
        if random.random() < prob_asalto:
            c_actual = conn.cursor()
            c_actual.execute("UPDATE caravanas SET estado='asaltada' WHERE id=?", (c["id"],))
            c_actual.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)",
                             (dia, "caravana",
                              f"Tu caravana hacia {obtener_nombre(c['ciudad_destino'])} fue asaltada. Perdida toda la mercancia."))
            conn.commit()
        else:
            ingreso = c["ingreso_estimado"]
            jugador["dinero"] += ingreso
            c_actual = conn.cursor()
            c_actual.execute("UPDATE caravanas SET estado='completada' WHERE id=?", (c["id"],))
            c_actual.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)",
                             (dia, "caravana",
                              f"Tu caravana llego a {obtener_nombre(c['ciudad_destino'])}. Ingreso: {ingreso} monedas."))
            conn.commit()