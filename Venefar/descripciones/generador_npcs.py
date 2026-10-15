# -*- coding: utf-8 -*-
"""
VENEFAR - Generador de rasgos fisicos para NPCs.
Cada NPC tiene su propia combinacion unica.
"""
import random


# ─── Cuerpo por sexo ───────────────────────────────
CUERPO_H = [
    "alto y delgado", "bajo y robusto", "de estatura media pero con espaldas anchas",
    "delgado y nervudo", "ancho de hombros y cuello grueso",
    "de complexion fragil", "grande como un oso", "menudo pero agil",
]
CUERPO_M = [
    "alta y delgada", "baja y de complexion fuerte", "de estatura media y hombros rectos",
    "esbelta y nervuda", "ancha de caderas y de porte firme",
    "pequena y agil", "alta y elegante", "fuerte de brazos",
]

ROSTROS = [
    "rostro cuadrado", "cara alargada", "nariz aguileña", "pomulos marcados",
    "rostro redondeado", "cara delgada", "menton fuerte", "nariz chata",
    "rostro curtido", "cara palida", "frente amplia", "rostro picado de viruela",
]

OJOS = [
    "ojos claros y penetrantes", "mirada cansada", "ojos oscuros y tranquilos",
    "mirada viva y curiosa", "ojos grises", "mirada fria y evaluadora",
    "ojos pequenos y vivaces", "mirada melancolica", "ojos verdes",
    "mirada franca y directa",
]

PELOS = [
    "pelo canoso y corto", "cabello oscuro y revuelto", "melena recogida",
    "calvo con barba", "pelo largo trenzado", "cabellera espesa",
    "pelo ralo", "cabello blanco prematuro", "pelo rapado",
    "cabello ondulado", "pelo liso y recortado", "con entradas visibles",
]

MANOS = [
    "manos callosas", "dedos largos", "manos pequenas", "nudillos anchos",
    "manos de dedos finos", "manos oscurecidas por el sol", "nudosos dedos",
    "manos de piel suave", "manos arañadas", "manos con una uña rota",
]

VOCES = [
    "voz grave", "voz suave", "habla rapida", "habla pausada",
    "voz rasposa", "voz cantarina", "tono seco", "tono calido",
    "voz grave y lenta", "habla con un leve acento",
]

GESTOS = [
    "no deja de mover las manos al hablar", "siempre se rasca la barbilla",
    "mira fijamente a los ojos", "esquiva la mirada",
    "se toca el pelo al pensar", "cruza los brazos al escuchar",
    "cambia el peso de un pie a otro", "tamborilea con los dedos",
    "tiene un tic en la ceja", "sonrie con facilidad",
]

MOVIMIENTOS = [
    "camina despacio, sin prisa", "se mueve con rapidez",
    "camina con paso firme", "va con la espalda recta",
    "camina ligeramente encorvado", "se mueve con economia de gestos",
    "va dando zancadas largas", "se desplaza con cautela",
]


# ─── Ropa especifica por oficio ────────────────────
ROPA_POR_OFICIO = {
    "Herrero":         "un delantal de cuero gastado y una camisa manchada de carbon",
    "Tabernero":       "ropa practica y limpia, con un trapo al hombro",
    "Comerciante":     "ropas finas aunque sobrias, apropiadas para negociar",
    "Guardia":         "una cota de cuero reforzada con placas de metal",
    "Médico":          "tunica oscura manchada de tinturas de hierbas",
    "Granjero":        "ropa de lino tosco, con las mangas remangadas",
    "Ganadero":        "una capa de lana gruesa y botas de cuero",
    "Pescador":        "camisa de lino manchada de escamas y sal",
    "Leñador":         "ropa de lana con restos de resina",
    "Minero":          "mono de tela gruesa, con polvo de carbon en los pliegues",
    "Molinero":        "ropa cubierta de polvo blanco de harina",
    "Panadero":        "un delantal blanco y un gorro de tela",
    "Cervecero":       "ropa tosca con olor a mosto",
    "Carpintero":      "ropa manchada de serrin y barniz",
    "Sastre":          "ropa bien cortada, sobria pero de calidad",
    "Albañil":         "ropa de tela gruesa cubierta de polvo de cal",
    "Transportista":   "ropas de viaje, con polvo de varios caminos",
    "Administrador":   "ropa oscura de buena factura y manos de tinta",
    "Sacerdote":       "tunica talar con un simbolo del Sol bordado en el pecho",
    "Alquimista":      "tunica manchada de reactivos y un cinturon con frascos",
    "Escriba":         "tunica sencilla y un estuche de plumas colgado del cinturon",
    "Cocinero":        "delantal blanco y un gorro de tela alta",
    "Cazador":         "ropa de cuero flexible, con capucha y botas altas",
    "Carpintero barcos": "ropa de trabajo con restos de brea",
    "Vidriero":        "ropa resistente con marcas de quemaduras en los brazos",
    "Tejedor":         "ropa sencilla con hilos de lana pegados",
    "Zapatero":        "delantal de cuero y manos manchadas de tinte",
    "Sacamuelas":      "tunica oscura y un estuche de instrumentos colgando",
    "Músico":          "ropa colorida y bien cuidada, aunque algo gastada",
    "Soldado":         "armadura sencilla con marcas de batalla",
    "Ballestero":      "ropa de cuero reforzado, con virotes en un cinto",
    "Carcelero":       "ropa oscura con un manojo de llaves al cinto",
    "Barrendero":      "ropa raida y un palo de escoba siempre a mano",
    "Mensajero":       "ropa practica de viaje, con un bolso cruzado",
    "Explorador":      "ropas resistentes con capucha, y un mapa asomando del bolsillo",
    "Salinero":        "ropa curtida por la sal, con las mangas remangadas",
    "Carbonero":       "ropa totalmente negra de carbon",
    "Peletero":        "delantal de cuero y las manos manchadas de curtiente",
}

OLOR_POR_OFICIO = {
    "Herrero":         "a hierro caliente y a sudor",
    "Tabernero":       "a cerveza, a guiso y a tabaco viejo",
    "Comerciante":     "a especias y a cuero nuevo",
    "Guardia":         "a aceite de armas y a sudor",
    "Médico":          "a hierbas medicinales y a algo mas profundo",
    "Granjero":        "a tierra, a heno y a sudor",
    "Ganadero":        "a oveja y a establo",
    "Pescador":        "a sal, a pescado y a brea",
    "Leñador":         "a resina y a bosque",
    "Minero":          "a tierra profunda y a carbon",
    "Molinero":        "a harina y a polvo de trigo",
    "Panadero":        "a pan recien hecho y a levadura",
    "Cervecero":       "a cebada y a fermento",
    "Carpintero":      "a madera recien cortada y a barniz",
    "Sastre":          "a tela nueva y a hilo",
    "Albañil":         "a cal, a piedra y a sudor",
    "Transportista":   "a caballo, a polvo y a humo de hoguera",
    "Administrador":   "a papel, a tinta y a autoridad",
    "Sacerdote":       "a incienso y a cera de velas",
    "Alquimista":      "a azufre y a reactivos extranos",
    "Escriba":         "a tinta y a papel viejo",
    "Cocinero":        "a especias y a grasa caliente",
    "Cazador":         "a cuero, a monte y a resina",
    "Carpintero barcos": "a brea y a madera humeda",
    "Vidriero":        "a ceniza caliente",
    "Tejedor":         "a lana y a tinte",
    "Zapatero":        "a cuero curtido y a cola",
    "Sacamuelas":      "a alcohol y a hierbas amargas",
    "Músico":          "a incienso suave y a vino",
    "Soldado":         "a sudor, a cuero y a hierro",
    "Ballestero":      "a aceite de ballesta y a cuero",
    "Carcelero":       "a hierro viejo y a humedad",
    "Barrendero":      "a polvo y a sudor",
    "Mensajero":       "a camino y a caballo",
    "Explorador":      "a monte, a humo y a cuero",
    "Salinero":        "a sal y a mar",
    "Carbonero":       "a carbon y a humo",
    "Peletero":        "a cuero crudo y a curtiente",
}


# ─── Cicatriz / historia fisica ────────────────────
CICATRICES = [
    "una cicatriz fina en la mejilla",
    "una marca de quemadura en el antebrazo",
    "un dedo ligeramente torcido de una vieja fractura",
    "una cicatriz en la ceja",
    "una vieja herida mal curada en el costado",
    "un diente menos de una pelea antigua",
    "una marca de latigo antigua en la espalda",
    "una cicatriz profunda en la mano",
    "un parche en un ojo",
    "una oreja con el lobulo partido",
    "un hombro que se queja con el frio",
    "una rodilla que cruje al andar",
]


def generar_atributos_fisicos(sexo, oficio):
    """
    Devuelve un dict con todos los rasgos fisicos unicos de un NPC.
    """
    return {
        "cuerpo": random.choice(CUERPO_H if sexo == "Hombre" else CUERPO_M),
        "rostro": random.choice(ROSTROS),
        "ojos": random.choice(OJOS),
        "pelo": random.choice(PELOS),
        "manos": random.choice(MANOS),
        "voz": random.choice(VOCES),
        "gesto": random.choice(GESTOS),
        "movimiento": random.choice(MOVIMIENTOS),
        "ropa": ROPA_POR_OFICIO.get(oficio, "ropa sencilla y practica"),
        "olor": OLOR_POR_OFICIO.get(oficio, "a persona comun"),
        "cicatriz": random.choice(CICATRICES),
    }


def construir_descripcion_larga(nombre_completo, edad, sexo, oficio, atributos):
    """
    Construye una descripcion unica a partir de los atributos.
    """
    pronombre = "El" if sexo == "Hombre" else "La"
    articulo = "un" if sexo == "Hombre" else "una"
    of_low = oficio.lower()

    partes = []
    # 1. Presentacion: nombre + oficio + edad + cuerpo
    partes.append(
        f"{nombre_completo.split()[0]} es {articulo} {of_low} de {edad} anos, "
        f"{atributos['cuerpo']}."
    )
    # 2. Rostro + ojos + pelo
    partes.append(
        f"Tiene {atributos['rostro']}, {atributos['ojos']} y {atributos['pelo']}."
    )
    # 3. Manos + cicatriz
    partes.append(
        f"Sus {atributos['manos']} hablan de anos de trabajo. "
        f"Se le nota {atributos['cicatriz']}."
    )
    # 4. Ropa + olor
    partes.append(
        f"Viste {atributos['ropa']}. Huele {atributos['olor']}."
    )
    # 5. Voz + gesto + movimiento
    partes.append(
        f"Tiene {atributos['voz']}, y {atributos['gesto']}. "
        f"{atributos['movimiento'].capitalize()}."
    )
    return " ".join(partes)


def construir_descripcion_breve(nombre_completo, oficio, atributos):
    """Version corta para las siguientes visitas."""
    return (
        f"{nombre_completo.split()[0]}, {oficio.lower()}, {atributos['movimiento']}. "
        f"Se le nota {atributos['cicatriz']}."
    )