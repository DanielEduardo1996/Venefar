# -*- coding: utf-8 -*-
"""VENEFAR - Guarniciones"""
import random

from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from descripciones.ciudades import obtener_nombre
from venefar_items import obtener_item, es_item_equipable
from venefar_economia import precio_actual
from venefar_inventario import nombre_bonito_item


SOLDADOS_POR_CIUDAD = {
    "capital_imperial": 200, "puerto_sal": 100, "villareal": 150, "santamera": 500,
    "piedrahonda": 30, "villafria": 25, "robledal": 20, "canterral": 40,
    "mareas": 20, "ermita_alta": 10, "calas": 8, "fresnillo": 10,
}

DIAS_ENTRE_REVISIONES = 60
PCT_DESGASTE = 0.10
PREMIO_COMPRA_LOCAL = 1.20
IMPUESTO_IMPORTACION = 1.15
MAX_PCT_IMPORTACION = 0.20

ARMAS_BUSCADAS = ["espada_corta", "hacha_mano", "lanza_corta", "daga"]
ARMADURAS_BUSCADAS = ["cota_malla", "yelmo", "tunica", "casco_cuero", "escudo_redondo"]


def init_guarniciones(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM guarniciones")
    if c.fetchone()[0] > 0: return
    for ciudad, soldados in SOLDADOS_POR_CIUDAD.items():
        c.execute("""INSERT INTO guarniciones
                     (ciudad, num_soldados, reservas_armas, reservas_armaduras, dia_ultima_revision)
                     VALUES (?, ?, ?, ?, 1)""",
                  (ciudad, soldados, soldados, soldados))
    conn.commit()


def obtener_guarnicion(conn, ciudad):
    c = conn.cursor()
    c.execute("SELECT * FROM guarniciones WHERE ciudad=?", (ciudad,))
    f = c.fetchone()
    return dict(f) if f else None


def listar_guarniciones(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM guarniciones ORDER BY num_soldados DESC")
    return [dict(r) for r in c.fetchall()]


def _buscar_locales(conn, ciudad, tipo_item, cantidad_necesaria):
    c = conn.cursor()
    c.execute("""SELECT n.id, n.nombre, n.dinero, i.producto, i.cantidad
                 FROM npcs n JOIN inventario i ON i.npc_id = n.id
                 WHERE n.ciudad=? AND n.oficio IN ('Herrero', 'Ballestero')
                 AND i.producto LIKE ?
                 ORDER BY i.cantidad DESC""", (ciudad, tipo_item + ":%"))
    filas = c.fetchall()
    encontrado = []
    total = 0
    for f in filas:
        if total >= cantidad_necesaria: break
        cant = min(f["cantidad"], cantidad_necesaria - total)
        encontrado.append({
            "npc_id": f["id"], "nombre": f["nombre"], "ciudad": ciudad,
            "item_id": f["producto"], "cantidad": cant,
        })
        total += cant
    return total, encontrado


def _buscar_importacion(conn, ciudad_excluida, tipo_item, cantidad_necesaria):
    c = conn.cursor()
    c.execute("""SELECT n.id, n.nombre, n.ciudad, i.producto, i.cantidad
                 FROM npcs n JOIN inventario i ON i.npc_id = n.id
                 WHERE n.ciudad != ? AND n.oficio IN ('Herrero', 'Ballestero')
                 AND i.producto LIKE ?
                 ORDER BY i.cantidad DESC""", (ciudad_excluida, tipo_item + ":%"))
    filas = c.fetchall()
    encontrado = []
    total = 0
    for f in filas:
        if total >= cantidad_necesaria: break
        cant = min(f["cantidad"], cantidad_necesaria - total)
        encontrado.append({
            "npc_id": f["id"], "nombre": f["nombre"], "ciudad": f["ciudad"],
            "item_id": f["producto"], "cantidad": cant,
        })
        total += cant
    return total, encontrado


def _aplicar_compra(conn, npcs, entrada, cant, total, comprador_nombre, dia, es_importacion):
    """
    Aplica compra. Ahora NO genera evento individual (solo resumen).
    """
    npc_mem = None
    for n in npcs:
        if n["id"] == entrada["npc_id"]:
            npc_mem = n
            break
    if npc_mem is None: return False
    item_id = entrada["item_id"]
    if npc_mem["inventario"].get(item_id, 0) < cant: return False
    # Actualizar memoria
    npc_mem["inventario"][item_id] -= cant
    if npc_mem["inventario"][item_id] <= 0:
        del npc_mem["inventario"][item_id]
    npc_mem["dinero"] += total
    # Actualizar BD
    c = conn.cursor()
    c.execute("SELECT cantidad FROM inventario WHERE npc_id=? AND producto=?",
              (entrada["npc_id"], item_id))
    fila = c.fetchone()
    if fila:
        nueva_cant = fila["cantidad"] - cant
        if nueva_cant > 0:
            c.execute("UPDATE inventario SET cantidad=? WHERE npc_id=? AND producto=?",
                      (nueva_cant, entrada["npc_id"], item_id))
        else:
            c.execute("DELETE FROM inventario WHERE npc_id=? AND producto=?",
                      (entrada["npc_id"], item_id))
    c.execute("UPDATE npcs SET dinero = dinero + ? WHERE id=?", (total, entrada["npc_id"]))
    # Registrar SOLO en transacciones (NO en eventos)
    item = obtener_item(item_id)
    nombre_bonito = item["nombre"] if item else item_id
    c.execute("""INSERT INTO transacciones
                 (dia, comprador, vendedor, producto, cantidad, precio_total)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (dia, comprador_nombre, entrada["nombre"], nombre_bonito, cant, total))
    conn.commit()
    return True


def _comprar_de_herreros(conn, npcs, guarnicion, encontrado, es_importacion, dia):
    ciudad_guarnicion = guarnicion["ciudad"]
    coste_total = 0
    cantidad_total = 0
    comprador_nombre = f"Guarnicion de {obtener_nombre(ciudad_guarnicion)}"
    for entrada in encontrado:
        item = obtener_item(entrada["item_id"])
        if not item: continue
        precio_base = item["precio"]
        if es_importacion:
            precio_unit = int(precio_base * PREMIO_COMPRA_LOCAL * IMPUESTO_IMPORTACION)
        else:
            precio_unit = int(precio_base * PREMIO_COMPRA_LOCAL)
        cant = entrada["cantidad"]
        total = precio_unit * cant
        if _aplicar_compra(conn, npcs, entrada, cant, total, comprador_nombre, dia, es_importacion):
            coste_total += total
            cantidad_total += cant
    return coste_total, cantidad_total


def revisar_guarnicion(conn, npcs, ciudad, dia, forzar=False):
    g = obtener_guarnicion(conn, ciudad)
    if not g: return None
    if not forzar:
        if dia - g["dia_ultima_revision"] < DIAS_ENTRE_REVISIONES:
            return None
    soldados = g["num_soldados"]
    armas_actuales = g["reservas_armas"]
    armaduras_actuales = g["reservas_armaduras"]
    armas_necesarias = max(0, soldados - armas_actuales)
    armaduras_necesarias = max(0, soldados - armaduras_actuales)
    desgaste_armas = int(soldados * PCT_DESGASTE)
    desgaste_armaduras = int(soldados * PCT_DESGASTE)
    total_armas = armas_necesarias + desgaste_armas
    total_armaduras = armaduras_necesarias + desgaste_armaduras
    if total_armas <= 0 and total_armaduras <= 0:
        c = conn.cursor()
        c.execute("UPDATE guarniciones SET dia_ultima_revision=? WHERE ciudad=?", (dia, ciudad))
        conn.commit()
        return None

    nuevas_reservas_armas = max(0, armas_actuales - desgaste_armas)
    nuevas_reservas_armaduras = max(0, armaduras_actuales - desgaste_armaduras)

    # Armas: local primero, luego importacion
    compradas_local_a = 0
    importadas_a = 0
    if total_armas > 0:
        restante = total_armas
        for tipo in ARMAS_BUSCADAS:
            if restante <= 0: break
            n, encontrados = _buscar_locales(conn, ciudad, tipo, restante)
            if n > 0:
                coste, cant = _comprar_de_herreros(conn, npcs, g, encontrados, False, dia)
                compradas_local_a += cant
                restante -= cant
        if restante > 0:
            max_import = int(total_armas * MAX_PCT_IMPORTACION)
            a_import = min(restante, max_import)
            for tipo in ARMAS_BUSCADAS:
                if a_import <= 0: break
                n, encontrados = _buscar_importacion(conn, ciudad, tipo, a_import)
                if n > 0:
                    coste, cant = _comprar_de_herreros(conn, npcs, g, encontrados, True, dia)
                    importadas_a += cant
                    a_import -= cant
        nuevas_reservas_armas += compradas_local_a + importadas_a

    # Armaduras
    compradas_local_d = 0
    importadas_d = 0
    if total_armaduras > 0:
        restante = total_armaduras
        for tipo in ARMADURAS_BUSCADAS:
            if restante <= 0: break
            n, encontrados = _buscar_locales(conn, ciudad, tipo, restante)
            if n > 0:
                coste, cant = _comprar_de_herreros(conn, npcs, g, encontrados, False, dia)
                compradas_local_d += cant
                restante -= cant
        if restante > 0:
            max_import = int(total_armaduras * MAX_PCT_IMPORTACION)
            a_import = min(restante, max_import)
            for tipo in ARMADURAS_BUSCADAS:
                if a_import <= 0: break
                n, encontrados = _buscar_importacion(conn, ciudad, tipo, a_import)
                if n > 0:
                    coste, cant = _comprar_de_herreros(conn, npcs, g, encontrados, True, dia)
                    importadas_d += cant
                    a_import -= cant
        nuevas_reservas_armaduras += compradas_local_d + importadas_d

    # Actualizar guarnicion
    c = conn.cursor()
    c.execute("""UPDATE guarniciones SET reservas_armas=?, reservas_armaduras=?,
                 dia_ultima_revision=?, dia_ultima_importacion=?
                 WHERE ciudad=?""",
              (nuevas_reservas_armas, nuevas_reservas_armaduras, dia,
               dia if (importadas_a + importadas_d) > 0 else g["dia_ultima_importacion"],
               ciudad))
    # UN SOLO evento resumen
    partes = []
    if compradas_local_a > 0 or compradas_local_d > 0:
        partes.append(f"{compradas_local_a} armas + {compradas_local_d} armaduras locales")
    if importadas_a > 0 or importadas_d > 0:
        partes.append(f"{importadas_a} armas + {importadas_d} armaduras importadas")
    if partes:
        desc = f"Guarnicion de {obtener_nombre(ciudad)}: " + " y ".join(partes) + "."
        c.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)",
                  (dia, "guarnicion", desc))
    conn.commit()
    return {
        "armas_compradas_local": compradas_local_a, "armas_importadas": importadas_a,
        "armaduras_compradas_local": compradas_local_d, "armaduras_importadas": importadas_d,
    }


def procesar_guarniciones_dia(conn, npcs, dia):
    for ciudad in SOLDADOS_POR_CIUDAD.keys():
        revisar_guarnicion(conn, npcs, ciudad, dia)


def menu_guarnicion(conn, jugador, mundo):
    ciudad = jugador.get("ciudad", "capital_imperial")
    g = obtener_guarnicion(conn, ciudad)
    if not g:
        limpiar(); titulo("GUARNICION"); narrar("En esta ciudad no hay guarnicion."); pausa(); return
    ciudad_nombre = obtener_nombre(ciudad)
    while True:
        soldados = g["num_soldados"]
        armas = g["reservas_armas"]
        armaduras = g["reservas_armaduras"]
        faltan_armas = max(0, soldados - armas)
        faltan_armaduras = max(0, soldados - armaduras)
        def contexto():
            titulo(f"GUARNICION DE {ciudad_nombre.upper()}")
            print(f"  Soldados: {soldados}")
            print(f"  Reservas de armas:     {C.CYAN}{armas}{C.RESET}")
            print(f"  Reservas de armaduras: {C.CYAN}{armaduras}{C.RESET}")
            if faltan_armas > 0 or faltan_armaduras > 0:
                print(f"  {C.RED}Faltan: {faltan_armas} armas, {faltan_armaduras} armaduras{C.RESET}")
            else:
                print(f"  {C.GREEN}Guarnicion completamente equipada.{C.RESET}")
            print()
            print(f"  {C.DIM}La guarnicion paga 20% por encima del precio de mercado.{C.RESET}")
        items = [("Vender armas a la guarnicion", "Precio premium"),
                 ("Vender armaduras a la guarnicion", "Precio premium"),
                 ("Volver", "")]
        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        if idx == 0: _vender_a_guarnicion(conn, jugador, g, "arma")
        elif idx == 1: _vender_a_guarnicion(conn, jugador, g, "armadura")
        elif idx == 2: return


def _vender_a_guarnicion(conn, jugador, guarnicion, categoria):
    ciudad = guarnicion["ciudad"]
    ciudad_nombre = obtener_nombre(ciudad)
    candidatos = []
    for i, item in enumerate(jugador["inventario"]):
        item_id = item.split("x ", 1)[1] if "x " in item else item
        if not es_item_equipable(item_id): continue
        item_data = obtener_item(item_id)
        if not item_data: continue
        tipo, _ = item_id.split(":", 1)
        if categoria == "arma" and tipo in ARMAS_BUSCADAS:
            candidatos.append((i, item_id, item_data))
        elif categoria == "armadura" and tipo in ARMADURAS_BUSCADAS:
            candidatos.append((i, item_id, item_data))
    if not candidatos:
        limpiar(); titulo(f"VENDER {categoria.upper()}S A LA GUARNICION")
        narrar(f"No tienes {categoria}s que la guarnicion necesite.")
        pausa(); return
    def contexto():
        titulo(f"VENDER {categoria.upper()}S A {ciudad_nombre.upper()}")
        print(f"  {C.DIM}La guarnicion paga 20% mas que el mercado normal.{C.RESET}")
    items_menu = []
    for _, item_id, item in candidatos:
        precio = int(item["precio"] * PREMIO_COMPRA_LOCAL)
        items_menu.append((item["nombre"], f"Te pagaran {precio} monedas"))
    idx = menu_flechas(items_menu, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    idx_inv, item_id, item_data = candidatos[idx]
    item = jugador["inventario"][idx_inv]
    cant = 1
    if "x " in item:
        try: cant = int(item.split("x ", 1)[0])
        except Exception: cant = 1
    precio_u = int(item_data["precio"] * PREMIO_COMPRA_LOCAL)
    if categoria == "arma":
        faltan = max(0, guarnicion["num_soldados"] - guarnicion["reservas_armas"])
    else:
        faltan = max(0, guarnicion["num_soldados"] - guarnicion["reservas_armaduras"])
    cant_max = min(cant, faltan) if faltan > 0 else cant
    if cant_max <= 0:
        limpiar(); titulo("GUARNICION")
        narrar("La guarnicion ya tiene suficiente equipo.")
        pausa(); return
    total = precio_u * cant_max
    def contexto_confirmar():
        titulo("CONFIRMAR VENTA A LA GUARNICION")
        print(f"  {C.BOLD}Item:{C.RESET}         {item_data['nombre']}")
        print(f"  {C.BOLD}Categoria:{C.RESET}    {categoria.capitalize()}")
        print(f"  {C.BOLD}Cantidad:{C.RESET}     {cant_max} de {cant}")
        print(f"  {C.BOLD}Precio/u:{C.RESET}     {C.YELLOW}{precio_u}{C.RESET} monedas")
        print(f"  {C.BOLD}Total:{C.RESET}        {C.GREEN}{total}{C.RESET} monedas")
        print()
        print(f"  {C.DIM}¿Confirmas la venta?{C.RESET}")
    if menu_flechas([("Confirmar venta", ""), ("Cancelar", "")],
                     contexto_fn=contexto_confirmar, permitir_cancelar=False) == 1: return
    jugador["dinero"] += total
    if cant_max >= cant: jugador["inventario"].pop(idx_inv)
    else: jugador["inventario"][idx_inv] = f"{cant - cant_max}x {item_id}"
    c = conn.cursor()
    if categoria == "arma":
        c.execute("UPDATE guarniciones SET reservas_armas = reservas_armas + ? WHERE ciudad=?", (cant_max, ciudad))
    else:
        c.execute("UPDATE guarniciones SET reservas_armaduras = reservas_armaduras + ? WHERE ciudad=?", (cant_max, ciudad))
    c.execute("""INSERT INTO transacciones (dia, comprador, vendedor, producto, cantidad, precio_total)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (mundo_dia_actual(conn), f"Guarnicion de {ciudad_nombre}", jugador["nombre"],
               item_data["nombre"], cant_max, total))
    conn.commit()
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("VENTA REALIZADA")
    narrar(f"Vendes {cant_max} de {item_data['nombre']} a la guarnicion.")
    narrar(f"Recibes {total} monedas.")
    print(f"  {C.GREEN}Dinero actual:{C.RESET} {jugador['dinero']} monedas")
    pausa()


def mundo_dia_actual(conn):
    c = conn.cursor()
    c.execute("SELECT dia FROM mundo WHERE id=1")
    f = c.fetchone()
    return f["dia"] if f else 1