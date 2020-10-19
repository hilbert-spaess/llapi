import random
import new_vocab_add

from connect import connect

def course_vocab_samples(cur, user_id):
    
    CRS_COMMAND = """SELECT course_id
    FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    
    course_id = cur.fetchall()[0][0]
    
    VOCAB_COMMAND = """SELECT v.word FROM course_vocab cv
    INNER JOIN vocab v
    ON cv.vocab_id = v.id
    WHERE cv.course_id=%s
    """
    cur.execute(VOCAB_COMMAND, (course_id,))
    
    vocab = cur.fetchall()
    vocab = random.sample([x[0] for x in vocab], min(20, len(vocab)))
    
    return vocab

def course_vocab_submit(user_id, words):
    
    conn, cur = connect()
    
    # get a sample rank
    
    # vlevel, message
    
    CRS_COMMAND = """SELECT course_id
    FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    
    course_id = cur.fetchall()[0][0]
    
    print(course_id)
    
    if course_id==1:
        
        message = "This is the Core TOEFL course. If you want to change the difficulty, or if you have any questions, get in touch."
        vlevel = "10000"
        
    if course_id==2:
        
        message = "This is the Core GRE course. If you want to change the difficulty, or if you have any questions, get in touch."
        vlevel = "30000"
        
    if course_id==5:
        
        message = "Primary school reading account. If you want to change the difficulty, or if you have any questions, get in touch."
        vlevel= "5000"
        
    COMMAND = """UPDATE users
    SET vlevel=%s, message=%s
    WHERE id=%s
    """
    cur.execute(COMMAND, (vlevel, message, user_id))
    
    cur.close()
    conn.commit()
    conn.close()
    
    new_vocab_add.new_course(user_id, course_id, words)
    
    