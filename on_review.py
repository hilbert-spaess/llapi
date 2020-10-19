import psycopg2
import numpy as np
import csv
import pickle
import random

def set_first(cur, user_id, req):
    
    chunk_id = req["chunkId"]
    
    COMMAND = """UPDATE user_nextchunk
    SET first=0
    WHERE user_id=%s AND chunk_id=%s
    """
    cur.execute(COMMAND, (user_id, chunk_id))
    

def on_review(cur, user_id, req):
    
    key_location = int(req["keyloc"])
    correct = req["answers"][key_location]
    
    streak = req["streak"]
    
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
        
         streak_to_days = {1: "1", 2: "2", 3: "3", 4: "6", 5: "14", 6: "30", 7: "60", 8: "100"}
    
         return streak_to_days[streak]
    
    def handle_levels():
        
        COMMAND = """UPDATE user_vocab
        SET levelled=1
        WHERE user_id=%s AND vocab_id=%s"""
        
        if streak == 4:
            
            cur.execute(COMMAND, (user_id, req["interaction"][req["keyloc"]]["v"]))
            
        LVL_COMMAND = """SELECT level
        FROM users WHERE id=%s"""
        cur.execute(LVL_COMMAND, (user_id,))
        
        level = cur.fetchall()[0][0]
        
        COMMAND = """SELECT levelled FROM user_vocab
        WHERE user_id=%s AND level=%s"""
        cur.execute(COMMAND, (user_id, level))
        records = cur.fetchall()
        
        total = len(records)
        levelled = len([x for x in records if x[0]])
        
        if (float(levelled)/float(total)) > 0.8:
            
            COMMAND = """UPDATE users
            SET level=level+1
            WHERE id=%s
            """
            cur.execute(COMMAND, (user_id,))
            
            populate_levels(level+1)
    
    def populate_levels(level):
        
        for crucial_level in [level, level+1]:
            
            CRS_COMMAND = """SELECT course_id FROM users
            WHERE id=%s
            """
            cur.execute(CRS_COMMAND, (user_id,))
            course_id = cur.fetchall()[0][0]
            
            ALL_COMMAND = """SELECT vocab_id, definition FROM user_vocab
            WHERE user_id=%s
            """
            cur.execute(ALL_COMMAND, (user_id,))
            all_current = cur.fetchall()
            
            COMMAND = """SELECT * FROM user_vocab
            WHERE level = %s AND user_id=%s
            """
            cur.execute(COMMAND, (str(crucial_level), user_id))
            
            t = len(cur.fetchall())

            if t < 15:
                
                COMMAND = """SELECT vocab_id, definition FROM course_vocab
                WHERE course_id=%s AND counts > 4
                """
                cur.execute(COMMAND, (course_id,))
                all_potentials = cur.fetchall()
                
                potentials = list(set(all_potentials) - set(all_current))
                
                new_vocab = random.sample(potentials, min(len(potentials), 15 - t))
                
                INS_COMMAND = """
                INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, definition, level, levelled, course_id)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                for item in new_vocab:
                    
                    cur.execute(INS_COMMAND, (user_id, str(item[0]), 0, 0, 0, item[1], crucial_level, 0, course_id))
                    
                    
                
                
            
            
            
            
        
    
    # log result
    
    log_result()
    
    print("Result logged")
    
    remove_chunk()
    
    print("Deleted")
    
    print("correct", correct)

    set_unscheduled()
    
    handle_levels()
    
def manual_level_up(cur, user_id):
    
    def populate_levels(level):
        
        for crucial_level in [level, level+1]:
            
            CRS_COMMAND = """SELECT course_id FROM users
            WHERE id=%s
            """
            cur.execute(CRS_COMMAND, (user_id,))
            course_id = cur.fetchall()[0][0]
            
            ALL_COMMAND = """SELECT vocab_id, definition FROM user_vocab
            WHERE user_id=%s
            """
            cur.execute(ALL_COMMAND, (user_id,))
            all_current = cur.fetchall()
            
            COMMAND = """SELECT * FROM user_vocab
            WHERE level = %s AND user_id=%s
            """
            cur.execute(COMMAND, (str(crucial_level), user_id))
            
            t = len(cur.fetchall())

            if t < 15:
                
                COMMAND = """SELECT vocab_id, definition FROM course_vocab
                WHERE course_id=%s AND counts > 4
                """
                cur.execute(COMMAND, (course_id,))
                all_potentials = cur.fetchall()
                
                potentials = list(set(all_potentials) - set(all_current))
                
                new_vocab = random.sample(potentials, min(len(potentials), 15 - t))
                
                INS_COMMAND = """
                INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, definition, level, levelled, course_id)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                for item in new_vocab:
                    
                    cur.execute(INS_COMMAND, (user_id, str(item[0]), 0, 0, 0, item[1], crucial_level, 0, course_id))
                    
        
    COMMAND = """UPDATE users
    SET level=level+1
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    
    COMMAND = """SELECT level FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    level = cur.fetchall()[0][0]

    populate_levels(level)