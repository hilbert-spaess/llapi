import psycopg2

def load_vocab(cur, user_id, req):
    
    def get_all_sample_sentences(v, sense):
    
        COMMAND = """SELECT c.chunk, c.sentence_breaks, cv.first_sentence, cv.locations FROM chunks c
        INNER JOIN chunk_vocab cv
        ON cv.chunk_id = c.id
        WHERE cv.vocab_id=%s AND cv.sense=%s
        """
        cur.execute(COMMAND, (v, sense))
        sentences = []

        for instance in cur.fetchall():

            sentence_breaks = [-1] + [int(k) for k in instance[1].split(",")]
            lower_cap = sentence_breaks[int(instance[2])] + 1
            upper_cap = sentence_breaks[int(instance[2])+1] + 1

            location = int(instance[3].split(",")[0]) - lower_cap
            sentence = "#".join(instance[0].split("#")[lower_cap: upper_cap])

            sentences.append((sentence, location))

            sentences.sort(key=lambda x: len(x[0]))

        return sentences
        
    
    def get_active_vocab():

        # return dictionary of active vocab with streaks

        COMMAND = """
        SELECT v.id, v.word, u.streak, v.definition, u.sense FROM user_vocab u
        INNER JOIN vocab v
        ON v.id = u.vocab_id
        WHERE u.user_id=%s AND u.active=%s
        """
        cur.execute(COMMAND, (user_id, "1"))

        known_vocab = cur.fetchall()
        
        active = {}

        for item in known_vocab:
            
            sentences = get_all_sample_sentences(item[0], item[4])

            active[item[0]] = {'w': item[1], 's': item[2], 'd': item[3]}
            
            if sentences:
                active[item[0]]['samples'] = sentences

        return active
    
    def get_future_vocab():

        # return dictionary of active vocab with streaks

        COMMAND = """
        SELECT v.id, v.word, v.definition, u.sense FROM user_vocab u
        INNER JOIN vocab v
        ON v.id = u.vocab_id
        WHERE u.user_id=%s AND u.active=%s
        """
        cur.execute(COMMAND, (user_id, "0"))

        known_vocab = cur.fetchall()
        
        future = {}

        for item in known_vocab:
            
            
            sentences = get_all_sample_sentences(item[0], item[3])

            future[item[0]] = {'w': item[1], "d": item[2]}
            
            if sentences:
                future[item[0]]['samples'] = sentences

        return future
    
    def get_user_level():
        
        COMMAND = """SELECT level FROM users
        WHERE id=%s
        """
        cur.execute(COMMAND, (user_id,))
        
        return cur.fetchall()[0][0]
    
    def get_max_level():
        
        COMMAND = """SELECT level FROM user_vocab
        WHERE user_id=%s
        """
        cur.execute(COMMAND, (user_id,))
        l = max([x[0] for x in cur.fetchall()])
        return l + 1
    
    def get_vocab_dict():
        
        # get all vocab with streak, sense, samples and level
        
        COMMAND = """
        SELECT v.id, v.word, v.definition, u.sense, u.level, u.streak, u.active FROM user_vocab u
        INNER JOIN vocab v
        ON v.id = u.vocab_id
        WHERE u.user_id=%s
        """
        cur.execute(COMMAND, (user_id,))
        records = cur.fetchall()
        print("all")
        
        print(records)
        
        vocablist = []
        
        for item in records:
            
            sentences = get_all_sample_sentences(item[0], item[3])

            vocablist.append({"samples": sentences, "w": item[1], "d": item[2], "s": item[5], "l": item[4], "a": item[6]})
            
            vocablist.sort(key=lambda x: int(x['l']))

        return vocablist
    
    out = {}
    
    
    out["vocab"] = get_vocab_dict()
    
    print(out["vocab"])
    
    out["level"] = get_user_level()
    
    out["maxlevel"] = get_max_level()
    
    print(out)
    
    return out

def new_word(cur, word, user_id):
    
    def check_in_course():
        
        CRS_COMMAND = """SELECT course_id FROM users
        WHERE id=%s
        """
        cur.execute(CRS_COMMAND, (user_id,))
        course_id = cur.fetchall()[0][0]
        
        COMMAND = """SELECT v.word, v.id, v.pos, v.definition FROM course_vocab cv
        INNER JOIN vocab v
        ON v.id = cv.vocab_id
        WHERE cv.course_id=%s AND v.word=%s
        """
        cur.execute(COMMAND, (course_id, word))
        return cur.fetchall()
    
    def check_in_dictionary():
        
        COMMAND = """SELECT word, id, pos FROM vocab
        WHERE word=%s
        """
        cur.execute(COMMAND, (word,))
        
        return cur.fetchall()
        
    # check if in course
    
    in_course = check_in_course()
    
    LVL_COMMAND = """SELECT * FROM user_vocab uv 
    INNER JOIN users u
    ON u.id = uv.user_id
    WHERE u.id=%s AND uv.level = u.level
    """
    cur.execute(LVL_COMMAND, (user_id,))
    l = len(cur.fetchall())
    
    m = 15
    level = l
    if l >= m:
        
        level = l+1
    
    if in_course:
        
        INS_COMMAND = """
        INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, definition, level, levelled)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        
        return {"state": "in_dictionary", "data": in_course}
    
    # check if in dictionary
    
    in_dictionary = check_in_dictionary()
    
    if in_dictionary:
        
        COMMAND = """INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, level, levelled)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
        
        return {"state": "in_dictionary", "data": in_dictionary}
    
    return {"state": "not_in_dictionary", "data": word}

def confirm_new_word(cur, data, user_id):
    
    word = data[0]
    vocab_id = data[1]
    
    def check_in_course():
        
        CRS_COMMAND = """SELECT course_id FROM users
        WHERE id=%s
        """
        cur.execute(CRS_COMMAND, (user_id,))
        course_id = cur.fetchall()[0][0]
        
        COMMAND = """SELECT * FROM course_vocab
        WHERE course_id=%s AND vocab_id=%s
        """
        cur.execute(COMMAND, (course_id, vocab_id))
        return cur.fetchall()
    
    def check_in_dictionary():
        
        COMMAND = """SELECT word, id, pos FROM vocab
        WHERE word=%s
        """
        cur.execute(COMMAND, (word,))
        
        return cur.fetchall()
    
    MAXLVL_COMMAND = """SELECT level FROM user_vocab
    WHERE user_id=%s
    """
    cur.execute(MAXLVL_COMMAND, (user_id,))
    level = max([x[0] for x in cur.fetchall()])
    
    LVL_COMMAND = """SELECT * FROM user_vocab
    WHERE user_id=%s AND level=%s
    """
    cur.execute(LVL_COMMAND, (user_id,str(level)))
                
    l = len(cur.fetchall())
    
    
    if l>=15:
        
        level += 1
        
    print("LEVEL", level)
               
        
    in_course = check_in_course()
    
    INS_COMMAND = """INSERT INTO user_vocab(user_id, vocab_id, active, scheduled, streak, level, levelled)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(INS_COMMAND, (user_id, vocab_id, "0", "0", "0", level, "0"))

    
    