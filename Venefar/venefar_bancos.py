# -*- coding: utf-8 -*-
"""VENEFAR - Bancos"""
from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from descripciones.ciudades import obtener_nombre
from venefar_reputacion import obtener_reputacion, etiqueta_reputacion


CIUDADES_CON_BANCO = {
    "capital_imperial", "puerto_sal", "villareal", "santamera",
    "piedrahonda", "canterral",
}

DEPOSITO_MINIMO = 50
INTERES_ANUAL = 0.12               # 12% anual
INTERES_MENSUAL = INTERES_ANUAL / 12   # 1% mensual
INTERES_PRESTAMO_MENSUAL = 0.05    # 5% mensual


def hay_banco(ciudad):
    return ciudad in CIUDADES_CON_BANCO


# ─── Cuentas ─────────────────────────────────────────
def obtener_cuenta(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("SELECT * FROM cuentas_banco WHERE jugador_id=? AND ciudad=?",
              (jugador_id, ciudad))
    f = c.fetchone()
    return dict(f) if f else None


def listar_cuentas(conn, jugador_id):
    c = conn.cursor()
    c.execute("SELECT * FROM cuentas_banco WHERE jugador_id=? ORDER BY ciudad", (jugador_id,))
    return [dict(r) for r in c.fetchall()]


def crear_cuenta(conn, jugador_id, ciudad):
    c = conn.cursor()
    c.execute("""INSERT INTO cuentas_banco
                 (jugador_id, ciudad, saldo, ultimo_interes_dia, interes_pendiente)
                 VALUES (?, ?, 0, 1, 0.0)""",
              (jugador_id, ciudad))
    conn.commit()


def depositar(conn, jugador_id, ciudad, cantidad):
    c = conn.cursor()
    c.execute("UPDATE cuentas_banco SET saldo = saldo + ? WHERE jugador_id=? AND ciudad=?",
              (cantidad, jugador_id, ciudad))
    conn.commit()


def retirar(conn, jugador_id, ciudad, cantidad):
    cuenta = obtener_cuenta(conn, jugador_id, ciudad)
    if not cuenta or cuenta["saldo"] < cantidad:
        return False
    c = conn.cursor()
    c.execute("UPDATE cuentas_banco SET saldo = saldo - ? WHERE jugador_id=? AND ciudad=?",
              (cantidad, jugador_id, ciudad))
    conn.commit()
    return True


# ─── Préstamos ───────────────────────────────────────
def listar_prestamos_activos(conn, jugador_id):
    c = conn.cursor()
    c.execute("SELECT * FROM prestamos WHERE jugador_id=? AND estado='activo'", (jugador_id,))
    return [dict(r) for r in c.fetchall()]


def tiene_prestamo_activo(conn, jugador_id):
    return len(listar_prestamos_activos(conn, jugador_id)) > 0


def max_prestamo(conn, jugador_id, ciudad):
    rep = obtener_reputacion(conn, jugador_id, ciudad)
    cuenta = obtener_cuenta(conn, jugador_id, ciudad)
    deposito = cuenta["saldo"] if cuenta else 0
    return max(0, int(500 + rep * 20 + deposito * 2))


def otorgar_prestamo(conn, jugador_id, ciudad, cantidad, dia):
    c = conn.cursor()
    c.execute("""INSERT INTO prestamos
                 (jugador_id, ciudad, monto_original, saldo_pendiente, dia_otorgado, dia_ultimo_interes, estado)
                 VALUES (?, ?, ?, ?, ?, ?, 'activo')""",
              (jugador_id, ciudad, cantidad, cantidad, dia, dia))
    conn.commit()


def pagar_prestamo(conn, jugador_id, prestamo_id, cantidad, ciudad_actual):
    c = conn.cursor()
    c.execute("SELECT * FROM prestamos WHERE id=? AND jugador_id=?", (prestamo_id, jugador_id))
    f = c.fetchone()
    if not f: return False
    saldo = f["saldo_pendiente"]
    pago = min(cantidad, saldo)
    nuevo = saldo - pago
    if nuevo <= 0:
        c.execute("UPDATE prestamos SET saldo_pendiente=0, estado='pagado' WHERE id=?", (prestamo_id,))
    else:
        c.execute("UPDATE prestamos SET saldo_pendiente=? WHERE id=?", (nuevo, prestamo_id))
    conn.commit()
    return pago


# ─── Interés mensual ────────────────────────────────
def procesar_interes_diario(conn, jugador, dia):
    """
    Aplica interés a cuentas (1% mensual) y préstamos (5% mensual)
    cuando han pasado 30 días. Usa acumulador fraccional.
    """
    jugador_id = jugador["identificador"]
    c = conn.cursor()

    # Cuentas
    c.execute("SELECT * FROM cuentas_banco WHERE jugador_id=?", (jugador_id,))
    for row in c.fetchall():
        dias = dia - row["ultimo_interes_dia"]
        if dias < 30: continue
        meses = dias // 30
        saldo = row["saldo"]
        pendiente = row["interes_pendiente"] if "interes_pendiente" in row.keys() else 0.0
        for _ in range(meses):
            ganancia_frac = saldo * INTERES_MENSUAL
            pendiente += ganancia_frac
            monedas_a_sumar = int(pendiente)
            saldo += monedas_a_sumar
            pendiente -= monedas_a_sumar
        nuevo_dia = row["ultimo_interes_dia"] + meses * 30
        c.execute("""UPDATE cuentas_banco SET saldo=?, ultimo_interes_dia=?, interes_pendiente=?
                     WHERE id=?""",
                  (saldo, nuevo_dia, pendiente, row["id"]))

    # Préstamos
    c.execute("SELECT * FROM prestamos WHERE jugador_id=? AND estado='activo'", (jugador_id,))
    for row in c.fetchall():
        dias = dia - row["dia_ultimo_interes"]
        if dias < 30: continue
        meses = dias // 30
        saldo = row["saldo_pendiente"]
        for _ in range(meses):
            interes = int(saldo * INTERES_PRESTAMO_MENSUAL)
            if interes < 1: interes = 1
            saldo += interes
        nuevo_dia = row["dia_ultimo_interes"] + meses * 30
        c.execute("UPDATE prestamos SET saldo_pendiente=?, dia_ultimo_interes=? WHERE id=?",
                  (saldo, nuevo_dia, row["id"]))

    conn.commit()


# ─── Menú ────────────────────────────────────────────
def menu_banco(conn, jugador, mundo):
    ciudad = jugador.get("ciudad", "capital_imperial")

    if not hay_banco(ciudad):
        limpiar(); titulo("BANCO")
        narrar("En esta aldea no hay banco. Los bancos solo estan en las ciudades grandes.")
        pausa(); return

    ciudad_nombre = obtener_nombre(ciudad)
    jugador_id = jugador["identificador"]

    while True:
        cuenta = obtener_cuenta(conn, jugador_id, ciudad)
        saldo = cuenta["saldo"] if cuenta else 0
        prestamos = listar_prestamos_activos(conn, jugador_id)

        def contexto():
            titulo(f"BANCO DE {ciudad_nombre.upper()}")
            print(f"  Tu dinero en mano: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas")
            print(f"  En este banco:     {C.YELLOW}{saldo}{C.RESET} monedas")
            if prestamos:
                total_deuda = sum(p["saldo_pendiente"] for p in prestamos)
                print(f"  {C.RED}Deuda total: {total_deuda} monedas en {len(prestamos)} prestamo(s){C.RESET}")
            print(f"  {C.DIM}Interes anual en depositos: 12% (1% mensual){C.RESET}")

        items = []
        claves = []

        if not cuenta:
            items.append(("Abrir cuenta en este banco", f"Minimo {DEPOSITO_MINIMO} monedas"))
            claves.append("abrir")
        else:
            items.append(("Depositar dinero", f"Tienes {jugador['dinero']} en mano"))
            claves.append("depositar")
            if saldo > 0:
                items.append(("Retirar dinero", f"Saldo: {saldo}"))
                claves.append("retirar")

        max_prest = max_prestamo(conn, jugador_id, ciudad)
        if max_prest >= 100 and not tiene_prestamo_activo(conn, jugador_id):
            items.append(("Pedir prestamo", f"Maximo: {max_prest} monedas (5% mensual)"))
            claves.append("prestamo")
        elif tiene_prestamo_activo(conn, jugador_id):
            items.append(("Pagar prestamo", f"Deuda: {sum(p['saldo_pendiente'] for p in prestamos)}"))
            claves.append("pagar")

        items.append(("Ver todas mis cuentas", ""))
        claves.append("ver_todas")
        items.append(("Volver", ""))
        claves.append("salir")

        idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
        acc = claves[idx]

        if acc == "salir":
            return
        elif acc == "abrir":
            _abrir_cuenta(conn, jugador, ciudad)
        elif acc == "depositar":
            _depositar(conn, jugador, ciudad)
        elif acc == "retirar":
            _retirar(conn, jugador, ciudad)
        elif acc == "prestamo":
            _pedir_prestamo(conn, jugador, ciudad, mundo["dia"], max_prest)
        elif acc == "pagar":
            _pagar_prestamo(conn, jugador, ciudad, prestamos)
        elif acc == "ver_todas":
            _ver_cuentas(conn, jugador)


def _abrir_cuenta(conn, jugador, ciudad):
    if jugador["dinero"] < DEPOSITO_MINIMO:
        limpiar(); titulo("ABRIR CUENTA")
        narrar(f"Necesitas al menos {DEPOSITO_MINIMO} monedas para abrir una cuenta.")
        pausa(); return
    limpiar(); titulo("ABRIR CUENTA")
    narrar(f"Deposito inicial minimo: {DEPOSITO_MINIMO} monedas.")
    print(f"  Tu dinero: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas\n")
    cant = pedir_numero(jugador["dinero"])
    if cant < DEPOSITO_MINIMO:
        narrar(f"{C.RED}Necesitas al menos {DEPOSITO_MINIMO} monedas.")
        pausa(); return
    crear_cuenta(conn, jugador["identificador"], ciudad)
    depositar(conn, jugador["identificador"], ciudad, cant)
    jugador["dinero"] -= cant
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("CUENTA ABIERTA")
    narrar(f"Has abierto una cuenta con {cant} monedas de deposito.")
    pausa()


def _depositar(conn, jugador, ciudad):
    if jugador["dinero"] <= 0:
        limpiar(); titulo("DEPOSITAR"); narrar("No tienes dinero en mano."); pausa(); return
    limpiar(); titulo("DEPOSITAR DINERO")
    print(f"  En mano: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas\n")
    print(f"  ¿Cuanto quieres depositar? (max {jugador['dinero']})")
    cant = pedir_numero(jugador["dinero"])
    depositar(conn, jugador["identificador"], ciudad, cant)
    jugador["dinero"] -= cant
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("DEPOSITO REALIZADO")
    narrar(f"Depositas {cant} monedas.")
    pausa()


def _retirar(conn, jugador, ciudad):
    cuenta = obtener_cuenta(conn, jugador["identificador"], ciudad)
    if not cuenta or cuenta["saldo"] <= 0:
        limpiar(); titulo("RETIRAR"); narrar("No tienes saldo."); pausa(); return
    limpiar(); titulo("RETIRAR DINERO")
    print(f"  Saldo: {C.YELLOW}{cuenta['saldo']}{C.RESET} monedas\n")
    cant = pedir_numero(cuenta["saldo"])
    if retirar(conn, jugador["identificador"], ciudad, cant):
        jugador["dinero"] += cant
        from venefar_jugador import guardar_jugador
        guardar_jugador(conn, jugador)
        limpiar(); titulo("RETIRO REALIZADO")
        narrar(f"Retiras {cant} monedas.")
    else:
        limpiar(); titulo("ERROR"); narrar("No se pudo retirar.")
    pausa()


def _pedir_prestamo(conn, jugador, ciudad, dia, max_prest):
    limpiar(); titulo("PEDIR PRESTAMO")
    print(f"  Maximo: {C.YELLOW}{max_prest}{C.RESET} monedas")
    print(f"  Interes: 5% mensual")
    print(f"  {C.DIM}Se acumula cada 30 dias sobre el saldo pendiente.{C.RESET}\n")
    print(f"  ¿Cuanto quieres pedir? (min 100)")
    if max_prest < 100:
        narrar(f"{C.RED}No puedes pedir tan poco."); pausa(); return
    cant = pedir_numero(max_prest)
    if cant < 100:
        narrar(f"{C.RED}Minimo 100 monedas."); pausa(); return
    confirm = menu_flechas([("Confirmar", f"Pedir {cant} monedas"),
                             ("Cancelar", "")],
                            contexto_fn=lambda: None, permitir_cancelar=False)
    if confirm == 1: return
    otorgar_prestamo(conn, jugador["identificador"], ciudad, cant, dia)
    jugador["dinero"] += cant
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("PRESTAMO OTORGADO")
    narrar(f"Recibes {cant} monedas. Recuerda pagar el prestamo.")
    pausa()


def _pagar_prestamo(conn, jugador, ciudad, prestamos):
    if not prestamos:
        limpiar(); titulo("PAGAR PRESTAMO"); narrar("No tienes prestamos activos."); pausa(); return
    items = []
    for p in prestamos:
        c_nombre = obtener_nombre(p["ciudad"])
        items.append((f"Prestamo de {c_nombre}",
                       f"Deuda: {p['saldo_pendiente']} monedas"))
    idx = menu_flechas(items, contexto_fn=lambda: titulo("PAGAR PRESTAMO"),
                        permitir_cancelar=True)
    if idx == -1: return
    p = prestamos[idx]

    limpiar(); titulo("PAGAR PRESTAMO")
    print(f"  Deuda pendiente: {C.RED}{p['saldo_pendiente']}{C.RESET} monedas")
    print(f"  Tu dinero: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas\n")
    if jugador["dinero"] <= 0:
        narrar("No tienes dinero para pagar."); pausa(); return
    max_pago = min(jugador["dinero"], p["saldo_pendiente"])
    print(f"  ¿Cuanto pagas? (max {max_pago})")
    cant = pedir_numero(max_pago)
    pagado = pagar_prestamo(conn, jugador["identificador"], p["id"], cant, ciudad)
    jugador["dinero"] -= pagado
    from venefar_jugador import guardar_jugador
    guardar_jugador(conn, jugador)
    limpiar(); titulo("PAGO REALIZADO")
    narrar(f"Pagas {pagado} monedas a tu prestamo.")
    pausa()


def _ver_cuentas(conn, jugador):
    limpiar(); titulo("MIS CUENTAS BANCARIAS")
    cuentas = listar_cuentas(conn, jugador["identificador"])
    if not cuentas:
        narrar("No tienes cuentas abiertas.")
        pausa(); return
    total = 0
    for cu in cuentas:
        nombre = obtener_nombre(cu["ciudad"])
        print(f"  {nombre:<15} {C.YELLOW}{cu['saldo']:>6}{C.RESET} monedas")
        total += cu["saldo"]
    print()
    print(f"  {C.BOLD}Total: {total} monedas{C.RESET}")

    prestamos = listar_prestamos_activos(conn, jugador["identificador"])
    if prestamos:
        print()
        print(f"  {C.RED}Prestamos activos:{C.RESET}")
        for p in prestamos:
            nombre = obtener_nombre(p["ciudad"])
            print(f"    {nombre}: {p['saldo_pendiente']} monedas de deuda")
    pausa()