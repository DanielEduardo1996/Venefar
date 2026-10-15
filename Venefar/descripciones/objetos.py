# -*- coding: utf-8 -*-
"""
VENEFAR - Descripciones de Objetos
Cada objeto tiene su descripcion. Fallback por palabras clave.
"""

OBJETOS = {
    "Ropa de lino": {
        "descripcion": (
            "Ropa sencilla de lino, del color del trigo. Esta limpia pero muy usada; "
            "los codos estan desgastados y el cuello ha perdido su forma original. "
            "Es la ropa de alguien que no tiene mucho, pero que cuida lo poco que tiene."
        ),
    },
    "Carta de recomendación": {
        "descripcion": (
            "Un pliego de papel grueso, doblado en cuatro. Lleva el sello de un noble menor "
            "de la capital y unas pocas lineas escritas con pluma cuidada. La tinta esta "
            "ligeramente corrida por la humedad. Quien te la dio, confiaba en ti. O queria "
            "librarse de ti."
        ),
    },
    "Anillo con sello": {
        "descripcion": (
            "Un anillo de plata con un sello tallado en la cara. El sello muestra una torre "
            "con tres almenas. El metal esta oscurecido por el uso, pero el sello sigue "
            "siendo legible. Con este anillo, puedes firmar documentos en nombre de una casa. "
            "Usalo bien, o acabara en el cuello de alguien."
        ),
    },
    "Ropa de terciopelo": {
        "descripcion": (
            "Ropa de terciopelo azul oscuro, con bordados de hilo dorado en los puños y el "
            "cuello. Esta hecha a medida, y se nota. Huele a lavanda, a madera de cedro y a "
            "dinero antiguo. Ponertela es recordar que hubo un tiempo en que tu familia tenia "
            "algo que perder."
        ),
    },
    "Espada de entrenamiento": {
        "descripcion": (
            "Una espada de madera pesada, marcada con cientos de golpes. El mango esta envuelto "
            "en tela gastada para no lastimar la mano. No corta, pero pesa como una espada de "
            "verdad, y quien te la dio, te hizo sudar con ella. Sigue siendo un buen recuerdo."
        ),
    },
    "Cuchillo de abordaje": {
        "descripcion": (
            "Un cuchillo corto de hoja ancha y curva, disenado para cortar cabos y, si hace "
            "falta, gargantas. La hoja esta manchada de oxido en la base, pero el filo sigue "
            "cuidado. El mango de madera tiene marcas de dedos. Huele a aceite de pescado."
        ),
    },
    "Amuleto de hueso": {
        "descripcion": (
            "Un pequeno amuleto de hueso tallado, colgado de un cordel de cuero. La talla "
            "representa un pez con la boca abierta. Los marineros dicen que protege del "
            "ahogamiento. No sabes si es verdad, pero no te lo quitas."
        ),
    },
    "Ropa raída": {
        "descripcion": (
            "Ropa que ha visto mejores tiempos. Esta remendada en varios sitios con hilo de "
            "distinto color, y el tejido esta tan gastado que es casi translucido en algunas "
            "zonas. Huele a humedad y a tierra. Es la ropa de quien ha dormido en el suelo "
            "mas de una vez."
        ),
    },
    "Un diente de lobo": {
        "descripcion": (
            "Un diente de lobo engarzado en un anillo de cuero. Esta amarillento por el tiempo. "
            "Lo llevas colgado del cuello, como recuerdo de algo que no quieres contar. "
            "Quien lo ve, sabe que no eres de los que huyen."
        ),
    },
    "Herramientas básicas": {
        "descripcion": (
            "Un juego de herramientas de artesano: un martillo, unas tenazas, un cincel y una "
            "lima. Todas estan marcadas con un punzon distinto, de distintos talleres. Huele a "
            "aceite y a hierro. Con esto puedes hacer reparaciones basicas."
        ),
    },
    "Hoz": {
        "descripcion": (
            "Una hoz de segar, con la hoja curvada y afilada, y el mango de madera envuelto en "
            "trapo. La hoja tiene pequenas mellas del uso, pero sigue cortando bien. Huele a "
            "hierba seca y a sudor de trabajo."
        ),
    },
    "Saco de semillas": {
        "descripcion": (
            "Un saco de tela gruesa, atado con un cordel, medio lleno de semillas de trigo. "
            "Pesa poco. Las semillas son pequenas, doradas, y suenan al mover el saco. "
            "Es la promesa de una cosecha futura, si el tiempo acompana."
        ),
    },
    "Herramientas de oficio": {
        "descripcion": (
            "Herramientas especificas de un oficio artesanal. Estan gastadas por el uso, pero "
            "cuidadas con esmero. El que las uso antes que tu, sabia lo que hacia. Ahora te "
            "toca a ti aprender."
        ),
    },
    "Delantal de cuero": {
        "descripcion": (
            "Un delantal de cuero grueso, manchado de tintes, de grasa y de mil cosas mas. "
            "Los bordes estan deshilachados y el cuero esta endurecido por el uso. Huele a "
            "taller y a trabajo. Ponertelo es casi un rito."
        ),
    },
    "Frasco de tinta": {
        "descripcion": (
            "Un pequeno frasco de vidrio oscuro, lleno a dos tercios de tinta negra. El tapon "
            "es de corcho, y esta manchado de dedos. La tinta es buena, no de las baratas que "
            "se corren. Huele a hierro y a humedad."
        ),
    },
    "Mapa antiguo": {
        "descripcion": (
            "Un mapa dibujado a mano en pergamino, ya amarillento por los anos. Muestra tierras "
            "que no reconoce del todo, con nombres escritos en una caligrafia antigua. Hay "
            "lineas trazadas y borradas varias veces. Alguien paso mucho tiempo con este mapa. "
            "Alguien, quizas, encontro lo que buscaba. O no."
        ),
    },
    "Azada": {
        "descripcion": (
            "Una azada de labranza, con la hoja de hierro gastada por el uso y el mango de "
            "madera pulida por las manos. Huele a tierra y a hierba. Con esto se ara la tierra, "
            "y con la tierra se come."
        ),
    },
    "Capa de lana": {
        "descripcion": (
            "Una capa gruesa de lana, del color de la tierra mojada. Esta tejida a mano, con "
            "puntos irregulares, hecha para durar mas que para verse bien. Abriga mucho. "
            "Huele a oveja y a humo de hogar."
        ),
    },
    "Libros": {
        "descripcion": (
            "Un pequeno fajo de libros encuadernados en cuero, con las esquinas gastadas y "
            "algunas paginas marcadas con tiras de tela. Los titulos estan escritos en latin "
            "y en una lengua mas antigua. Pesan mas de lo que parecen. Dentro hay conocimiento, "
            "y a veces, peligro."
        ),
    },
    "Pluma y tinta": {
        "descripcion": (
            "Una pluma de ganso, cortada en punta fina, y un pequeno tintero de ceramica. La "
            "pluma esta manchada de tinta seca y el tintero tiene el borde gastado. Con esto "
            "se escriben cartas, contratos, y a veces mentiras."
        ),
    },
    "Arco": {
        "descripcion": (
            "Un arco corto de tejo, con la cuerda de tripa tensada. La madera esta pulida y "
            "encerada para protegerla de la humedad. Huele a madera y a resina. Es un arma "
            "silenciosa, paciente, y letal si se usa bien."
        ),
    },
    "Cuchillo de desollar": {
        "descripcion": (
            "Un cuchillo corto de hoja curva, disenado para desollar animales sin danar la piel. "
            "La hoja esta muy afilada y manchada de grasa y sangre seca. El mango de asta esta "
            "gastado por el uso. Huele a caza, a cuero y a monte."
        ),
    },
    "Ganzúas": {
        "descripcion": (
            "Un juego de ganzuas de acero fino, enganchadas en un anillo de cuero. Cada una "
            "tiene una forma distinta, para cerraduras distintas. Estan limpias, cuidadas, y "
            "guardadas en un estuche de tela. Herramientas de un oficio silencioso."
        ),
    },
    "Daga envenenada": {
        "descripcion": (
            "Una daga corta de hoja oscura, casi negra. La hoja tiene un brillo extrano que no "
            "es del todo metalico. En la base hay una muesca, donde se aplica el veneno. "
            "Manejarla con cuidado, o el que se corte, sera el primero en caer."
        ),
    },
    "Kit de alquimia": {
        "descripcion": (
            "Una bolsa de cuero con compartimentos, llena de frasquitos, morteros, y sobres de "
            "polvo. Todo esta etiquetado con una caligrafia pequena y cuidadosa. Huele a "
            "hierbas, a azufre y a algo mas que no sabes nombrar. Con esto se hacen remedios "
            "y venenos."
        ),
    },
    "Hierbas medicinales": {
        "descripcion": (
            "Un manojo de hierbas secas, atadas con un cordel. Reconoces tomillo, romero y "
            "algunas otras que no sabes nombrar. Huelen fuerte, a campo y a medicina. Con "
            "ellas se curan heridas y fiebres."
        ),
    },
    "Espada corta": {
        "descripcion": (
            "Una espada corta de acero, sencilla, sin adornos. La hoja esta manchada en la "
            "base donde el metal se ha desgastado con el tiempo. La empunadura de cuero "
            "trenzado esta oscurecida por el sudor. En la guarda hay una pequena marca: una "
            "torre con tres almenas. Es un arma de factura comun, pero bien cuidada."
        ),
    },
    "Espada de calidad": {
        "descripcion": (
            "Una espada corta de acero de buena factura. La hoja tiene un brillo azulado, senal "
            "de buen temple. El equilibrio es perfecto, la empunadura esta envuelta en cuero "
            "nuevo, y la guarda tiene un grabado fino en forma de hoja de roble. No es un arma "
            "noble, pero es un arma que salva vidas."
        ),
    },
    "Chaqueta de cuero": {
        "descripcion": (
            "Una chaqueta de cuero grueso, curtido y trabajado para darle flexibilidad. Esta "
            "forrada por dentro con lana, y tiene varios bolsillos interiores. Huele a cuero, "
            "a aceite y a sudor. Ha visto mejores dias, pero sigue siendo buena proteccion."
        ),
    },
    "Armadura de cuero": {
        "descripcion": (
            "Una armadura ligera de cuero hervido, con refuerzos de metal en los hombros y el "
            "pecho. Esta ajustada con correas de cuero, y por dentro tiene un forro de tela. "
            "No te hara invulnerable, pero te dara una oportunidad."
        ),
    },
    "Piel de cabra": {
        "descripcion": (
            "Una piel de cabra curtida, usada como capa o como manta. Es aspera al tacto, "
            "pero abriga mucho. Huele a animal y a humo de hoguera. En las noches frias, "
            "vale mas que el oro."
        ),
    },
    "Cayado tallado": {
        "descripcion": (
            "Un cayado de pastor, largo y resistente, con la punta curvada y tallada con "
            "figuras que parecen ovejas. La madera esta pulida por anos de uso. Huele a "
            "monte y a lana. Sirve para caminar, para guiar, y si hace falta, para defenderse."
        ),
    },
    "Balanza de bolsillo": {
        "descripcion": (
            "Una balanza pequena de bronce, con dos platillos colgados de cadenas finas. "
            "Esta guardada en un estuche de cuero acolchado. Con ella se pesan monedas, "
            "especias, oro en polvo. Herramienta de mercader, y a veces, de estafador."
        ),
    },
    "Libro de cuentas": {
        "descripcion": (
            "Un libro de contabilidad encuadernado en cuero, con las esquinas gastadas. "
            "Las paginas estan llenas de numeros, fechas y nombres escritos con caligrafia "
            "apretada. Algunas hojas estan marcadas con tiras de tela de distintos colores. "
            "Aqui esta la historia economica de una familia."
        ),
    },
    "Brújula improvisada": {
        "descripcion": (
            "Una brujula rudimentaria, hecha con una aguja de hierro imantada flotando en "
            "un pequeno cuenco de agua. No es precisa, pero apunta aproximadamente al norte. "
            "Con ella no te perderas del todo."
        ),
    },
    "Manta de viaje": {
        "descripcion": (
            "Una manta de lana gruesa, enrollada y atada con una correa de cuero. Esta "
            "gastada en los bordes, pero abriga bien. Huele a camino y a hierba. La mejor "
            "companera en una noche al raso."
        ),
    },
    "Mercancía variada": {
        "descripcion": (
            "Un conjunto de mercancias de todo tipo: telas, especias, pequenas herramientas, "
            "abalorios. Todo esta guardado en cajas y sacos, cuidadosamente organizado. "
            "Con esto se comercia en cualquier mercado."
        ),
    },
    "Balanza": {
        "descripcion": (
            "Una balanza grande de bronce, de las que se usan en los mercados. Los platillos "
            "estan pulidos por el uso, y el fiel esta bien equilibrado. Con ella se pesa todo "
            "lo que se vende, y se evitan discusiones."
        ),
    },
    "Documentos falsos": {
        "descripcion": (
            "Un fajo de documentos con sellos que parecen autenticos. El papel es bueno, la "
            "tinta es buena, y los nombres son creibles. Solo alguien muy experto notaria "
            "que el sello esta ligeramente descentrado. Con esto, puedes ser quien quieras."
        ),
    },
    "Una carta sin firma": {
        "descripcion": (
            "Una carta doblada, escrita con pluma cuidadosa pero sin firma. Las palabras son "
            "ambiguas, y el que la escribio conocia bien a quien iba dirigida. Puede ser una "
            "promesa, una amenaza, o ambas cosas."
        ),
    },
    "Media moneda partida": {
        "descripcion": (
            "Media moneda de plata, cortada por la mitad con un golpe limpio. El borde cortado "
            "esta alisado por el desgaste. Alguien tiene la otra mitad. Si algun dia "
            "encuentras a esa persona, sabras quien es."
        ),
    },
    "Recuerdo del amor perdido": {
        "descripcion": (
            "Un pequeno objeto, sin valor material, pero con un valor enorme para ti. Cada "
            "vez que lo miras, recuerdas algo que ya no esta. Hay que ser fuerte para "
            "cargar con esto. Y para no cargar con esto."
        ),
    },
    "Objeto del descubrimiento": {
        "descripcion": (
            "Un objeto extrano, encontrado en circunstancias que no olvidaras. Su forma no "
            "corresponde a nada que hayas visto antes, y su material no parece comun. "
            "Al mirarlo, sientes que hay algo mas detras, algo que aun no comprendes."
        ),
    },
    "Objeto de esa persona": {
        "descripcion": (
            "Un objeto personal que pertenecio a alguien que ya no esta. Lo llevas contigo "
            "para no olvidar. Huele ligeramente a su perfume, o a su tabaco, o a su casa. "
            "No tiene precio. No hay dinero que lo pague."
        ),
    },
}


PALABRAS_CLAVE = {
    "pan": (
        "Un pan redondo de corteza dorada y crujiente, aun tibio. Huele a horno y a trigo. "
        "Partirlo es casi un ritual. Comerlo, un placer sencillo."
    ),
    "vino": (
        "Una botella de vino de color oscuro. El corcho esta puesto a mano, y el liquido "
        "tiene posos. No es un gran vino, pero cumple su funcion."
    ),
    "hierro": (
        "Un lingote de hierro en bruto, de forma irregular y peso considerable. Su superficie "
        "esta oxidada en algunas zonas. Con esto se forjan herramientas, armas y mil cosas mas."
    ),
    "madera": (
        "Un fajo de madera cortada y secada al aire, lista para usar. Huele a resina y a "
        "bosque. Con esto se construye, se cocina y se calienta."
    ),
    "trigo": (
        "Una bolsa de trigo limpio, sin cascaras. Los granos son dorados y pesados. Con esto "
        "se hace harina, y con harina, pan."
    ),
    "uva": (
        "Un racimo de uvas oscuras, o una cesta con varias. Estan maduras, dulces, con la piel "
        "tirante. Se comen frescas, o se prensan para hacer vino."
    ),
    "hierba": (
        "Un manojo de hierbas secas, aromaticas. Huelen a campo. Sirven para cocinar, para "
        "curar y, en manos expertas, para envenenar."
    ),
    "espada": (
        "Un arma de acero, de hoja recta y afilada. Su peso y equilibrio dicen mucho de quien "
        "la forjo. En las manos correctas, decide destinos."
    ),
    "daga": (
        "Un arma corta y discreta, facil de ocultar. Su hoja es corta pero afilada, y su "
        "mango esta hecho para sujetarse con firmeza. No es un arma de honor, es un arma "
        "de resultado."
    ),
    "armadura": (
        "Un conjunto de proteccion para el cuerpo, hecho de cuero, metal o ambos. Pesa, "
        "pero salva vidas. Un buen guerrero cuida su armadura como a su propia piel."
    ),
    "libro": (
        "Un libro encuadernado en cuero, con las paginas amarillentas por el tiempo. "
        "Contiene palabras, y las palabras contienen mundos."
    ),
    "moneda": (
        "Una moneda de curso comun. De un lado, la efigie del rey; del otro, el escudo del "
        "reino. Con monedas se compra pan, se paga deudas y se compra silencio."
    ),
}


def obtener_descripcion_objeto(nombre_objeto):
    """Devuelve descripcion del objeto por nombre exacto, palabra clave o fallback."""
    # Limpiar nombre por si es "3x Pan" o similar
    limpio = nombre_objeto
    if "x " in limpio:
        limpio = limpio.split("x ", 1)[1]

    # Busqueda exacta
    if limpio in OBJETOS:
        return OBJETOS[limpio]["descripcion"]

    # Busqueda por palabra clave
    limpio_low = limpio.lower()
    for kw, desc in PALABRAS_CLAVE.items():
        if kw in limpio_low:
            return desc

    # Fallback generico
    return (
        f"Un objeto llamado '{limpio}'. No tienes una descripcion detallada de el, "
        f"pero su simple presencia te recuerda a algo, o a alguien."
    )