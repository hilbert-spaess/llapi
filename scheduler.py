import psycopg2
import csv
import pickle
import random
from connect import connect
import test_data
import json

from warning import log_warning
import time

import os
from config import COURSE_DIRECTORY

def find_unscheduled_vocab(cur, user_id):
    
    FIND_COMMAND = """
    SELECT vocab_id FROM user_vocab
    WHERE user_id=%s AND active=%s AND scheduled=%s
    """
    cur.execute(FIND_COMMAND, (user_id,1,0))
    unscheduled_vocab = [x[0] for x in cur.fetchall()]
    
    print("UNSCHEDULED VOCAB")
    print(unscheduled_vocab)
    
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
    
    CRS_COMMAND = """SELECT course_id
    FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    with open(os.path.join(COURSE_DIRECTORY, 'course_source.txt'), 'r') as CSFILE:
        
         lines = CSFILE.readlines()
            
    course_source = {x.split(":")[0].strip():[y.strip() for y in x.split(":")[1].split(",")] for x in lines}
    
    source_list = course_source[str(course_id)]
    
    NEXT_COMMAND = """
    SELECT chunk_id FROM chunk_vocab cv
    INNER JOIN chunks c
    ON c.id = cv.chunk_id
    WHERE cv.vocab_id = %s AND c.source=%s
    """
    
    # look for the chunks the user has already seen
    
    ALREADY_COMMAND = """
    SELECT chunk_id FROM user_vocab_log
    WHERE user_id = %s AND vocab_id=%s
    """
    cur.execute(ALREADY_COMMAND, (user_id, vocab_id,))
    already_seen = [x[0] for x in cur.fetchall()]
    
    for source in source_list:
        
        cur.execute(NEXT_COMMAND, (vocab_id, source))
        potential_nexts = [x[0] for x in cur.fetchall()]
        
        candidates = list(set(potential_nexts) - set(already_seen))
        random.shuffle(candidates)
        
        if candidates:
            
            next_chunk = random.sample(candidates, 1)[0]
            
            return next_chunk
        
        elif potential_nexts:
            
            next_chunk = random.sample(potential_nexts, 1)[0]
            
    return 0
    
    #candidates = list(set(potential_nexts) - set(already_seen))
    
    #random.shuffle(candidates)

def get_unknown_vocab(cur, vocab_id, user_id):
    
    # TODO: code for unknown vocab
    
    return "0"

def get_streak(cur, vocab_id, user_id):
    
    COMMAND = """SELECT streak FROM user_vocab
    WHERE user_id=%s AND vocab_id=%s
    """
    cur.execute(COMMAND, (user_id, vocab_id))
    
    return cur.fetchall()[0]

def schedule_next_chunk_basic(cur, vocab_id, user_id):
    
    # works well while the user hasn't seen that much stuff.
    
    # look for all chunks containing the vocab
    
    next_chunk = choose_next_chunk(cur, vocab_id, user_id)

    if not next_chunk:
        return 0
    
    schedule_time = get_schedule_time(cur, vocab_id, user_id)
    
    unknown_vocab = get_unknown_vocab(cur, vocab_id, user_id)
    
    my_test_data = test_data.get_test_data(cur, vocab_id, user_id, next_chunk)
    
    SCHEDULE_COMMAND = """
    INSERT INTO user_nextchunk(user_id, chunk_id, next, test_data, unknown_vocab, first, vocab_id)
    VALUES(%s, %s, %s, %s, %s, 1, %s)
    """
    cur.execute(SCHEDULE_COMMAND, (user_id, next_chunk, schedule_time, json.dumps(my_test_data), unknown_vocab, vocab_id))

def schedule_next_chunk_fixed(cur, vocab_id, user_id, next_chunk):
    
    unknown_vocab = get_unknown_vocab(cur, vocab_id, user_id)
    
    my_test_data = test_data.get_test_data(cur, vocab_id, user_id, next_chunk)
    
    SCHEDULE_COMMAND = """
    INSERT INTO user_nextchunk(user_id, chunk_id, next, test_data, unknown_vocab, first, vocab_id)
    VALUES(%s, %s, NOW(), %s, %s, 1, %s)
    """
    cur.execute(SCHEDULE_COMMAND, (user_id, next_chunk, json.dumps(my_test_data), unknown_vocab, vocab_id))
    
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
