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
        SELECT v.id, v.word, u.streak, u.definition, u.sense FROM user_vocab u
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
        SELECT v.id, v.word, u.definition, u.sense FROM user_vocab u
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
    
    def get_vocab_dict():
        
        # get all vocab with streak, sense, samples and level
        
        COMMAND = """
        SELECT v.id, v.word, u.definition, u.sense, u.level, u.streak FROM user_vocab u
        INNER JOIN vocab v
        ON v.id = u.vocab_id
        WHERE u.user_id=%s
        """
        cur.execute(COMMAND, (user_id,))
        records = cur.fetchall()
        print("all")
        
        print(records)
        
        vocabdict = {}
        
        for item in records:
            
            sentences = get_all_sample_sentences(item[0], item[3])
            
            if item[4] in vocabdict.keys():
                vocabdict[item[4]][item[0]] = {"samples": sentences, "w": item[1], "d": item[2], "s": item[5]}
            else:
                print("bemloe")
                vocabdict[item[4]] = {item[0]: {"samples": sentences, "w": item[1], "d": item[2], "s": item[5]}}

        return vocabdict
    
    out = {}
    
    out["vocab"] = get_vocab_dict()
    
    out["level"] = get_user_level()
    
    print(out)
    
    return out
    
    
    