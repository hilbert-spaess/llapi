import psycopg2

def load_progress(cur, user_id):
    
    out = {}
    
    def load_course_name():
        
        COMMAND = """SELECT c.name FROM courses c
        INNER JOIN users u
        ON u.course_id = c.id
        WHERE u.id=%s
        """
        cur.execute(COMMAND, (user_id,))
        
        course_name = cur.fetchall()[0][0]
        
        return course_name
    
    def load_vocab_progress():
        
        COMMAND = """
        SELECT v.id, v.word, u.streak, u.active FROM user_vocab u
        INNER JOIN vocab v
        ON v.id = u.vocab_id
        WHERE u.user_id=%s
        """
        cur.execute(COMMAND, (user_id,))
        
        records = cur.fetchall()
        
        active = 0.0
        streaks = 0.0
        total = len(records)
        mastered = 0
        
        for instance in records:
            if instance[2] > 0:
                active += 1
                streaks += instance[2]
            if instance[2] > 4:
                mastered += 1
                
        return active, streaks, total, mastered
    
    out["course_name"] = load_course_name()
    active, streaks, total, mastered = load_vocab_progress()
    
    print("active", active)
    print("streaks", streaks)
    print("total", total)
    
    level_prop = round((float(streaks)/150.0)*100)
    out["level_prop"] = level_prop
    
    out["active"] = active
    out["mastered"] = mastered
    
    active_prop = round(float(active)/float(total) * 100)
    print("active_prop", active_prop)
    
    out["active_prop"] = active_prop
    
    return out
    
    