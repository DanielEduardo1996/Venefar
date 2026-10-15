# -*- coding: utf-8 -*-
"""VENEFAR - Propiedades (casas, cofre, negocios)"""
from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from descripciones.ciudades import obtener_nombre, CIUDADES
from venefar_reputacion import obtener_reputacion, etiqueta_reputacion
from venefar_inventario import menu_inventario_agrupado, nombre_bonito_item


PRECIO_BASE_CASA = 600
MULTIPLICADOR_CIUDAD = {
    "capital_imperial": 3.0, "puerto_sal": 2.5, "villareal": 2.5, "santamera": 2.0,
    "piedrahonda": 1.3, "villafria": 1.0, "robledal": 1.1, "canterral": 1.2,
    "mareas": 1.0, "ermita_alta": 0.7, "calas": 0.6, "fresnillo": 0.8,
}
REPUTACION_MINIMA = -20
CAPACIDAD_COFRE = 500


def precio_casa(ciudad):
    multi = MULTIPLICADOR_CIUDAD.get(ciudad, 1.0)
    return int(PRECIO_BASE_CASA * multi)


def tiene_casa(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM propiedades WHERE jugador_id=? AND ciudad=? AND tipo='casa'",
              (jugador_id, ciudad))
    return c.fetchone()[0] > 0


def listar_propiedades(conn, jugador_id):
    c = conn.cursor()
    c.execute("SELECT * FROM propiedades WHERE jugador_id=? ORDER BY ciudad", (jugador_id,))
    return [dict(r) for r in c.fetchall()]


def contenido_cofre(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("SELECT producto, cantidad FROM cofre WHERE jugador_id=? AND ciudad=? ORDER BY producto",
              (jugador_id, ciudad))
    return [(r["producto"], r["cantidad"]) for r in c.fetchall()]


def espacio_cofre_ocupado(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("SELECT SUM(cantidad) FROM cofre WHERE jugador_id=? AND ciudad=?",
              (jugador_id, ciudad))
    return c.fetchone()[0] or 0


def guardar_en_cofre(conn, jugador_id, ciudad, producto, cantidad):
    if espacio_cofre_ocupado(conn, jugador_id, ciudad) + cantidad > CAPACIDAD_COFRE:
        return False
    c = conn.cursor()
    c.execute("""INSERT INTO cofre (jugador_id, ciudad, producto, cantidad) VALUES (?, ?, ?, ?)
                 ON CONFLICT(jugador_id, ciudad, producto) DO UPDATE SET cantidad = cantidad + excluded.cantidad""",
              (jugador_id, ciudad, producto, cantidad))
    conn.commit()
    return True


def sacar_de_cofre(conn, jugador_id, ciudad, producto, cantidad):
    c = conn.cursor()
    c.execute("SELECT cantidad FROM cofre WHERE jugador_id=? AND ciudad=? AND producto=?",
              (jugador_id, ciudad, producto))
    f = c.fetchone()
    if not f or f["cantidad"] < cantidad:
        return False
    c.execute("""UPDATE cofre SET cantidad = cantidad - ? WHERE jugador_id=? AND ciudad=? AND producto=?""",
              (cantidad, jugador_id, ciudad, producto))
    c.execute("DELETE FROM cofre WHERE jugador_id=? AND ciudad=? AND producto=? AND cantidad <= 0",
              (jugador_id, ciudad, producto))
    conn.commit()
    return True


def menu_propiedades(conn, jugador, mundo):
    from venefar_negocios import menu_negocios
    while True:
        ciudad = jugador.get("ciudad", "capital_imperial")
        ciudad_nombre = obtener_nombre(ciudad)
        casas = listar_propiedades(conn, jugador["identificador"])
        tiene_aqui = tiene_casa(conn, jugador["identificador"], ciudad)

        def contexto():
            titulo(f"PROPIEDADES · {ciudad_nombre.upper()}")
            print(f"  Dinero: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
            if casas:
                print(f"  {C.DIM}Tienes {len(casas)} propiedad(es).{C.RESET}")
            else:
                print(f"  {C.DIM}No tienes ninguna propiedad todavia.{C.RESET}")

        items = [("Ver mis propiedades", f"{len(casas)} en total")]
        if not tiene_aqui:
            precio = precio_casa(ciudad)
            puede = jugador["dinero"] >= precio
            detalle = f"{precio} monedas" if puede else f"{precio} monedas - no alcanza"
            items.append((f"Comprar casa en {ciudad_nombre}", detalle))
        else:
            items.append(("Acceder al cofre",
                          f"{espacio_cofre_ocupado(conn, jugador['identificador'], ciudad)}/{CAPACIDAD_COFRE} unidades"))
        items.append(("Negocios", "Montar y gestionar negocios"))
        items.append(("Volver", ""))

        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)

        if idx == 0:
            _ver_propiedades(conn, jugador)
        elif idx == 1:
            if not tiene_aqui:
                _comprar_casa(conn, jugador, ciudad)
            else:
                _menu_cofre(conn, jugador, ciudad)
        elif idx == 2:
            menu_negocios(conn, jugador, mundo)
        elif idx == 3:
            return


def _ver_propiedades(conn, jugador):
    limpiar(); titulo("MIS PROPIEDADES")
    props = listar_propiedades(conn, jugador["identificador"])
    if not props:
        narrar("No tienes ninguna propiedad.")
        pausa(); return
    for p in props:
        tipo = p["tipo"].capitalize()
        nombre = obtener_nombre(p["ciudad"])
        nivel = p.get("nivel", 1)
        print(f"  {C.BOLD}{tipo}{C.RESET} en {C.CYAN}{nombre}{C.RESET}  {C.DIM}(nivel {nivel}){C.RESET}")
    print()
    pausa()


def _comprar_casa(conn, jugador, ciudad):
    precio = precio_casa(ciudad)
    rep = obtener_reputacion(conn, jugador["identificador"], ciudad)
    etq, col = etiqueta_reputacion(rep)
    ciudad_nombre = obtener_nombre(ciudad)
    limpiar(); titulo(f"COMPRAR CASA EN {ciudad_nombre.upper()}")
    print(f"  {C.DIM}Una casa modesta en esta ciudad te daria:{C.RESET}")
    print(f"    - Un lugar donde dormir mejor")
    print(f"    - Un cofre para guardar hasta {CAPACIDAD_COFRE} objetos")
    print(f"    - La base para montar un negocio")
    print()
    print(f"  Precio:           {C.YELLOW}{precio}{C.RESET} monedas")
    print(f"  Tu dinero:        {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
    print(f"  Reputacion aqui:  {col}{etq}{C.RESET} ({rep})")
    print()
    if rep < REPUTACION_MINIMA:
        narrar(f"{C.RED}Tu reputacion es demasiado baja."); pausa(); return
    if jugador["dinero"] < precio:
        narrar(f"{C.RED}No tienes suficiente dinero."); pausa(); return
    confirm = menu_flechas([("Comprar casa", f"{precio} monedas"), ("Cancelar", "")],
                            contexto_fn=lambda: None, permitir_cancelar=False)
    if confirm == 1: return
    c = conn.cursor()
    c.execute("""INSERT INTO propiedades (jugador_id, ciudad, tipo, nivel)
                 VALUES (?, ?, 'casa', 1)""",
              (jugador["identificador"], ciudad))
    conn.commit()
    jugador["dinero"] -= precio
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("¡CASA COMPRADA!")
    narrar(f"Ahora tienes una casa en {ciudad_nombre}.")
    print(f"  {C.GREEN}Dinero actual:{C.RESET} {jugador['dinero']} monedas")
    pausa()


def _menu_cofre(conn, jugador, ciudad):
    jugador_id = jugador["identificador"]
    while True:
        ocupado = espacio_cofre_ocupado(conn, jugador_id, ciudad)
        def contexto():
            titulo(f"COFRE DE {obtener_nombre(ciudad).upper()}")
            print(f"  Espacio: {ocupado}/{CAPACIDAD_COFRE} unidades")
        items = [
            ("Guardar objeto del inventario", ""),
            ("Sacar objeto del cofre", ""),
            ("Ver contenido del cofre", ""),
            ("Volver", ""),
        ]
        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        if idx == 0:
            _guardar_en_cofre(conn, jugador, ciudad)
        elif idx == 1:
            _sacar_del_cofre(conn, jugador, ciudad)
        elif idx == 2:
            _ver_cofre(conn, jugador, ciudad)
        elif idx == 3:
            return


def _guardar_en_cofre(conn, jugador, ciudad):
    if not jugador["inventario"]:
        limpiar(); titulo("GUARDAR EN COFRE")
        narrar("No llevas nada.")
        pausa(); return
    idx = menu_inventario_agrupado(jugador["inventario"],
                                    contexto_fn=lambda: titulo("GUARDAR - ELIGE OBJETO"),
                                    permitir_cancelar=True)
    if idx == -1: return
    item = jugador["inventario"][idx]
    prod = item.split("x ", 1)[1] if "x " in item else item
    cant = 1
    if "x " in item:
        try: cant = int(item.split("x ", 1)[0])
        except Exception: cant = 1
    ok = guardar_en_cofre(conn, jugador["identificador"], ciudad, prod, cant)
    if not ok:
        limpiar(); titulo("COFRE LLENO")
        narrar(f"No cabe todo en el cofre.")
        pausa(); return
    jugador["inventario"].pop(idx)
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("GUARDADO")
    narrar(f"Guardas {cant} de {nombre_bonito_item(prod)} en el cofre.")
    pausa()


def _sacar_del_cofre(conn, jugador, ciudad):
    contenido = contenido_cofre(conn, jugador["identificador"], ciudad)
    if not contenido:
        limpiar(); titulo("SACAR DEL COFRE")
        narrar("El cofre esta vacio.")
        pausa(); return
    items = [(nombre_bonito_item(prod), f"{cant} unidades") for prod, cant in contenido]
    idx = menu_flechas(items, contexto_fn=lambda: titulo("SACAR - ELIGE OBJETO"),
                        permitir_cancelar=True)
    if idx == -1: return
    prod, cant_total = contenido[idx]
    print(f"\n¿Cuantas unidades? (max {cant_total})")
    cant = pedir_numero(cant_total)
    if sacar_de_cofre(conn, jugador["identificador"], ciudad, prod, cant):
        if cant > 1:
            jugador["inventario"].append(f"{cant}x {prod}")
        else:
            jugador["inventario"].append(prod)
        from venefar_jugador import guardar_jugador
        guardar_jugador(conn, jugador)
        limpiar(); titulo("RETIRADO")
        narrar(f"Sacas {cant} de {nombre_bonito_item(prod)} del cofre.")
    else:
        limpiar(); titulo("ERROR"); narrar("No se pudo retirar.")
    pausa()


def _ver_cofre(conn, jugador, ciudad):
    contenido = contenido_cofre(conn, jugador["identificador"], ciudad)
    limpiar(); titulo(f"COFRE EN {obtener_nombre(ciudad).upper()}")
    if not contenido:
        narrar("El cofre esta vacio.")
    else:
        for prod, cant in contenido:
            print(f"  {nombre_bonito_item(prod)}: {cant} unidades")
        print()
        print(f"  {C.DIM}Espacio usado: {espacio_cofre_ocupado(conn, jugador['identificador'], ciudad)}/{CAPACIDAD_COFRE}{C.RESET}")
    pausa()