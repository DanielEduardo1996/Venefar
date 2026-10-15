# -*- coding: utf-8 -*-
"""VENEFAR - Modulo NPC"""
import json, random

from venefar_ui import titulo, narrar, opcion, pausa, limpiar, menu_flechas, C
from venefar_db import hash_frase
from venefar_npcs_mundo import generar_todos_los_npcs


# Items D2 que reciben algunos NPCs al inicio (aditivo)
ITEMS_D2_INICIALES_POR_OFICIO = {
    "Herrero":          ["espada_corta:hierro"],
    "Ballestero":       ["ballesta_ligera:hierro"],
    "Sastre":           ["tunica:hierro"],
    "Zapatero":         ["botas_cuero:hierro"],
    "Peletero":         ["guantes_cuero:hierro"],
    "Carpintero barcos":["escudo_redondo:hierro"],
    "Soldado":          ["espada_corta:hierro"],
    "Guardia":          ["espada_corta:hierro"],
    "Carcelero":        ["daga:hierro"],
}


def seed_inicial(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM npcs")
    if c.fetchone()[0] > 0:
        # Migracion silenciosa: dar items D2 a NPCs que no los tengan
        _migrar_items_d2(conn)
        c.execute("SELECT COUNT(*) FROM mundo")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO mundo (id, dia, estacion) VALUES (1, 1, 'Primavera')")
            conn.commit()
        return
    todos = generar_todos_los_npcs()
    for n in todos:
        atributos_json = json.dumps(n.get("atributos_fisicos", {}), ensure_ascii=False)
        c.execute("""INSERT INTO npcs
            (nombre, edad, sexo, oficio, rasgos, pasado, sueno, miedo, secreto, detalle,
             mood, dinero, ciudad, atributos_fisicos)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (n["nombre"], n["edad"], n["sexo"], n["oficio"],
             json.dumps(n["rasgos"], ensure_ascii=False),
             n["pasado"], n["sueno"], n["miedo"], n["secreto"],
             n["detalle"],
             random.choice(["neutral","contento","cansado","preocupado"]),
             n["dinero"], n.get("ciudad", "capital_imperial"),
             atributos_json))
        npc_id = c.lastrowid
        for prod, cant in n["inventario"].items():
            c.execute("INSERT INTO inventario (npc_id, producto, cantidad) VALUES (?,?,?)",
                      (npc_id, prod, cant))
        # Items D2 segun oficio
        oficio = n["oficio"]
        if oficio in ITEMS_D2_INICIALES_POR_OFICIO:
            for item_id in ITEMS_D2_INICIALES_POR_OFICIO[oficio]:
                 c.execute("INSERT INTO inventario (npc_id, producto, cantidad) VALUES (?,?,?)",
                          (npc_id, item_id, random.randint(1, 2)))
    c.execute("INSERT INTO mundo (id, dia, estacion) VALUES (1, 1, 'Primavera')")
    conn.commit()


def _migrar_items_d2(conn):
    """Migracion: añade items D2 a NPCs existentes que no los tengan."""
    c = conn.cursor()
    c.execute("""SELECT n.id, n.oficio FROM npcs n
                 WHERE n.oficio IN ({})
                 AND NOT EXISTS (
                     SELECT 1 FROM inventario i
                     WHERE i.npc_id = n.id AND i.producto LIKE '%:%'
                 )""".format(",".join("?" * len(ITEMS_D2_INICIALES_POR_OFICIO))),
              list(ITEMS_D2_INICIALES_POR_OFICIO.keys()))
    filas = c.fetchall()
    for fila in filas:
        npc_id = fila["id"]
        oficio = fila["oficio"]
        for item_id in ITEMS_D2_INICIALES_POR_OFICIO[oficio]:
            c.execute("INSERT INTO inventario (npc_id, producto, cantidad) VALUES (?,?,?)",
                      (npc_id, item_id, random.randint(1, 3)))
    if filas:
        conn.commit()


def cargar_npcs(conn, ciudad=None):
    c = conn.cursor()
    if ciudad:
        c.execute("SELECT * FROM npcs WHERE ciudad=?", (ciudad,))
    else:
        c.execute("SELECT * FROM npcs")
    npcs = []
    for f in c.fetchall():
        c2 = conn.cursor()
        c2.execute("SELECT producto, cantidad FROM inventario WHERE npc_id=?", (f["id"],))
        inv = {r["producto"]: r["cantidad"] for r in c2.fetchall()}
        desc_vista = f["descripcion_vista"] if "descripcion_vista" in f.keys() else 0
        ciudad_val = f["ciudad"] if "ciudad" in f.keys() else "capital_imperial"
        atributos = f["atributos_fisicos"] if "atributos_fisicos" in f.keys() else "{}"
        npcs.append({
            "id": f["id"], "nombre": f["nombre"], "edad": f["edad"],
            "sexo": f["sexo"], "oficio": f["oficio"],
            "rasgos": json.loads(f["rasgos"]),
            "pasado": f["pasado"], "sueno": f["sueno"], "miedo": f["miedo"],
            "secreto": f["secreto"], "detalle": f["detalle"],
            "mood": f["mood"], "relacion": f["relacion"],
            "te_conoce": bool(f["te_conoce"]),
            "dias_sin_hablar": f["dias_sin_hablar"],
            "dinero": f["dinero"], "inventario": inv,
            "descripcion_vista": desc_vista,
            "ciudad": ciudad_val,
            "atributos_fisicos": atributos,
        })
    return npcs


def guardar_npc(conn, npc):
    c = conn.cursor()
    desc_vista = npc.get("descripcion_vista", 0)
    c.execute("""UPDATE npcs SET relacion=?, te_conoce=?, mood=?, dias_sin_hablar=?, dinero=?, descripcion_vista=?
                 WHERE id=?""",
              (npc["relacion"], 1 if npc["te_conoce"] else 0,
               npc["mood"], npc["dias_sin_hablar"], npc["dinero"],
               desc_vista, npc["id"]))
    c.execute("DELETE FROM inventario WHERE npc_id=?", (npc["id"],))
    for prod, cant in npc["inventario"].items():
        if cant > 0:
            c.execute("INSERT INTO inventario (npc_id, producto, cantidad) VALUES (?,?,?)",
                      (npc["id"], prod, cant))
    conn.commit()


def guardar_todos(conn, npcs):
    for npc in npcs:
        guardar_npc(conn, npc)


def tiene(npc, r): return r in npc["rasgos"]


def aplicar_voz(npc, texto):
    if not texto: return texto
    def cortar(t):
        c = t.split(". ")[0]
        return c if c.endswith((".","!","?")) else c + "."
    if tiene(npc, "gruñón") and random.random() < 0.7:
        return random.choice(["Bah. ","Tsk. ","Hmf. ",""]) + cortar(texto) + random.choice([""," Ya esta."," Nada mas."," ¿Y bien?"])
    if tiene(npc, "callado") and random.random() < 0.6:
        return cortar(texto)
    if tiene(npc, "hablador") and random.random() < 0.5:
        return texto + random.choice([" Aunque, pensandolo bien, tambien pasa lo contrario.",
                                       " Ya me estoy enrollando, disculpa.", " Cosas de uno, ya sabes."])
    if tiene(npc, "melancolico") and random.random() < 0.4:
        return texto + random.choice([" Pero al final, ¿que importa?", " La vida es asi de triste."])
    if tiene(npc, "orgulloso") and random.random() < 0.4:
        return texto + random.choice([" Y lo hago mejor que nadie.", " Pocos pueden decir lo mismo."])
    if tiene(npc, "avaro") and random.random() < 0.5:
        return texto + random.choice([" Y todo cuesta monedas.", " El oro manda, siempre."])
    if tiene(npc, "chismoso") and random.random() < 0.5:
        return texto + random.choice([" Y de esto no digo mas.", " Pero no me metas en lios."])
    if tiene(npc, "intelectual") and random.random() < 0.3:
        return texto + random.choice([" Es mas complejo de lo que parece.", " Habria que estudiarlo."])
    if tiene(npc, "cuidadoso") and random.random() < 0.3:
        return texto + random.choice([" Hay que tener cuidado.", " No conviene precipitarse."])
    if tiene(npc, "observador") and random.random() < 0.3:
        return texto + random.choice([" Me fijo en los detalles.", " Uno se da cuenta."])
    if tiene(npc, "amable") and random.random() < 0.3:
        return texto + random.choice([" Pero no te aburro mas.", " Si necesitas algo, pideme."])
    if tiene(npc, "viajero") and random.random() < 0.4:
        return texto + random.choice([" Como en tierras lejanas.", " Lo he visto en otros lugares."])
    if tiene(npc, "calculador") and random.random() < 0.3:
        return texto + random.choice([" Pero hay que medirlo.", " Todo tiene su cuenta."])
    if tiene(npc, "desconfiado") and random.random() < 0.4:
        return texto + random.choice([" No le digas a nadie.", " ¿Por que preguntas tanto?"])
    if tiene(npc, "trabajador") and random.random() < 0.3:
        return texto + random.choice([" El trabajo da valor.", " Con esfuerzo se consigue."])
    return texto


POOL_OFICIO = {
    "Herrero": [
        "El metal no miente. Si esta bien forjado, aguanta. Como la gente.",
        "Llevo el yunque en la sangre. Mi padre fue herrero, y el padre de mi padre.",
        "Sin hierro no soy nada. Y el hierro escasea.",
    ],
    "Tabernero": [
        "El trabajo es duro pero se gana. Los rumores llegan solos con cada jarra.",
        "Sirvo bebida, escucho historias, y a veces me llevo alguna.",
        "A veces pienso en dejar esto. Pero no se hacer otra cosa.",
    ],
    "Comerciante": [
        "El comercio es una guerra sin sangre.",
        "Compro barato, vendo caro. El resto son detalles.",
        "El dinero no duerme. Y si duerme, lo roban.",
    ],
    "Guardia": [
        "La ciudad duerme tranquila porque nosotros no dormimos.",
        "El orden tiene un precio. Y yo soy el que lo cobra.",
        "La violencia no me gusta. Pero a veces es necesaria.",
    ],
    "Médico": [
        "Curo lo que puedo. Lo que no puedo, lo entierra el sacerdote.",
        "Las plantas curan. Las mismas plantas, en otra dosis, matan.",
        "El dolor es una senal. Hay que escucharla.",
    ],
    "Granjero": [
        "La tierra da lo que le das. Ni mas, ni menos.",
        "Trabajo desde antes de que salga el sol.",
        "El campo no entiende de prisas.",
    ],
    "Ganadero": [
        "Los animales son mas leales que las personas.",
        "Cada manana los cuento. Si falta uno, algo va mal.",
        "El ganado es la familia que no se queja.",
    ],
    "Pescador": [
        "El mar no tiene ley. Solo tiene hambre.",
        "En el mar, o eres rapido o eres comida.",
        "Salimos al amanecer y volvemos al atardecer. Si volvemos.",
    ],
    "Leñador": [
        "El bosque me conoce mejor que mi mujer.",
        "La madera buena se nota al golpearla.",
        "Vivo del bosque. Y el bosque vive de mi respeto.",
    ],
    "Minero": [
        "Bajo cada manana y subo cada noche. Si subo.",
        "La piedra es dura. Pero el hambre es mas dura.",
        "He visto galerias derrumbarse. Y he salido vivo.",
    ],
    "Molinero": [
        "El trigo entra, la harina sale. Asi es la vida.",
        "El molino no para. Si para, el pueblo pasa hambre.",
        "Todo tiene su ritmo. El molino tambien.",
    ],
    "Panadero": [
        "El pan es lo primero que se hace cada manana.",
        "Sin pan, no hay vida. Por eso madrugo.",
        "El horno no perdona. Ni el pan tampoco.",
    ],
    "Cervecero": [
        "La cerveza buena se hace con paciencia.",
        "Cada lote es distinto. Como las personas.",
        "Vendo alegria embotellada. Y a veces tristeza.",
    ],
    "Carpintero": [
        "La madera habla. Solo hay que escucharla.",
        "Un buen mueble dura tres generaciones.",
        "Cada corte importa.",
    ],
    "Sastre": [
        "La ropa dice quien eres. Aunque tu no lo quieras decir.",
        "Un buen traje abre puertas que la espada no puede.",
        "Hilo, aguja, paciencia. Y despues, dinero.",
    ],
    "Albañil": [
        "Construyo casas que duran mas que quien las paga.",
        "La piedra bien puesta aguanta siglos.",
        "Sin albaniles, no habria ciudades.",
    ],
    "Transportista": [
        "Llevo mercancia de aqui para alla. Como la sangre en el cuerpo.",
        "Sin transportistas, el reino moriria de hambre.",
        "Cada viaje es un riesgo.",
    ],
    "Administrador": [
        "Alguien tiene que organizar este caos.",
        "El orden cuesta. Pero la anarquia cuesta mas.",
        "Gobierno para el reino, no para mi.",
    ],
    "Sacerdote": [
        "El Sol ve todo. Y todo lo juzga.",
        "La fe sostiene lo que la espada no puede.",
        "Rezo por los vivos y por los muertos.",
    ],
    "Alquimista": [
        "Mezclo cosas. A veces explotan. Aprendo.",
        "Todo depende de la dosis. La medicina y el veneno.",
        "El secreto de la vida eterna esta en alguna parte.",
    ],
    "Escriba": [
        "Copio leyes que nadie lee. Pero alguien tiene que hacerlo.",
        "La pluma es mas peligrosa que la espada.",
        "Se leer y escribir. Eso me hace mas rico que muchos nobles.",
    ],
    "Cocinero": [
        "La cocina es el alma de la casa.",
        "Sin especias, todo sabe igual.",
        "Cocino con lo que hay. Y a veces con lo que no.",
    ],
    "Cazador": [
        "Los bosques ensenan paciencia. Y silencio.",
        "Un buen cazador sabe esperar.",
        "La naturaleza no perdona errores.",
    ],
    "Carpintero barcos": [
        "Un barco bien hecho aguanta tormentas.",
        "La madera buena se conoce al golpearla.",
        "Cada barco es un hijo que se va al mar.",
    ],
    "Vidriero": [
        "El vidrio es fragil, pero hermoso.",
        "Un mal golpe y todo se rompe.",
        "Trabajo con fuego y arena. Y creo belleza.",
    ],
    "Tejedor": [
        "La lana es paciencia. Y buen ojo.",
        "Un tapiz bien hecho cuenta una historia.",
        "El telar no para. Como el tiempo.",
    ],
    "Zapatero": [
        "Un buen zapato dura anos. Y camina mil leguas.",
        "Cuero bueno, zapato bueno.",
        "Conozco los pies de medio pueblo. Sus zapatos, digo.",
    ],
    "Sacamuelas": [
        "Saco lo que duele. A veces con mano firme.",
        "El dolor de muelas es el peor. Yo lo curo.",
        "No me gusta el oficio. Pero alguien tiene que hacerlo.",
    ],
    "Músico": [
        "La musica calma a las fieras. Y a los borrachos.",
        "Un buen cantar gana mas que una espada.",
        "Toco para vivir. Y vivo para tocar.",
    ],
    "Soldado": [
        "Sirvo al reino. No pregunto mucho.",
        "La guerra es un oficio como otro. Pero mata.",
        "Entreno cada dia. Por si acaso.",
    ],
    "Ballestero": [
        "Una ballesta bien tensada mata a un caballero.",
        "El virote no perdona.",
        "La guerra moderna se gana con acero y paciencia.",
    ],
    "Carcelero": [
        "Los presos son personas. Pero tambien son presos.",
        "Las llaves pesan mas de lo que parecen.",
        "Alguien tiene que hacer el trabajo sucio.",
    ],
    "Barrendero": [
        "Barro la ciudad. Otros la ensucian.",
        "Sin mi, las calles serian un vertedero.",
        "Nadie me mira. Pero yo lo veo todo.",
    ],
    "Mensajero": [
        "Llevo cartas. Y a veces secretos.",
        "Rapido, discreto, fiable. Esa es mi divisa.",
        "Camino mas que nadie en este reino.",
    ],
    "Explorador": [
        "Conozco rutas que no aparecen en los mapas.",
        "El mundo es mas grande de lo que crees.",
        "Hay lugares que nadie deberia pisar.",
    ],
    "Salinero": [
        "Sin sal, la comida se pudre. Y la gente tambien.",
        "El mar da lo que le pides.",
        "La sal vale mas de lo que parece.",
    ],
    "Carbonero": [
        "El carbon calienta las casas. Y forja las espadas.",
        "Todo negro, pero todo util.",
        "Los arboles mueren para que otros vivan.",
    ],
    "Peletero": [
        "El cuero es la piel del mundo.",
        "Un buen curtido dura anos.",
        "Convierto pieles en ropa. Y en recuerdos.",
    ],
}

POOL_RUMORES = [
    "Dicen que el Duque de Leon conspira contra el Rey.",
    "He oido que bandidos han asaltado una caravana.",
    "Se rumorea que la cosecha de este ano sera mala.",
    "Un mercader de paso dijo que hay guerra en el norte.",
    "La Iglesia del Sol anda recaudando diezmos con fuerza.",
    "Dicen que ha aparecido una grieta extrana al este.",
    "El alguacil de Varencia anda metido en algo raro.",
    "Una mujer de Salmura dijo que vio un barco sin tripulacion.",
    "Hay quien dice que el viejo rey esta mas enfermo.",
    "He oido que el obispo tiene un hijo secreto.",
    "Los gremios estan peleandose por el control del mercado.",
    "Un cazador vio algo en el bosque. No dice que.",
    "La hija del duque ha desaparecido.",
    "Hay un nuevo predicador en Corvalis. Dice cosas raras.",
    "Un marinero conto que hay islas al oeste sin mapa.",
]

POOL_LUGAR = [
    "Aqui se decide todo. Lo que pasa aqui, pasa en el reino.",
    "Los nobles van y vienen. Nosotros solo miramos.",
    "Cuidado con lo que dices. Aqui las paredes tienen oidos.",
    "He visto caer gobiernos sin moverme de mi puesto.",
    "Los que mandan cambian. El lugar sigue igual.",
]

POOL_FAMILIA = [
    "Mi familia es grande. Muchos primos, muchos sobrinos.",
    "Tengo dos hijos. Uno trabaja conmigo. El otro se fue.",
    "Mi mujer murio hace tres anos. Desde entonces estoy solo.",
    "Mis padres aun viven. Ya son mayores. Los cuido.",
    "No tengo familia. Nunca la tuve. Uno se acostumbra.",
    "Mi hermano es soldado. No lo veo nunca.",
    "Tengo una hija pequena. Es lo unico que me importa.",
]

POOL_POLITICA = [
    "El rey esta viejo. El hijo es debil. Mal asunto.",
    "Los nobles hacen lo que quieren. Nosotros pagamos.",
    "Si el duque se rebela, aqui lo sabremos tarde.",
    "La Iglesia manda mas que el rey. Todos lo saben.",
    "Yo no me meto. Pero escucho. Y lo que escucho no me gusta.",
    "El pueblo esta cansado. Y el pueblo cansado es peligroso.",
]

PREGUNTAS_NPC = [
    {"id": "origen", "pregunta": "¿Y tu de donde sales? No te he visto antes por aqui.",
     "opciones": [
        {"texto": "De Salmura. Vine a buscar trabajo.", "tipo": "verdad", "rel": 3,
         "reacciones": {"default": ["Salmura, buena gente."], "gruñón": ["Bah. Otro forastero."],
                         "desconfiado": ["Muchos vienen del puerto."]}},
        {"texto": "De por ahi. No tiene importancia.", "tipo": "evasiva", "rel": 0,
         "reacciones": {"default": ["Como quieras."]}},
        {"texto": "De Corvalis. Soy mercader de paso.", "tipo": "mentira", "rel": -1,
         "reacciones": {"default": ["Mmm. Ya."], "desconfiado": ["Mentira. Lo veo."]}},
        {"texto": "Antes de responder, ¿por que quieres saberlo?", "tipo": "contra", "rel": 1,
         "reacciones": {"default": ["Solo preguntaba."], "desconfiado": ["Buena pregunta."]}},
        {"texto": "No es asunto tuyo.", "tipo": "cortante", "rel": -3,
         "reacciones": {"default": ["Vaya. Perdona."], "gruñón": ["Bien dicho."]}},
     ]},
    {"id": "proposito", "pregunta": "¿Que te trae por aqui?",
     "opciones": [
        {"texto": "Busco trabajo. Soy bueno con las manos.", "tipo": "verdad", "rel": 3,
         "reacciones": {"default": ["Trabajo hay. Si sabes buscarlo."]}},
        {"texto": "Solo pasaba.", "tipo": "evasiva", "rel": 0,
         "reacciones": {"default": ["Buen viaje entonces."]}},
        {"texto": "Vengo a visitar a un familiar.", "tipo": "mentira", "rel": -1,
         "reacciones": {"default": ["Ya. ¿Quien?"]}},
        {"texto": "Busco respuestas.", "tipo": "verdad", "rel": 4,
         "reacciones": {"default": ["Aqui hay mas preguntas que respuestas."]}},
        {"texto": "Eso no es de tu incumbencia.", "tipo": "cortante", "rel": -3,
         "reacciones": {"default": ["Vaya. Perdona."]}},
     ]},
]


def seleccionar_reaccion(npc, opciones_reaccion):
    if "default" not in opciones_reaccion: return "Mmm."
    for r in npc["rasgos"]:
        if r in opciones_reaccion:
            return random.choice(opciones_reaccion[r])
    return random.choice(opciones_reaccion["default"])


def npc_hace_pregunta(conn, npc, jugador, dia):
    preg = random.choice(PREGUNTAS_NPC)
    def contexto():
        titulo(f"{npc['nombre'].upper()} TE PREGUNTA")
        print(f"  {C.DIM}{npc['oficio']}, {npc['edad']} anos{C.RESET}")
        print(f"  {C.DIM}{npc['detalle']}{C.RESET}")
        print(f"  {C.DIM}Estado: {npc['mood']}{C.RESET}")
        if npc["relacion"] != 0:
            col = C.GREEN if npc["relacion"] > 0 else C.RED
            print(f"  {col}Relacion: {npc['relacion']}{C.RESET}")
        print()
        print(f"{C.WHITE}{npc['nombre'].split()[0]} te mira un momento antes de hablar.{C.RESET}")
        print(f"{C.WHITE}\"{preg['pregunta']}\"{C.RESET}")
        print()
        print(f"{C.BOLD}{C.CYAN}¿Como respondes?{C.RESET}")
    items = [(op["texto"], "") for op in preg["opciones"]]
    idx = menu_flechas(items, contexto_fn=contexto, permitir_cancelar=False)
    elegida = preg["opciones"][idx]
    reaccion = seleccionar_reaccion(npc, elegida["reacciones"])
    npc["relacion"] += elegida["rel"]
    guardar_npc(conn, npc)
    guardar_recuerdo(conn, npc["id"], dia, "pregunta", f"{preg['id']}:{elegida['tipo']}", 2)
    limpiar(); titulo(npc["nombre"].upper())
    narrar(f"\"{reaccion}\"")
    pausa()


VENTANA_DIAS = 15


def frase_reciente(conn, npc_id, hash_f, dia):
    c = conn.cursor()
    c.execute("""SELECT COUNT(*) FROM frases_usadas WHERE npc_id=? AND hash=? AND dia > ?""",
              (npc_id, hash_f, dia - VENTANA_DIAS))
    return c.fetchone()[0] > 0


def registrar_frase(conn, npc_id, texto, dia):
    c = conn.cursor()
    c.execute("INSERT INTO frases_usadas (npc_id, hash, dia) VALUES (?,?,?)",
              (npc_id, hash_frase(texto), dia))
    conn.commit()


def guardar_recuerdo(conn, npc_id, dia, tipo, contenido, imp=1):
    c = conn.cursor()
    c.execute("""INSERT INTO recuerdos (npc_id, dia, tipo, contenido, importancia)
                 VALUES (?,?,?,?,?)""", (npc_id, dia, tipo, contenido, imp))
    conn.commit()


def tiene_recuerdo(conn, npc_id, tipo):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM recuerdos WHERE npc_id=? AND tipo=?", (npc_id, tipo))
    return c.fetchone()[0] > 0


def elegir_no_repetida(conn, npc, opciones, dia):
    disponibles = [o for o in opciones if not frase_reciente(conn, npc["id"], hash_frase(o), dia)]
    if not disponibles: disponibles = opciones
    elegida = random.choice(disponibles)
    registrar_frase(conn, npc["id"], elegida, dia)
    return elegida


def generar_respuesta(conn, npc, tema, jugador, dia):
    if tema == "oficio":
        opciones = POOL_OFICIO.get(npc["oficio"], ["Es un trabajo como cualquier otro."])
    elif tema == "rumores": opciones = POOL_RUMORES
    elif tema == "lugar": opciones = POOL_LUGAR
    elif tema == "familia": opciones = POOL_FAMILIA
    elif tema == "politica": opciones = POOL_POLITICA
    elif tema == "clima":
        h = jugador["hora"]
        if h < 12: opciones = ["La manana esta fresca.", "El sol asoma."]
        elif h < 18: opciones = ["La tarde es pesada.", "El sol pega fuerte."]
        else: opciones = ["La noche es peligrosa.", "A esta hora solo salen los que no quieren ser vistos."]
    elif tema == "pasado":
        opciones = [npc["pasado"], f"{npc['pasado']} A veces lo pienso.",
                    f"{npc['pasado']} Pero eso ya paso."]
    elif tema == "sueno":
        opciones = [npc["sueno"], f"{npc['sueno']} Aunque no se si lo vere."]
    elif tema == "miedo":
        opciones = [npc["miedo"], f"{npc['miedo']} Pero no se lo digas a nadie."]
    elif tema == "secreto":
        if not npc["secreto"]:
            return aplicar_voz(npc, "Secretos... todos tenemos. Pero no te los voy a contar a ti.")
        if npc["relacion"] < 45:
            return aplicar_voz(npc, "Eso es cosa mia. Cuando te conozca mejor, hablaremos.")
        if tiene_recuerdo(conn, npc["id"], "secreto_revelado"):
            return f"Ya te lo conte. {npc['secreto']}"
        guardar_recuerdo(conn, npc["id"], dia, "secreto_revelado", npc["secreto"], 5)
        return f"Bueno... te lo dire porque me caes bien. {npc['secreto']} Pero no se lo digas a nadie."
    else: return "..."
    base = elegir_no_repetida(conn, npc, opciones, dia)
    return aplicar_voz(npc, base)