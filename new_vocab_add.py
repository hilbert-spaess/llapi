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

def initialise_vocab_user(user_id, vocab, word_no):
    
    conn, cur = connect()
    
    # vocab added to user_vocab
    
    INS_COMMAND = """
    INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak)
    VALUES(%s, %s, %s, %s, %s)
    """
    
    for vocab_id in vocab:
        cur.execute(INS_COMMAND, (user_id, vocab_id, 0, 0, 0))
    
    # ?10? words added to reviews IF there are >1 chunks using IT.
                    
    new_vocab_add(cur, user_id, word_no, 0)
    
    cur.close()
    conn.commit()
    conn.close()
    
    scheduler.schedule(user_id)
    
def new_vocab_add(cur, user_id, word_no, delay):
    
    LVL_COMMAND = """
    SELECT level FROM users
    WHERE id=%s
    """
    cur.execute(LVL_COMMAND, (user_id,))
    lvl = cur.fetchall()[0][0]
    
    NEW_COMMAND = """
    SELECT u.vocab_id FROM user_vocab u
    INNER JOIN vocab v
    ON u.vocab_id = v.id
    WHERE u.user_id = %s AND v.counts > 1 and u.active = 0 and u.level <= %s
    """
    cur.execute(NEW_COMMAND, (user_id, lvl))
    potential_new_words = [z[0] for z in cur.fetchall()]
    
    print("potential: ", potential_new_words)

    if len(potential_new_words) < word_no:
        params = {"user_id": user_id, "text": "Not enough new word to add", "time": str(time.time())}
        log_warning(params)
    
    new_words = random.sample(potential_new_words, min(word_no, len(potential_new_words)))
    
    print(new_words)
    
    for vocab_id in new_words:
        
        first_set_active(cur, user_id, vocab_id, delay)
        
def new_course(user_id, course_id):
    
    print("YO")
    print(course_id == 1)
    
    if course_id in [1, "1"]:
        
        conn, cur = connect()
        
        with open(DIRECTORY + "/data/core/core_curriculum.txt", 'r', errors='replace') as curriculumfile:
            
            lines = curriculumfile.readlines()
            
            for row in lines:

                print(row)

                row = row.split(":")

                print(row)
                
                if row[0].strip():

                    
                    INS_COMMAND = """
                    INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, sense, definition, level, levelled)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(INS_COMMAND, (user_id, row[3].strip(), 0, 0, 0, row[1].strip(), row[2].strip(), row[4].strip(), 0))
        
        cur.close()
        conn.commit()
        conn.close()
        
        scheduler.schedule(user_id)
        
    if course_id in [2, "2"]:
        
        print("BBEMLO")

        conn, cur = connect()

        with open(COURSE_DIRECTORY + "2_GRE/curriculum.txt", 'r') as curriculumfile:

            lines = curriculumfile.readlines()
            
            for row in lines:
                
                row = row.split(":")
                
                if row[0].strip():
                    
                    print(row)
                    print(row[3].strip())
                    
                    INS_COMMAND = """
                    INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, definition, level)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(INS_COMMAND, (user_id, row[3].strip(), 0, 0, 0, row[2].strip(), row[4].strip()))
        

        new_vocab_add(cur, user_id, 5, 0)

        cur.close()
        conn.commit()
        conn.close()

        scheduler.schedule(user_id)
    
