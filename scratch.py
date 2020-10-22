# port definitions from course_vocab to vocab

from connect import connect

def port_definition(cur, course_id, vocab_id):
    
    DEFCOM = """SELECT definition FROM course_vocab
    WHERE course_id=%s AND vocab_id=%s
    """
    cur.execute(DEFCOM, (course_id, vocab_id))
    
    definition = cur.fetchall()[0][0]
    
    COMM = """UPDATE vocab 
    SET definition=%s
    WHERE id=%s
    """
    cur.execute(COMM, (definition, vocab_id))
    
def port_all_definitions(cur):
    
    cur.execute("SELECT course_id, vocab_id FROM course_vocab")
    records = cur.fetchall()
    print(records)
    
    for instance in records:
        
        print(instance[0])
        port_definition(cur, instance[0], instance[1])
    
conn, cur = connect()

port_all_definitions(cur)

cur.close()
conn.commit()
conn.close()