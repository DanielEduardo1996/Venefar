# -*- coding: utf-8 -*-
"""VENEFAR - Base de Datos"""
import sqlite3, hashlib

DB_PATH = "venefar_mundo.db"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = conectar()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS mundo (id INTEGER PRIMARY KEY, dia INTEGER, estacion TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS npcs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE, edad INTEGER, sexo TEXT, oficio TEXT,
        rasgos TEXT, pasado TEXT, sueno TEXT, miedo TEXT, secreto TEXT,
        detalle TEXT, mood TEXT, relacion INTEGER DEFAULT 0,
        te_conoce INTEGER DEFAULT 0, dias_sin_hablar INTEGER DEFAULT 0,
        dinero INTEGER DEFAULT 0,
        descripcion_vista INTEGER DEFAULT 0,
        ciudad TEXT DEFAULT 'capital_imperial',
        atributos_fisicos TEXT DEFAULT '{}')""")
    c.execute("""CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        npc_id INTEGER, producto TEXT, cantidad INTEGER,
        FOREIGN KEY (npc_id) REFERENCES npcs(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS recuerdos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        npc_id INTEGER, dia INTEGER, tipo TEXT, contenido TEXT,
        importancia INTEGER DEFAULT 1,
        FOREIGN KEY (npc_id) REFERENCES npcs(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS frases_usadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        npc_id INTEGER, hash TEXT, dia INTEGER,
        FOREIGN KEY (npc_id) REFERENCES npcs(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dia INTEGER, tipo TEXT, descripcion TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS transacciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dia INTEGER, comprador TEXT, vendedor TEXT,
        producto TEXT, cantidad INTEGER, precio_total INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS jugador (
        identificador TEXT PRIMARY KEY,
        nombre TEXT,
        dinero INTEGER DEFAULT 0,
        inventario TEXT DEFAULT '[]',
        hambre INTEGER DEFAULT 100,
        sed INTEGER DEFAULT 100,
        cansancio INTEGER DEFAULT 0,
        salud INTEGER DEFAULT 100,
        energia INTEGER DEFAULT 100,
        hora INTEGER DEFAULT 8,
        ciudad TEXT DEFAULT 'capital_imperial',
        ciudades_vistas TEXT DEFAULT '[]')""")
    c.execute("""CREATE TABLE IF NOT EXISTS eventos_activos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT, dia_inicio INTEGER, dias_restantes INTEGER,
        datos TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS reputacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT, ciudad TEXT, valor INTEGER DEFAULT 0,
        UNIQUE(jugador_id, ciudad))""")
    c.execute("""CREATE TABLE IF NOT EXISTS propiedades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT, ciudad TEXT, tipo TEXT,
        nivel INTEGER DEFAULT 1, mejora TEXT DEFAULT '{}',
        UNIQUE(jugador_id, ciudad, tipo))""")
    c.execute("""CREATE TABLE IF NOT EXISTS cofre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT, ciudad TEXT, producto TEXT, cantidad INTEGER,
        UNIQUE(jugador_id, ciudad, producto))""")
    c.execute("""CREATE TABLE IF NOT EXISTS cuentas_banco (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT, ciudad TEXT,
        saldo INTEGER DEFAULT 0,
        ultimo_interes_dia INTEGER DEFAULT 1,
        interes_pendiente REAL DEFAULT 0.0,
        UNIQUE(jugador_id, ciudad))""")
    c.execute("""CREATE TABLE IF NOT EXISTS prestamos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT, ciudad TEXT,
        monto_original INTEGER,
        saldo_pendiente INTEGER,
        dia_otorgado INTEGER,
        dia_ultimo_interes INTEGER,
        estado TEXT DEFAULT 'activo')""")
    c.execute("""CREATE TABLE IF NOT EXISTS negocios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT, ciudad TEXT, tipo TEXT,
        nivel INTEGER DEFAULT 1,
        dia_apertura INTEGER,
        ganancia_acumulada INTEGER DEFAULT 0,
        activo INTEGER DEFAULT 1,
        UNIQUE(jugador_id, ciudad))""")
    c.execute("""CREATE TABLE IF NOT EXISTS caravanas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT,
        ciudad_origen TEXT, ciudad_destino TEXT,
        contenido TEXT,
        coste INTEGER,
        dia_salida INTEGER, dia_llegada INTEGER,
        estado TEXT DEFAULT 'en_camino',
        ingreso_estimado INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS equipado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id TEXT, slot TEXT, item_id TEXT,
        UNIQUE(jugador_id, slot))""")
    # ─── Guarniciones ───
    c.execute("""CREATE TABLE IF NOT EXISTS guarniciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ciudad TEXT UNIQUE,
        num_soldados INTEGER,
        reservas_armas INTEGER DEFAULT 0,
        reservas_armaduras INTEGER DEFAULT 0,
        dia_ultima_revision INTEGER DEFAULT 1,
        dia_ultima_importacion INTEGER DEFAULT 0)""")

    for migracion in [
        "ALTER TABLE npcs ADD COLUMN descripcion_vista INTEGER DEFAULT 0",
        "ALTER TABLE npcs ADD COLUMN ciudad TEXT DEFAULT 'capital_imperial'",
        "ALTER TABLE npcs ADD COLUMN atributos_fisicos TEXT DEFAULT '{}'",
        "ALTER TABLE jugador ADD COLUMN ciudad TEXT DEFAULT 'capital_imperial'",
        "ALTER TABLE jugador ADD COLUMN ciudades_vistas TEXT DEFAULT '[]'",
        "ALTER TABLE cuentas_banco ADD COLUMN interes_pendiente REAL DEFAULT 0.0",
    ]:
        try: c.execute(migracion)
        except Exception: pass

    conn.commit()
    return conn


def hash_frase(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()