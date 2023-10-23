import json
import psycopg2
from psycopg2 import sql
import os


def lambda_handler(event,context):
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']


    try:
        conn = psycopg2.connect(
            host = db_host,
            port = db_port,
            database = db_name,
            user = db_user,
            password = db_password
        )
        body=json.loads(event['body'])
        nombre = body['nombre']
        tipo = body['tipo']
        region = body['region']

        cursor = conn.cursor()
        sql = sql.SQL("INSERT INTO values POKEMONS (nombre)returnig id;")
        cursor.execute(insert)
        id.pokemon= cursor.fetchone()[0]
        conn.commit()
        insert = sql.SQL("INSERT INTO TIPO POKEMON = id.pokemon, tipo = tipo")
        cursor.execute(insert)
        conn.commit()
        insert = sql.SQL("INSERT INTO REGION POKEMON = id.pokemon, region = region")
        cursor.execute(insert)
        conn.commit()

        cursor.close()
        conn.close()

        response = {
            "statusCode": 200,
            "body":"Pokemon insertado correctamente" 
        }

    except Exception as e:
        response = {
        "statusCode": 500,
            "body":str(e)
        }
    
    return response
    