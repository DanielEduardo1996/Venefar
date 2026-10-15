# -*- coding: utf-8 -*-
"""VENEFAR - Inventario por categorias"""
from venefar_ui import C
from venefar_items import es_item_equipable, obtener_item


KEYWORDS_EQUIPO = [
    "espada", "arma", "ballesta", "arco", "daga", "cuchillo",
    "armadura", "cota", "casco", "yelmo", "escudo",
    "botas", "zapatos", "ropa", "capa", "delantal",
    "anillo", "amuleto", "guantes", "cinturon",
]
KEYWORDS_CONSUMIBLES = [
    "pan", "carne", "verduras", "pescado", "leche", "agua",
    "cerveza", "vino", "comida", "pocion", "veneno",
    "remedio", "medicina", "hierba", "queso", "sal",
    "flecha", "virote",
]
KEYWORDS_DOCUMENTOS = [
    "carta", "documento", "mapa", "permiso", "libro",
    "pergamino", "pliego", "esquela",
]


def limpiar_nombre_producto(item):
    if "x " in item:
        return item.split("x ", 1)[1]
    return item


def nombre_bonito_item(item):
    if not isinstance(item, str):
        return str(item)
    prefijo = ""
    if "x " in item:
        partes = item.split("x ", 1)
        prefijo = f"{partes[0]}x "
        item_id = partes[1]
    else:
        item_id = item
    if es_item_equipable(item_id):
        item_data = obtener_item(item_id)
        if item_data:
            return prefijo + item_data["nombre"]
    return item


def categorizar_item(item):
    item_id = limpiar_nombre_producto(item)
    if es_item_equipable(item_id):
        return "equipo"
    nombre = item_id.lower()
    for kw in KEYWORDS_EQUIPO:
        if kw in nombre:
            return "equipo"
    for kw in KEYWORDS_CONSUMIBLES:
        if kw in nombre:
            return "consumibles"
    for kw in KEYWORDS_DOCUMENTOS:
        if kw in nombre:
            return "documentos"
    return "miscelaneo"


def agrupar_inventario(inventario):
    grupos = {"equipo": [], "consumibles": [], "documentos": [], "miscelaneo": []}
    for item in inventario:
        cat = categorizar_item(item)
        grupos[cat].append(item)
    return grupos


NOMBRES_CATEGORIA = {
    "equipo": "EQUIPO",
    "consumibles": "CONSUMIBLES",
    "documentos": "DOCUMENTOS",
    "miscelaneo": "MISCELANEO",
}

COLORES_CATEGORIA = {
    "equipo": C.CYAN,
    "consumibles": C.GREEN,
    "documentos": C.YELLOW,
    "miscelaneo": C.MAGENTA,
}


def items_con_categorias(inventario):
    grupos = agrupar_inventario(inventario)
    resultado = []
    for cat in ["equipo", "consumibles", "documentos", "miscelaneo"]:
        for item in grupos[cat]:
            resultado.append((item, cat, item))
    return resultado


def menu_inventario_agrupado(inventario, contexto_fn=None, permitir_cancelar=True):
    """
    Funcion reutilizable: muestra el inventario agrupado por categorias con nombres bonitos.
    Devuelve el indice del item en la lista original, o -1 si cancela.
    """
    from venefar_ui import menu_flechas
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