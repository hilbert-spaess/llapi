import psycopg2
import numpy as np
import csv
import pickle
import random

def on_review(cur, user_id, req):
    
    key_location = int(req["keyloc"])
    correct = req["answers"][key_location]
    
    def calculate_streak():
        
        current_streak = req["interaction"][str(key_location)]["streak"]
        
        if not correct:
            return 1
        
        else:
            return current_streak + 1
        
    streak = calculate_streak()
    
    print("Streak", streak)
            
    
    def log_result():
    
        # user_vocab_log

        COMMAND = """
        INSERT INTO user_vocab_log(user_id, vocab_id, chunk_id, result, time)
        VALUES(%s, %s, %s, %s, NOW())
        """
        cur.execute(COMMAND, (user_id, req["interaction"][req["keyloc"]]["v"], req["chunkId"], correct))
        
        # user_recentchunk
        
        COMMAND = """
        UPDATE user_recentchunk
        SET chunk2=chunk1, chunk1=%s
        WHERE user_id=%s AND vocab_id=%s AND sense=%s
        """
        cur.execute(COMMAND, (req["chunkId"], user_id, req["interaction"][req["keyloc"]]["v"], req["interaction"][req["keyloc"]]["sense"]))
        
    def remove_chunk():
    
        COMMAND = """
        DELETE FROM user_nextchunk
        WHERE user_id=%s and chunk_id=%s
        """
        cur.execute(COMMAND, (user_id, req["chunkId"]))
        
    def set_unscheduled():
        
        print(next_time())
        print(streak)
    
        COMMAND = """
        UPDATE user_vocab
        SET scheduled=0, next=(NOW() + (%s * INTERVAL '1 day')), streak=%s
        WHERE user_id=%s AND vocab_id=%s
        """
        cur.execute(COMMAND, (next_time(), streak, user_id, req["interaction"][req["keyloc"]]["v"]))
        
    def next_time():
        
         streak_to_days = {1: "1", 2: "2", 3: "4", 4: "7", 5: "14"}
    
         return streak_to_days[streak]
        
    
    # log result
    
    log_result()
    
    print("Result logged")
    
    remove_chunk()
    
    print("Deleted")
    
    print("correct", correct)

    set_unscheduled()
    