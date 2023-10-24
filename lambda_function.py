import json
import psycopg2
from psycopg2 import sql
import os


def lambda_handler(event, context):
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
        insert = sql.SQL("INSERT INTO POKEMON (nombre) values ('"+nombre+"')returning id;")
        cursor.execute(insert)
        id_pokemon= cursor.fetchone()[0]
        conn.commit()
        insert = sql.SQL("INSERT INTO TIPO (tipo,pokemon_id) values ('"+tipo+"','"+str(id_pokemon)+"')returning id")
        cursor.execute(insert)
        conn.commit()
        insert = sql.SQL("INSERT INTO REGION (region,pokemon_id) values ('"+region+"','"+str(id_pokemon)+"')returning id")
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
    