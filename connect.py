import psycopg2

def connect()
    
    conn = psycopg2.connect("dbname=ll user=postgres password=postgres")
    cur = conn.cursor()
    
    return conn, cur