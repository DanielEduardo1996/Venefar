# -*- coding: utf-8 -*-
"""VENEFAR - Acciones del Jugador"""
import random

from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from venefar_economia import PRODUCTOS, precio_actual
from venefar_reputacion import modificar_reputacion, obtener_reputacion, etiqueta_reputacion
from descripciones.ciudades import obtener_nombre
from venefar_inventario import (agrupar_inventario, NOMBRES_CATEGORIA,
                                 COLORES_CATEGORIA, nombre_bonito_item)
from venefar_items import es_item_equipable, obtener_item


TRABAJOS_SIMPLES = [
    {"nombre": "Descargar cajas en el puerto", "pago": (5, 9)},
    {"nombre": "Ayudar en la taberna", "pago": (6, 10)},
    {"nombre": "Limpiar establos", "pago": (5, 8)},
    {"nombre": "Repartir agua por la ciudad", "pago": (4, 7)},
    {"nombre": "Ayudar en la panaderia", "pago": (6, 10)},
    {"nombre": "Cargar mercancia en el mercado", "pago": (6, 11)},
]

TRABAJOS_ESPECIALIZADOS = {
    "Herreria": {"nombre": "Forjar herramientas sencillas", "pago": (14, 22)},
    "Erudicion": {"nombre": "Copiar documentos para un escriba", "pago": (13, 20)},
    "Alquimia": {"nombre": "Preparar remedios con hierbas", "pago": (14, 21)},
    "Medicina": {"nombre": "Ayudar al medico con los enfermos", "pago": (12, 20)},
    "Combate": {"nombre": "Entrenar reclutas de la guardia", "pago": (12, 18)},
    "Comercio": {"nombre": "Acompanar a un mercader como ayudante", "pago": (11, 18)},
    "Sigilo": {"nombre": "Trabajos discretos para un comerciante", "pago": (14, 22)},
    "Navegacion": {"nombre": "Ayudar en el mantenimiento de un barco", "pago": (12, 20)},
    "Supervivencia": {"nombre": "Guiar a un grupo por los alrededores", "pago": (11, 18)},
    "Artesania": {"nombre": "Reparar objetos para un artesano", "pago": (11, 18)},
    "Atletismo": {"nombre": "Ayudar con cargas pesadas", "pago": (10, 16)},
    "Tactica": {"nombre": "Ayudar a planificar defensas", "pago": (13, 20)},
}


def accion_trabajar(conn, jugador, npcs, mundo):
    limpiar(); titulo("BUSCAR TRABAJO")
    print(f"  {C.DIM}Un dia de trabajo. Elige que hacer.{C.RESET}\n")

    opciones = []
    claves = []
    for t in TRABAJOS_SIMPLES[:3]:
        pago_min, pago_max = t["pago"]
        opciones.append((t["nombre"], f"Pago: {pago_min}-{pago_max} monedas"))
        claves.append(("simple", t))

    habilidades = jugador.get("habilidades", {})
    for hab, val in list(habilidades.items())[:3]:
        if hab in TRABAJOS_ESPECIALIZADOS and val >= 1:
            t = TRABAJOS_ESPECIALIZADOS[hab]
            pago_min, pago_max = t["pago"]
            bonus = val
            opciones.append((t["nombre"], f"Pago: {pago_min + bonus}-{pago_max + bonus} monedas"))
            claves.append(("especializado", t, val))

    if not opciones:
        narrar("No encuentras trabajo por aqui.")
        pausa()
        return

    idx = menu_flechas(opciones, contexto_fn=lambda: None, permitir_cancelar=True)
    if idx == -1: return

    tipo, *resto = claves[idx]
    if tipo == "simple":
        t = resto[0]
        pago_min, pago_max = t["pago"]
        pago = random.randint(pago_min, pago_max)
    else:
        t, val = resto
        pago_min, pago_max = t["pago"]
        bonus = val
        pago = random.randint(pago_min + bonus, pago_max + bonus)

    ciudad = jugador.get("ciudad", "capital_imperial")
    nueva_rep = modificar_reputacion(conn, jugador["identificador"], ciudad, 1, "trabajo")

    jugador["dinero"] += pago
    jugador["cansancio"] = min(100, jugador.get("cansancio", 0) + 25)
    jugador["energia"] = max(0, jugador.get("energia", 100) - 20)

    limpiar(); titulo("TRABAJO TERMINADO")
    narrar(f"Trabajas todo el dia como {t['nombre'].lower()}.")
    narrar(f"Al atardecer, recibes {pago} monedas.")
    print(f"  {C.GREEN}Dinero actual:{C.RESET} {jugador['dinero']} monedas")
    print(f"  {C.DIM}Cansancio: +25  Energia: -20{C.RESET}")
    etiqueta, color = etiqueta_reputacion(nueva_rep)
    print(f"  Reputacion en {obtener_nombre(ciudad)}: {color}{etiqueta} ({nueva_rep}){C.RESET}")
    pausa()


def accion_pedir_limosna(conn, jugador, npcs, mundo):
    limpiar(); titulo("PEDIR LIMOSNA")

    if jugador["dinero"] >= 20:
        narrar("Tienes suficiente dinero. No necesitas pedir limosna.")
        pausa()
        return

    ciudad = jugador.get("ciudad", "capital_imperial")
    rep_actual = obtener_reputacion(conn, jugador["identificador"], ciudad)
    npcs_ciudad = [n for n in npcs if n.get("ciudad") == ciudad]
    if not npcs_ciudad:
        narrar("No hay nadie a quien pedir.")
        pausa()
        return

    roll = random.random() - (rep_actual / 200.0)

    if roll < 0.15:
        npc = random.choice(npcs_ciudad)
        npc["relacion"] -= 1
        narrar(f"{npc['nombre']} te mira con desprecio. 'Busca trabajo, vago.'")
        ganancia = 0
    elif roll < 0.5:
        ganancia = random.randint(0, 2)
        if ganancia > 0:
            narrar(f"Un anciano te da {ganancia} monedas sin decir nada.")
        else:
            narrar("Nadie te da nada. Sigues con las manos vacias.")
    elif roll < 0.85:
        ganancia = random.randint(1, 4)
        narrar(f"Varias personas te dan unas monedas. Consigues {ganancia}.")
    else:
        ganancia = random.randint(4, 8)
        narrar(f"Un mercader compasivo te da {ganancia} monedas. 'Que el Sol te acompane.'")

    nueva_rep = modificar_reputacion(conn, jugador["identificador"], ciudad, -1, "limosna")
    jugador["dinero"] += ganancia
    jugador["cansancio"] = min(100, jugador.get("cansancio", 0) + 10)

    print(f"\n  {C.GREEN}Dinero actual:{C.RESET} {jugador['dinero']} monedas")
    etiqueta, color = etiqueta_reputacion(nueva_rep)
    print(f"  Reputacion en {obtener_nombre(ciudad)}: {color}{etiqueta} ({nueva_rep}){C.RESET}")
    pausa()


OFICIOS_COMPRADORES = {
    "Herrero":     ["Mineral", "Hierro", "Carbón", "Herramientas", "Armas", "Espadas", "Picos", "Hachas"],
    "Panadero":    ["Harina", "Leña", "Trigo"],
    "Cervecero":   ["Trigo", "Agua", "Cebada"],
    "Tabernero":   ["Pan", "Carne", "Cerveza", "Vino", "Verduras"],
    "Médico":      ["Hierbas", "Remedios", "Medicinas"],
    "Carpintero":  ["Madera", "Tablones"],
    "Sastre":      ["Lana", "Tela", "Cuero", "Cuero crudo", "Ropa"],
    "Granjero":    ["Herramientas"],
    "Ganadero":    ["Pienso"],
    "Pescador":    ["Redes"],
    "Minero":      ["Picos"],
    "Leñador":     ["Hachas"],
    "Comerciante": ["Pan", "Vino", "Tela", "Herramientas"],
    "Alquimista":  ["Hierbas", "Mineral", "Agua"],
    "Cocinero":    ["Carne", "Verduras", "Pan"],
    "Tejedor":     ["Lana"],
    "Zapatero":    ["Cuero"],
    "Peletero":    ["Cuero crudo", "Pieles"],
    "Carbonero":   ["Madera"],
    "Salinero":    ["Agua"],
}


def _limpiar_nombre_producto(item):
    if "x " in item:
        return item.split("x ", 1)[1]
    return item


def _menu_inventario_agrupado(inventario, contexto_fn=None, permitir_cancelar=True):
    """Menu con nombres bonitos agrupados por categoria."""
    if not inventario:
        return -1
    grupos = agrupar_inventario(inventario)
    items_menu = []
    indices_originales = []
    for cat in ["equipo", "consumibles", "documentos", "miscelaneo"]:
        lista = grupos[cat]
        if not lista:
            continue
        items_menu.append((f"--- {NOMBRES_CATEGORIA[cat]} ---", ""))
        indices_originales.append(-1)
        for item in lista:
            items_menu.append((nombre_bonito_item(item), ""))
            indices_originales.append(inventario.index(item))
    def contexto():
        if contexto_fn:
            contexto_fn()
    idx = menu_flechas(items_menu, contexto_fn=contexto, permitir_cancelar=permitir_cancelar)
    if idx == -1:
        return -1
    if indices_originales[idx] == -1:
        return -1
    return indices_originales[idx]


def accion_vender(conn, jugador, npcs, mundo):
    """Venta desde el menu principal. Ahora usa nombres bonitos y panel detallado."""
    if not jugador["inventario"]:
        limpiar(); titulo("VENDER")
        narrar("No tienes nada que vender.")
        pausa()
        return

    def contexto_obj():
        titulo("VENDER - ELIGE OBJETO")
        print(f"  {C.DIM}Tu dinero: {jugador['dinero']} monedas{C.RESET}")

    idx = _menu_inventario_agrupado(jugador["inventario"],
                                     contexto_fn=contexto_obj,
                                     permitir_cancelar=True)
    if idx == -1:
        return

    item = jugador["inventario"][idx]
    producto = _limpiar_nombre_producto(item)

    # ─── ITEM D2 (equipable) ───
    if es_item_equipable(producto):
        item_data = obtener_item(producto)
        if not item_data:
            limpiar(); titulo("VENDER")
            narrar("Item invalido.")
            pausa(); return

        cantidad = 1
        if "x " in item:
            try: cantidad = int(item.split("x ", 1)[0])
            except Exception: cantidad = 1

        ciudad = jugador.get("ciudad", "capital_imperial")
        npcs_ciudad = [n for n in npcs if n.get("ciudad") == ciudad and n["dinero"] > 0]
        if not npcs_ciudad:
            limpiar(); titulo("VENDER")
            narrar("No hay nadie con dinero para comprarte eso.")
            pausa(); return

        def contexto_npc():
            titulo(f"VENDER {item_data['nombre'].upper()}")
            print(f"  {C.DIM}Elige a quien venderselo.{C.RESET}")
            print(f"  {C.DIM}Los herreros y ballesteros pagan mas por armas.{C.RESET}")

        items_npc = []
        for n in npcs_ciudad:
            if n["oficio"] in ("Herrero", "Ballestero"):
                interes = f" {C.GREEN}(interesado){C.RESET}"
            else:
                interes = ""
            items_npc.append((n["nombre"], f"{n['oficio']}{interes} - Dinero: {n['dinero']}"))
        idx2 = menu_flechas(items_npc, contexto_fn=contexto_npc, permitir_cancelar=True)
        if idx2 == -1: return
        npc = npcs_ciudad[idx2]

        precio_base = item_data["precio"]
        if npc["oficio"] in ("Herrero", "Ballestero"):
            multi = 0.60
            razon = f"{npc['oficio']} - puede revenderlo o usarlo. Paga 60% del valor."
        else:
            multi = 0.30
            razon = f"{npc['oficio']} - no trafica con armas. Paga 30% del valor."
        precio_u = max(1, int(precio_base * multi))
        max_dinero = npc["dinero"] // precio_u
        if max_dinero <= 0:
            limpiar(); titulo("VENDER")
            narrar(f"{npc['nombre']} no puede pagarte eso.")
            print(f"  {C.DIM}Precio por unidad: {precio_u} monedas{C.RESET}")
            print(f"  {C.DIM}Dinero de {npc['nombre']}: {npc['dinero']} monedas{C.RESET}")
            pausa(); return
        cant_v = min(cantidad, max_dinero)
        total = precio_u * cant_v

        def contexto_venta_equipo():
            titulo("CONFIRMAR VENTA")
            print(f"  {C.BOLD}Item:{C.RESET}              {item_data['nombre']}")
            print(f"  {C.BOLD}Vendedor:{C.RESET}          {npc['nombre']}")
            print(f"  {C.BOLD}Valor base:{C.RESET}        {precio_base} monedas")
            print(f"  {C.BOLD}Cantidad:{C.RESET}          {cant_v} de {cantidad}")
            print(f"  {C.BOLD}Precio por unidad:{C.RESET} {C.YELLOW}{precio_u}{C.RESET} monedas")
            print(f"  {C.BOLD}Total a recibir:{C.RESET}   {C.GREEN}{total}{C.RESET} monedas")
            print()
            print(f"  {C.DIM}Motivo del precio: {razon}{C.RESET}")
            if cant_v < cantidad:
                print(f"  {C.DIM}(Solo te compra {cant_v} porque no le alcanza el dinero){C.RESET}")
            print()
            print(f"  {C.DIM}¿Confirmas la venta?{C.RESET}")

        if menu_flechas([("Confirmar venta", ""), ("Cancelar", "")],
                         contexto_fn=contexto_venta_equipo, permitir_cancelar=False) == 1:
            return

        jugador["dinero"] += total
        npc["dinero"] -= total
        npc["inventario"][producto] = npc["inventario"].get(producto, 0) + cant_v
        if cant_v >= cantidad:
            jugador["inventario"].pop(idx)
        else:
            jugador["inventario"][idx] = f"{cantidad - cant_v}x {producto}"

        from venefar_jugador import guardar_jugador
        from venefar_npc import guardar_npc
        guardar_jugador(conn, jugador)
        guardar_npc(conn, npc)

        limpiar(); titulo("VENTA REALIZADA")
        narrar(f"Vendes {cant_v} de {item_data['nombre']} a {npc['nombre']} por {total} monedas.")
        print(f"  {C.GREEN}Dinero actual:{C.RESET} {jugador['dinero']} monedas")
        pausa()
        return

    # ─── ITEM NORMAL ───
    if producto not in PRODUCTOS:
        limpiar(); titulo("VENDER")
        narrar(f"No hay mercado para '{producto}'.")
        pausa()
        return

    cantidad = 1
    if "x " in item:
        try: cantidad = int(item.split("x ", 1)[0])
        except Exception: cantidad = 1

    ciudad = jugador.get("ciudad", "capital_imperial")
    npcs_ciudad = [n for n in npcs if n.get("ciudad") == ciudad and n["dinero"] > 0]
    if not npcs_ciudad:
        limpiar(); titulo("VENDER")
        narrar("No hay nadie con dinero para comprarte eso.")
        pausa()
        return

    def contexto_npc():
        titulo(f"VENDER {producto}")
        print(f"  {C.DIM}Elige a quien venderle.{C.RESET}")

    items_npc = []
    for n in npcs_ciudad:
        compra = OFICIOS_COMPRADORES.get(n["oficio"], [])
        interes = f" {C.GREEN}(interesado){C.RESET}" if producto in compra else ""
        items_npc.append((n["nombre"], f"{n['oficio']}{interes} - Dinero: {n['dinero']}"))
    idx2 = menu_flechas(items_npc, contexto_fn=contexto_npc, permitir_cancelar=True)
    if idx2 == -1:
        return
    npc = npcs_ciudad[idx2]

    precio_local = precio_actual(conn, producto, ciudad=ciudad)
    compra = OFICIOS_COMPRADORES.get(npc["oficio"], [])
    if producto in compra:
        multi = 0.70
        razon = f"{npc['oficio']} necesita {producto} para su oficio. Paga 70%."
    else:
        multi = 0.50
        razon = f"{npc['oficio']} no usa {producto}. Paga 50%."
    precio_unitario = max(1, int(precio_local * multi))

    max_por_dinero = npc["dinero"] // precio_unitario
    if max_por_dinero <= 0:
        limpiar(); titulo("VENDER")
        narrar(f"{npc['nombre']} no tiene dinero suficiente.")
        print(f"  {C.DIM}Precio por unidad: {precio_unitario} monedas{C.RESET}")
        print(f"  {C.DIM}Dinero de {npc['nombre']}: {npc['dinero']} monedas{C.RESET}")
        pausa()
        return

    cantidad_vendible = min(cantidad, max_por_dinero)
    total = precio_unitario * cantidad_vendible

    def contexto_confirmar():
        titulo("CONFIRMAR VENTA")
        print(f"  {C.BOLD}Producto:{C.RESET}          {producto}")
        print(f"  {C.BOLD}Vendedor:{C.RESET}          {npc['nombre']}")
        print(f"  {C.BOLD}Precio local:{C.RESET}      {precio_local} monedas")
        print(f"  {C.BOLD}Cantidad:{C.RESET}          {cantidad_vendible} de {cantidad}")
        print(f"  {C.BOLD}Precio por unidad:{C.RESET} {C.YELLOW}{precio_unitario}{C.RESET} monedas")
        print(f"  {C.BOLD}Total a recibir:{C.RESET}   {C.GREEN}{total}{C.RESET} monedas")
        print()
        print(f"  {C.DIM}Motivo del precio: {razon}{C.RESET}")
        if cantidad_vendible < cantidad:
            print(f"  {C.DIM}(Solo te compra {cantidad_vendible} porque no le alcanza el dinero){C.RESET}")
        print()
        print(f"  {C.DIM}¿Confirmas la venta?{C.RESET}")

    if menu_flechas([("Confirmar venta", ""), ("Cancelar", "")],
                     contexto_fn=contexto_confirmar, permitir_cancelar=False) == 1:
        return

    jugador["dinero"] += total
    npc["dinero"] -= total
    npc["inventario"][producto] = npc["inventario"].get(producto, 0) + cantidad_vendible

    if cantidad_vendible >= cantidad:
        jugador["inventario"].pop(idx)
    else:
        restante = cantidad - cantidad_vendible
        jugador["inventario"][idx] = f"{restante}x {producto}"

    if total >= 20:
        modificar_reputacion(conn, jugador["identificador"], ciudad, 1, "venta")

    from venefar_jugador import guardar_jugador
    from venefar_npc import guardar_npc
    guardar_jugador(conn, jugador)
    guardar_npc(conn, npc)

    limpiar(); titulo("VENTA REALIZADA")
    narrar(f"Vendes {cantidad_vendible} de {producto} a {npc['nombre']}.")
    narrar(f"Recibes {total} monedas.")
    print(f"  {C.GREEN}Dinero actual:{C.RESET} {jugador['dinero']} monedas")
    pausa()


def auto_venta_emergencia(conn, jugador, npcs):
    if jugador["dinero"] > 3: return False
    if jugador["hambre"] > 20 and jugador["sed"] > 20: return False
    if not jugador["inventario"]: return False

    ciudad = jugador.get("ciudad", "capital_imperial")
    npcs_ciudad = [n for n in npcs if n.get("ciudad") == ciudad and n["dinero"] > 5]
    if not npcs_ciudad: return False

    for i, item in enumerate(jugador["inventario"]):
        producto = _limpiar_nombre_producto(item)
        if producto not in PRODUCTOS: continue
        cantidad = 1
        if "x " in item:
            try: cantidad = int(item.split("x ", 1)[0])
            except Exception: cantidad = 1
        precio_local = precio_actual(conn, producto, ciudad=ciudad)
        precio = max(1, int(precio_local * 0.5))
        npc = random.choice(npcs_ciudad)
        if npc["dinero"] < precio: continue

        npc["dinero"] -= precio
        npc["inventario"][producto] = npc["inventario"].get(producto, 0) + 1
        jugador["dinero"] += precio
        if cantidad > 1:
            jugador["inventario"][i] = f"{cantidad - 1}x {producto}"
        else:
            jugador["inventario"].pop(i)

        from venefar_jugador import guardar_jugador
        from venefar_npc import guardar_npc
        guardar_jugador(conn, jugador)
        guardar_npc(conn, npc)
        return True
    return False