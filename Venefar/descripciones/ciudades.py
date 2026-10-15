# -*- coding: utf-8 -*-
"""
VENEFAR - Descripciones de Ciudades y Asentamientos
12 asentamientos: 4 ciudades, 5 pueblos, 3 aldeas.
IDs internos se mantienen estables para no romper partidas.
"""

CIUDADES = {
    # ─── CIUDADES ──────────────────────────────
    "capital_imperial": {
        "nombre": "Corvalis",
        "tipo": "ciudad",
        "larga": (
            "Corvalis se alza sobre siete colinas, rodeada por una muralla de piedra "
            "gris que ha resistido siglos de asedios. Al cruzarla por la Puerta del Sol, "
            "lo primero que golpea es el ruido: el bullicio de miles de voces, el chirrido "
            "de carros sobre adoquin, el pregon de los vendedores, el tanido de campanas "
            "de una docena de iglesias. Las calles suben y bajan sin orden aparente, y en "
            "cada esquina hay un puesto, un predicador, un mendigo, un noble apurado o un "
            "guardia con la mano en la espada."
        ),
        "breve": "Corvalis te recibe con su bullicio incesante y el olor a piedra vieja y a multitud.",
        "olores": [
            "Huele a pan recien hecho, a caballo, a sudor y a piedra mojada por la lluvia de la manana.",
            "El aire mezcla el olor a especias del mercado con el de los canales abiertos.",
        ],
        "sonidos": [
            "Se oyen campanas, gritos de vendedores y el rumor constante de una ciudad que nunca duerme.",
            "El eco de los cascos de caballo sobre el adoquin resuena entre los edificios.",
        ],
        "perfil": "Capital del reino. Centro politico, comercial y administrativo.",
        "produce": ["Servicios", "Comercio", "Administracion"],
    },
    "puerto_sal": {
        "nombre": "Salmura",
        "tipo": "ciudad",
        "larga": (
            "Salmura huele a mar antes de que lo veas. Al bajar la colina que lleva a la "
            "ciudad, el olor a sal, a pescado y a brea impregna el aire. Las casas estan "
            "construidas con prisa y sin estilo, apinadas alrededor del muelle. Los marineros "
            "cantan en las tabernas, los mercaderes regatean a gritos, y las gaviotas gritan "
            "sobre los tejados como si tambien quisieran vender algo. Aqui el dinero cambia "
            "de manos rapido, y el que no sabe nadar, se ahoga."
        ),
        "breve": "Salmura huele a pescado y a sal. Las gaviotas gritan sobre el puerto.",
        "olores": [
            "Huele a pescado fresco, a sal, a brea y a cerveza rancia.",
            "El aire huele a mar, a madera humeda y a sudor de marineros.",
        ],
        "sonidos": [
            "Se oye el golpear de las olas contra el muelle, las gaviotas y las canciones de taberna.",
            "Los marineros cantan desafinados mientras descargan cajas de un barco.",
        ],
        "perfil": "Puerto principal del reino. Comercio maritimo, pesca y entrada de importaciones.",
        "produce": ["Pescado", "Sal", "Comercio maritimo"],
    },
    "villareal": {
        "nombre": "Varencia",
        "tipo": "ciudad",
        "larga": (
            "Varencia es una ciudad de piedra clara y calles limpias, construida alrededor del "
            "Castillo Ducal. Aqui se respira poder. Los guardias patrullan con armaduras "
            "pulidas, los nobles pasean en literas, y en la Catedral del Sol se reza con la "
            "misma solemnidad con la que se conspira en los pasillos del castillo. La ciudad "
            "es hermosa, pero fria; quien no tiene apellido, no cuenta. Aqui las sonrisas "
            "duran lo que dura una reverencia."
        ),
        "breve": "Varencia, la ciudad ducal. Piedra clara, calles limpias, y la sombra del castillo sobre todo.",
        "olores": [
            "Huele a incienso de la catedral, a piedra limpia y a hierro pulido.",
            "El aire huele a cera, a velas y a incienso quemado.",
        ],
        "sonidos": [
            "Se oyen campanas de catedral, cascos de caballo sobre el adoquin y murmullos de cortesanos.",
            "El sonido de espadas de entrenamiento resuena desde el patio del castillo.",
        ],
        "perfil": "Sede del Ducado. Nobleza, iglesia y artesania fina.",
        "produce": ["Ropa fina", "Armas de calidad", "Administracion ducal"],
    },
    "santamera": {
        "nombre": "Ferrocast",
        "tipo": "ciudad",
        "larga": (
            "Ferrocast es una fortaleza antes que una ciudad. La muralla es gruesa, las puertas "
            "de hierro, y los guardias no sonrien. Aqui huele a guerra. Los soldados entrenan "
            "en el patio de armas, los herreros no dan abasto, y las posadas estan llenas de "
            "hombres con cicatrices. Al otro lado de la frontera, dicen, hay tambores. Nadie "
            "sabe cuando empezara, pero todos saben que empezara."
        ),
        "breve": "Ferrocast, fortaleza de frontera. Aqui huele a guerra.",
        "olores": [
            "Huele a hierro, a cuero y a sudor de soldados.",
            "El aire huele a aceite de armas y a caballo.",
        ],
        "sonidos": [
            "Se oyen ordenes gritadas, el choque de espadas de entrenamiento y tambores lejanos.",
            "Las trompetas suenan al amanecer y al anochecer.",
        ],
        "perfil": "Fortaleza militar del norte. Armas, herreria pesada, guarnicion.",
        "produce": ["Armas", "Armaduras", "Servicios militares"],
    },

    # ─── PUEBLOS ───────────────────────────────
    "piedrahonda": {
        "nombre": "Trigalba",
        "tipo": "pueblo",
        "larga": (
            "Trigalba es un pueblo agricola en el cruce de tres caminos importantes. A ambos "
            "lados de la calle principal se extienden campos de trigo que llegan hasta donde "
            "alcanza la vista. El molino de viento, en lo alto de la colina, gira sin descanso "
            "y se ve desde lejos. En el mercado, dos veces por semana, los granjeros venden su "
            "cosecha y compran herramientas. Aqui el tiempo se mide por cosechas, no por dias."
        ),
        "breve": "Trigalba, el pueblo del trigo. Molino en la colina y campos hasta el horizonte.",
        "olores": [
            "Huele a trigo recien cortado, a harina y a tierra seca.",
            "El aire huele a pan horneandose y a estiercol de mula.",
        ],
        "sonidos": [
            "Se oyen las aspas del molino, gallos y conversaciones de granjeros.",
            "Los carros de trigo chirrian sobre el empedrado del mercado.",
        ],
        "perfil": "Pueblo agricola. Produccion de trigo, harina y pan para toda la region.",
        "produce": ["Trigo", "Harina", "Pan"],
    },
    "villafria": {
        "nombre": "Cornava",
        "tipo": "pueblo",
        "larga": (
            "Cornava es un pueblo ganadero en un valle protegido del viento. Los rebanos de "
            "ovejas y vacas pastan por las laderas, y el sonido de los cencerros acompana "
            "todo el dia. Las casas huelen a lana, a cuero y a leche. Aqui se curte el cuero "
            "que viste medio reino, y se hace el queso que se vende en la capital. La gente "
            "es ruda pero hospitalaria, y el trabajo empieza antes del amanecer."
        ),
        "breve": "Cornava, el pueblo del ganado. Rebanos por las laderas y olor a lana.",
        "olores": [
            "Huele a oveja, a cuero curtido y a leche fresca.",
            "El aire huele a lana sucia y a estiercol de vaca.",
        ],
        "sonidos": [
            "Se oyen cencerros, mugidos y el ladrido de perros pastores.",
            "El viento silba entre las colinas y trae el sonido lejano de los rebanos.",
        ],
        "perfil": "Pueblo ganadero. Carne, cuero y lana para la region.",
        "produce": ["Carne", "Cuero", "Lana", "Leche"],
    },
    "robledal": {
        "nombre": "Roblenar",
        "tipo": "pueblo",
        "larga": (
            "Roblenar es un pueblo lenador entre robles centenarios. El silencio es tan denso "
            "que se oye el crujir de las ramas a cien pasos. Los lenadores trabajan desde el "
            "amanecer, y por la noche las hogueras se encienden en cada casa. Los ancianos "
            "cuentan historias de espiritus del bosque que nadie cree del todo, pero que nadie "
            "se atreve a negar en voz alta. Aqui lo sobrenatural esta a la vuelta de cada arbol."
        ),
        "breve": "Roblenar, la aldea lenadora. Silencio, arboles y leyendas.",
        "olores": [
            "Huele a resina, a lena verde y a tierra de bosque.",
            "El aire huele a humedad y a hojas podridas.",
        ],
        "sonidos": [
            "Se oyen los hachazos lejanos y el canto de los pajaros.",
            "El viento entre las ramas suena como susurros.",
        ],
        "perfil": "Pueblo forestal. Madera, lena y carbon vegetal.",
        "produce": ["Madera", "Lena", "Carbon vegetal"],
    },
    "canterral": {
        "nombre": "Canterral",
        "tipo": "pueblo",
        "larga": (
            "Canterral esta construido sobre una cantera antigua, de la que se ha extraido "
            "piedra durante generaciones. Las casas son grises, de piedra bruta, y el polvo "
            "cubre todo. Los mineros bajan cada manana a las galerias con picos al hombro y "
            "suben al atardecer, negros de carbon. Aqui el trabajo es duro y la vida corta. "
            "Pero el mineral y la piedra de Canterral construyen medio reino."
        ),
        "breve": "Canterral, el pueblo minero. Polvo gris y galerias profundas.",
        "olores": [
            "Huele a polvo de piedra, a carbon y a sudor de mineros.",
            "El aire huele a tierra profunda y a hierro.",
        ],
        "sonidos": [
            "Se oyen los picos contra la piedra y el rodar de vagonetas.",
            "Los gritos de los capataces resuenan desde las galerias.",
        ],
        "perfil": "Pueblo minero. Mineral, carbon y piedra para todo el reino.",
        "produce": ["Mineral", "Carbon", "Piedra"],
    },
    "mareas": {
        "nombre": "Mareas",
        "tipo": "pueblo",
        "larga": (
            "Mareas es un pueblo pesquero colgado sobre un acantilado, con las casas blancas "
            "encaladas contra la sal. Los barcos salen al amanecer y vuelven al atardecer. "
            "Las mujeres reparan redes en la orilla y salan el pescado en grandes cubas de "
            "madera. Aqui todos conocen el mar desde ninos, y todos han perdido a alguien "
            "en el. El pescado salado de Mareas llega a todas las mesas del reino."
        ),
        "breve": "Mareas, el pueblo pesquero. Huele a sal y a pescado curado.",
        "olores": [
            "Huele a sal, a pescado y a redes de cuerda.",
            "El aire huele a mar abierto y a madera de barco.",
        ],
        "sonidos": [
            "Se oyen las olas contra el acantilado, las gaviotas y las voces de las mujeres.",
            "El crujir de los barcos al mecerse en la cala.",
        ],
        "perfil": "Pueblo pesquero y salazonero. Pescado salado y conservas para el interior.",
        "produce": ["Pescado salado", "Sal", "Conservas"],
    },

    # ─── ALDEAS ────────────────────────────────
    "ermita_alta": {
        "nombre": "Peñalta",
        "tipo": "aldea",
        "larga": (
            "Peñalta esta en lo alto de una colina, donde el viento nunca deja de soplar. "
            "Es una aldea de pastores y de una pequena ermita de piedra donde un monje viejo "
            "oficia misa una vez por semana. Desde arriba se ve todo el valle, y en los dias "
            "claros, dicen, se alcanza a ver la capital. La vida aqui es simple y dura, y el "
            "invierno se lleva a los viejos y a los debiles sin pedir permiso."
        ),
        "breve": "Peñalta, la aldea de pastores. Aqui nace el viento.",
        "olores": [
            "Huele a hierba, a oveja y a incienso viejo.",
            "El aire huele a nieve lejana y a tomillo silvestre.",
        ],
        "sonidos": [
            "Se oye el viento constante, cencerros y el rezo lejano del monje.",
            "El silencio es tan grande que se oye el latido del propio corazon.",
        ],
        "perfil": "Aldea de pastores. Lana, queso y guias de montana.",
        "produce": ["Lana", "Queso", "Guias de montana"],
    },
    "calas": {
        "nombre": "Rocalmar",
        "tipo": "aldea",
        "larga": (
            "Rocalmar es una aldea de pescadores colgada sobre un acantilado pequeno. "
            "Las casas son de piedra oscura, casi negras por la humedad, y huelen a sal "
            "y a humo de hoguera. Aqui viven apenas treinta familias, y todas salen a "
            "pescar al amanecer en barcas que han pasado de padres a hijos. Es un lugar "
            "tranquilo, casi olvidado por el reino, pero el pescado de Rocalmar es el "
            "mejor de la costa."
        ),
        "breve": "Rocalmar, la aldea de pescadores. Piedra oscura y olor a mar.",
        "olores": [
            "Huele a sal, a pescado y a hoguera.",
            "El aire huele a mar y a piedra humeda.",
        ],
        "sonidos": [
            "Se oyen las olas, las gaviotas y las conversaciones tranquilas de los pescadores.",
            "El silencio solo se rompe con el chirriar de las cuerdas de los barcos.",
        ],
        "perfil": "Aldea pesquera pequena. Pescado fresco para pueblos cercanos.",
        "produce": ["Pescado fresco"],
    },
    "fresnillo": {
        "nombre": "Fresnillo",
        "tipo": "aldea",
        "larga": (
            "Fresnillo es una aldea agricola pequena, de casas bajas y tejados de paja, "
            "rodeada de fresnos y campos de trigo. Aqui vive poca gente, pero todos se "
            "conocen y se ayudan. Hay un molino de agua en el rio, junto a la aldea, y el "
            "panadero del pueblo cuece el pan para toda la comarca. Es un lugar tranquilo, "
            "donde nada malo pasa nunca. O casi nunca."
        ),
        "breve": "Fresnillo, la aldea de fresnos. Tranquila y olvidada del mundo.",
        "olores": [
            "Huele a pan recien hecho, a heno y a rio.",
            "El aire huele a hierba y a humo de cocina.",
        ],
        "sonidos": [
            "Se oyen ranas en el rio, el molino de agua y conversaciones suaves.",
            "El canto de los gallos marca las horas del dia.",
        ],
        "perfil": "Aldea agricola. Trigo y pan para los alrededores.",
        "produce": ["Trigo", "Pan"],
    },
}


def obtener_descripcion_ciudad(ciudad_id, primera_vez=False):
    """Devuelve descripcion larga o breve + fragmento sensorial."""
    import random
    datos = CIUDADES.get(ciudad_id)
    if not datos:
        return f"Estas en {ciudad_id.replace('_', ' ').title()}."

    lineas = []
    if primera_vez:
        lineas.append(datos["larga"])
        if datos.get("olores"):
            lineas.append(random.choice(datos["olores"]))
        if datos.get("sonidos"):
            lineas.append(random.choice(datos["sonidos"]))
    else:
        lineas.append(datos["breve"])
        if datos.get("sonidos") and random.random() < 0.4:
            lineas.append(random.choice(datos["sonidos"]))

    return "\n\n  ".join(lineas)


def obtener_nombre(ciudad_id):
    return CIUDADES.get(ciudad_id, {}).get("nombre", ciudad_id)


def obtener_tipo(ciudad_id):
    return CIUDADES.get(ciudad_id, {}).get("tipo", "desconocido")