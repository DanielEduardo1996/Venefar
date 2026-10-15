# -*- coding: utf-8 -*-
"""
VENEFAR - Modulo Mapa
Rutas entre asentamientos, peligrosidad, mapa visual.
"""

# Rutas bidireccionales.
# Formato: (ciudad_a, ciudad_b, dias, peligrosidad)
# Peligrosidad: 0=segura, 1=moderada, 2=peligrosa, 3=mortal
RUTAS = [
    ("capital_imperial", "villareal",       4, 0),
    ("capital_imperial", "santamera",       5, 1),
    ("capital_imperial", "piedrahonda",     3, 0),
    ("capital_imperial", "robledal",        3, 1),
    ("capital_imperial", "canterral",       6, 1),
    ("villareal",        "puerto_sal",      3, 0),
    ("villareal",        "robledal",        2, 0),
    ("villareal",        "piedrahonda",     4, 0),
    ("puerto_sal",       "mareas",          2, 0),
    ("puerto_sal",       "calas",           2, 0),
    ("santamera",        "villafria",       3, 1),
    ("santamera",        "canterral",       4, 2),
    ("santamera",        "ermita_alta",     1, 2),
    ("piedrahonda",      "fresnillo",       1, 0),
    ("piedrahonda",      "villafria",       2, 0),
    ("piedrahonda",      "canterral",       5, 1),
    ("robledal",         "canterral",       3, 1),
]


# Mapa visual en texto
MAPA_ASCII = """
                                  PENALTA
                                     |
                                FERROCAST
                              /      |      \\
                       CORNAVA    CORVALIS   CANTERRAL
                            \\      /    \\      /
                            TRIGALBA -- ROBLENAR
                                |            |
                            FRESNILLO    VARENCIA
                                             |
                                          SALMURA
                                         /       \\
                                     MAREAS   ROCALMAR
"""


NIVELES_PELIGRO = {
    0: ("Segura",    "Camino real vigilado. Sin peligros conocidos."),
    1: ("Moderada",  "Caminos abiertos con algun riesgo de asaltantes."),
    2: ("Peligrosa", "Zonas con bandidos conocidos. Conviene ir armado."),
    3: ("Mortal",    "Rutas salvajes o disputadas. Solo para valientes o necios."),
}


def conexiones_de(ciudad_id):
    """Devuelve dict {destino: (dias, peligrosidad)}."""
    conexiones = {}
    for r in RUTAS:
        a, b, dias, peligro = r
        if a == ciudad_id:
            conexiones[b] = (dias, peligro)
        elif b == ciudad_id:
            conexiones[a] = (dias, peligro)
    return conexiones


def descripcion_ruta(peligro):
    return NIVELES_PELIGRO.get(peligro, ("Desconocida", "Sin datos."))


def mostrar_mapa(ciudad_actual=None):
    """Imprime el mapa del mundo, con la ciudad actual destacada."""
    from venefar_ui import C, linea, titulo
    from descripciones.ciudades import obtener_nombre

    titulo("MAPA DE VENEFAR")

    # Leyenda de tipos de asentamiento
    print(f"  {C.BOLD}{C.CYAN}CIUDADES{C.RESET} (grandes)")
    for cid in ["capital_imperial", "puerto_sal", "villareal", "santamera"]:
        marca = " <-- Estas aqui" if cid == ciudad_actual else ""
        color = C.YELLOW if cid == ciudad_actual else C.WHITE
        print(f"    - {color}{obtener_nombre(cid)}{C.RESET}{marca}")

    print(f"\n  {C.BOLD}{C.CYAN}PUEBLOS{C.RESET} (medianos)")
    for cid in ["piedrahonda", "villafria", "robledal", "canterral", "mareas"]:
        marca = " <-- Estas aqui" if cid == ciudad_actual else ""
        color = C.YELLOW if cid == ciudad_actual else C.WHITE
        print(f"    - {color}{obtener_nombre(cid)}{C.RESET}{marca}")

    print(f"\n  {C.BOLD}{C.CYAN}ALDEAS{C.RESET} (pequenas)")
    for cid in ["ermita_alta", "calas", "fresnillo"]:
        marca = " <-- Estas aqui" if cid == ciudad_actual else ""
        color = C.YELLOW if cid == ciudad_actual else C.WHITE
        print(f"    - {color}{obtener_nombre(cid)}{C.RESET}{marca}")

    print()
    linea()
    print(f"  {C.BOLD}{C.CYAN}RUTAS PRINCIPALES{C.RESET}\n")

    for a, b, dias, peligro in RUTAS:
        na = obtener_nombre(a)
        nb = obtener_nombre(b)
        nivel, _ = NIVELES_PELIGRO[peligro]
        if peligro == 0: col = C.GREEN
        elif peligro == 1: col = C.YELLOW
        elif peligro == 2: col = C.RED
        else: col = C.MAGENTA
        print(f"  {na:<12} <-> {nb:<12} {dias} dia(s)  {col}[{nivel}]{C.RESET}")

    print()