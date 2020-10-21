from connect import connect
import random
from test_data import get_test_data
import api_helpers
import os

from config import COURSE_DIRECTORY

def next_chunk(cur, user_id, vocab_id, chunk_id):
    
    COMMAND = """
    SELECT chunk FROM chunks
    WHERE id=%s
    """
    cur.execute(COMMAND, (chunk_id,))
    chunk = cur.fetchall()[0][0]
    
    out = {}
    
    out["displayType"] = "readforfun"
    
    chunk = chunk.split("#")
    grammar = api_helpers.get_grammar(chunk_id, cur)
    vocab = api_helpers.get_vocab(chunk_id, cur)
    
    out["context"] = api_helpers.build_context(chunk, grammar, vocab, [])
    out["grammar"] = api_helpers.build_grammar(grammar)
    out["chunkid"] = chunk_id
    
    test_data = get_test_data(cur, vocab_id, user_id, chunk_id)
    
    for i in test_data.keys():
        
        # put together the test_data
        
        mode = test_data[i]['mode']
        interaction_data = api_helpers.get_vocab_interaction_data(cur, user_id, chunk_id, test_data[i]['v'], mode)
        test_data[i]["tag"] = api_helpers.translate_tag(interaction_data["tag"])
        test_data[i]["mode"] = interaction_data["mode"]
        mode = test_data[i]["mode"]
        if mode == "1":
            for j, sen in enumerate(interaction_data["raw"]):
                test_data[i][str(j)] = {'s': sen[1], 'l': sen[2]}
        if mode == "2":
            for j, sen in enumerate(interaction_data["raw"]):
                test_data[i][str(j)] = {'s': sen[0]}
        if mode == "3":
            test_data[i]["samples"] = interaction_data["samples"]
        if mode in ["4", "6"]:
            test_data[i]["def"] = interaction_data["raw"]
            test_data[i]["samples"] = interaction_data["samples"]
                
        # give context access to test_data
        
        out["context"][test_data[i]["location"]]["i"] = i

    out["length"] = test_data["0"]["length"]

    out["currentInteraction"] = "0"
    
    for i in test_data.keys():
        if test_data[i]["key"] == "1":
            out["keyloc"] = i
    
    out["interaction"] = test_data
    
    out["first"] = "1"
    
    return out

def read_for_fun(cur, user_id):
    
    # get all chunks in a manner similar to api helpers
    
    CRS_COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    COMMAND = """SELECT uv.vocab_id FROM user_vocab uv
    INNER JOIN course_vocab cv
    ON cv.vocab_id = uv.vocab_id
    WHERE uv.user_id=%s AND cv.counts > 0
    """
    cur.execute(COMMAND, (user_id,))
    records = cur.fetchall()
    
    vocab_ids = random.sample(records, min(10, len(records)))
    
    allchunks = []
    
    with open(os.path.join(COURSE_DIRECTORY, 'course_source.txt'), 'r') as CSFILE:
        
         lines = CSFILE.readlines()
            
    course_source = {x.split(":")[0].strip():[y.strip() for y in x.split(":")[1].split(",")] for x in lines}
    
    source_list = course_source[str(course_id)]
    
    COMMAND = """SELECT chunk_id FROM chunk_vocab cv
    INNER JOIN chunks c
    ON c.id = cv.chunk_id
    WHERE cv.vocab_id=%s AND c.source=%s
    """
    
    ALL_PREV_COMMAND = """SELECT chunk_id FROM user_vocab_log
    WHERE user_id=%s
    """
    cur.execute(ALL_PREV_COMMAND, (user_id,))
    all_prev = [x[0] for x in cur.fetchall()]
    
    for vocab_id in vocab_ids:
        
        for source in source_list:
            
            cur.execute(COMMAND, (vocab_id, source))
            records = [x[0] for x in cur.fetchall()]
            
            new = list(set(records) - set(all_prev))
            
            if new:
                
                chunk_id = random.sample(new, 1)[0]
                
                allchunks.append(next_chunk(cur, user_id, vocab_id, chunk_id))
                
                break
            
            elif records:

                chunk_id = random.sample(records, 1)[0]

                allchunks.append(next_chunk(cur, user_id, vocab_id, chunk_id))
                
                break
        
    return allchunks