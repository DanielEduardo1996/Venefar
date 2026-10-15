# -*- coding: utf-8 -*-
"""VENEFAR - Punto de Entrada"""
import sys, random

from venefar_ui import (limpiar, linea, titulo, narrar, opcion, pausa,
                        pedir_numero, barra_estado, menu_flechas, C)
from venefar_db import init_db
from venefar_npc import (seed_inicial, cargar_npcs, guardar_npc, guardar_todos,
                         npc_hace_pregunta, generar_respuesta, tiene)
from venefar_economia import PRODUCTOS, precio_actual, limpiar_cache_precios
from venefar_jugador import elegir_personaje, guardar_jugador, avanzar_estado_jugador
from venefar_mundo import (avanzar_un_dia, formatear_fecha, formatear_fecha_corta,
                            obtener_estacion)
from venefar_descripciones import (
    imprimir_descripcion_npc, imprimir_descripcion_ciudad, imprimir_descripcion_objeto,
)
from descripciones.ciudades import CIUDADES, obtener_nombre
from venefar_mapa import conexiones_de, mostrar_mapa, NIVELES_PELIGRO
from venefar_jugador_acciones import accion_trabajar, accion_pedir_limosna, accion_vender
from venefar_eventos_mundo import listar_eventos_activos
from venefar_reputacion import (obtener_reputacion, obtener_todas, etiqueta_reputacion,
                                 multiplicador_precio_reputacion)
from venefar_propiedades import menu_propiedades, tiene_casa
from venefar_bancos import menu_banco, hay_banco
from venefar_negocios import menu_venta_manual, listar_negocios
from venefar_caravanas import menu_caravanas, listar_caravanas
from venefar_inventario import (agrupar_inventario, NOMBRES_CATEGORIA,
                                 COLORES_CATEGORIA, limpiar_nombre_producto,
                                 nombre_bonito_item)
from venefar_items import es_item_equipable, obtener_item
from venefar_equipamiento import menu_equipamiento
from venefar_guarniciones import (init_guarniciones, menu_guarnicion,
                                   obtener_guarnicion)


PRODUCTOS_COMPRABLES_JUGADOR = {
    "Pan", "Carne", "Verduras", "Pescado", "Leche", "Agua",
    "Cerveza", "Vino", "Comida cocinada",
    "Hierbas", "Remedios", "Medicinas", "Pociones", "Venenos",
    "Herramientas", "Picos", "Hachas", "Espadas", "Armas",
    "Ballestas", "Virotes", "Flechas", "Arcos",
    "Botas", "Zapatos", "Ropa", "Cuero",
    "Madera", "Leña", "Hierro", "Mineral", "Piedra", "Carbón",
    "Lana", "Tela", "Cuero crudo", "Provisiones", "Mapas",
}


def _precio_jugador(conn, producto, jugador, ciudad=None):
    if ciudad is None:
        ciudad = jugador.get("ciudad", "capital_imperial")
    rep = obtener_reputacion(conn, jugador["identificador"], ciudad)
    multi = multiplicador_precio_reputacion(rep)
    return precio_actual(conn, producto, ciudad=ciudad, multi_reputacion=multi)


def _menu_inventario_agrupado(inventario, contexto_fn=None, permitir_cancelar=True):
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


def conversar(conn, jugador, npc, mundo):
    dia = mundo["dia"]
    limpiar(); titulo(npc["nombre"].upper())
    print(f"  {C.DIM}{npc['oficio']}, {npc['edad']} anos{C.RESET}")
    if npc["relacion"] != 0:
        col = C.GREEN if npc["relacion"] > 0 else C.RED
        print(f"  {col}Relacion: {npc['relacion']}{C.RESET}")
    print()
    ya_visto = npc.get("descripcion_vista", 0) == 1
    imprimir_descripcion_npc(npc, jugador, primera_vez=not ya_visto)
    if not ya_visto:
        npc["descripcion_vista"] = 1
        guardar_npc(conn, npc)
    if not npc["te_conoce"]:
        saludos = ["Salve, forastero. ¿Que te trae por aqui?",
                   "Buenos dias. No te he visto antes.", "Dime, viajero."]
        if tiene(npc, "gruñón"): saludos = ["¿Que quieres?", "Habla rapido."]
        elif tiene(npc, "amable"): saludos = ["Buenos dias. Siéntate, si quieres.", "Salve. Bienvenido."]
        elif tiene(npc, "desconfiado"): saludos = ["¿Que quieres de mi?", "No me fio de desconocidos."]
        elif tiene(npc, "hablador"): saludos = ["¡Ah, un rostro nuevo! Cuentame.", "¡Salve! ¿De donde vienes?"]
        narrar(f"\"{random.choice(saludos)}\"")
        npc["te_conoce"] = True; npc["relacion"] += 2; guardar_npc(conn, npc); pausa()
    else:
        if npc["dias_sin_hablar"] > 7: narrar(f"\"Vaya, cuanto tiempo sin verte.\"")
        elif npc["relacion"] >= 50: narrar(f"\"Hombre, {jugador['nombre']}. Me alegro de verte.\"")
        elif npc["relacion"] >= 20: narrar(f"\"Hola otra vez. ¿Que necesitas?\"")
        elif npc["relacion"] > 0: narrar(f"\"Ah, tu. ¿Que quieres ahora?\"")
        else: narrar(f"\"Otra vez tu. ¿Que quieres?\"")
        pausa()
    npc["dias_sin_hablar"] = 0
    sub_menu(conn, jugador, npc, mundo)


def sub_menu(conn, jugador, npc, mundo):
    dia = mundo["dia"]
    ciudad_jugador = jugador.get("ciudad", "capital_imperial")
    while True:
        def contexto():
            titulo(npc["nombre"].upper())
            print(f"  {C.DIM}{npc['oficio']}, {npc['edad']} anos{C.RESET}")
            print(f"  {C.DIM}{npc['detalle']}{C.RESET}")
            print(f"  {C.DIM}Estado: {npc['mood']}{C.RESET}")
            if npc["relacion"] != 0:
                col = C.GREEN if npc["relacion"] > 0 else C.RED
                print(f"  {col}Relacion: {npc['relacion']}{C.RESET}")
        items = [
            ("Su oficio", "Preguntarle por su trabajo"),
            ("Rumores locales", "Escuchar que se dice"),
            ("El lugar", "Preguntarle por el lugar"),
            ("El clima", "Comentar el tiempo"),
        ]
        claves = ["oficio", "rumores", "lugar", "clima"]
        if npc["relacion"] >= 8: items.append(("La politica del reino", "")); claves.append("politica")
        if npc["relacion"] >= 15: items.append(("Su familia", "")); claves.append("familia")
        if npc["relacion"] >= 20: items.append(("Su pasado", "")); claves.append("pasado")
        if npc["relacion"] >= 30: items.append(("Sus suenos", "")); claves.append("sueno")
        if npc["relacion"] >= 35: items.append(("Sus miedos", "")); claves.append("miedo")
        if npc["secreto"] and npc["relacion"] >= 45: items.append(("Sus secretos", "")); claves.append("secreto")
        vende_util = any((p in PRODUCTOS_COMPRABLES_JUGADOR or es_item_equipable(p)) and c_ > 0
                          for p, c_ in npc["inventario"].items())
        if vende_util:
            items.append(("Comprarle algo", "")); claves.append("comprar")
        if jugador["inventario"]:
            items.append(("Venderle algo", "")); claves.append("vender")
        items.append(("Ver su inventario", "")); claves.append("ver_inv")
        items.append(("Despedirte", "")); claves.append("salir")
        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        accion = claves[idx]
        if accion == "salir":
            limpiar(); titulo(npc["nombre"].upper())
            despedidas = ["Que el Sol te acompane.", "Vete con cuidado.", "Nos veremos."]
            if tiene(npc, "gruñón"): despedidas = ["Ya era hora.", "Vete."]
            elif tiene(npc, "amable"): despedidas = ["Que te vaya bien.", "Vuelve cuando quieras."]
            narrar(f"\"{random.choice(despedidas)}\"")
            guardar_npc(conn, npc); pausa(); return
        if accion == "ver_inv":
            limpiar(); titulo(f"INVENTARIO DE {npc['nombre'].upper()}")
            if not npc["inventario"]: narrar("No tiene nada.")
            else:
                for p, c_ in npc["inventario"].items():
                    if es_item_equipable(p):
                        print(f"  {nombre_bonito_item(p)}: {c_} unidades")
                    else:
                        precio = _precio_jugador(conn, p, jugador, ciudad_jugador)
                        print(f"  {p}: {c_} unidades (a {precio} monedas cada una aqui)")
            pausa(); continue
        if accion == "vender":
            _vender_a_npc(conn, jugador, npc, mundo); continue
        if accion == "comprar":
            opciones_compra = []
            for p, c_ in npc["inventario"].items():
                if c_ <= 0: continue
                if p in PRODUCTOS and p in PRODUCTOS_COMPRABLES_JUGADOR:
                    precio = _precio_jugador(conn, p, jugador, ciudad_jugador)
                    opciones_compra.append((p, c_, precio, p))
                elif es_item_equipable(p):
                    item = obtener_item(p)
                    if item:
                        rep = obtener_reputacion(conn, jugador["identificador"], ciudad_jugador)
                        multi = multiplicador_precio_reputacion(rep)
                        precio = max(1, int(item["precio"] * multi))
                        opciones_compra.append((item["nombre"], c_, precio, p))
            if not opciones_compra:
                limpiar(); titulo(npc["nombre"].upper()); narrar("No tiene nada que venderte.")
                pausa(); continue
            def contexto_compra():
                titulo(f"COMPRAR A {npc['nombre'].upper()}")
                print(f"  Tu dinero: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
                print(f"  {C.DIM}(precios ya incluyen tu reputacion){C.RESET}")
            items_c = [(nombre_mostrar, f"{c_} disponibles - {pr} monedas cada uno")
                       for nombre_mostrar, c_, pr, _ in opciones_compra]
            idx2 = menu_flechas(items_c, contexto_fn=contexto_compra, permitir_cancelar=True)
            if idx2 == -1: continue
            nombre_mostrar, cant_disp, precio_u, prod_id = opciones_compra[idx2]
            max_posible = min(cant_disp, jugador["dinero"] // precio_u)
            if max_posible <= 0:
                limpiar(); titulo(npc["nombre"].upper())
                narrar(f"{C.RED}No tienes suficiente dinero.{C.RESET}"); pausa(); continue
            limpiar(); titulo(f"COMPRAR {nombre_mostrar.upper()}")
            print(f"  Precio unitario: {C.YELLOW}{precio_u}{C.RESET} monedas")
            print(f"  Tu dinero: {C.YELLOW}{jugador['dinero']}{C.RESET}")
            print(f"  {C.DIM}El vendedor tiene {cant_disp} disponibles.{C.RESET}")
            print(f"  {C.DIM}Puedes comprar hasta {max_posible}.{C.RESET}\n")
            print(f"  ¿Cuantas unidades quieres?")
            cant = pedir_numero(max_posible)
            total = cant * precio_u
            def contexto_confirmar_compra():
                titulo("CONFIRMAR COMPRA")
                print(f"  {C.BOLD}Producto:{C.RESET}          {nombre_mostrar}")
                print(f"  {C.BOLD}Precio unitario:{C.RESET}   {precio_u} monedas")
                print(f"  {C.BOLD}Cantidad:{C.RESET}          {cant}")
                print(f"  {C.BOLD}Total a pagar:{C.RESET}    {C.YELLOW}{total}{C.RESET} monedas")
                print(f"  {C.BOLD}Dinero restante:{C.RESET}  {jugador['dinero'] - total} monedas")
                print()
                print(f"  {C.DIM}¿Confirmas la compra?{C.RESET}")
            if menu_flechas([("Confirmar compra", ""), ("Cancelar", "")],
                             contexto_fn=contexto_confirmar_compra, permitir_cancelar=False) == 1:
                continue
            jugador["dinero"] -= total; npc["dinero"] += total
            npc["inventario"][prod_id] -= cant
            if npc["inventario"][prod_id] <= 0: del npc["inventario"][prod_id]
            if cant > 1: jugador["inventario"].append(f"{cant}x {prod_id}")
            else: jugador["inventario"].append(prod_id)
            c = conn.cursor()
            c.execute("""INSERT INTO transacciones (dia, comprador, vendedor, producto, cantidad, precio_total)
                         VALUES (?,?,?,?,?,?)""",
                      (dia, jugador["nombre"], npc["nombre"], prod_id, cant, total))
            conn.commit(); guardar_npc(conn, npc); guardar_jugador(conn, jugador)
            limpiar(); titulo("COMPRA REALIZADA")
            narrar(f"Compras {cant} de {nombre_mostrar} por {total} monedas.")
            npc["relacion"] += 2; pausa(); continue
        etiquetas = {
            "oficio": f"Le preguntas sobre su trabajo como {npc['oficio'].lower()}.",
            "rumores": "Le preguntas si ha oido algo interesante.",
            "lugar": "Le preguntas sobre el lugar.", "clima": "Comentas algo sobre el clima.",
            "politica": "Le preguntas sobre la politica del reino.",
            "familia": "Le preguntas por su familia.",
            "pasado": "Le pides que te cuente sobre su vida.",
            "sueno": "Le preguntas que le gustaria hacer algun dia.",
            "miedo": "Le preguntas que es lo que mas teme.",
            "secreto": "Le preguntas si guarda algun secreto.",
        }
        limpiar(); titulo(npc["nombre"].upper())
        narrar(etiquetas.get(accion, "Hablas con el."))
        resp = generar_respuesta(conn, npc, accion, jugador, dia)
        narrar(f"\"{resp}\"")
        npc["relacion"] += 2; guardar_npc(conn, npc); pausa()
        if random.random() < 0.35 and accion not in ("secreto",):
            npc_hace_pregunta(conn, npc, jugador, dia)


def _vender_a_npc(conn, jugador, npc, mundo):
    if not jugador["inventario"]:
        limpiar(); titulo("VENDER"); narrar("No tienes nada que vender."); pausa(); return
    idx = _menu_inventario_agrupado(
        jugador["inventario"],
        contexto_fn=lambda: titulo(f"VENDER A {npc['nombre'].upper()}"),
        permitir_cancelar=True
    )
    if idx == -1: return
    item = jugador["inventario"][idx]
    prod = item.split("x ", 1)[1] if "x " in item else item
    cant = 1
    if "x " in item:
        try: cant = int(item.split("x ", 1)[0])
        except Exception: cant = 1
    if es_item_equipable(prod):
        item_data = obtener_item(prod)
        if not item_data:
            limpiar(); titulo("VENDER"); narrar("Item invalido."); pausa(); return
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
        cant_v = min(cant, max_dinero)
        total = precio_u * cant_v
        def contexto_venta_equipo():
            titulo("CONFIRMAR VENTA")
            print(f"  {C.BOLD}Item:{C.RESET}              {item_data['nombre']}")
            print(f"  {C.BOLD}Valor base:{C.RESET}        {precio_base} monedas")
            print(f"  {C.BOLD}Cantidad:{C.RESET}          {cant_v} de {cant}")
            print(f"  {C.BOLD}Precio por unidad:{C.RESET} {C.YELLOW}{precio_u}{C.RESET} monedas")
            print(f"  {C.BOLD}Total a recibir:{C.RESET}   {C.GREEN}{total}{C.RESET} monedas")
            print()
            print(f"  {C.DIM}Motivo del precio: {razon}{C.RESET}")
            if cant_v < cant:
                print(f"  {C.DIM}(Solo te compra {cant_v} porque no le alcanza el dinero){C.RESET}")
            print()
            print(f"  {C.DIM}¿Confirmas la venta?{C.RESET}")
        if menu_flechas([("Confirmar venta", ""), ("Cancelar", "")],
                         contexto_fn=contexto_venta_equipo, permitir_cancelar=False) == 1:
            return
        jugador["dinero"] += total; npc["dinero"] -= total
        npc["inventario"][prod] = npc["inventario"].get(prod, 0) + cant_v
        if cant_v >= cant: jugador["inventario"].pop(idx)
        else: jugador["inventario"][idx] = f"{cant - cant_v}x {prod}"
        guardar_jugador(conn, jugador); guardar_npc(conn, npc)
        limpiar(); titulo("VENTA REALIZADA")
        narrar(f"Vendes {cant_v} de {item_data['nombre']} por {total} monedas.")
        pausa(); return
    if prod not in PRODUCTOS:
        limpiar(); titulo("VENDER"); narrar(f"No hay mercado para '{prod}'."); pausa(); return
    ciudad = jugador.get("ciudad", "capital_imperial")
    precio_local = precio_actual(conn, prod, ciudad=ciudad)
    from venefar_jugador_acciones import OFICIOS_COMPRADORES
    interesados = OFICIOS_COMPRADORES.get(npc["oficio"], [])
    if prod in interesados:
        multi = 0.70
        razon = f"{npc['oficio']} necesita {prod} para su oficio. Paga 70%."
    else:
        multi = 0.50
        razon = f"{npc['oficio']} no usa {prod}. Paga 50%."
    precio_u = max(1, int(precio_local * multi))
    max_dinero = npc["dinero"] // precio_u
    if max_dinero <= 0:
        limpiar(); titulo("VENDER")
        narrar(f"{npc['nombre']} no puede pagarte eso.")
        print(f"  {C.DIM}Precio por unidad: {precio_u} monedas{C.RESET}")
        print(f"  {C.DIM}Dinero de {npc['nombre']}: {npc['dinero']} monedas{C.RESET}")
        pausa(); return
    cant_v = min(cant, max_dinero)
    total = precio_u * cant_v
    def contexto_venta_normal():
        titulo("CONFIRMAR VENTA")
        print(f"  {C.BOLD}Producto:{C.RESET}          {prod}")
        print(f"  {C.BOLD}Precio local:{C.RESET}      {precio_local} monedas")
        print(f"  {C.BOLD}Cantidad:{C.RESET}          {cant_v} de {cant}")
        print(f"  {C.BOLD}Precio por unidad:{C.RESET} {C.YELLOW}{precio_u}{C.RESET} monedas")
        print(f"  {C.BOLD}Total a recibir:{C.RESET}   {C.GREEN}{total}{C.RESET} monedas")
        print()
        print(f"  {C.DIM}Motivo del precio: {razon}{C.RESET}")
        if cant_v < cant:
            print(f"  {C.DIM}(Solo te compra {cant_v} porque no le alcanza el dinero){C.RESET}")
        print()
        print(f"  {C.DIM}¿Confirmas la venta?{C.RESET}")
    if menu_flechas([("Confirmar venta", ""), ("Cancelar", "")],
                     contexto_fn=contexto_venta_normal, permitir_cancelar=False) == 1:
        return
    jugador["dinero"] += total; npc["dinero"] -= total
    npc["inventario"][prod] = npc["inventario"].get(prod, 0) + cant_v
    if cant_v >= cant: jugador["inventario"].pop(idx)
    else: jugador["inventario"][idx] = f"{cant - cant_v}x {prod}"
    from venefar_reputacion import modificar_reputacion
    if total >= 20:
        modificar_reputacion(conn, jugador["identificador"], ciudad, 1, "venta")
    guardar_jugador(conn, jugador); guardar_npc(conn, npc)
    limpiar(); titulo("VENTA REALIZADA")
    narrar(f"Vendes {cant_v} de {prod} a {npc['nombre']} por {total} monedas.")
    pausa()


def menu_viajar(conn, jugador, npcs_globales, mundo):
    ciudad_actual = jugador.get("ciudad", "capital_imperial")
    conexiones = conexiones_de(ciudad_actual)
    if not conexiones:
        limpiar(); titulo("VIAJAR"); narrar("Desde aqui no hay caminos."); pausa(); return
    def contexto():
        titulo("VIAJAR")
        print(f"  Estas en: {C.BOLD}{obtener_nombre(ciudad_actual)}{C.RESET}")
        print(f"  {C.DIM}Elige tu destino.{C.RESET}")
    items = []; destinos = []
    for dest_id, (dias, peligro) in conexiones.items():
        dest_nombre = obtener_nombre(dest_id)
        nivel, _ = NIVELES_PELIGRO[peligro]
        items.append((dest_nombre, f"{dias} dia(s) - {nivel}"))
        destinos.append((dest_id, dias, peligro))
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    destino_id, dias, peligro = destinos[idx]
    escolta = False
    if peligro >= 2:
        coste_escolta = 5 * dias * peligro
        if jugador["dinero"] >= coste_escolta:
            limpiar(); titulo("CONTRATAR ESCOLTA")
            narrar(f"La ruta hacia {obtener_nombre(destino_id)} es peligrosa.")
            narrar(f"Puedes contratar una escolta por {coste_escolta} monedas.")
            resp = menu_flechas([
                ("Contratar escolta", f"Coste: {coste_escolta} monedas. Reduce asaltos."),
                ("Viajar sin escolta", "Gratis, pero mas peligroso."),
            ], contexto_fn=lambda: None, permitir_cancelar=False)
            if resp == 0:
                jugador["dinero"] -= coste_escolta
                escolta = True
                narrar(f"Contratas una escolta por {coste_escolta} monedas.")
            pausa()
    viajar(conn, jugador, npcs_globales, mundo, destino_id, dias, peligro, escolta)


def viajar(conn, jugador, npcs_globales, mundo, destino_id, dias, peligro, escolta):
    origen_nombre = obtener_nombre(jugador.get("ciudad", "capital_imperial"))
    destino_nombre = obtener_nombre(destino_id)
    nivel, desc = NIVELES_PELIGRO[peligro]
    limpiar(); titulo(f"VIAJE A {destino_nombre.upper()}")
    narrar(f"Partes de {origen_nombre} hacia {destino_nombre}.")
    narrar(f"El viaje tomara {dias} dia(s).")
    print(f"  {C.DIM}Peligrosidad: {nivel} - {desc}{C.RESET}")
    if escolta: print(f"  {C.GREEN}Vas con escolta.{C.RESET}")
    pausa()
    for d in range(dias):
        limpiar(); titulo(f"DIA {d + 1} DE VIAJE · {formatear_fecha(mundo['dia'])}")
        ultimo = (d == dias - 1)
        avanzar_un_dia(conn, npcs_globales, mundo, jugador, guardar=ultimo)
        prob_bandidos = [0.0, 0.10, 0.30, 0.55][peligro]
        if escolta: prob_bandidos *= 0.25
        if random.random() < prob_bandidos:
            _ataque_bandidos(jugador, peligro)
        else:
            prob_encuentro = [0.25, 0.40, 0.55, 0.70][peligro]
            if random.random() < prob_encuentro:
                enc = generar_encuentro(peligro)
                narrar(enc["texto"])
                if enc.get("monedas"):
                    jugador["dinero"] += enc["monedas"]
                    narrar(f"{C.GREEN}Ganas {enc['monedas']} monedas.{C.RESET}")
            else:
                narrar("El dia pasa sin incidentes.")
        pausa()
    jugador["ciudad"] = destino_id
    guardar_jugador(conn, jugador)
    limpiar(); titulo(f"HAS LLEGADO A {destino_nombre.upper()}")
    ya_vista = destino_id in jugador.get("ciudades_vistas", [])
    imprimir_descripcion_ciudad(destino_id, primera_vez=not ya_vista)
    if not ya_vista:
        jugador.setdefault("ciudades_vistas", []).append(destino_id)
        guardar_jugador(conn, jugador)
    pausa()


def _ataque_bandidos(jugador, peligro):
    limpiar(); titulo("¡BANDIDOS!")
    narrar("Un grupo de bandidos sale del bosque. Te rodean.")
    narrar("\"El dinero o la vida, forastero.\"")
    factor = [0.0, 0.20, 0.35, 0.50][peligro]
    robo = int(jugador["dinero"] * factor)
    robo = max(robo, min(5, jugador["dinero"]))
    if jugador["dinero"] <= 0:
        narrar("Los bandidos te registran y no encuentran nada.")
        jugador["salud"] = max(0, jugador["salud"] - 5)
        print(f"  {C.RED}Te dan un golpe. Salud -5.{C.RESET}")
        return
    jugador["dinero"] -= robo
    narrar(f"Te quitan {robo} monedas y se marchan entre risas.")
    print(f"  {C.RED}Dinero perdido: {robo}{C.RESET}")
    print(f"  {C.YELLOW}Dinero restante: {jugador['dinero']}{C.RESET}")
    dano = random.randint(5, 15)
    jugador["salud"] = max(0, jugador["salud"] - dano)
    print(f"  {C.RED}Te dan una paliza. Salud -{dano}.{C.RESET}")


def generar_encuentro(peligro):
    if peligro == 0:
        pool = [
            {"texto": "Ves un ciervo cruzar el camino. Nada mas."},
            {"texto": "Un mercader solitario te saluda y sigue su camino."},
            {"texto": "Pasas junto a una granja abandonada."},
            {"texto": "Un campesino te ofrece agua de su pozo."},
            {"texto": "Encuentras una bolsa con 3 monedas.", "monedas": 3},
        ]
    elif peligro == 1:
        pool = [
            {"texto": "Un grupo de peregrinos canta mientras camina."},
            {"texto": "Ves huellas de lobo en el barro."},
            {"texto": "Un cazador te saluda desde lejos."},
            {"texto": "Encuentras una posada abandonada."},
        ]
    elif peligro == 2:
        pool = [
            {"texto": "Pasas junto a los restos de una caravana asaltada."},
            {"texto": "Un mendigo te advierte de bandidos mas adelante."},
            {"texto": "Encuentras una daga rota en el camino."},
        ]
    else:
        pool = [
            {"texto": "Oyes gritos a lo lejos. Apresuras el paso."},
            {"texto": "Ves cuerpos colgando de un arbol."},
            {"texto": "Un lobo te observa desde lo alto de una colina."},
        ]
    return random.choice(pool)


def menu_hablar(conn, jugador, npcs_ciudad, mundo):
    ciudad_id = jugador.get("ciudad", "capital_imperial")
    ciudad_nombre = obtener_nombre(ciudad_id)
    def contexto():
        titulo(f"HABLAR CON GENTE EN {ciudad_nombre.upper()}")
        print(f"  {C.DIM}{len(npcs_ciudad)} personas en esta zona.{C.RESET}")
    if not npcs_ciudad:
        limpiar(); titulo("HABLAR CON GENTE"); narrar("No hay nadie aqui."); pausa(); return
    items = []
    for npc in npcs_ciudad:
        rel = f" [relacion: {npc['relacion']}]" if npc["relacion"] != 0 else ""
        items.append((npc["nombre"] + rel, f"{npc['oficio']} - {npc['detalle']}"))
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    conversar(conn, jugador, npcs_ciudad[idx], mundo)


def menu_avanzar(conn, jugador, npcs_globales, mundo):
    def contexto():
        titulo("AVANZAR EL TIEMPO")
        print(f"Hoy es {formatear_fecha(mundo['dia'])}")
        print(f"Estacion: {obtener_estacion(mundo['dia'])}")
    items = [("Avanzar 1 dia", ""), ("Avanzar 1 semana (7 dias)", ""), ("Avanzar 1 mes (30 dias)", "")]
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    cant = [1, 7, 30][idx]
    dia_inicial = mundo["dia"]
    limpiar(); titulo(f"SIMULANDO {cant} DIAS...")
    print(f"  {C.DIM}Por favor espera.{C.RESET}\n")
    for i in range(cant):
        ultimo = (i == cant - 1)
        avanzar_un_dia(conn, npcs_globales, mundo, jugador, guardar=ultimo)
        if (i + 1) % 5 == 0 or ultimo:
            print(f"  {formatear_fecha(mundo['dia'])}")
    guardar_todos(conn, npcs_globales); guardar_jugador(conn, jugador)
    c = conn.cursor(); c.execute("UPDATE mundo SET dia=? WHERE id=1", (mundo["dia"],)); conn.commit()
    c = conn.cursor()
    c.execute("SELECT * FROM eventos WHERE dia > ? AND tipo='mundo' ORDER BY dia ASC", (dia_inicial,))
    eventos_mundo = c.fetchall()
    if eventos_mundo:
        limpiar(); print(); linea("=", 62)
        print(f"{C.BOLD}{C.YELLOW}{'  EVENTOS DEL MUNDO  '.center(62)}{C.RESET}")
        linea("=", 62)
        for e in eventos_mundo:
            print(f"\n  {C.BOLD}{C.MAGENTA}[{formatear_fecha_corta(e['dia'])}]{C.RESET}")
            print(f"  {C.YELLOW}{e['descripcion']}{C.RESET}")
        print(); linea("-", 62); pausa()
    c = conn.cursor()
    c.execute("SELECT * FROM eventos WHERE dia > ? ORDER BY dia DESC LIMIT 15", (dia_inicial,))
    eventos = c.fetchall()
    c.execute("SELECT * FROM transacciones WHERE dia > ? ORDER BY dia DESC LIMIT 10", (dia_inicial,))
    trans = c.fetchall()
    limpiar(); titulo(f"PERIODO SIMULADO: {cant} DIAS")
    print(f"  {formatear_fecha(dia_inicial)} → {formatear_fecha(mundo['dia'])}\n")
    print(f"{C.BOLD}{C.CYAN}EVENTOS{C.RESET}"); linea()
    if not eventos: narrar("No ha pasado nada destacable.")
    else:
        for e in eventos:
            print(f"  {C.YELLOW}{formatear_fecha_corta(e['dia'])}{C.RESET} {C.DIM}[{e['tipo']}]{C.RESET}")
            print(f"     {e['descripcion']}"); print()
    if trans:
        print(f"{C.BOLD}{C.CYAN}TRANSACCIONES{C.RESET}"); linea()
        for t in trans:
            print(f"  {C.YELLOW}{formatear_fecha_corta(t['dia'])}{C.RESET} {t['comprador']} compro {t['cantidad']}x {t['producto']} a {t['vendedor']} por {t['precio_total']} monedas")
        print()
    pausa()


def accion_comer(conn, jugador):
    def contexto(): titulo("COMER"); print(f"Hambre actual: {jugador['hambre']}/100")
    if jugador["hambre"] > 80:
        limpiar(); titulo("COMER"); narrar("No tienes hambre."); pausa(); return
    items = [("Comida sencilla (2 monedas)", "Sube el hambre 50 puntos"),
             ("Buena comida (5 monedas)", "Sube el hambre 80 puntos")]
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    coste, ganancia = [(2, 50), (5, 80)][idx]
    limpiar(); titulo("COMER")
    if jugador["dinero"] >= coste:
        jugador["dinero"] -= coste
        jugador["hambre"] = min(100, jugador["hambre"] + ganancia)
        narrar("Comes con calma."); guardar_jugador(conn, jugador)
    else: narrar(f"{C.RED}No tienes dinero suficiente.{C.RESET}")
    pausa()


def accion_beber(conn, jugador):
    def contexto(): titulo("BEBER"); print(f"Sed actual: {jugador['sed']}/100")
    if jugador["sed"] > 80:
        limpiar(); titulo("BEBER"); narrar("No tienes sed."); pausa(); return
    items = [("Agua (1 moneda)", "Sube la sed 60 puntos"), ("Vino (3 monedas)", "Sube la sed 40 puntos")]
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    coste, ganancia = [(1, 60), (3, 40)][idx]
    limpiar(); titulo("BEBER")
    if jugador["dinero"] >= coste:
        jugador["dinero"] -= coste
        jugador["sed"] = min(100, jugador["sed"] + ganancia)
        narrar("Bebes."); guardar_jugador(conn, jugador)
    else: narrar(f"{C.RED}No tienes dinero suficiente.{C.RESET}")
    pausa()


def accion_descansar(conn, jugador):
    def contexto():
        titulo("DESCANSAR"); print(f"Energia: {jugador['energia']}/100")
        print(f"Cansancio: {jugador['cansancio']}/100")
    items = [("Siesta corta (2 horas)", "Recupera 30 de energia"),
             ("Dormir toda la noche", "Recupera toda la energia")]
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    limpiar(); titulo("DESCANSAR")
    if idx == 0:
        jugador["energia"] = min(100, jugador["energia"] + 30)
        jugador["cansancio"] = max(0, jugador["cansancio"] - 20)
        narrar("Descansas un rato.")
    else:
        jugador["energia"] = 100; jugador["cansancio"] = 0
        ciudad = jugador.get("ciudad", "capital_imperial")
        if tiene_casa(conn, jugador["identificador"], ciudad):
            jugador["hambre"] = max(0, jugador["hambre"] - 30)
            jugador["sed"] = max(0, jugador["sed"] - 30)
            jugador["salud"] = min(100, jugador["salud"] + 15)
            narrar("Duermes en tu casa. Despiertas completamente renovado.")
            print(f"  {C.GREEN}Bonus de casa: Salud +15, Hambre -30, Sed -30.{C.RESET}")
        else:
            jugador["hambre"] = max(0, jugador["hambre"] - 20)
            jugador["sed"] = max(0, jugador["sed"] - 20)
            narrar("Duermes toda la noche.")
    guardar_jugador(conn, jugador); pausa()


def menu_inventario(jugador):
    while True:
        def contexto():
            titulo("INVENTARIO COMPLETO")
            print(f"  Dinero: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
            print(f"  {C.DIM}Elige un objeto para verlo en detalle.{C.RESET}")
        if not jugador["inventario"]:
            limpiar(); titulo("INVENTARIO COMPLETO"); narrar("No llevas nada."); pausa(); return
        idx = _menu_inventario_agrupado(jugador["inventario"],
                                         contexto_fn=contexto,
                                         permitir_cancelar=True)
        if idx == -1: return
        nombre = jugador["inventario"][idx]
        item_id = nombre.split("x ", 1)[1] if "x " in nombre else nombre
        limpiar()
        if es_item_equipable(item_id):
            item = obtener_item(item_id)
            titulo(item["nombre"].upper())
            print(f"  Tipo: {item['tipo']}")
            if item["tipo"] == "arma":
                print(f"  Dano: {item['dano_min']}-{item['dano_max']}")
                print(f"  Velocidad: {item['velocidad']}/5")
                print(f"  Alcance: {item['alcance']}")
            else:
                print(f"  Defensa: {item['defensa']}")
                print(f"  Slot: {item['slot']}")
            print(f"  Peso: {item['peso']} kg")
            print(f"  Valor: {item['precio']} monedas")
            print(f"  Requisito fuerza: {item['req_fuerza']}")
            if item.get("dos_manos"): print(f"  {C.DIM}(a dos manos){C.RESET}")
            pausa()
        else:
            titulo(nombre.upper())
            imprimir_descripcion_objeto(nombre); pausa()


def menu_eventos(conn, mundo):
    limpiar(); titulo("CRONICA DEL MUNDO")
    c = conn.cursor()
    c.execute("SELECT * FROM eventos ORDER BY dia DESC LIMIT 60")
    eventos = c.fetchall()
    if not eventos:
        narrar("No hay eventos.")
    else:
        for e in eventos:
            color_tipo = {
                "guarnicion": C.CYAN,
                "comercio": C.GREEN,
                "mundo": C.MAGENTA,
            }.get(e["tipo"], C.YELLOW)
            print(f"  {C.YELLOW}{formatear_fecha_corta(e['dia'])}{C.RESET} {color_tipo}[{e['tipo']}]{C.RESET}")
            print(f"     {e['descripcion']}")
    pausa()


def menu_eventos_activos(conn):
    limpiar(); titulo("EVENTOS ACTIVOS DEL MUNDO")
    activos = listar_eventos_activos(conn)
    if not activos:
        narrar("No hay eventos activos en este momento."); pausa(); return
    for ev in activos:
        datos = ev["datos"]
        print(f"  {C.BOLD}{C.YELLOW}{datos.get('descripcion', 'Evento')}{C.RESET}")
        print(f"     {C.DIM}Dias restantes: {ev['dias_restantes']}{C.RESET}")
        efectos = datos.get("efectos", {})
        precios = efectos.get("precios", {})
        if precios:
            print(f"     {C.MAGENTA}Productos afectados:{C.RESET}", end=" ")
            for prod, multi in precios.items():
                signo = "+" if multi > 1 else "-"
                pct = abs(int((multi - 1) * 100))
                print(f"{prod}({signo}{pct}%)", end=" ")
            print()
        print()
    pausa()


def menu_reputacion(conn, jugador):
    limpiar(); titulo("MI REPUTACION")
    todas = obtener_todas(conn, jugador["identificador"])
    ciudad_actual = jugador.get("ciudad", "capital_imperial")
    filas = []
    for cid in CIUDADES.keys():
        valor = todas.get(cid, 0)
        filas.append((cid, valor))
    filas.sort(key=lambda x: (x[0] != ciudad_actual, -x[1]))
    for cid, valor in filas:
        etiqueta, color = etiqueta_reputacion(valor)
        marca = " <-- Estas aqui" if cid == ciudad_actual else ""
        nombre = obtener_nombre(cid)
        print(f"  {C.WHITE}{nombre:<15}{C.RESET} {color}{etiqueta:<12}{C.RESET} ({valor:>4}){marca}")
    print()
    print(f"  {C.DIM}La reputacion afecta a los precios, la actitud de los")
    print(f"  habitantes y tu acceso a favores.{C.RESET}")
    pausa()


def menu_economia(conn, npcs_globales, jugador):
    ciudad_jugador = jugador.get("ciudad", "capital_imperial")
    ciudad_nombre = obtener_nombre(ciudad_jugador)
    rep = obtener_reputacion(conn, jugador["identificador"], ciudad_jugador)
    etiqueta, color_rep = etiqueta_reputacion(rep)
    multi = multiplicador_precio_reputacion(rep)
    limpiar(); titulo(f"ECONOMIA DE {ciudad_nombre.upper()}")
    print(f"  Tu reputacion aqui: {color_rep}{etiqueta} ({rep}){C.RESET}")
    if multi != 1.0:
        pct = int((multi - 1) * 100)
        signo = "+" if pct > 0 else ""
        print(f"  {C.YELLOW}Precios de compra para ti: {signo}{pct}%{C.RESET}")
    print()
    print(f"{C.BOLD}{C.CYAN}PRECIOS EN ESTA CIUDAD (para ti){C.RESET}"); linea()
    limpiar_cache_precios()
    for prod in list(PRODUCTOS.keys())[:25]:
        p = _precio_jugador(conn, prod, jugador, ciudad_jugador)
        base = PRODUCTOS[prod]["base"]
        if p > base: color, flecha = C.RED, "^"
        elif p < base: color, flecha = C.GREEN, "v"
        else: color, flecha = C.WHITE, "="
        print(f"  {prod:<15} {color}{p:>3} {flecha}{C.RESET}  {C.DIM}(base {base}){C.RESET}")
    print()
    print(f"{C.BOLD}{C.CYAN}RIQUEZA GLOBAL (top 15){C.RESET}"); linea()
    for npc in sorted(npcs_globales, key=lambda n: -n["dinero"])[:15]:
        ciudad_corta = obtener_nombre(npc.get("ciudad", "?"))[:12]
        print(f"  {npc['nombre']:<22} {C.DIM}({ciudad_corta}){C.RESET} {C.YELLOW}{npc['dinero']:>5}{C.RESET}")
    print()
    pausa()


def menu_comparar_precios(conn, jugador):
    limpiar(); titulo("COMPARAR PRECIOS ENTRE CIUDADES")
    print(f"  {C.DIM}Elige un producto para comparar.{C.RESET}\n")
    prods = ["Trigo", "Pan", "Cerveza", "Hierro", "Mineral", "Herramientas",
             "Madera", "Pescado", "Carne", "Piedra", "Carbón", "Lana", "Tela", "Vino"]
    items = [(p, "") for p in prods]
    idx = menu_flechas(items, contexto_fn=lambda: None, permitir_cancelar=True)
    if idx == -1: return
    prod = prods[idx]
    limpiar_cache_precios()
    ciudad_jugador = jugador.get("ciudad", "capital_imperial")
    filas = []
    for cid in CIUDADES.keys():
        precio = _precio_jugador(conn, prod, jugador, cid)
        filas.append((cid, precio))
    filas.sort(key=lambda x: x[1])
    limpiar(); titulo(f"PRECIO DE {prod.upper()} POR CIUDAD")
    print(f"  {C.BOLD}Ciudad{C.RESET}                    {C.BOLD}Precio{C.RESET}"); linea()
    for cid, precio in filas:
        nombre = obtener_nombre(cid)
        marca = " <-- Estas aqui" if cid == ciudad_jugador else ""
        color = C.YELLOW if cid == ciudad_jugador else C.WHITE
        print(f"  {color}{nombre:<22}{C.RESET} {precio:>3} monedas{marca}")
    print()
    if filas:
        b_cid, b_p = filas[0]; c_cid, c_p = filas[-1]
        diff = c_p - b_p
        if diff >= 3:
            print(f"  {C.GREEN}Oportunidad:{C.RESET} comprar en {obtener_nombre(b_cid)} ({b_p})")
            print(f"              y vender en {obtener_nombre(c_cid)} ({c_p})")
            print(f"              Ganancia potencial: {diff} monedas por unidad.")
        else: print(f"  {C.DIM}No hay diferencias grandes.{C.RESET}")
    pausa()


def menu_npc_detalle(conn, npcs_ciudad):
    def contexto():
        ciudad_id = npcs_ciudad[0]["ciudad"] if npcs_ciudad else "?"
        titulo(f"PERSONAJES DE {obtener_nombre(ciudad_id).upper()}")
    if not npcs_ciudad:
        limpiar(); titulo("PERSONAJES"); narrar("No hay nadie aqui."); pausa(); return
    items = [(npc["nombre"], npc["oficio"]) for npc in npcs_ciudad]
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=True)
    if idx == -1: return
    npc = npcs_ciudad[idx]
    limpiar(); titulo(npc["nombre"].upper())
    print(f"  Oficio: {npc['oficio']}"); print(f"  Ciudad: {obtener_nombre(npc['ciudad'])}")
    print(f"  Edad: {npc['edad']}"); print(f"  Rasgos: {', '.join(npc['rasgos'])}")
    print(f"  Estado: {npc['mood']}"); print(f"  Relacion: {npc['relacion']}")
    print(f"  Dinero: {npc['dinero']} monedas"); print()
    if npc["inventario"]:
        print(f"{C.BOLD}{C.CYAN}INVENTARIO{C.RESET}"); linea()
        for p, c_ in npc["inventario"].items():
            print(f"  {nombre_bonito_item(p)}: {c_}")
        print()
    c = conn.cursor()
    c.execute("SELECT * FROM recuerdos WHERE npc_id=? ORDER BY dia DESC LIMIT 6", (npc["id"],))
    recs = c.fetchall()
    if recs:
        print(f"{C.BOLD}{C.CYAN}RECUERDOS{C.RESET}"); linea()
        for rec in recs:
            print(f"  {C.DIM}{formatear_fecha_corta(rec['dia'])} [{rec['tipo']}]{C.RESET}")
            print(f"     {rec['contenido'][:80]}")
    pausa()


def menu_principal(conn, jugador, npcs_globales, mundo):
    while True:
        ciudad_id = jugador.get("ciudad", "capital_imperial")
        ciudad_nombre = obtener_nombre(ciudad_id)
        npcs_ciudad = [n for n in npcs_globales if n.get("ciudad") == ciudad_id]
        rep_actual = obtener_reputacion(conn, jugador["identificador"], ciudad_id)
        etq_rep, col_rep = etiqueta_reputacion(rep_actual)
        tiene_negocio_aqui = any(n["ciudad"] == ciudad_id for n in listar_negocios(conn, jugador["identificador"]))
        num_caravanas_activas = len([c for c in listar_caravanas(conn, jugador["identificador"])
                                      if c["estado"] == "en_camino"])
        guarnicion = obtener_guarnicion(conn, ciudad_id)
        def contexto():
            estacion = obtener_estacion(mundo["dia"])
            titulo(f"{ciudad_nombre.upper()} · {formatear_fecha(mundo['dia'])}")
            print(f"  {C.DIM}{estacion}{C.RESET}\n")
            print(f"  {C.BOLD}{jugador['nombre']}{C.RESET}  {col_rep}({etq_rep}){C.RESET}\n")
            sal = C.RED if jugador["salud"] < 40 else C.GREEN
            ene = C.RED if jugador["energia"] < 30 else C.GREEN
            ham = C.RED if jugador["hambre"] < 40 else C.GREEN
            sed = C.RED if jugador["sed"] < 40 else C.GREEN
            can = C.RED if jugador["cansancio"] > 60 else C.GREEN
            print(f"  Salud:     {sal}{barra_estado(jugador['salud'])}{C.RESET} {jugador['salud']:>3}")
            print(f"  Energia:   {ene}{barra_estado(jugador['energia'])}{C.RESET} {jugador['energia']:>3}")
            print(f"  Hambre:    {ham}{barra_estado(jugador['hambre'])}{C.RESET} {jugador['hambre']:>3}")
            print(f"  Sed:       {sed}{barra_estado(jugador['sed'])}{C.RESET} {jugador['sed']:>3}")
            print(f"  Cansancio: {can}{barra_estado(jugador['cansancio'])}{C.RESET} {jugador['cansancio']:>3}")
            print(f"  Dinero:    {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
            if jugador["inventario"]:
                llevo = ", ".join(nombre_bonito_item(x) for x in jugador["inventario"][:5])
                extra = "..." if len(jugador["inventario"]) > 5 else ""
                print(f"\n  {C.DIM}Llevas: {llevo}{extra}{C.RESET}")
            print(f"\n  {C.BOLD}{C.CYAN}Precios aqui:{C.RESET}", end=" ")
            limpiar_cache_precios()
            for prod in ["Pan", "Mineral", "Herramientas", "Vino"]:
                p = _precio_jugador(conn, prod, jugador, ciudad_id)
                base = PRODUCTOS[prod]["base"]
                if p > base: col, fl = C.RED, "^"
                elif p < base: col, fl = C.GREEN, "v"
                else: col, fl = C.WHITE, "="
                print(f"{prod}({col}{p}{fl}{C.RESET})", end=" ")
            print()
            c = conn.cursor()
            c.execute("SELECT * FROM eventos ORDER BY dia DESC LIMIT 3")
            eventos = c.fetchall()
            if eventos:
                print(f"\n  {C.BOLD}{C.CYAN}Ultimos sucesos:{C.RESET}")
                for e in eventos:
                    print(f"    {C.DIM}{formatear_fecha_corta(e['dia'])} [{e['tipo']}]{C.RESET} {e['descripcion'][:50]}")
        items = [
            ("Observar el lugar", "Ver descripcion"),
            ("Viajar a otro lugar", "Ir a otro asentamiento"),
            ("Ver mapa del mundo", "Mapa completo"),
            ("Hablar con alguien", f"{len(npcs_ciudad)} personas aqui"),
            ("Buscar trabajo", "Ganar dinero en un dia"),
            ("Pedir limosna", "Conseguir algo de dinero"),
            ("Avanzar el tiempo", ""),
            ("Comer", f"Hambre: {jugador['hambre']}/100"),
            ("Beber", f"Sed: {jugador['sed']}/100"),
            ("Descansar / Dormir", f"Cansancio: {jugador['cansancio']}/100"),
            ("Ver inventario completo", "Examinar cada objeto"),
            ("Equipamiento", "Armas, armaduras, accesorios"),
            ("Vender objetos", "Vender a un NPC"),
            ("Propiedades y casa", "Comprar casa, cofre, negocios"),
        ]
        claves_items = ["observar", "viajar", "mapa", "hablar", "trabajar", "limosna",
                        "avanzar", "comer", "beber", "descansar", "inventario",
                        "equipamiento", "vender", "propiedades"]
        if hay_banco(ciudad_id):
            items.append(("Banco", "Depositar, retirar, prestamos"))
            claves_items.append("banco")
        if tiene_negocio_aqui:
            items.append(("Venta manual del negocio", "Vender al 100% en el mercado"))
            claves_items.append("venta_manual")
        if guarnicion:
            items.append(("Visitar guarnicion", f"Vender equipo militar (premium)"))
            claves_items.append("guarnicion")
        items.append(("Caravanas", f"Enviar mercancia · {num_caravanas_activas} en camino"))
        claves_items.append("caravanas")
        items.extend([
            ("Ver mi reputacion", "En todas las ciudades"),
            ("Ver economia de esta ciudad", ""),
            ("Comparar precios entre ciudades", ""),
            ("Ver eventos del mundo", "Eventos activos"),
            ("Ver personajes", ""),
            ("Ver cronica completa", ""),
            ("Salir", ""),
        ])
        claves_items.extend(["reputacion", "economia", "comparar", "eventos_mundo",
                              "npcs", "eventos", "salir"])
        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        accion = claves_items[idx]
        if accion == "salir":
            guardar_todos(conn, npcs_globales); guardar_jugador(conn, jugador)
            limpiar(); print(f"\n{C.DIM}Hasta pronto, {jugador['nombre']}.{C.RESET}\n"); return
        elif accion == "observar":
            limpiar(); titulo(ciudad_nombre.upper())
            imprimir_descripcion_ciudad(ciudad_id, primera_vez=True); pausa()
        elif accion == "viajar":
            menu_viajar(conn, jugador, npcs_globales, mundo)
            npcs_globales = cargar_npcs(conn)
        elif accion == "mapa":
            limpiar(); mostrar_mapa(ciudad_actual=ciudad_id); pausa()
        elif accion == "hablar": menu_hablar(conn, jugador, npcs_ciudad, mundo)
        elif accion == "trabajar":
            accion_trabajar(conn, jugador, npcs_globales, mundo)
            guardar_jugador(conn, jugador)
        elif accion == "limosna":
            accion_pedir_limosna(conn, jugador, npcs_globales, mundo)
            guardar_jugador(conn, jugador)
        elif accion == "avanzar": menu_avanzar(conn, jugador, npcs_globales, mundo)
        elif accion == "comer": accion_comer(conn, jugador)
        elif accion == "beber": accion_beber(conn, jugador)
        elif accion == "descansar": accion_descansar(conn, jugador)
        elif accion == "inventario": menu_inventario(jugador)
        elif accion == "equipamiento":
            menu_equipamiento(conn, jugador); guardar_jugador(conn, jugador)
        elif accion == "vender":
            if npcs_ciudad: accion_vender(conn, jugador, npcs_ciudad, mundo)
        elif accion == "propiedades":
            menu_propiedades(conn, jugador, mundo); guardar_jugador(conn, jugador)
        elif accion == "banco":
            menu_banco(conn, jugador, mundo); guardar_jugador(conn, jugador)
        elif accion == "venta_manual": menu_venta_manual(conn, jugador, mundo)
        elif accion == "guarnicion":
            menu_guarnicion(conn, jugador, mundo)
        elif accion == "caravanas":
            menu_caravanas(conn, jugador, mundo); guardar_jugador(conn, jugador)
        elif accion == "reputacion": menu_reputacion(conn, jugador)
        elif accion == "economia": menu_economia(conn, npcs_globales, jugador)
        elif accion == "comparar": menu_comparar_precios(conn, jugador)
        elif accion == "eventos_mundo": menu_eventos_activos(conn)
        elif accion == "npcs": menu_npc_detalle(conn, npcs_ciudad)
        elif accion == "eventos": menu_eventos(conn, mundo)


def main():
    limpiar(); print(); linea("=")
    print(f"{C.BOLD}{C.CYAN}{'VENEFAR - MUNDO VIVO'.center(62)}{C.RESET}")
    print(f"{C.DIM}{'El mundo continua sin ti'.center(62)}{C.RESET}")
    linea("="); print()
    conn = init_db()
    seed_inicial(conn)
    init_guarniciones(conn)
    c = conn.cursor()
    c.execute("SELECT * FROM mundo WHERE id=1")
    f = c.fetchone()
    mundo = {"dia": f["dia"], "estacion": f["estacion"]}
    jugador = elegir_personaje(conn)
    if not jugador:
        conn.close(); return
    if "espada_corta:hierro" not in jugador["inventario"]:
        jugador["inventario"].append("espada_corta:hierro")
    if "tunica:hierro" not in jugador["inventario"]:
        jugador["inventario"].append("tunica:hierro")
    if "zapatos:hierro" not in jugador["inventario"]:
        jugador["inventario"].append("zapatos:hierro")
    if "anillo_sello:hierro" not in jugador["inventario"]:
        jugador["inventario"].append("anillo_sello:hierro")
    guardar_jugador(conn, jugador)
    npcs_globales = cargar_npcs(conn)
    ciudad_id = jugador.get("ciudad", "capital_imperial")
    ciudad_nombre = obtener_nombre(ciudad_id)
    limpiar(); titulo(f"BIENVENIDO A {ciudad_nombre.upper()}, {jugador['nombre'].upper()}")
    print(f"  {C.DIM}{formatear_fecha(mundo['dia'])} · {obtener_estacion(mundo['dia'])}{C.RESET}\n")
    ya_vista = ciudad_id in jugador.get("ciudades_vistas", [])
    imprimir_descripcion_ciudad(ciudad_id, primera_vez=not ya_vista)
    if not ya_vista:
        jugador.setdefault("ciudades_vistas", []).append(ciudad_id)
        guardar_jugador(conn, jugador)
    npcs_aqui = [n for n in npcs_globales if n.get("ciudad") == ciudad_id]
    narrar(f"Conoces a {len(npcs_aqui)} personas aqui.")
    pausa()
    menu_principal(conn, jugador, npcs_globales, mundo)
    conn.close()


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print(f"\n{C.RED}Cancelado.{C.RESET}\n"); sys.exit(0)