import psycopg2
import csv
import pickle
import random

def find_unscheduled_vocab(cur, user_id):
    
    FIND_COMMAND = """
    SELECT vocab_id FROM user_vocab
    WHERE user_id=%s AND active=1 AND scheduled=0
    """
    cur.execute(FIND_COMMAND, (user_id,))
    unscheduled_vocab = [x[0] for x in cur.fetchall()]
    
    return unscheduled_vocab

def get_schedule_time(cur, vocab_id, user_id):
    
    COMMAND="""
    SELECT next FROM user_vocab
    WHERE user_id = %s AND vocab_id = %s
    """
    cur.execute(COMMAND, (user_id, vocab_id))
    schedule_time = cur.fetchall()[0][0]
    
    return schedule_time

def schedule_next_chunk_basic(cur, vocab_id, user_id, schedule_time):
    
    # works well while the user hasn't seen that much stuff.
    
    # look for all chunks containing the vocab
    
    NEXT_COMMAND = """
    SELECT chunk_id FROM chunk_vocab
    WHERE vocab_id = %s
    """
    cur.execute(NEXT_COMMAND, (vocab_id,))
    potential_nexts = [x[0] for x in cur.fetchall()]
    
    # look for the chunks the user has already seen
    
    ALREADY_COMMAND = """
    SELECT chunk_id FROM user_vocab_log
    WHERE user_id = %s AND vocab_id=%s
    """
    cur.execute(ALREADY_COMMAND, (user_id, vocab_id,))
    already_seen = [x[0] for x in cur.fetchall()]
    
    candidates = list(set(potential_nexts) - set(already_seen))
    
    next_chunk = random.sample(candidates, 1)[0]
    
    # schedule the next chunk
    
    SCHEDULE_COMMAND = """
    INSERT INTO user_nextchunk(user_id, chunk_id, next, vocab, unknown_vocab, vocab_interaction)
    VALUES(%s, %s, %s, %s, 0, %s)
    """
    cur.execute(SCHEDULE_COMMAND, (user_id, next_chunk, schedule_time, vocab_id, "3"))
    
def set_scheduled(cur, vocab_id, user_id):
    
    COMMAND = """
    UPDATE user_vocab
    SET scheduled=1
    WHERE user_id=%s and vocab_id=%s
    """
    cur.execute(COMMAND, (user_id, vocab_id))
    
def schedule(cur, user_id):
    
    # find active yet unscheduled words
    
    unscheduled_vocab = find_unscheduled_vocab(cur, user_id)
    
    for vocab_id in unscheduled_vocab:
        
        schedule_time = get_schedule_time(cur, vocab_id, user_id)
    
        schedule_next_chunk_basic(cur, vocab_id, user_id, schedule_time)
        
        set_scheduled(cur, vocab_id, user_id)

def optimise(user_id):
    
    pass

def new_review_add(user_id):
    
    pass

conn = psycopg2.connect("dbname=ll user=postgres password=postgres")
cur = conn.cursor()

schedule(cur, "1")

cur.close()
conn.commit()
conn.close()