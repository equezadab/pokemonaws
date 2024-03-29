import json
import psycopg2
import os
from psycopg2 import sql

def lambda_handler(event, context):
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_port = os.environ['DB_PORT']

    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        print("Connected to database")
        cursor = conn.cursor()
        body = json.loads(event['body'])
        nombre = body['nombre_pokemon']
        tipo = body['tipo_pokemon']
        region = body['region_pokemon']

        insert = sql.SQL("INSERT INTO pokemon (nombre) VALUES ({}) returning id").format(sql.Literal(nombre))
        cursor.execute(insert)
        id_pokemon = cursor.fetchone()[0]
        conn.commit()  # Agregué los paréntesis aquí

        insert = sql.SQL("INSERT INTO region (region) VALUES ({}) returning id").format(sql.Literal(region))
        cursor.execute(insert)
        conn.commit()  # Agregué los paréntesis aquí
        id_region = cursor.fetchone()[0]

        insert = sql.SQL("INSERT INTO tipo (tipo) VALUES ({}) returning id").format(sql.Literal(tipo))
        cursor.execute(insert)
        conn.commit()  # Agregué los paréntesis aquí
        id_tipo = cursor.fetchone()[0]

        insert = sql.SQL("INSERT INTO region_pokemon (id_region, id_pokemon) VALUES ({}, {}) returning id").format(sql.Literal(id_region), sql.Literal(id_pokemon))
        cursor.execute(insert)
        conn.commit()  # Agregué los paréntesis aquí

        insert = sql.SQL("INSERT INTO tipo_pokemon (id_tipo, id_pokemon) VALUES ({}, {}) returning id").format(sql.Literal(id_tipo), sql.Literal(id_pokemon))
        cursor.execute(insert)
        conn.commit()  # Agregué los paréntesis aquí

        cursor.close()
        conn.close()

        response = {
            "statusCode": 200,
            "body": "Pokemon insertado correctamente"
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": str(e)
        }
    return response

