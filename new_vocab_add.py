import psycopg2
import csv
import pickle
import random
from connect import connect
import scheduler
from config import DIRECTORY, COURSE_DIRECTORY
import time

from warning import log_warning

print("dependencies loaded")

def first_set_active(cur, user_id, vocab_id, delay):
    
    ACTIVE_COMMAND = """
    UPDATE user_vocab
    SET active=1, next=(NOW() + (%s * INTERVAL '1 day'))
    WHERE user_id=%s AND vocab_id=%s
    """
    cur.execute(ACTIVE_COMMAND, (delay, user_id, vocab_id)) 
    
def new_vocab_add(cur, user_id, word_no, delay):
    
    LVL_COMMAND = """
    SELECT level FROM users
    WHERE id=%s
    """
    cur.execute(LVL_COMMAND, (user_id,))
    lvl = cur.fetchall()[0][0]
    
    NEW_COMMAND = """
    SELECT u.vocab_id FROM user_vocab u
    INNER JOIN course_vocab cv
    ON u.vocab_id = cv.vocab_id
    WHERE u.user_id = %s AND cv.counts > 1 and u.active = 0 and u.level <= %s
    """
    cur.execute(NEW_COMMAND, (user_id, lvl))
    potential_new_words = [z[0] for z in cur.fetchall()]
    
    print("potential: ", potential_new_words)
    
    new_words = random.sample(potential_new_words, min(word_no, len(potential_new_words)))
    
    print(new_words)
    
    for vocab_id in new_words:
        
        first_set_active(cur, user_id, vocab_id, delay)
        
def new_course(user_id, course_id, words):
    
    conn, cur = connect()
    
    print("YO")
    print(course_id == 1)
    print(course_id == 2)
    
    COMMAND = """SELECT vocab_id, definition FROM course_vocab
    WHERE course_id=%s AND counts > 5
    """
    cur.execute(COMMAND, (course_id,))
    vocab_ids = cur.fetchall()
    level1 = random.sample(vocab_ids, min(15, len(vocab_ids)))
    
    left = list(set(vocab_ids) - set(level1))
    
    INS_COMMAND = """
    INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, definition, level, levelled)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for item in level1:
        print(item)
        cur.execute(INS_COMMAND, (user_id, item[0], 0, 0, 0, item[1], 1, 0))
        
    level2 = random.sample(left, min(15, len(left)))
    
    for item in level2:
        print(item)
        cur.execute(INS_COMMAND, (user_id, item[0], 0, 0, 0, item[1], 2, 0))
        
    new_vocab_add(cur, user_id, 5, 0)
        
    cur.close()
    conn.commit()
    conn.close()
    
    scheduler.schedule(user_id)
    
    