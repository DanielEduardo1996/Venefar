# -*- coding: utf-8 -*-
"""VENEFAR - Negocios
Cada negocio produce un producto y vende automaticamente.
"""
import json
from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from descripciones.ciudades import obtener_nombre
from venefar_reputacion import obtener_reputacion, etiqueta_reputacion
from venefar_economia import precio_actual


# ─── Tipos de negocio ───────────────────────────────
# Cada tipo tiene un producto y produccion base por dia.
TIPOS_NEGOCIO = {
    "panaderia":   {"nombre": "Panaderia",   "producto": "Pan",              "base_produccion": 20},
    "cerveceria":  {"nombre": "Cerveceria",  "producto": "Cerveza",          "base_produccion": 18},
    "herreria":    {"nombre": "Herreria",    "producto": "Herramientas",     "base_produccion": 5},
    "carpinteria": {"nombre": "Carpinteria", "producto": "Tablones",         "base_produccion": 8},
    "sastreria":   {"nombre": "Sastreria",   "producto": "Ropa",             "base_produccion": 6},
    "zapateria":   {"nombre": "Zapateria",   "producto": "Botas",            "base_produccion": 5},
    "alquimia":    {"nombre": "Alquimia",    "producto": "Pociones",         "base_produccion": 6},
    "tejeduria":   {"nombre": "Tejeduria",   "producto": "Tela",             "base_produccion": 10},
    "peleteria":   {"nombre": "Peleteria",   "producto": "Cuero",            "base_produccion": 8},
    "carboneria":  {"nombre": "Carboneria",  "producto": "Carbon vegetal",   "base_produccion": 12},
}


# Precio base del local (por ciudad)
PRECIO_LOCAL_BASE = {
    "capital_imperial": 3500,
    "puerto_sal":       2500,
    "villareal":        2500,
    "santamera":        2000,
    "piedrahonda":      1400,
    "villafria":        1200,
    "robledal":         1200,
    "canterral":        1400,
    "mareas":           1200,
    "ermita_alta":      900,
    "calas":            800,
    "fresnillo":        1000,
}

PERMISO_PCT = 0.10        # 10% del local
REPUTACION_MINIMA = 10    # Necesitas "Neutral+" en la ciudad
IMPUESTO_DIARIO = 0.05    # 5% de ingresos
COSTE_INSUMOS = 0.35      # 35% de ingresos en materia prima
SALARIO_POR_NIVEL = 5     # 5 * nivel monedas/dia al trabajador
MULTI_PRODUCCION = {1: 1.0, 2: 1.8, 3: 2.5}


def precio_local_negocio(ciudad):
    return PRECIO_LOCAL_BASE.get(ciudad, 1000)


def precio_permiso(ciudad):
    return int(precio_local_negocio(ciudad) * PERMISO_PCT)


def coste_mejora(ciudad, nivel_actual):
    """Coste para subir del nivel actual al siguiente."""
    base = precio_local_negocio(ciudad)
    if nivel_actual == 1: return base * 2
    if nivel_actual == 2: return base * 4
    return None


# ─── Persistencia ────────────────────────────────────
def tiene_casa(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM propiedades WHERE jugador_id=? AND ciudad=? AND tipo='casa'",
              (jugador_id, ciudad))
    return c.fetchone()[0] > 0


def obtener_negocio(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("SELECT * FROM negocios WHERE jugador_id=? AND ciudad=?", (jugador_id, ciudad))
    f = c.fetchone()
    return dict(f) if f else None


def listar_negocios(conn, jugador_id):
    c = conn.cursor()
    c.execute("SELECT * FROM negocios WHERE jugador_id=? ORDER BY ciudad", (jugador_id,))
    return [dict(r) for r in c.fetchall()]


def crear_negocio(conn, jugador_id, ciudad, tipo, dia):
    c = conn.cursor()
    c.execute("""INSERT INTO negocios (jugador_id, ciudad, tipo, nivel, dia_apertura, ganancia_acumulada, activo)
                 VALUES (?, ?, ?, 1, ?, 0, 1)""",
              (jugador_id, ciudad, tipo, dia))
    conn.commit()


def retirar_ganancia(conn, jugador_id, ciudad):
    n = obtener_negocio(conn, jugador_id, ciudad)
    if not n: return 0
    cant = n["ganancia_acumulada"]
    c = conn.cursor()
    c.execute("UPDATE negocios SET ganancia_acumulada=0 WHERE id=?", (n["id"],))
    conn.commit()
    return cant


# ─── Producción diaria ───────────────────────────────
def procesar_negocios_dia(conn, jugador, dia):
    """Cada negocio activo produce y acumula ganancia."""
    jugador_id = jugador["identificador"]
    negocios = listar_negocios(conn, jugador_id)
    if not negocios: return 0

    total = 0
    for n in negocios:
        if n["activo"] != 1: continue
        tipo = n["tipo"]
        if tipo not in TIPOS_NEGOCIO: continue

        info = TIPOS_NEGOCIO[tipo]
        multi = MULTI_PRODUCCION.get(n["nivel"], 1.0)
        produccion = int(info["base_produccion"] * multi)

        # Precio local del producto
        precio = precio_actual(conn, info["producto"], ciudad=n["ciudad"])

        # Venta automatica (70%)
        ingresos = int(produccion * precio * 0.70)
        # Gastos
        gastos_insumos = int(ingresos * COSTE_INSUMOS)
        salario = SALARIO_POR_NIVEL * n["nivel"]
        impuesto = int(ingresos * IMPUESTO_DIARIO)
        neto = ingresos - gastos_insumos - salario - impuesto
        if neto < 0: neto = 0

        c = conn.cursor()
        c.execute("UPDATE negocios SET ganancia_acumulada = ganancia_acumulada + ? WHERE id=?",
                  (neto, n["id"]))
        total += neto

    conn.commit()
    return total


# ─── Menú ────────────────────────────────────────────
def menu_negocios(conn, jugador, mundo):
    ciudad = jugador.get("ciudad", "capital_imperial")
    ciudad_nombre = obtener_nombre(ciudad)
    jugador_id = jugador["identificador"]

    while True:
        negocio = obtener_negocio(conn, jugador_id, ciudad)
        rep = obtener_reputacion(conn, jugador_id, ciudad)
        etq, col = etiqueta_reputacion(rep)

        def contexto():
            titulo(f"NEGOCIOS · {ciudad_nombre.upper()}")
            print(f"  Dinero: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
            print(f"  Reputacion: {col}{etq}{C.RESET} ({rep})")
            if negocio:
                info = TIPOS_NEGOCIO.get(negocio["tipo"], {})
                print(f"  Negocio activo: {C.BOLD}{info.get('nombre','?')}{C.RESET} (nivel {negocio['nivel']})")
                print(f"  {C.GREEN}Ganancia acumulada: {negocio['ganancia_acumulada']}{C.RESET} monedas")
            else:
                print(f"  {C.DIM}No tienes negocio en esta ciudad.{C.RESET}")

        items = []
        claves = []

        if not negocio:
            # Ver si puede montar
            tiene_casa_aqui = tiene_casa(conn, jugador_id, ciudad)
            precio_local = precio_local_negocio(ciudad)
            precio_perm = precio_permiso(ciudad)
            coste_total = precio_local + precio_perm
            puede = tiene_casa_aqui and rep >= REPUTACION_MINIMA and jugador["dinero"] >= coste_total
            motivo = ""
            if not tiene_casa_aqui: motivo = "Necesitas casa aqui"
            elif rep < REPUTACION_MINIMA: motivo = f"Reputacion {REPUTACION_MINIMA}+ requerida"
            elif jugador["dinero"] < coste_total: motivo = f"Necesitas {coste_total} monedas"
            else: motivo = f"Coste: {coste_total}"
            items.append(("Montar negocio", motivo))
            claves.append("montar")
        else:
            items.append(("Retirar ganancias",
                          f"{negocio['ganancia_acumulada']} disponibles"))
            claves.append("retirar")
            items.append(("Mejorar negocio",
                          f"Coste: {coste_mejora(ciudad, negocio['nivel']) or 0}"))
            claves.append("mejorar")
            items.append(("Cerrar negocio",
                          "Recuperas 50% del valor"))
            claves.append("cerrar")

        items.append(("Ver todos mis negocios", ""))
        claves.append("ver_todos")
        items.append(("Volver", ""))
        claves.append("salir")

        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        acc = claves[idx]

        if acc == "salir":
            return
        elif acc == "montar":
            _montar_negocio(conn, jugador, ciudad, rep)
        elif acc == "retirar":
            _retirar_ganancias(conn, jugador, ciudad)
        elif acc == "mejorar":
            _mejorar_negocio(conn, jugador, ciudad)
        elif acc == "cerrar":
            _cerrar_negocio(conn, jugador, ciudad)
        elif acc == "ver_todos":
            _ver_negocios(conn, jugador)


def _montar_negocio(conn, jugador, ciudad, rep):
    if not tiene_casa(conn, jugador["identificador"], ciudad):
        limpiar(); titulo("MONTAR NEGOCIO")
        narrar("Necesitas una casa en esta ciudad antes de montar un negocio.")
        pausa(); return
    if rep < REPUTACION_MINIMA:
        limpiar(); titulo("MONTAR NEGOCIO")
        narrar(f"Necesitas reputacion {REPUTACION_MINIMA}+ en esta ciudad.")
        pausa(); return
    precio_local = precio_local_negocio(ciudad)
    precio_perm = precio_permiso(ciudad)
    coste = precio_local + precio_perm
    if jugador["dinero"] < coste:
        limpiar(); titulo("MONTAR NEGOCIO")
        narrar(f"Necesitas {coste} monedas (tienes {jugador['dinero']}).")
        pausa(); return

    # Elegir tipo
    limpiar(); titulo("MONTAR NEGOCIO · ELIGE TIPO")
    print(f"  {C.DIM}Coste total: {coste} monedas (local {precio_local} + permiso {precio_perm}){C.RESET}\n")
    items = []
    claves = []
    for k, info in TIPOS_NEGOCIO.items():
        items.append((info["nombre"], f"Produce {info['producto']}"))
        claves.append(k)
    idx = menu_flechas(items, contexto_fn=lambda: None, permitir_cancelar=True)
    if idx == -1: return
    tipo = claves[idx]

    confirm = menu_flechas([
        ("Confirmar", f"Pagar {coste} monedas"),
        ("Cancelar", ""),
    ], contexto_fn=lambda: titulo(f"MONTAR {TIPOS_NEGOCIO[tipo]['nombre'].upper()}"),
       permitir_cancelar=False)
    if confirm == 1: return

    crear_negocio(conn, jugador["identificador"], ciudad, tipo, 1)
    jugador["dinero"] -= coste
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("NEGOCIO MONTADO")
    narrar(f"Has montado una {TIPOS_NEGOCIO[tipo]['nombre']} en {obtener_nombre(ciudad)}.")
    narrar(f"El trabajador empezara a producir manana.")
    pausa()


def _retirar_ganancias(conn, jugador, ciudad):
    n = obtener_negocio(conn, jugador["identificador"], ciudad)
    if not n or n["ganancia_acumulada"] <= 0:
        limpiar(); titulo("RETIRAR GANANCIAS")
        narrar("No tienes ganancias acumuladas.")
        pausa(); return
    cant = retirar_ganancia(conn, jugador["identificador"], ciudad)
    jugador["dinero"] += cant
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("GANANCIAS RETIRADAS")
    narrar(f"Retiras {cant} monedas de tu negocio.")
    pausa()


def _mejorar_negocio(conn, jugador, ciudad):
    n = obtener_negocio(conn, jugador["identificador"], ciudad)
    if not n:
        return
    coste = coste_mejora(ciudad, n["nivel"])
    if coste is None:
        limpiar(); titulo("MEJORAR")
        narrar("Este negocio ya esta al maximo nivel.")
        pausa(); return
    if jugador["dinero"] < coste:
        limpiar(); titulo("MEJORAR")
        narrar(f"Necesitas {coste} monedas.")
        pausa(); return
    confirm = menu_flechas([
        (f"Subir a nivel {n['nivel']+1}", f"Coste: {coste}"),
        ("Cancelar", ""),
    ], contexto_fn=lambda: titulo("MEJORAR NEGOCIO"), permitir_cancelar=False)
    if confirm == 1: return
    c = conn.cursor()
    c.execute("UPDATE negocios SET nivel=nivel+1 WHERE id=?", (n["id"],))
    conn.commit()
    jugador["dinero"] -= coste
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("NEGOCIO MEJORADO")
    narrar(f"Tu negocio ahora es nivel {n['nivel']+1}.")
    pausa()


def _cerrar_negocio(conn, jugador, ciudad):
    n = obtener_negocio(conn, jugador["identificador"], ciudad)
    if not n: return
    local = precio_local_negocio(ciudad)
    devolucion = int(local * 0.5)
    confirm = menu_flechas([
        ("Confirmar cierre", f"Recuperas {devolucion} monedas"),
        ("Cancelar", ""),
    ], contexto_fn=lambda: titulo("CERRAR NEGOCIO"), permitir_cancelar=False)
    if confirm == 1: return
    c = conn.cursor()
    c.execute("DELETE FROM negocios WHERE id=?", (n["id"],))
    conn.commit()
    jugador["dinero"] += devolucion
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("NEGOCIO CERRADO")
    narrar(f"Recuperas {devolucion} monedas del local.")
    pausa()


def _ver_negocios(conn, jugador):
    limpiar(); titulo("MIS NEGOCIOS")
    negocios = listar_negocios(conn, jugador["identificador"])
    if not negocios:
        narrar("No tienes ningun negocio.")
        pausa(); return
    for n in negocios:
        info = TIPOS_NEGOCIO.get(n["tipo"], {})
        ciudad_nombre = obtener_nombre(n["ciudad"])
        print(f"  {C.BOLD}{info.get('nombre','?')}{C.RESET} en {C.CYAN}{ciudad_nombre}{C.RESET}")
        print(f"    Nivel {n['nivel']} · Ganancia acumulada: {C.GREEN}{n['ganancia_acumulada']}{C.RESET} monedas")
    pausa()


# ─── Venta manual ────────────────────────────────────
def menu_venta_manual(conn, jugador, mundo):
    """Ir al mercado a vender la produccion al 100% del precio."""
    ciudad = jugador.get("ciudad", "capital_imperial")
    negocio = obtener_negocio(conn, jugador["identificador"], ciudad)
    if not negocio:
        limpiar(); titulo("VENTA MANUAL")
        narrar("Necesitas un negocio en esta ciudad para esto.")
        pausa(); return

    info = TIPOS_NEGOCIO.get(negocio["tipo"], {})
    producto = info["producto"]
    multi = MULTI_PRODUCCION.get(negocio["nivel"], 1.0)
    produccion_dia = int(info["base_produccion"] * multi)
    # Disponible = ganancia del dia expresada en productos
    # Simplificacion: puedes vender produccion de los proximos 5 dias de golpe

    limpiar(); titulo(f"VENTA MANUAL · {info['nombre'].upper()}")
    print(f"  Producto: {producto}")
    print(f"  Produccion tipica: {produccion_dia}/dia")
    print(f"  {C.DIM}Si vas al mercado, vendes al 100%.{C.RESET}")
    print(f"  {C.DIM}Venta automatica solo te da el 70%.{C.RESET}\n")

    max_unidades = produccion_dia * 5  # 5 dias de produccion max
    print(f"  ¿Cuantas unidades vas a vender? (max {max_unidades})")
    cant = pedir_numero(max_unidades)

    precio_local = precio_actual(conn, producto, ciudad=ciudad)
    # Si vendes manual, cobras 100%
    ganancia_extra = int(cant * precio_local * 0.30)  # 30% extra sobre automatico
    jugador["dinero"] += ganancia_extra
    jugador["cansancio"] = min(100, jugador.get("cansancio", 0) + 15)
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)

    limpiar(); titulo("VENTA MANUAL REALIZADA")
    narrar(f"Vas al mercado y vendes {cant} unidades.")
    narrar(f"Ganas {ganancia_extra} monedas extra (30% mas que automatico).")
    print(f"  {C.GREEN}Dinero actual:{C.RESET} {jugador['dinero']} monedas")
    pausa()