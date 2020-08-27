import psycopg2
import numpy as np
import csv
import pickle
import random

def on_review(cur, req):
    
    # log result
    
    log_result(cur, req)
    
    remove_chunk(cur, req)
    
    correct = req["answeredCorrect"]
    
    if correct:
        
        # set unscheduled in user_vocab; set time for next review to be scheduled.

        set_unscheduled(cur, req)
    
def log_result(cur, req):
    
    # user_vocab_log
    
    COMMAND = """
    INSERT INTO user_vocab_log(user_id, vocab_id, chunk_id, result)
    VALUES(%s, %s, %s, %s)
    """
    cur.execute(COMMAND, (req["userId"], req["interaction"][req["currentInteraction"]]["v"], req["chunkId"], req["answeredCorrect"]))

def remove_chunk(cur, req):
    
    COMMAND = """
    DELETE FROM user_nextchunk
    WHERE user_id=%s and chunk_id=%s
    """
    cur.execute(COMMAND, (req["userId"], req["chunkId"]))

def set_unscheduled(cur, req):
    
    COMMAND = """
    UPDATE user_vocab
    SET scheduled=0, next=(NOW() + (%s * INTERVAL '1 day')), streak=%s
    WHERE user_id=%s AND vocab_id=%s
    """
    cur.execute(COMMAND, (next_time(req), req["streak"], req["userId"], req["interaction"][req["currentInteraction"]]["v"]))
    
def next_time(req):
    
    # return time to next review in days
    
    streak_to_days = {1: "1", 2: "2", 3: "4", 4: "7", 5: "14"}
    
    return streak_to_days[req["streak"]]
    