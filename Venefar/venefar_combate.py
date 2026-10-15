# -*- coding: utf-8 -*-
"""
VENEFAR - Sistema de Combate y Encuentros con Bandidos
Combate por turnos utilizando el equipo y stats del jugador.
"""
import random
from venefar_ui import C, titulo, narrar, pausa, limpiar, menu_flechas, pedir_numero
from venefar_equipamiento import obtener_equipado
from venefar_items import obtener_item, calcular_stats_jugador
from venefar_inventario import nombre_bonito_item

BANDIDOS_POOL = [
    {"nombre": "Bandido novato", "arma": "daga:hierro", "armadura": "capucha_cuero:hierro", "salud": 30, "dano": (1, 4), "defensa": 2, "oro": 5},
    {"nombre": "Salteador de caminos", "arma": "espada_corta:hierro", "armadura": "casco_cuero:hierro", "salud": 45, "dano": (1, 6), "defensa": 4, "oro": 12},
    {"nombre": "Bandido veterano", "arma": "hacha_mano:hierro", "armadura": "gambeson:hierro", "salud": 60, "dano": (1, 8), "defensa": 6, "oro": 25},
]

def generar_bandidos(peligro_ruta):
    cantidad = random.randint(1, 1 + int(peligro_ruta))
    grupo = []
    for _ in range(cantidad):
        if peligro_ruta == 0:
            b = dict(random.choice(BANDIDOS_POOL[:1]))
        elif peligro_ruta <= 2:
            b = dict(random.choice(BANDIDOS_POOL[:2]))
        else:
            b = dict(random.choice(BANDIDOS_POOL))
        grupo.append(b)
    return grupo

def menu_emboscada(conn, jugador, mundo, peligro_ruta):
    limpiar()
    titulo("¡EMBOSCADA EN EL CAMINO!")
    narrar("Mientras viajas por la ruta, sombras armadas emergen de los matorrales cortando el paso.")
    narrar("¡Un grupo de bandidos te exige todo tu dinero y pertenencias!")
    print()

    bandidos = generar_bandidos(peligro_ruta)
    print(f"  {C.RED}Enemigos detectados: {len(bandidos)}{C.RESET}")
    for b in bandidos:
        print(f"    - {b['nombre']} (Salud: {b['salud']}, Arma: {nombre_bonito_item(b['arma'])})")
    print()

    opciones = [
        ("Luchar", "Enfrentarte a los bandidos en combate"),
        ("Negociar", "Intentar sobornarles con dinero"),
        ("Huir", "Tratar de escapar a la carrera"),
    ]
    
    idx = menu_flechas(opciones, contexto_fn=lambda: None, permitir_cancelar=False)
    
    if idx == 0:
        return iniciar_combate(conn, jugador, mundo, bandidos)
    elif idx == 1:
        return intentar_negociar(conn, jugador, mundo, bandidos)
    elif idx == 2:
        return intentar_huir(conn, jugador, mundo, peligro_ruta)

def intentar_negociar(conn, jugador, mundo, bandidos):
    coste_soborno = sum(b['oro'] * 2 for b in bandidos) + 20
    limpiar()
    titulo("NEGOCIAR CON BANDIDOS")
    print(f"  Los bandidos te miran con desconfianza.")
    print(f"  Exigen un tributo de {C.YELLOW}{coste_soborno}{C.RESET} monedas para dejarte marchar.")
    print(f"  Tu dinero actual: {C.YELLOW}{jugador['dinero']}{C.RESET} monedas\n")
    
    if jugador['dinero'] < coste_soborno:
        narrar("No tienes suficiente dinero para pagar el soborno exigido.")
        narrar("¡No te dejan otra opción que luchar!")
        pausa()
        return iniciar_combate(conn, jugador, mundo, bandidos)
    
    opc = menu_flechas([("Pagar el tributo y marcharte", ""), ("Rechazar y luchar", "")],
                        contexto_fn=lambda: None, permitir_cancelar=False)
    if opc == 0:
        jugador['dinero'] -= coste_soborno
        from venefar_jugador import guardar_jugador
        guardar_jugador(conn, jugador)
        limpiar()
        titulo("NEGOCIACION EXITOSA")
        narrar("Aceptan el oro, gruñen una advertencia y desaparecen entre los árboles.")
        pausa()
        return True
    else:
        return iniciar_combate(conn, jugador, mundo, bandidos)

def intentar_huir(conn, jugador, mundo, peligro_ruta):
    limpiar()
    titulo("HUIR DE LA EMBOSCADA")
    prob = [0.8, 0.6, 0.4, 0.2][peligro_ruta]
    if random.random() < prob:
        narrar("¡Logras despistar a los bandidos en la espesura y escapar a toda prisa!")
        pausa()
        return True
    else:
        narrar("¡Te han cortado la retirada! No puedes escapar y te obligan a combatir.")
        pausa()
        return iniciar_combate(conn, jugador, mundo, bandidos)

def iniciar_combate(conn, jugador, mundo, bandidos):
    if "salud_combate" not in jugador:
        jugador["salud_combate"] = jugador.get("salud", 100)

    defensa_defendiendo = False

    while bandidos and jugador["salud_combate"] > 0:
        equipado = obtener_equipado(conn, jugador["identificador"])
        stats_eq = calcular_stats_jugador(equipado)
        defensa_total = stats_eq["defensa_total"] + (5 if defensa_defendiendo else 0)

        def contexto_combate():
            limpiar()
            titulo("COMBATE TACTICO")
            print(f"  {C.BOLD}Tu Salud:{C.RESET} {C.GREEN}{jugador['salud_combate']}/100{C.RESET} | {C.BOLD}Defensa:{C.RESET} {defensa_total}")
            print(f"  {C.BOLD}Enemigos restantes:{C.RESET} {len(bandidos)}\n")
            for i, b in enumerate(bandidos, 1):
                print(f"    {i}. {C.RED}{b['nombre']}{C.RESET} - Salud: {b['salud']} | Arma: {nombre_bonito_item(b['arma'])}")
            print()

        opciones_combate = [
            ("Atacar enemigo", "Golpear con tu arma equipada"),
            ("Defenderse", "Aumentar defensa temporalmente (+5 en este turno)"),
            ("Huir desesperadamente", "Intentar escapar a mitad del combate"),
        ]

        defensa_defendiendo = False
        idx = menu_flechas(opciones_combate, contexto_fn=contexto_combate, permitir_cancelar=False)

        if idx == 2:
            if random.random() < 0.4:
                limpiar()
                titulo("HUIDA EXITOSA")
                narrar("¡Arriesgando tu vida, logras romper el cerco y huir del combate!")
                pausa()
                return True
            else:
                narrar("¡Intentaste huir pero te bloquearon el paso! Pierdes la oportunidad de actuar.")
                pausa()

        elif idx == 1:
            defensa_defendiendo = True
            narrar("Adoptas una postura defensiva, esperando el golpe.")
            pausa()

        elif idx == 0:
            if len(bandidos) == 1:
                target_idx = 0
            else:
                items_en_combate = [(b['nombre'], f"Salud: {b['salud']}") for b in bandidos]
                target_idx = menu_flechas(items_en_combate, contexto_fn=contexto_combate, permitir_cancelar=False)

            enemigo = bandidos[target_idx]
            dmin = stats_eq["dano_min"]
            dmax = stats_eq["dano_max"]
            if dmin == 0 and dmax == 0:
                daño_jugador = random.randint(1, 3)
            else:
                daño_jugador = random.randint(int(dmin), max(int(dmin)+1, int(dmax)))

            daño_real_jugador = max(1, daño_jugador - enemigo["defensa"])
            enemigo["salud"] -= daño_real_jugador

            limpiar()
            titulo("INTERCAMBIO DE GOLPES")
            narrar(f"Atacas a {enemigo['nombre']} y le infliges {C.YELLOW}{daño_real_jugador}{C.RESET} puntos de daño.")

            if enemigo["salud"] <= 0:
                narrar(f"¡Has derrotado a {enemigo['nombre']}!")
                bandidos.pop(target_idx)
            pausa()

        if bandidos:
            limpiar()
            titulo("TURNO ENEMIGO")
            for enemigo in bandidos:
                d_min, d_max = enemigo["dano"]
                daño_enemigo = random.randint(d_min, d_max)
                daño_recibido = max(1, daño_enemigo - (defensa_total // 2))
                jugador["salud_combate"] -= daño_recibido
                narrar(f"{enemigo['nombre']} te ataca y te inflige {C.RED}{daño_recibido}{C.RESET} de daño.")
            pausa()

    if jugador["salud_combate"] <= 0:
        limpiar()
        titulo("DERROTADO")
        narrar("Has caído inconsciente bajo los golpes de los bandidos...")
        narrar("Despiertas horas más tarde tirado en el camino, despojado de parte de tu oro...")
        jugador["salud_combate"] = 30
        jugador["dinero"] = max(0, jugador["dinero"] - 50)
        from venefar_jugador import guardar_jugador
        guardar_jugador(conn, jugador)
        pausa()
        return False
    else:
        limpiar()
        titulo("¡VICTORIA!")
        narrar("¡Has aniquilado o puesto en fuga a todos los bandidos!")
        oro_ganado = random.randint(10, 30)
        jugador["dinero"] += oro_ganado
        narrar(f"Recompensa obtenida: {C.YELLOW}{oro_ganado}{C.RESET} monedas de oro.")
        
        if random.random() < 0.6:
            loot_posible = ["daga:hierro", "espada_corta:hierro", "casco_cuero:hierro", "tunica:hierro"]
            item_encontrado = random.choice(loot_posible)
            jugador["inventario"].append(item_encontrado)
            narrar(f"¡Has encontrado un objeto abandonado: {nombre_bonito_item(item_encontrado)}!")

        from venefar_jugador import guardar_jugador
        guardar_jugador(conn, jugador)
        pausa()
        return True