import psycopg2
from connect import connect
from config import COURSE_DIRECTORY

def user_update(cur, course_id):

    course_dict = {"2": "2_GRE/"}

    CHECK_COMMAND = """SELECT * FROM user_vocab
    WHERE user_id=%s AND vocab_id=%s
    """
    
    INS_COMMAND ="""INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, definition, level, levelled)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
    """
    
    USR_COMMAND="""SELECT id FROM users
    WHERE course_id=%s"""
    
    cur.execute(USR_COMMAND, (course_id,))
    users = [x[0] for x in cur.fetchall()]
    
    
    with open(COURSE_DIRECTORY + course_dict[course_id] + "curriculum.txt", 'r', errors='replace') as curriculumfile:

            lines = [x for x in curriculumfile.readlines() if x.strip()]
            vocablist = [x.split(":") for x in lines]
            
            print(vocablist)
    
    for user_id in users:
        for vocab in vocablist:
            cur.execute(CHECK_COMMAND, (user_id, vocab[3].strip()))
            r = cur.fetchall()
            if not r:
                cur.execute(INS_COMMAND, (user_id, vocab[3].strip(), 0, 0, 0, vocab[2].strip(), vocab[4].strip(), 0))
            
def course_message(cur, course_id, course_message):
    
    COMMAND = """UPDATE users 
    SET message=%s
    WHERE course_id=%s
    """
    cur.execute(COMMAND, (course_message, course_id))
        
conn, cur = connect()

user_update(cur, "2")

cur.close()
conn.commit()
conn.close()
