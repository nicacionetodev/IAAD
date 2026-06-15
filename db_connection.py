"""
Módulo de conexão com o banco de dados MySQL — Copa do Mundo.
Contém funções utilitárias para queries e mapeamento de bandeiras.
"""

import mysql.connector
import pandas as pd
import json
import os

CONFIG_FILE = "db_config.json"

DEFAULT_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "nikond600",
    "database": "Copa_do_Mundo",
    "charset": "utf8mb4",
    "use_unicode": True,
}

def load_db_config():
    """Carrega as credenciais do banco a partir de um arquivo local JSON."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Garantir valores default se faltar alguma chave
                for k, v in DEFAULT_CONFIG.items():
                    if k not in config:
                        config[k] = v
                return config
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_db_config(host, port, user, password, database="Copa_do_Mundo"):
    """Salva as credenciais do banco no arquivo local JSON."""
    config = {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "database": database,
        "charset": "utf8mb4",
        "use_unicode": True,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    global DB_CONFIG
    DB_CONFIG = config

DB_CONFIG = load_db_config()

# ============================================================
# Mapeamento de Países
# ============================================================
COUNTRY_FLAGS = {
    "Brasil": "br",
    "Argentina": "ar",
    "Alemanha": "de",
    "França": "fr",
    "Espanha": "es",
    "Portugal": "pt",
    "Itália": "it",
    "Inglaterra": "gb",
    "Holanda": "nl",
    "Países Baixos": "nl",
    "Uruguai": "uy",
    "Bélgica": "be",
    "Croácia": "hr",
    "Colômbia": "co",
    "México": "mx",
    "Japão": "jp",
    "Coreia do Sul": "kr",
    "Austrália": "au",
    "Estados Unidos": "us",
    "Canadá": "ca",
    "Marrocos": "ma",
    "Senegal": "sn",
    "Gana": "gh",
    "Camarões": "cm",
    "Nigéria": "ng",
    "Tunísia": "tn",
    "Arábia Saudita": "sa",
    "Irã": "ir",
    "Catar": "qa",
    "Equador": "ec",
    "Chile": "cl",
    "Peru": "pe",
    "Paraguai": "py",
    "Bolívia": "bo",
    "Venezuela": "ve",
    "Costa Rica": "cr",
    "Panamá": "pa",
    "Honduras": "hn",
    "Jamaica": "jm",
    "Suíça": "ch",
    "Dinamarca": "dk",
    "Suécia": "se",
    "Noruega": "no",
    "Polônia": "pl",
    "República Tcheca": "cz",
    "Sérvia": "rs",
    "Escócia": "gb",
    "País de Gales": "gb",
    "Irlanda": "ie",
    "Rússia": "ru",
    "Ucrânia": "ua",
    "Romênia": "ro",
    "Grécia": "gr",
    "Turquia": "tr",
    "Egito": "eg",
    "Argélia": "dz",
    "Costa do Marfim": "ci",
    "Áustria": "at",
    "Hungria": "hu",
    "Paraguai": "py",
    "China": "cn",
    "Coreia do Norte": "kp",
}


def get_flag_url(country_name, width=80):
    """Retorna a URL da bandeira do país via flagcdn.com."""
    code = COUNTRY_FLAGS.get(country_name, "")
    if code:
        return f"https://flagcdn.com/w{width}/{code}.png"

    return ""


def get_connection():
    """Cria e retorna uma nova conexão com o banco MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


def test_connection(host, port, user, password, database=None):
    """Testa a conexão com o MySQL usando parâmetros específicos."""
    config = {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "charset": "utf8mb4",
    }
    if database:
        config["database"] = database
    
    conn = mysql.connector.connect(**config)
    conn.close()


def execute_sql_script(conn, filepath):
    """Executa um arquivo script SQL tratando comandos DELIMITER (especialmente para triggers)."""
    with open(filepath, "r", encoding="utf-8") as f:
        sql_content = f.read()

    cursor = conn.cursor()
    statements = []
    current_statement = []
    delimiter = ";"

    for line in sql_content.split("\n"):
        # Remover comentários e espaços vazios
        line_clean = line.split("--")[0].strip()
        if not line_clean:
            continue

        if line_clean.upper().startswith("DELIMITER"):
            parts = line_clean.split()
            if len(parts) > 1:
                delimiter = parts[1]
            continue

        current_statement.append(line_clean)

        if line_clean.endswith(delimiter):
            stmt = " ".join(current_statement)
            if delimiter != ";":
                stmt = stmt[:-len(delimiter)].strip()
            else:
                stmt = stmt.strip()
            if stmt:
                statements.append(stmt)
            current_statement = []

    for stmt in statements:
        cursor.execute(stmt)
    cursor.close()


def init_database(host, port, user, password):
    """Cria o banco de dados e executa os scripts SQL para criar as tabelas e dados iniciais."""
    # 1. Conectar sem especificar database para poder criá-la se necessário
    config = {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "charset": "utf8mb4",
    }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    # Dropar o banco se já existir para garantir uma inicialização limpa com os novos dados
    cursor.execute("DROP DATABASE IF EXISTS `Copa_do_Mundo`")
    cursor.execute("CREATE DATABASE `Copa_do_Mundo` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.close()
    conn.close()

    # 2. Conectar ao banco criado e rodar os scripts
    config["database"] = "Copa_do_Mundo"
    conn = mysql.connector.connect(**config)
    try:
        # Executar Copa_do_Mundo.sql
        if os.path.exists("Copa_do_Mundo.sql"):
            execute_sql_script(conn, "Copa_do_Mundo.sql")
        
        # Executar setup_database.sql
        if os.path.exists("setup_database.sql"):
            execute_sql_script(conn, "setup_database.sql")
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def execute_query(query, params=None):
    """Executa uma query de modificação (INSERT, UPDATE, DELETE).
    Retorna o lastrowid do cursor.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def fetch_all(query, params=None):
    """Executa um SELECT e retorna todos os resultados como lista de dicionários."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def fetch_dataframe(query, params=None):
    """Executa um SELECT e retorna o resultado como DataFrame pandas."""
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        conn.close()


def get_next_id(table, id_column):
    """Retorna o próximo ID disponível (MAX + 1) para uma tabela."""
    result = fetch_all(
        f"SELECT IFNULL(MAX(`{id_column}`), 0) + 1 AS next_id FROM `{table}`"
    )
    return result[0]["next_id"]
