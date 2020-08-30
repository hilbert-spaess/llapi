import psycopg2
import csv
import pickle
import random
from connect import connect
import test_data
import json

def find_unscheduled_vocab(cur, user_id):
    
    FIND_COMMAND = """
    SELECT vocab_id FROM user_vocab
    WHERE user_id=%s AND active=%s AND scheduled=%s
    """
    cur.execute(FIND_COMMAND, (user_id,1,0))
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

def choose_next_chunk(cur, vocab_id, user_id):
    
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
    
    return next_chunk

def get_unknown_vocab(cur, vocab_id, user_id):
    
    # TODO: code for unknown vocab
    
    return "0"


def schedule_next_chunk_basic(cur, vocab_id, user_id):
    
    # works well while the user hasn't seen that much stuff.
    
    # look for all chunks containing the vocab
    
    next_chunk = choose_next_chunk(cur, vocab_id, user_id)
    
    schedule_time = get_schedule_time(cur, vocab_id, user_id)
    
    unknown_vocab = get_unknown_vocab(cur, vocab_id, user_id)
    
    my_test_data = test_data.get_test_data(cur, vocab_id, user_id, next_chunk)
    
    SCHEDULE_COMMAND = """
    INSERT INTO user_nextchunk(user_id, chunk_id, next, test_data, unknown_vocab)
    VALUES(%s, %s, %s, %s, %s)
    """
    cur.execute(SCHEDULE_COMMAND, (user_id, next_chunk, schedule_time, json.dumps(my_test_data), unknown_vocab))
    
def set_scheduled(cur, vocab_id, user_id):
    
    COMMAND = """
    UPDATE user_vocab
    SET scheduled=1
    WHERE user_id=%s and vocab_id=%s
    """
    cur.execute(COMMAND, (user_id, vocab_id))
    
def schedule(user_id):
    
    conn, cur = connect()
    
    print("HEMLO")
    
    # find active yet unscheduled words
    
    unscheduled_vocab = find_unscheduled_vocab(cur, user_id)
    
    print("unscheduled: ", unscheduled_vocab)
    
    for vocab_id in unscheduled_vocab:
    
        schedule_next_chunk_basic(cur, vocab_id, user_id)
        
        set_scheduled(cur, vocab_id, user_id)
        
    cur.close()
    conn.commit()
    conn.close()

def optimise(user_id):
    
    pass

def new_review_add(user_id):
    
    pass
