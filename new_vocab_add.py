import psycopg2
import csv
import pickle
import random
from connect import connect
import scheduler

def first_set_active(cur, user_id, vocab_id):
    
    ACTIVE_COMMAND = """
    UPDATE user_vocab
    SET active=1, next=NOW()
    WHERE user_id=%s AND vocab_id=%s
    """
    cur.execute(ACTIVE_COMMAND, (user_id, vocab_id))             

def initialise_vocab_user(cur, user_id, vocab, word_no):
    
    # vocab added to user_vocab
    
    INS_COMMAND = """
    INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak)
    VALUES(%s, %s, %s, %s, %s)
    """
    
    for vocab_id in vocab:
        cur.execute(INS_COMMAND, (user_id, vocab_id, 0, 0, 0))
    
    # ?10? words added to reviews IF there are >1 chunks using IT.
                    
    new_vocab_add(cur, user_id, word_no)
    
    scheduler.schedule(cur, user_id)
    
    
    
    
def new_vocab_add(cur, user_id, word_no):
    
    NEW_COMMAND = """
    SELECT u.vocab_id FROM user_vocab u
    INNER JOIN vocab v
    ON u.vocab_id = v.id
    WHERE u.user_id = %s AND v.counts > 1 and u.active = 0
    """
    cur.execute(NEW_COMMAND, (user_id,))
    potential_new_words = [z[0] for z in cur.fetchall()]
    
    print("potential: ", potential_new_words)
    
    new_words = random.sample(potential_new_words, min(word_no, len(potential_new_words)))
    
    print(new_words)
    
    for vocab_id in new_words:
        
        first_set_active(cur, user_id, vocab_id)
    
    
    

conn, cur = connect()

core_ids = pickle.load(open("./data/core/toefl_core_ids.data", 'rb'))
initialise_vocab_user(cur, "1", core_ids, 5)

cur.close()
conn.commit()
conn.close()
