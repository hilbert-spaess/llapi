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

def get_vocab_interaction_data(chunkid, cur, vocab, interaction):
    interaction_data = []
    for idx, v in enumerate(vocab):
        
        COMMAND = """
        SELECT v.pos, v.zipf, v.word, uv.streak FROM vocab v
        INNER JOIN user_vocab uv
        ON uv.vocab_id = v.id
        WHERE v.id = %s
        """
        cur.execute(COMMAND, (v,))
        
        # WHILE NOT ALL HAVE STREAKS.
        out = cur.fetchall()[0]
        pos = out[0]; zipf = out[1]; wd = out[2];
        if len(out) > 2: 
            streak = out[3]
        else:
            streak = 0
         
        outdata = {}
        outdata["pos"] = pos
        outdata["zipf"] = zipf
        outdata["wd"] = wd
        outdata["streak"] = streak
        
        if interaction[idx]=="1":

            COMMAND = """
            SELECT c.id, c.chunk, cv.locations FROM chunks c
            INNER JOIN chunk_vocab cv
            ON c.id = cv.chunk_id
            WHERE cv.vocab_id=%s AND c.id !=%s AND c.sentence=1
            """
            cur.execute(COMMAND, (v,chunkid))
            options = cur.fetchall()
            outdata["raw"] = random.sample(options, min(2, len(options)))
        
        if interaction[idx]=="2":
            
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
            
        if interaction[idx]=="3":
            
            COMMAND = """
            SELECT word, zipf FROM vocab
            WHERE pos=%s AND ABS(id - %s) < 200 AND id != %s
            """
            cur.execute(COMMAND, (pos, v, v))
            options = cur.fetchall()
            options.sort(key=lambdaa x: np.abs(x[1] - zipf))
            y = options[:min(len(options), 3):]
            y.append((wd, zipf))
            random.shuffle(y)
            outdata["raw"] = y
            
        interaction_data.append(outdata)
                        
    return interaction_data

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
    
def next_chunk(cur, user_id, chunkid):
    
    COMMAND = """
    SELECT c.id, c.chunk, u.test_data, u.unknown_vocab FROM chunks C
    INNER JOIN user_nextchunk u
    ON c.id = u.chunk_id
    WHERE c.id = %s AND u.user_id=%s 
    """
    cur.execute(COMMAND, (chunk_id, user_id))
    choices = cur.fetchall()
    
    out = {}
    
    out["displayType"] = "sentence"

    chunk = choices[0][1].split("#")
    grammar = get_grammar(choices[0][0], cur)
    vocab = get_vocab(choices[0][0], cur)
    unknown_vocab = choices[0][3].split(",")

    out["context"] = build_context(chunk, grammar, vocab, vocab_to_test)
    out["grammar"] = build_grammar(grammar)
    out["chunkid"] = choices[0][0]

    #print(choices)
    interactions = choices[0][3].split(",")[next_interaction:]

    # organise the vocab and interactions

    get_sentences_command = """SELECT first_sentence, locations FROM chunk_vocab WHERE chunk_id=%s AND vocab_id=%s"""
    v_sentences = []
    for v in vocab_to_test:
        cur.execute(get_sentences_command, (choices[0][0], v))
        records = cur.fetchall()
        sentence = records[0][0].split(",")[0]
        location = records[0][1].split(",")[0]
        v_sentences.append((v, sentence, location))
    v_sentences = sorted(v_sentences, key=lambda x: x[1])

    #print(v_sentences)
    #print(sentencebreaks)

    vocab_to_test = [x[0] for x in v_sentences]
    lengths = [sentencebreaks[int(y[1])] for y in v_sentences]
    locations = [x[2] for x in v_sentences]

    out["length"] = str(lengths[0])

    # get interaction data

    interactiondict = {}
    vocab_interaction_data = get_vocab_interaction_data(choices[0][0], cur, vocab_to_test, interactions)

    for i, word in enumerate(vocab_to_test):
        interactiondict[str(i)] = {}
        interactiondict[str(i)]["mode"] = str(interactions[i])
        interactiondict[str(i)]["location"] = str(locations[i])
        interactiondict[str(i)]["v"] = word
        interactiondict[str(i)]["length"] = str(lengths[i])
        interactiondict[str(i)]["streak"] = vocab_interaction_data[i]["streak"]
        if interactiondict[str(i)]["mode"] == "1":
            for j, sen in enumerate(vocab_interaction_data[i]["raw"]):
                interactiondict[str(i)][str(j)] = {'s': sen[1], 'l': sen[2]}
        if interactiondict[str(i)]["mode"] == "2":
            for j, sen in enumerate(vocab_interaction_data[i]["raw"]):
                interactiondict[str(i)][str(j)] = {'s': sen[0]}
        if interactiondict[str(i)]["mode"] == "3":
            for j, sen in enumerate(vocab_interaction_data[i]["raw"]):
                interactiondict[str(i)][str(j)] = {'s': sen[0]}



    out["currentInteraction"] = "0"

    #print("interactiondict", interactiondict)
    out["interaction"] = interactiondict

        
    return out

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
