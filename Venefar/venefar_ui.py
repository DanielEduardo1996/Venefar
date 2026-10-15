# -*- coding: utf-8 -*-
"""VENEFAR - Modulo UI
Descripciones siempre alineadas a la derecha, con truncado si son largas.
"""
import os, sys

try:
    import msvcrt
    MSVCRT_OK = True
except ImportError:
    MSVCRT_OK = False


class C:
    RESET='\033[0m'; BOLD='\033[1m'; DIM='\033[2m'
    RED='\033[91m'; GREEN='\033[92m'; YELLOW='\033[93m'
    BLUE='\033[94m'; MAGENTA='\033[95m'; CYAN='\033[96m'; WHITE='\033[97m'


def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')


def linea(c='-', n=62):
    print(f"{C.CYAN}{c*n}{C.RESET}")


def titulo(t):
    print(); linea('=')
    print(f"{C.BOLD}{C.CYAN}{t.center(62)}{C.RESET}")
    linea('='); print()


def narrar(t):
    print(f"{C.WHITE}{t}{C.RESET}\n")


def opcion(n, t, d=""):
    print(f"  {C.YELLOW}{n}.{C.RESET} {C.BOLD}{t}{C.RESET}")
    if d:
        print(f"     {C.MAGENTA}({d}){C.RESET}")


def pausa():
    input(f"\n{C.DIM}(Pulsa Enter para continuar){C.RESET}")


def pedir_numero(maximo, permitir_cero=False):
    while True:
        try:
            r = int(input(f"{C.GREEN}> {C.RESET}").strip())
            if permitir_cero and r == 0: return 0
            if 1 <= r <= maximo: return r
            print(f"{C.RED}Opcion no valida (1-{maximo}).{C.RESET}")
        except (ValueError, KeyboardInterrupt):
            print(f"{C.RED}Introduce un numero.{C.RESET}")


def barra_estado(val, ancho=15):
    lleno = int((val / 100) * ancho)
    if lleno < 0: lleno = 0
    if lleno > ancho: lleno = ancho
    return "[" + "#" * lleno + "." * (ancho - lleno) + "]"


def _truncar(texto, ancho):
    """Trunca un texto al ancho dado, con '...' al final si es necesario."""
    if len(texto) <= ancho:
        return texto
    return texto[:ancho - 3] + "..."


def menu_flechas(items, contexto_fn=None, default=0, permitir_cancelar=True):
    """
    Descripciones SIEMPRE a la derecha, en columna fija.
    """
    ops = []
    for o in items:
        if isinstance(o, tuple):
            ops.append(o)
        else:
            ops.append((o, ""))
    if not ops: return -1

    seleccion = default % len(ops)

    if not MSVCRT_OK:
        if contexto_fn: contexto_fn()
        print()
        for i, (t, d) in enumerate(ops, 1): opcion(i, t, d)
        print()
        if permitir_cancelar: print(f"  {C.DIM}0. Cancelar{C.RESET}\n")
        r = pedir_numero(len(ops), permitir_cero=permitir_cancelar)
        return -1 if r == 0 else r - 1

    pista = "Flechas arriba/abajo + Enter, o numero directo"
    if permitir_cancelar: pista += ", Q para cancelar"

    ancho_num = len(str(len(ops)))
    ANCHO_NOMBRE = 28   # Nombre + relleno
    ANCHO_DESC = 38     # Descripcion (dentro de parentesis)

    def dibujar_todo():
        limpiar()
        if contexto_fn:
            contexto_fn()
        print()
        for i, (txt, det) in enumerate(ops):
            num = f"{i+1:>{ancho_num}}."
            marca = ">> " if i == seleccion else "   "
            nombre = _truncar(txt, ANCHO_NOMBRE)
            relleno = " " * (ANCHO_NOMBRE - len(nombre))
            desc = _truncar(det, ANCHO_DESC) if det else ""

            if i == seleccion:
                base = f"  {C.GREEN}{num} {marca}{C.BOLD}{nombre}{C.RESET}{relleno}"
            else:
                base = f"  {C.YELLOW}{num}{C.RESET} {marca}{nombre}{relleno}"
            if desc:
                base += f"{C.MAGENTA}({desc}){C.RESET}"
            print(base)
        print()
        print(f"  {C.DIM}({pista}){C.RESET}")

    dibujar_todo()

    while True:
        tecla = msvcrt.getch()
        redib = False
        if tecla in (b'\xe0', b'\x00'):
            t2 = msvcrt.getch()
            if t2 == b'H':
                seleccion = (seleccion - 1) % len(ops)
                redib = True
            elif t2 == b'P':
                seleccion = (seleccion + 1) % len(ops)
                redib = True
        elif tecla == b'\r':
            return seleccion
        elif tecla.lower() == b'q' and permitir_cancelar:
            return -1
        elif b'1' <= tecla <= b'9':
            n = int(tecla) - 1
            if 0 <= n < len(ops):
                return n

        if redib:
            dibujar_todo()