import psycopg2

def connect():

    conn = psycopg2.connect("host=ll.csjkx7ne9zoj.us-east-1.rds.amazonaws.com port=5432 user=postgres password=Tortoise13")
    cur = conn.cursor()

    return conn, cur


