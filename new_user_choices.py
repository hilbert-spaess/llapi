import random
import new_vocab_add

from connect import connect

def course_vocab_samples(cur, course_id):
    
    VOCAB_COMMAND = """SELECT v.word FROM course_vocab cv
    INNER JOIN vocab v
    ON cv.vocab_id = v.id
    WHERE cv.course_id=%s
    """
    cur.execute(VOCAB_COMMAND, (course_id,))
    
    vocab = cur.fetchall()
    vocab = random.sample([x[0] for x in vocab], min(35, len(vocab)))
    
    return vocab

def course_vocab_submit(user_id, course_id, words):
    
    conn, cur = connect()
    
    # get a sample rank
    
    # vlevel, message
    
    course_id = int(course_id)
    
    if course_id==1:
        
        message = "This is the Core TOEFL course. If you want to change the difficulty, or if you have any questions, get in touch."
        vlevel = "10000"
        
    if course_id==2:
        
        message = "This is the Core GRE course. If you want to change the difficulty, or if you have any questions, get in touch."
        vlevel = "30000"
        
    if course_id==5:
        
        message = "Primary school reading account. If you want to change the difficulty, or if you have any questions, get in touch."
        vlevel= "5000"
        
    if course_id==7:
        
        message = "Year 4 reading account. Get in touch if you have questions."
        vlevel = "7000"
        
    if course_id==6:
        
        message = "Essay vocab account. Get in touch if you have questions."
        vlevel = "10000"
        
    COMMAND = """UPDATE users
    SET vlevel=%s, message=%s
    WHERE id=%s
    """
    cur.execute(COMMAND, (vlevel, message, user_id))
    
    cur.close()
    conn.commit()
    conn.close()
    
    new_vocab_add.new_course(user_id, course_id, words)
    
    