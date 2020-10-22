from config import COURSE_DIRECTORY
import os

from connect import connect

with open(os.path.join(COURSE_DIRECTORY, "course_course.txt"), 'r') as CSFILE:

    lines = CSFILE.readlines()

    course_course = {x.split(":")[0].strip():[y.strip() for y in x.split(":")[1].split(",")] for x in lines}
        
def hanging_vocab(cur, user_id):
    
    CRS_COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    COMMAND = """SELECT course_id, vocab_id FROM user_vocab
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))
    
    records = cur.fetchall()
    
    hanging_ids = []
    
    for instance in records:
        
        if not instance[0]:
            
            hanging_ids.append(instance[1])
            
    CRS_COMMAND = """SELECT definition FROM course_vocab
    WHERE course_id=%s AND vocab_id=%s
    """
    
    INS_COMMAND = """UPDATE user_vocab
    SET active=0, scheduled=0, streak=0, definition=%s, levelled=0, course_id=%s
    WHERE vocab_id=%s AND user_id=%s
    """
            
    for vocab_id in hanging_ids:
        
        CRS_COMMAND = """SELECT definition FROM course_vocab
        WHERE course_id=%s AND vocab_id=%s
        """
        
        course_list = [course_id] + course_course[str(course_id)]
        
        for course in course_list:
            
            cur.execute(CRS_COMMAND, (course, vocab_id))
            r = cur.fetchall()
            
            if r:
                cur.execute(INS_COMMAND, (r[0][0], course, vocab_id, user_id))
                break
                
                
        
conn, cur = connect()
hanging_vocab(cur, "308")

cur.close()
conn.commit()
conn.close()