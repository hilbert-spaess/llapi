from config import COURSE, LIST, LIST_NO
from connect import connect

def add_list(cur):

    with open(LIST, 'r') as listfile:
        
        newlist = [x.strip() for x in listfile.readlines() if x.strip()]

        print(newlist)

    COMMAND = """SELECT vocab_id FROM course_vocab cv INNER JOIN vocab v
    ON v.id = cv.vocab_id
    WHERE course_id=%s AND word=%s
    """
    
    INS_COMMAND = """INSERT INTO list_vocab(list_id, vocab_id)
    VALUES(%s, %s)
    """
    
    vocab_ids = []

    for wd in newlist:

        cur.execute(COMMAND, (COURSE, wd))
        vocab_id = cur.fetchall()[0][0]
        
        print(wd)
        print(vocab_id)

        cur.execute(INS_COMMAND, (LIST_NO, vocab_id))
        


    

conn, cur = connect()
add_list(cur)       
cur.close()
conn.commit()
conn.close()

