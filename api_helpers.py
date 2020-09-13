import numpy as np
import random
import psycopg2
import threading
import scheduler

def get_grammar(chunkid, cur):

    COMMAND = """
    SELECT g.id, g.item, cg.locations FROM grammar g
    INNER JOIN chunk_grammar cg
    ON g.id = cg.grammar_id
    WHERE cg.chunk_id=%s
    """
    cur.execute(COMMAND, (chunkid,))
    return(cur.fetchall())

def get_vocab(chunkid, cur):

    COMMAND = """
    SELECT v.id, v.word, cv.locations, v.pos, cv.first_sentence FROM vocab v
    INNER JOIN chunk_vocab cv
    ON v.id = cv.vocab_id
    WHERE cv.chunk_id=%s
    """
    cur.execute(COMMAND, (chunkid,))
    return(cur.fetchall())

def get_relevant_sentences(cur, user_id, v, chunkids):
    
    # return array of the relevant sentences
    
    COMMAND = """SELECT c.chunk, c.sentence_breaks, cv.first_sentence, cv.locations FROM chunks c
    INNER JOIN chunk_vocab cv
    ON cv.chunk_id = c.id
    WHERE c.id=%s OR c.id=%s
    """
    cur.execute(COMMAND, chunkids)
    sentences = []
    
    for instance in cur.fetchall():
        
        sentence_breaks = [-1] + [int(k) for k in instance[1].split(",")]
        lower_cap = sentence_breaks[int(instance[2])] + 1

        location = int(instance[3].split(",")[0]) - lower_cap
        sentence = instance[0].split("#")[lower_cap: upper_cap]
        
        sentences.append((sentence, location))
    
    return sentences
        

def get_vocab_interaction_data(cur, user_id, chunkid, v, interaction):
    
    interaction_data = []
    COMMAND = """
    SELECT v.pos, v.zipf, v.word, cv.tags FROM vocab v
    INNER JOIN chunk_vocab cv
    ON cv.vocab_id = v.id
    WHERE v.id = %s AND chunk_id=%s
    """
    cur.execute(COMMAND, (v, chunkid))

    out = cur.fetchall()[0]
    pos = out[0]; zipf = out[1]; wd = out[2]; tag = out[3].split(",")[0]
    
    outdata = {}
    
    outdata["tag"] = tag

    if interaction=="1":
        
        # load a sentence

        COMMAND = """
        SELECT c.id, c.chunk, cv.locations FROM chunks c
        INNER JOIN chunk_vocab cv
        ON c.id = cv.chunk_id
        WHERE cv.vocab_id=%s AND c.id !=%s AND c.sentence=1
        """
        cur.execute(COMMAND, (v,chunkid))
        options = cur.fetchall()
        outdata["raw"] = random.sample(options, min(2, len(options)))

    if interaction=="2":
        
        # load synonyms from synonym database

        COMMAND = """
        SELECT v.word, v.zipf FROM vocab v
        INNER JOIN synonyms s
        ON s.vocab2_id = v.id
        WHERE s.vocab1_id=%s
        """
        cur.execute(COMMAND, (v,))
        options = cur.fetchall()
        options.sort(key=lambda x: x[1])
        outdata["raw"] = options[max(-len(options), -3):]

    if interaction=="3":
        
        # 

        COMMAND = """
        SELECT word, zipf FROM vocab
        WHERE pos=%s AND ABS(id - %s) < 200 AND id != %s
        """
        cur.execute(COMMAND, (pos, v, v))
        options = cur.fetchall()
        options.sort(key=lambda x: np.abs(x[1] - zipf))
        y = options[:min(len(options), 3):]
        y.append((wd, zipf))
        random.shuffle(y)
        outdata["raw"] = y
    
    if interaction=="4":
        
        COMMAND = """
        SELECT s.definition FROM synsets s
        INNER JOIN chunk_vocab cv
        ON cv.sense = s.id
        WHERE cv.chunk_id=%s AND cv.vocab_id=%s
        """
        print(chunkid, v)
        cur.execute(COMMAND, (chunkid, v))
        r = cur.fetchall()
        if not r:
            return get_vocab_interaction_data(cur, user_id, chunkid, v, "3")
        print(r)
        definition = r[0][0]
        outdata["raw"] = definition
        
    if interaction=="5":
        
        COMMAND = """
        SELECT rc.chunk1, rc.chunk2 FROM user_recentchunk rc
        INNER JOIN chunk_vocab cv
        ON cv.sense = rc.sense
        WHERE rc.user_id=%s AND  rc.vocab_id=%s AND cv.chunk_id=%s
        """
        cur.execute(COMMAND, (user_id, v, chunkid))
        chunk_ids = cur.fetchall()[0]
        outdata["raw"] = get_relevant_sentences(cur, user_id, v, chunk_ids)
    
    outdata["mode"] = interaction
    return outdata

def choose_next_chunk(cur, user_id):
    
    # check if next chunk is determined
    
    COMMAND = """
    SELECT c.id FROM chunks C
    INNER JOIN user_nextchunk u
    ON c.id = u.chunk_id
    WHERE u.user_id = %s AND EXTRACT(DAY FROM u.next) <= EXTRACT(DAY FROM NOW()) 
    """
    cur.execute(COMMAND, (user_id,))
    choices = cur.fetchall()
    
    out = {}
    
    if not choices:
        return None
    
    else:
        choices = random.sample(choices, 1)
        return choices[0]
    

def build_context(chunk, grammar, vocab, unknown_vocab):
    
    context = {}
    
    for idx, word in enumerate(chunk):
        context[str(idx)] = {'w': word, 'g': [], 'v': 0, 'u': 0}
        
    for item in grammar:
        for j in item[2].split(","):
            context[j]['g'].append(str(item[0]))

    for item in vocab:
        for j in item[2].split(","):
            context[j]['v'] = str(item[0])
            context[j]['vw'] = str(item[1])
            context[j]['p'] = str(item[3])
     
    for key in context.keys():
        if key in unknown_vocab:
            context[key]['u'] = 1
        context[key]['g'] = ','.join(context[key]['g'])
        context[key]['v'] = str(context[key]['v'])
    
    return context

def build_grammar(grammar):
    
    grammardict = {}
    
    for item in grammar:
        grammardict[item[0]] = {'n': item[1], 'l': item[2], 'u': 0, 't':0}
        
    return grammardict

def translate_tag(tag):
    
    tagdict = {"NNS": "Plural noun.", "NN": "Singular noun", "VB": "Present tense verb", "RB": "Adverb", "VBG": "Verb participle", "VBN": "Verb past tense", "VBD": "Verb past tense", "JJ": "adjective"}
    
    if tag in tagdict.keys():
        return tagdict[tag]
    else:
        return tag
    
def next_chunk(cur, user_id, chunk_id):
    
    COMMAND = """
    SELECT c.id, c.chunk, u.test_data, u.unknown_vocab FROM chunks C
    INNER JOIN user_nextchunk u
    ON c.id = u.chunk_id
    WHERE c.id = %s AND u.user_id=%s 
    """
    cur.execute(COMMAND, (chunk_id, user_id))
    choices = cur.fetchall()
    
    print(choices)
    
    out = {}
    
    out["displayType"] = "sentence"

    chunk = choices[0][1].split("#")
    grammar = get_grammar(choices[0][0], cur)
    vocab = get_vocab(choices[0][0], cur)
    unknown_vocab = choices[0][3].split(",")

    out["context"] = build_context(chunk, grammar, vocab, unknown_vocab)
    out["grammar"] = build_grammar(grammar)
    out["chunkid"] = choices[0][0]
    
    test_data = choices[0][2]
    
    for i in test_data.keys():
        
        # put together the test_data
        
        mode = test_data[i]['mode']
        interaction_data = get_vocab_interaction_data(cur, user_id, choices[0][0], test_data[i]['v'], mode)
        test_data[i]["tag"] = translate_tag(interaction_data["tag"])
        test_data[i]["mode"] = interaction_data["mode"]
        mode = test_data[i]["mode"]
        if mode == "1":
            for j, sen in enumerate(interaction_data["raw"]):
                test_data[i][str(j)] = {'s': sen[1], 'l': sen[2]}
        if mode == "2":
            for j, sen in enumerate(interaction_data["raw"]):
                test_data[i][str(j)] = {'s': sen[0]}
        if mode == "3":
            for j, sen in enumerate(interaction_data["raw"]):
                test_data[i][str(j)] = {'s': sen[0]}
        if mode == "4":
            test_data[i]["def"] = interaction_data["raw"]
                
        # give context access to test_data
        
        out["context"][test_data[i]["location"]]["i"] = i

    out["length"] = test_data["0"]["length"]

    out["currentInteraction"] = "0"
    
    # what is the key interaction
    
    for i in test_data.keys():
        if test_data[i]["key"] == "1":
            out["keyloc"] = i
            

    #print("interactiondict", interactiondict)
    out["interaction"] = test_data
    
    print("HEMMMMMLO")
    print(out["keyloc"])

    return out

def get_data(cur, req):
    
    stats = {}
    
    user_id = req["userId"]
    
    # how many reviews to do?
    
    COMMAND = """
    SELECT chunk_id FROM user_nextchunk
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))
    review_no = len(cur.fetchall())
    
    stats["rn"] = review_no
    
    # how many key words of each type?
    
    COMMAND = """
    SELECT streak FROM user_vocab
    WHERE user_id=%s AND active=%s
    """
    cur.execute(COMMAND, (user_id, "1"))
    active_words = cur.fetchall()
    
    streaks = {}
    
    for i in range(20):
        streaks[i] = 0
    
    for word in active_words:
        streaks[word[0]] += 1
        
    stats["streaks"] = streaks
    
    return stats
               

def record_result(userid, req, cur):
    
    # get data

    vocabid = req["interaction"][req["currentInteraction"]]["v"]
    streak = req["interaction"][req["currentInteraction"]]["streak"]
    chunkid = req["chunkid"]
    correct = req["answeredCorrect"]
    
    if correct:
        streak = int(streak) + 1
    
    # log the data
   
    COMMAND = """
    INSERT INTO user_vocab_log (user_id, vocab_id, chunk_id, result)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(COMMAND, (userid, vocabid, chunkid, correct))
    
    insert_command = """
    INSERT INTO user_chunk_log (user_id, chunk_id)
    VALUES (%s, %s)
    """
    cur.execute(insert_command, (userid, chunkid))
    
    # remove from user_nextchunk
    
    remove_chunk(userid, chunkid, cur)
    
    # pre-schedule in user_vocab
    
    COMMAND = """
    UPDATE user_vocab
    SET scheduled=0, next=(NOW() + INTERVAL '1 day'), streak=%s
    WHERE user_id=%s AND vocab_id=%s
    """
    cur.execute(COMMAND, (str(streak), userid, vocabid))

def remove_chunk(userid, chunkid, cur):
    
    remove_command = """
    DELETE FROM user_nextchunk
    WHERE user_id = %s AND chunk_id = %s
    """
    cur.execute(remove_command, (userid, chunkid))
    
def get_next(streak, correct):
    
    # will compute when next to test the vocab item, given whether correct and the current streak
    
    pass
