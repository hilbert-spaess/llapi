import psycopg2
import numpy as np
import csv
import pickle
import random

def on_review(cur, req):
    
    key_location = int(req["key"])
    correct = req["answers"][key_location]
    streak = req["interaction"][str(key_location)]["streak"] + correct
    
    print("Streak", streak)
    
    def log_result():
    
        # user_vocab_log

        COMMAND = """
        INSERT INTO user_vocab_log(user_id, vocab_id, chunk_id, result)
        VALUES(%s, %s, %s, %s)
        """
        cur.execute(COMMAND, (req["userId"], req["interaction"][req["key"]]["v"], req["chunkId"], correct))
        
    def remove_chunk():
    
        COMMAND = """
        DELETE FROM user_nextchunk
        WHERE user_id=%s and chunk_id=%s
        """
        cur.execute(COMMAND, (req["userId"], req["chunkId"]))
        
    def set_unscheduled():
    
        COMMAND = """
        UPDATE user_vocab
        SET scheduled=0, next=(NOW() + (%s * INTERVAL '1 day')), streak=%s
        WHERE user_id=%s AND vocab_id=%s
        """
        cur.execute(COMMAND, (next_time(), streak, req["userId"], req["interaction"][req["key"]]["v"]))
        
    def next_time():
        
         streak_to_days = {1: "1", 2: "2", 3: "4", 4: "7", 5: "14"}
    
         return streak_to_days[streak]
        
    
    # log result
    
    log_result()
    
    print("Result logged")
    
    remove_chunk()
    
    print("Deleted")
    
    if correct:
        
        print("CORRECT")
        
        # set unscheduled in user_vocab; set time for next review to be scheduled.

        set_unscheduled()
    