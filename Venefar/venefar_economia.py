# -*- coding: utf-8 -*-
"""VENEFAR - Modulo Economia"""
import random


PRODUCTOS = {
    "Trigo": {"base": 5, "cat": "materia"}, "Cebada": {"base": 4, "cat": "materia"},
    "Verduras": {"base": 3, "cat": "materia"}, "Uva": {"base": 6, "cat": "materia"},
    "Hierbas": {"base": 4, "cat": "materia"}, "Mineral": {"base": 8, "cat": "materia"},
    "Hierro": {"base": 16, "cat": "elaborado"}, "Carbón": {"base": 6, "cat": "materia"},
    "Piedra": {"base": 5, "cat": "materia"}, "Madera": {"base": 10, "cat": "materia"},
    "Leña": {"base": 4, "cat": "materia"}, "Lana": {"base": 6, "cat": "materia"},
    "Cuero crudo": {"base": 5, "cat": "materia"}, "Cuero": {"base": 12, "cat": "elaborado"},
    "Tela": {"base": 10, "cat": "elaborado"}, "Pescado": {"base": 4, "cat": "materia"},
    "Carne": {"base": 7, "cat": "materia"}, "Leche": {"base": 3, "cat": "materia"},
    "Agua": {"base": 1, "cat": "materia"}, "Pienso": {"base": 3, "cat": "materia"},
    "Sal": {"base": 3, "cat": "materia"}, "Harina": {"base": 8, "cat": "elaborado"},
    "Pan": {"base": 3, "cat": "elaborado"}, "Cerveza": {"base": 6, "cat": "elaborado"},
    "Vino": {"base": 8, "cat": "elaborado"}, "Herramientas": {"base": 25, "cat": "elaborado"},
    "Picos": {"base": 22, "cat": "elaborado"}, "Hachas": {"base": 20, "cat": "elaborado"},
    "Muebles": {"base": 30, "cat": "elaborado"}, "Tablones": {"base": 15, "cat": "elaborado"},
    "Redes": {"base": 10, "cat": "elaborado"}, "Barcas": {"base": 100, "cat": "elaborado"},
    "Carros": {"base": 80, "cat": "elaborado"}, "Ropa": {"base": 18, "cat": "elaborado"},
    "Remedios": {"base": 12, "cat": "elaborado"}, "Medicinas": {"base": 20, "cat": "elaborado"},
    "Bendiciones": {"base": 8, "cat": "servicio"}, "Pociones": {"base": 25, "cat": "elaborado"},
    "Venenos": {"base": 30, "cat": "elaborado"}, "Documentos": {"base": 15, "cat": "servicio"},
    "Cartas": {"base": 5, "cat": "servicio"}, "Comida cocinada": {"base": 6, "cat": "elaborado"},
    "Pieles": {"base": 8, "cat": "materia"}, "Piel trabajada": {"base": 20, "cat": "elaborado"},
    "Flechas": {"base": 2, "cat": "elaborado"}, "Arcos": {"base": 35, "cat": "elaborado"},
    "Vasos": {"base": 12, "cat": "elaborado"}, "Ventanas": {"base": 40, "cat": "elaborado"},
    "Tapices": {"base": 60, "cat": "elaborado"}, "Botas": {"base": 25, "cat": "elaborado"},
    "Zapatos": {"base": 18, "cat": "elaborado"}, "Instrumentos": {"base": 45, "cat": "elaborado"},
    "Ballestas": {"base": 55, "cat": "elaborado"}, "Virotes": {"base": 3, "cat": "elaborado"},
    "Llaves": {"base": 20, "cat": "elaborado"}, "Cadenas": {"base": 25, "cat": "elaborado"},
    "Escobas": {"base": 3, "cat": "elaborado"}, "Mapas": {"base": 35, "cat": "elaborado"},
    "Provisiones": {"base": 10, "cat": "elaborado"}, "Carbon vegetal": {"base": 7, "cat": "materia"},
    "Arena": {"base": 4, "cat": "materia"}, "Tinta": {"base": 6, "cat": "materia"},
    "Papel": {"base": 5, "cat": "materia"}, "Servicios": {"base": 15, "cat": "servicio"},
}


RECETAS = {
    "Granjero": [{"produce": "Trigo", "consume": {}, "cantidad": 3}, {"produce": "Verduras", "consume": {}, "cantidad": 3}],
    "Ganadero": [{"produce": "Carne", "consume": {"Pienso": 1}, "cantidad": 2}, {"produce": "Cuero crudo", "consume": {}, "cantidad": 2}, {"produce": "Leche", "consume": {}, "cantidad": 3}],
    "Pescador": [{"produce": "Pescado", "consume": {}, "cantidad": 4}],
    "Leñador": [{"produce": "Madera", "consume": {}, "cantidad": 3}, {"produce": "Leña", "consume": {}, "cantidad": 3}],
    "Minero": [{"produce": "Mineral", "consume": {}, "cantidad": 3}, {"produce": "Carbón", "consume": {}, "cantidad": 2}, {"produce": "Piedra", "consume": {}, "cantidad": 3}],
    "Molinero": [{"produce": "Harina", "consume": {"Trigo": 2}, "cantidad": 3}],
    "Panadero": [{"produce": "Pan", "consume": {"Harina": 2, "Leña": 1}, "cantidad": 4}],
    "Cervecero": [{"produce": "Cerveza", "consume": {"Trigo": 1, "Agua": 1}, "cantidad": 3}],
    "Herrero": [
        {"produce": "Hierro", "consume": {"Mineral": 2, "Carbón": 1}, "cantidad": 1},
        {"produce": "espada_corta:hierro", "consume": {"Hierro": 2, "Madera": 1}, "cantidad": 1},
        {"produce": "hacha_mano:hierro", "consume": {"Hierro": 1, "Madera": 1}, "cantidad": 1},
        {"produce": "daga:hierro", "consume": {"Hierro": 1}, "cantidad": 1},
        {"produce": "yelmo:hierro", "consume": {"Hierro": 2}, "cantidad": 1},
        {"produce": "cota_malla:hierro", "consume": {"Hierro": 4, "Carbón": 1}, "cantidad": 1},
        {"produce": "Herramientas", "consume": {"Hierro": 1, "Carbón": 1}, "cantidad": 1},
        {"produce": "Picos", "consume": {"Hierro": 1, "Madera": 1}, "cantidad": 1},
        {"produce": "Hachas", "consume": {"Hierro": 1, "Madera": 1}, "cantidad": 1},
    ],
    "Carpintero": [{"produce": "Tablones", "consume": {"Madera": 2}, "cantidad": 2}, {"produce": "Muebles", "consume": {"Madera": 3, "Herramientas": 1}, "cantidad": 1}],
    "Sastre": [{"produce": "Tela", "consume": {"Lana": 2}, "cantidad": 2}, {"produce": "Ropa", "consume": {"Tela": 2, "Cuero": 1}, "cantidad": 1}],
    "Albañil": [],
    "Tabernero": [{"produce": "Comida cocinada", "consume": {"Pan": 1, "Carne": 1, "Verduras": 1}, "cantidad": 3}],
    "Comerciante": [], "Transportista": [],
    "Médico": [{"produce": "Remedios", "consume": {"Hierbas": 2}, "cantidad": 1}, {"produce": "Medicinas", "consume": {"Hierbas": 3, "Agua": 1}, "cantidad": 1}],
    "Guardia": [], "Administrador": [], "Sacerdote": [],
    "Alquimista": [{"produce": "Pociones", "consume": {"Hierbas": 3, "Agua": 1}, "cantidad": 1}, {"produce": "Venenos", "consume": {"Hierbas": 2, "Mineral": 1}, "cantidad": 1}],
    "Escriba": [{"produce": "Documentos", "consume": {"Papel": 2, "Tinta": 1}, "cantidad": 1}, {"produce": "Cartas", "consume": {"Papel": 1, "Tinta": 1}, "cantidad": 2}],
    "Cocinero": [{"produce": "Comida cocinada", "consume": {"Carne": 1, "Verduras": 1}, "cantidad": 3}],
    "Cazador": [{"produce": "Pieles", "consume": {}, "cantidad": 2}, {"produce": "Carne", "consume": {}, "cantidad": 2}],
    "Carpintero barcos": [{"produce": "Barcas", "consume": {"Madera": 8, "Tela": 2}, "cantidad": 1}, {"produce": "Redes", "consume": {"Tela": 1}, "cantidad": 2}, {"produce": "escudo_redondo:hierro", "consume": {"Madera": 4, "Hierro": 2}, "cantidad": 1}],
    "Vidriero": [{"produce": "Vasos", "consume": {"Arena": 2}, "cantidad": 3}, {"produce": "Ventanas", "consume": {"Arena": 4}, "cantidad": 1}],
    "Tejedor": [{"produce": "Tela", "consume": {"Lana": 2}, "cantidad": 2}, {"produce": "Tapices", "consume": {"Lana": 5, "Tela": 2}, "cantidad": 1}],
    "Zapatero": [{"produce": "botas_cuero:hierro", "consume": {"Cuero": 3}, "cantidad": 1}, {"produce": "zapatos:hierro", "consume": {"Cuero": 1}, "cantidad": 2}],
    "Sacamuelas": [], "Músico": [], "Soldado": [],
    "Ballestero": [{"produce": "ballesta_ligera:hierro", "consume": {"Madera": 4, "Hierro": 2, "Carbón": 1}, "cantidad": 1}, {"produce": "Virotes", "consume": {"Madera": 1, "Hierro": 1}, "cantidad": 5}],
    "Carcelero": [], "Barrendero": [], "Mensajero": [], "Explorador": [],
    "Salinero": [{"produce": "Sal", "consume": {"Agua": 3}, "cantidad": 4}],
    "Carbonero": [{"produce": "Carbon vegetal", "consume": {"Madera": 3}, "cantidad": 4}],
    "Peletero": [{"produce": "Cuero", "consume": {"Cuero crudo": 2}, "cantidad": 2}, {"produce": "Piel trabajada", "consume": {"Pieles": 2}, "cantidad": 1}, {"produce": "guantes_cuero:hierro", "consume": {"Cuero": 1}, "cantidad": 1}],
}


CONSUMO_DIARIO = {
    "Granjero": {"Pan": 1, "Cerveza": 1}, "Ganadero": {"Pan": 1, "Cerveza": 1, "Verduras": 1, "Pienso": 1},
    "Pescador": {"Pan": 1, "Cerveza": 1}, "Leñador": {"Pan": 1, "Cerveza": 1},
    "Minero": {"Pan": 1, "Cerveza": 1, "Carne": 1}, "Molinero": {"Pan": 1, "Cerveza": 1, "Trigo": 1},
    "Panadero": {"Carne": 1, "Cerveza": 1, "Harina": 1, "Leña": 1}, "Cervecero": {"Pan": 1, "Carne": 1, "Trigo": 1, "Agua": 1},
    "Herrero": {"Pan": 1, "Cerveza": 1, "Carne": 1, "Mineral": 2, "Carbón": 1},
    "Carpintero": {"Pan": 1, "Cerveza": 1, "Madera": 1}, "Sastre": {"Pan": 1, "Vino": 1, "Lana": 1},
    "Albañil": {"Pan": 1, "Cerveza": 1, "Carne": 1, "Piedra": 1}, "Tabernero": {"Pan": 1, "Verduras": 1},
    "Comerciante": {"Pan": 1, "Vino": 1, "Carne": 1}, "Transportista": {"Pan": 1, "Carne": 1, "Cerveza": 1, "Pienso": 1},
    "Médico": {"Pan": 1, "Vino": 1, "Hierbas": 1}, "Guardia": {"Pan": 1, "Carne": 1, "Cerveza": 1},
    "Administrador": {"Pan": 1, "Vino": 1, "Carne": 1}, "Sacerdote": {"Pan": 1, "Vino": 2},
    "Alquimista": {"Pan": 1, "Hierbas": 2}, "Escriba": {"Pan": 1, "Vino": 1, "Papel": 1, "Tinta": 1},
    "Cocinero": {"Carne": 1, "Verduras": 1}, "Cazador": {"Pan": 1, "Carne": 1},
    "Carpintero barcos": {"Pan": 1, "Cerveza": 1, "Madera": 1}, "Vidriero": {"Pan": 1, "Cerveza": 1, "Arena": 1},
    "Tejedor": {"Pan": 1, "Cerveza": 1, "Lana": 1}, "Zapatero": {"Pan": 1, "Cerveza": 1, "Cuero": 1},
    "Sacamuelas": {"Pan": 1, "Vino": 1}, "Músico": {"Pan": 1, "Vino": 2},
    "Soldado": {"Pan": 1, "Carne": 1, "Cerveza": 1}, "Ballestero": {"Pan": 1, "Carne": 1, "Cerveza": 1, "Madera": 1, "Hierro": 1},
    "Carcelero": {"Pan": 1, "Cerveza": 1}, "Barrendero": {"Pan": 1, "Cerveza": 1},
    "Mensajero": {"Pan": 1, "Carne": 1}, "Explorador": {"Pan": 1, "Carne": 1},
    "Salinero": {"Pan": 1, "Pescado": 1, "Agua": 1}, "Carbonero": {"Pan": 1, "Cerveza": 1, "Madera": 1},
    "Peletero": {"Pan": 1, "Carne": 1, "Cuero crudo": 1},
}


STOCK_MAX_POR_PRODUCTO = {
    "espada_corta:hierro": 4, "hacha_mano:hierro": 4, "daga:hierro": 5,
    "yelmo:hierro": 3, "cota_malla:hierro": 2,
    "Herramientas": 5, "Picos": 4, "Hachas": 4,
    "ballesta_ligera:hierro": 2, "escudo_redondo:hierro": 3,
    "botas_cuero:hierro": 4, "zapatos:hierro": 5, "guantes_cuero:hierro": 4,
    "Hierro": 10,
}
STOCK_MAX_DEFAULT = 20


# ─── Compradores individuales de equipo ────────────
# NPCs militares que compran armas individualmente cada X dias.
COMPRADORES_INDIVIDUALES = {
    "Soldado":     {"prob": 0.15, "armas": True, "armaduras": True},
    "Guardia":     {"prob": 0.10, "armas": True, "armaduras": True},
    "Carcelero":   {"prob": 0.08, "armas": True, "armaduras": False},
    "Explorador":  {"prob": 0.12, "armas": True, "armaduras": False},
    "Cazador":     {"prob": 0.08, "armas": True, "armaduras": False},
    "Ballestero":  {"prob": 0.10, "armas": True, "armaduras": False},
    "Mercader":    {"prob": 0.05, "armas": True, "armaduras": True},
}

ARMAS_BUSCADAS_INDIV = ["espada_corta", "hacha_mano", "daga", "lanza_corta"]
ARMADURAS_BUSCADAS_INDIV = ["tunica", "casco_cuero", "yelmo", "cota_malla", "escudo_redondo"]


_PRECIO_CACHE = {}


def limpiar_cache_precios():
    _PRECIO_CACHE.clear()


def _nombre_bonito(producto):
    try:
        from venefar_inventario import nombre_bonito_item
        return nombre_bonito_item(producto)
    except Exception:
        return producto


def _stock_local(conn, producto, ciudad):
    c = conn.cursor()
    if ciudad:
        c.execute("""SELECT SUM(i.cantidad) FROM inventario i
                     JOIN npcs n ON i.npc_id = n.id
                     WHERE i.producto=? AND n.ciudad=?""", (producto, ciudad))
    else:
        c.execute("SELECT SUM(cantidad) FROM inventario WHERE producto=?", (producto,))
    return c.fetchone()[0] or 0


def precio_actual(conn, producto, ciudad=None, multi_reputacion=1.0):
    key = (producto, ciudad)
    if key in _PRECIO_CACHE:
        base_calc = _PRECIO_CACHE[key]
    else:
        if isinstance(producto, str) and ":" in producto:
            try:
                from venefar_items import obtener_item
                item = obtener_item(producto)
                if item:
                    base_calc = item["precio"]
                    try:
                        from venefar_eventos_mundo import modificador_precio
                        multi = modificador_precio(conn, producto)
                        base_calc = max(1, int(base_calc * multi))
                    except Exception:
                        pass
                    _PRECIO_CACHE[key] = base_calc
                    if multi_reputacion != 1.0:
                        return max(1, int(base_calc * multi_reputacion))
                    return base_calc
            except Exception:
                pass
        if producto not in PRODUCTOS:
            base_calc = 5
        else:
            stock = _stock_local(conn, producto, ciudad)
            base = PRODUCTOS[producto]["base"]
            if stock <= 0: base_calc = int(base * 1.8)
            elif stock < 5: base_calc = int(base * 1.4)
            elif stock < 15: base_calc = int(base * 1.1)
            elif stock > 50: base_calc = int(base * 0.85)
            else: base_calc = base
            try:
                from venefar_eventos_mundo import modificador_precio
                multi = modificador_precio(conn, producto)
                base_calc = max(1, int(base_calc * multi))
            except Exception:
                pass
        _PRECIO_CACHE[key] = base_calc
    if multi_reputacion != 1.0:
        return max(1, int(base_calc * multi_reputacion))
    return base_calc


def intercambio(conn, comprador, vendedor, producto, cantidad, dia, guardar=True):
    if vendedor["inventario"].get(producto, 0) < cantidad: return False
    precio_unit = precio_actual(conn, producto, ciudad=comprador.get("ciudad"))
    total = precio_unit * cantidad
    if comprador["dinero"] < total: return False
    comprador["dinero"] -= total
    vendedor["dinero"] += total
    comprador["inventario"][producto] = comprador["inventario"].get(producto, 0) + cantidad
    vendedor["inventario"][producto] -= cantidad
    if vendedor["inventario"][producto] <= 0:
        del vendedor["inventario"][producto]
    if guardar:
        c = conn.cursor()
        c.execute("""INSERT INTO transacciones (dia, comprador, vendedor, producto, cantidad, precio_total)
                     VALUES (?,?,?,?,?,?)""",
                  (dia, comprador["nombre"], vendedor["nombre"], _nombre_bonito(producto), cantidad, total))
    return True


def _limite_stock(producto):
    if producto in STOCK_MAX_POR_PRODUCTO:
        return STOCK_MAX_POR_PRODUCTO[producto]
    return STOCK_MAX_DEFAULT


def producir_dia(conn, npc, dia, guardar=True):
    """
    El NPC produce UN item. Ahora elige la receta
    del producto del que MENOS tiene (para variar la produccion).
    """
    from venefar_npc import guardar_recuerdo
    recetas_posibles = []
    for rec in RECETAS.get(npc["oficio"], []):
        if "produce" not in rec: continue
        prod = rec["produce"]
        tiene = npc["inventario"].get(prod, 0)
        if tiene >= _limite_stock(prod): continue
        puede = all(npc["inventario"].get(p, 0) >= c for p, c in rec["consume"].items())
        if puede:
            recetas_posibles.append((rec, tiene))
    if not recetas_posibles:
        return False

    # Elegir la receta del producto con menos stock (mas necesidad)
    recetas_posibles.sort(key=lambda x: x[1])
    # De las que tienen menos stock, elegir una al azar para no ser totalmente deterministico
    min_stock = recetas_posibles[0][1]
    candidatas = [r for r, t in recetas_posibles if t <= min_stock + 1]
    rec = random.choice(candidatas)

    for p, c in rec["consume"].items():
        npc["inventario"][p] -= c
        if npc["inventario"][p] <= 0:
            del npc["inventario"][p]
    prod = rec["produce"]
    npc["inventario"][prod] = npc["inventario"].get(prod, 0) + rec["cantidad"]
    if guardar:
        guardar_recuerdo(conn, npc["id"], dia, "produccion",
                         f"Produjo {rec['cantidad']} {prod}", 1)
    return True


def consumo_diario(conn, npc, dia):
    for prod, cant in CONSUMO_DIARIO.get(npc["oficio"], {}).items():
        if npc["inventario"].get(prod, 0) >= cant:
            npc["inventario"][prod] -= cant
            if npc["inventario"][prod] <= 0:
                del npc["inventario"][prod]


def buscar_compras(conn, npcs, dia, guardar=True):
    compras = 0
    total_gastado = 0
    por_ciudad = {}
    for n in npcs:
        por_ciudad.setdefault(n.get("ciudad", "?"), []).append(n)
    for comprador in npcs:
        vecinos = por_ciudad.get(comprador.get("ciudad", "?"), [])
        for prod, cant in CONSUMO_DIARIO.get(comprador["oficio"], {}).items():
            if comprador["inventario"].get(prod, 0) >= cant * 3: continue
            candidatos = [(n, n["inventario"].get(prod, 0)) for n in vecinos
                          if n["id"] != comprador["id"] and n["inventario"].get(prod, 0) > 0]
            if not candidatos: continue
            vendedor, stock_v = max(candidatos, key=lambda x: x[1])
            cantidad = min(cant * 2, stock_v)
            precio_unit = precio_actual(conn, prod, ciudad=comprador.get("ciudad"))
            coste = precio_unit * cantidad
            if intercambio(conn, comprador, vendedor, prod, cantidad, dia, guardar=guardar):
                compras += 1
                total_gastado += coste
    if compras > 0 and guardar:
        c = conn.cursor()
        desc = f"Se realizaron {compras} transacciones entre vecinos (total {total_gastado} monedas)."
        c.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)",
                  (dia, "economia", desc))
    return compras


def compras_militares_individuales(conn, npcs, dia, guardar=True):
    """
    Soldados, guardias y otros NPCs militares compran armas/armaduras
    individualmente a herreros locales.
    """
    compras = 0
    for comprador in npcs:
        if comprador["oficio"] not in COMPRADORES_INDIVIDUALES: continue
        cfg = COMPRADORES_INDIVIDUALES[comprador["oficio"]]
        if random.random() > cfg["prob"]: continue
        # Buscar herreros locales
        ciudad = comprador.get("ciudad", "capital_imperial")
        herreros = [n for n in npcs if n.get("ciudad") == ciudad
                    and n["oficio"] in ("Herrero", "Ballestero")
                    and n["id"] != comprador["id"]]
        if not herreros: continue

        # Decidir si busca arma o armadura
        categorias = []
        if cfg["armas"]: categorias.append("arma")
        if cfg["armaduras"]: categorias.append("armadura")
        categoria = random.choice(categorias)

        if categoria == "arma":
            tipos = ARMAS_BUSCADAS_INDIV
        else:
            tipos = ARMADURAS_BUSCADAS_INDIV

        # Buscar items disponibles
        candidatos = []
        for h in herreros:
            for item_id, cant in h["inventario"].items():
                if ":" not in item_id: continue
                tipo_item, _ = item_id.split(":", 1)
                if tipo_item in tipos and cant > 0:
                    candidatos.append((h, item_id))
        if not candidatos: continue

        # Elegir uno al azar
        herrero, item_id = random.choice(candidatos)
        precio_unit = precio_actual(conn, item_id, ciudad=ciudad)
        if comprador["dinero"] < precio_unit: continue

        if intercambio(conn, comprador, herrero, item_id, 1, dia, guardar=guardar):
            compras += 1
    return compras


def comercio_inter_ciudad(conn, npcs, dia, guardar=True):
    from venefar_mapa import RUTAS
    from descripciones.ciudades import obtener_nombre
    limpiar_cache_precios()
    ruta = random.choice(RUTAS)
    ciudad_a, ciudad_b, dias, peligro = ruta
    origen, destino = (ciudad_a, ciudad_b) if random.random() < 0.5 else (ciudad_b, ciudad_a)
    mercaderes = [n for n in npcs if n.get("ciudad") == origen and n["oficio"] in ("Transportista", "Comerciante")]
    if not mercaderes: return None
    mercader = random.choice(mercaderes)
    mejor_prod, mejor_diff, mejor_stock = None, 0, 0
    for prod in PRODUCTOS.keys():
        p_o = precio_actual(conn, prod, ciudad=origen)
        p_d = precio_actual(conn, prod, ciudad=destino)
        diff = p_d - p_o
        if diff > mejor_diff:
            stock_o = _stock_local(conn, prod, origen)
            if stock_o >= 5:
                mejor_prod, mejor_diff, mejor_stock = prod, diff, stock_o
    if not mejor_prod or mejor_diff < 3: return None
    precio_o = precio_actual(conn, mejor_prod, ciudad=origen)
    cantidad = min(5, mejor_stock, mercader["dinero"] // precio_o)
    if cantidad <= 0: return None
    vendedores = [n for n in npcs if n.get("ciudad") == origen and n["id"] != mercader["id"]
                  and n["inventario"].get(mejor_prod, 0) > 0]
    if not vendedores: return None
    vendedor = max(vendedores, key=lambda n: n["inventario"].get(mejor_prod, 0))
    cantidad = min(cantidad, vendedor["inventario"].get(mejor_prod, 0))
    if cantidad <= 0: return None
    total_compra = precio_o * cantidad
    mercader["dinero"] -= total_compra
    vendedor["dinero"] += total_compra
    vendedor["inventario"][mejor_prod] -= cantidad
    if vendedor["inventario"][mejor_prod] <= 0: del vendedor["inventario"][mejor_prod]
    prob_perdida = [0.05, 0.15, 0.30, 0.50][peligro]
    if random.random() < prob_perdida:
        if guardar:
            desc = f"Caravana asaltada: {mercader['nombre']} perdio {cantidad} de {_nombre_bonito(mejor_prod)} camino a {obtener_nombre(destino)}."
            c = conn.cursor()
            c.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)", (dia, "comercio", desc))
        return "asalto"
    compradores = [n for n in npcs if n.get("ciudad") == destino and n["id"] != mercader["id"]]
    if not compradores:
        mercader["inventario"][mejor_prod] = mercader["inventario"].get(mejor_prod, 0) + cantidad
        return "sin_comprador"
    precio_d = precio_actual(conn, mejor_prod, ciudad=destino)
    compradores_validos = [n for n in compradores if n["dinero"] >= precio_d * cantidad]
    if not compradores_validos:
        mercader["inventario"][mejor_prod] = mercader["inventario"].get(mejor_prod, 0) + cantidad
        return "sin_comprador"
    comprador = random.choice(compradores_validos)
    total_venta = precio_d * cantidad
    comprador["dinero"] -= total_venta
    mercader["dinero"] += total_venta
    comprador["inventario"][mejor_prod] = comprador["inventario"].get(mejor_prod, 0) + cantidad
    if guardar:
        desc = (f"{mercader['nombre']} llevo {cantidad} de {_nombre_bonito(mejor_prod)} de "
                f"{obtener_nombre(origen)} a {obtener_nombre(destino)}. "
                f"Ganancia: {total_venta - total_compra} monedas.")
        c = conn.cursor()
        c.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)", (dia, "comercio", desc))
        c.execute("""INSERT INTO transacciones (dia, comprador, vendedor, producto, cantidad, precio_total)
                     VALUES (?,?,?,?,?,?)""",
                  (dia, comprador["nombre"], mercader["nombre"], _nombre_bonito(mejor_prod), cantidad, total_venta))
    return "exito"


def caravana_externa(conn, npcs, dia, guardar=True):
    if random.random() > 0.05: return None
    ciudades = list(set(n.get("ciudad", "capital_imperial") for n in npcs))
    if not ciudades: return None
    ciudad = random.choice(ciudades)
    mercaderes = [n for n in npcs if n["oficio"] == "Comerciante" and n.get("ciudad") == ciudad]
    if not mercaderes: return None
    mercader = random.choice(mercaderes)
    prod = random.choice(["Mineral", "Madera", "Hierbas", "Uva", "Trigo", "Lana", "Pescado"])
    cant = random.randint(5, 12)
    precio_unit = int(PRODUCTOS[prod]["base"] * 0.7)
    total = precio_unit * cant
    if mercader["dinero"] < total: return None
    mercader["dinero"] -= total
    mercader["inventario"][prod] = mercader["inventario"].get(prod, 0) + cant
    if guardar:
        from descripciones.ciudades import obtener_nombre
        desc = f"Caravana externa llego a {obtener_nombre(ciudad)}: {cant} de {_nombre_bonito(prod)}."
        c = conn.cursor()
        c.execute("INSERT INTO eventos (dia, tipo, descripcion) VALUES (?,?,?)", (dia, "comercio", desc))
    return True


def simular_dia_economico(conn, npcs, dia, guardar=True):
    limpiar_cache_precios()
    for npc in npcs:
        producir_dia(conn, npc, dia, guardar=guardar)
    for npc in npcs:
        consumo_diario(conn, npc, dia)
    buscar_compras(conn, npcs, dia, guardar=guardar)
    compras_militares_individuales(conn, npcs, dia, guardar=guardar)
    n_viajes = random.choice([0, 1, 1, 2])
    for _ in range(n_viajes):
        comercio_inter_ciudad(conn, npcs, dia, guardar=guardar)
    caravana_externa(conn, npcs, dia, guardar=guardar)
    if guardar:
        from venefar_npc import guardar_todos
        guardar_todos(conn, npcs)