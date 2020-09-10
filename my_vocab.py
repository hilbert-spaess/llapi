import psycopg2

def load_vocab(cur, user_id, req):
    
    out = {}
    
    def get_active_vocab():

        # return dictionary of active vocab with streaks

        COMMAND = """
        SELECT v.id, v.word, u.streak FROM user_vocab u
        INNER JOIN vocab v
        ON v.id = u.vocab_id
        WHERE u.user_id=%s AND u.active=%s
        """
        cur.execute(COMMAND, (user_id, "1"))

        known_vocab = cur.fetchall()
        
        active = {}

        for item in known_vocab:

            active[item[0]] = {'w': item[1], 's': item[2]}

        return active
    
    def get_future_vocab():

        # return dictionary of active vocab with streaks

        COMMAND = """
        SELECT v.id, v.word FROM user_vocab u
        INNER JOIN vocab v
        ON v.id = u.vocab_id
        WHERE u.user_id=%s AND u.active=%s
        """
        cur.execute(COMMAND, (user_id, "0"))

        known_vocab = cur.fetchall()
        
        future = {}

        for item in known_vocab:

            future[item[0]] = {'w': item[1]}

        return future
    
    out["active"] = get_active_vocab()
    
    out["future"] = get_future_vocab()
    
    return out
    
    
    