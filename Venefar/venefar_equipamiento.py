# -*- coding: utf-8 -*-
"""VENEFAR - Sistema de equipamiento
Menu para equipar, desequipar y ver stats.
"""
from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from venefar_items import (SLOTS, NOMBRES_SLOT, obtener_item, es_item_equipable,
                           parsear_item_id, calcular_stats_jugador)


def obtener_equipado(conn, jugador_id):
    """Devuelve dict {slot: item_id} de lo que lleva equipado."""
    c = conn.cursor()
    c.execute("SELECT slot, item_id FROM equipado WHERE jugador_id=?", (jugador_id,))
    return {r["slot"]: r["item_id"] for r in c.fetchall()}


def equipar(conn, jugador_id, slot, item_id):
    c = conn.cursor()
    c.execute("""INSERT INTO equipado (jugador_id, slot, item_id) VALUES (?, ?, ?)
                 ON CONFLICT(jugador_id, slot) DO UPDATE SET item_id=excluded.item_id""",
              (jugador_id, slot, item_id))
    conn.commit()


def desequipar(conn, jugador_id, slot):
    c = conn.cursor()
    c.execute("DELETE FROM equipado WHERE jugador_id=? AND slot=?", (jugador_id, slot))
    conn.commit()


def listar_items_equipables_del_inventario(inventario):
    """Devuelve lista de (item_id, indice_en_inventario) de items equipables."""
    resultado = []
    for i, item in enumerate(inventario):
        # Extraer item_id si es formato 'Nx item_id'
        item_id = item
        if "x " in item:
            item_id = item.split("x ", 1)[1]
        if es_item_equipable(item_id):
            resultado.append((item_id, i))
    return resultado


def menu_equipamiento(conn, jugador):
    jugador_id = jugador["identificador"]

    while True:
        equipado = obtener_equipado(conn, jugador_id)
        stats = calcular_stats_jugador(equipado)

        def contexto():
            titulo("EQUIPAMIENTO")
            print(f"  {C.BOLD}Estadisticas derivadas:{C.RESET}")
            print(f"    Defensa total:    {C.CYAN}{stats['defensa_total']}{C.RESET}")
            if stats['dano_min'] > 0:
                print(f"    Dano del arma:    {C.RED}{stats['dano_min']}-{stats['dano_max']}{C.RESET}")
            else:
                print(f"    Dano del arma:    {C.DIM}(sin arma equipada){C.RESET}")
            print(f"    Peso equipado:    {stats['peso_total']:.1f} kg")
            if stats['penal_vision'] != 0:
                print(f"    Penal. vision:    {stats['penal_vision']}")
            if stats['penal_vel'] != 0:
                print(f"    Penal. velocidad: {stats['penal_vel']}")
            if stats['carisma'] != 0:
                print(f"    Carisma:          +{stats['carisma']}")
            if stats['voluntad'] != 0:
                print(f"    Voluntad:         +{stats['voluntad']}")
            if stats['reputacion'] != 0:
                print(f"    Reputacion:       +{stats['reputacion']}")
            print()
            print(f"  {C.BOLD}Slots de equipo:{C.RESET}")

        # Menu de slots
        items = []
        for slot_id, slot_nombre in SLOTS:
            item_actual = equipado.get(slot_id)
            if item_actual:
                item = obtener_item(item_actual)
                if item:
                    texto = item["nombre"]
                    detalle = item_actual
                else:
                    texto = item_actual
                    detalle = "(desconocido)"
            else:
                texto = f"(vacio)"
                detalle = ""
            items.append((f"{slot_nombre}", texto))
        items.append(("Volver", ""))
        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)

        if idx == len(SLOTS):
            return

        slot_id, slot_nombre = SLOTS[idx]
        _menu_slot(conn, jugador, slot_id, slot_nombre)


def _menu_slot(conn, jugador, slot_id, slot_nombre):
    jugador_id = jugador["identificador"]
    equipado = obtener_equipado(conn, jugador_id)
    item_actual = equipado.get(slot_id)

    while True:
        def contexto():
            titulo(f"SLOT: {slot_nombre.upper()}")
            if item_actual:
                item = obtener_item(item_actual)
                if item:
                    print(f"  {C.BOLD}Equipado:{C.RESET} {item['nombre']}")
                    if item["tipo"] == "arma":
                        print(f"    Dano: {item['dano_min']}-{item['dano_max']}")
                    else:
                        print(f"    Defensa: {item['defensa']}")
                    print(f"    Peso: {item['peso']} kg")
                    print(f"    Valor: {item['precio']} monedas")
            else:
                print(f"  {C.DIM}(vacio){C.RESET}")

        items = []
        claves = []

        if item_actual:
            items.append(("Desequipar", f"Guardar en inventario"))
            claves.append(("desequipar", None))

        items.append(("Equipar algo del inventario", ""))
        claves.append(("equipar", None))

        items.append(("Volver", ""))
        claves.append(("volver", None))

        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        acc = claves[idx][0]

        if acc == "volver":
            return
        elif acc == "desequipar":
            jugador["inventario"].append(item_actual)
            desequipar(conn, jugador_id, slot_id)
            from venefar_jugador import guardar_jugador
            guardar_jugador(conn, jugador)
            limpiar(); titulo("DESEQUIPADO")
            narrar(f"Guardas {item_actual} en el inventario.")
            pausa()
            return
        elif acc == "equipar":
            _elegir_item_para_slot(conn, jugador, slot_id, slot_nombre)


def _elegir_item_para_slot(conn, jugador, slot_id, slot_nombre):
    """Muestra los items del inventario que se pueden equipar en el slot."""
    equipables = listar_items_equipables_del_inventario(jugador["inventario"])
    validos = []
    for item_id, idx_inv in equipables:
        item = obtener_item(item_id)
        if item and item["slot"] == slot_id:
            validos.append((item_id, idx_inv, item))

    if not validos:
        limpiar(); titulo(f"EQUIPAR EN {slot_nombre.upper()}")
        narrar("No tienes nada que se pueda equipar en este slot.")
        pausa(); return

    def contexto():
        titulo(f"EQUIPAR EN {slot_nombre.upper()}")

    items = []
    for item_id, idx_inv, item in validos:
        detalle = ""
        if item["tipo"] == "arma":
            detalle = f"Dano {item['dano_min']}-{item['dano_max']}"
        else:
            detalle = f"Defensa {item['defensa']}"
        items.append((item["nombre"], detalle))

    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return

    item_id, idx_inv, item = validos[idx]

    # Si ya hay algo equipado, va al inventario
    equipado = obtener_equipado(conn, jugador["identificador"])
    item_anterior = equipado.get(slot_id)

    # Quitar del inventario
    jugador["inventario"].pop(idx_inv)
    if item_anterior:
        jugador["inventario"].append(item_anterior)

    equipar(conn, jugador["identificador"], slot_id, item_id)

    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)

    limpiar(); titulo("EQUIPADO")
    narrar(f"Te equipas {item['nombre']}.")
    if item_anterior:
        narrar(f"Guardas {item_anterior} en el inventario.")
    pausa()


def dar_item_inicial(conn, jugador, item_id):
    """Utilidad: añade un item al inventario del jugador si no lo tiene."""
    if item_id not in jugador["inventario"]:
        jugador["inventario"].append(item_id)
        return True
    return False