from read_for_fun import next_chunk
from config import COURSE_DIRECTORY
import os
import random
import numpy as np

def load_lists(cur, user_id):
    
    def get_user_lists():
        
        return []
    
    def get_course_lists():
        
        course_lists = []
        
        CRS_COMMAND = """SELECT course_id FROM users
        WHERE id=%s
        """
        cur.execute(CRS_COMMAND, (user_id,))
        course_id = cur.fetchall()[0][0]
        
        VOC_COM = """SELECT v.id, v.word FROM course_vocab cv
        INNER JOIN vocab v
        ON v.id=cv.vocab_id
        WHERE cv.course_id=%s AND cv.counts>5"""
        cur.execute(VOC_COM, (course_id,))
        course_lists = [{"words": cur.fetchall(), "name": "Smart session", "id": 0}]
        
        print(course_id)
        
        LST_COMMAND = """SELECT lc.list_id, l.name FROM list_course lc
        INNER JOIN lists l
        ON l.id= lc.list_id
        WHERE course_id=%s
        """
        cur.execute(LST_COMMAND, (course_id,))
        list_ids = cur.fetchall()
        
        VOC_COMMAND = """SELECT v.id, v.word FROM list_vocab lv
        INNER JOIN vocab v
        ON v.id=lv.vocab_id
        WHERE list_id=%s
        """
        
        for item in list_ids:
            cur.execute(VOC_COMMAND, (item[0],))
            course_lists.append({"words": cur.fetchall(), "name": item[1], "id": item[0]})
            
        return course_lists
    
    out = {}
    out["userlists"] = get_user_lists()
    out["courselists"] = get_course_lists()
    
    print(out["courselists"])
    
    return out

def read_list(cur, user_id, data):
    
    print(data)
    
    print("read list " + str(data["id"]))
    
    list_id = data["id"]
    
    if list_id == 0:
        
        return quicksession(cur, user_id, data)
    
    LISTNAME = """SELECT name FROM lists
    WHERE id=%s
    """
    cur.execute(LISTNAME, (list_id,))
    list_name= cur.fetchall()[0][0]
      
    CRS_COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    with open(os.path.join(COURSE_DIRECTORY, 'course_source.txt'), 'r') as CSFILE:
        
         lines = CSFILE.readlines()
            
    course_source = {x.split(":")[0].strip():[y.strip() for y in x.split(":")[1].split(",")] for x in lines}
    
    source_list = course_source[str(course_id)]
    
    def get_interaction_mode(vocab_id, k):
        
        if k == 0:
            
            return "6"
        
        else:
            
            return "4"
        
    all_chunks = []
    

    VOC_COMMAND = """SELECT lv.vocab_id FROM list_vocab lv
    INNER JOIN course_vocab cv
    ON cv.vocab_id = lv.vocab_id
    WHERE list_id=%s AND cv.counts>5
    """
    cur.execute(VOC_COMMAND, (list_id,))
    vocab_ids = [x[0] for x in cur.fetchall()]
    
    vocab_ids = random.sample(vocab_ids, min(13, len(vocab_ids)))

    CHUNK_COMMAND = """SELECT chunk_id FROM chunk_vocab cv
    INNER JOIN chunks c
    ON c.id=cv.chunk_id
    WHERE vocab_id=%s AND source=%s
    """
    random.shuffle(vocab_ids)
    
    for vocab_id in vocab_ids:

        cur.execute(CHUNK_COMMAND, (vocab_id, source_list[0]))
        r = cur.fetchall()

        if r:
            chunk_ids = random.sample(r,5)


        all_chunks.append([next_chunk(cur, user_id, vocab_id, chunk_id, options={"interaction_mode": get_interaction_mode(vocab_id, k)}) for (k, chunk_id) in enumerate(chunk_ids)])
        
    WD_COMMAND = """SELECT word FROM vocab
    WHERE id=%s
    """
    new_all_chunks = [[], [], [], [], []]
    words = []
    
    idx_dict = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3, 10: 3, 11: 3, 12: 3}
    for idx, v in enumerate(vocab_ids):
        
        cur.execute(WD_COMMAND, (v,))
        words.append(cur.fetchall()[0][0])
        
        for j in range(5):
            if j >= idx_dict[idx]:
                new_all_chunks[j].append(all_chunks[idx][j-idx_dict[idx]])
    
    for j in range(5):
        newj = new_all_chunks[j][:]
        random.shuffle(newj)
        new_all_chunks[j] = newj
    
    return {"allChunks": new_all_chunks, "words": words, "name": list_name}

def quicksession(cur, user_id, data):
    
    CRS_COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    with open(os.path.join(COURSE_DIRECTORY, 'course_source.txt'), 'r') as CSFILE:
        
         lines = CSFILE.readlines()
            
    course_source = {x.split(":")[0].strip():[y.strip() for y in x.split(":")[1].split(",")] for x in lines}
    
    source_list = course_source[str(course_id)]
    source_id = source_list[0]
    
    qno = data["qno"]
    
    def get_interaction_mode(vocab_id, k):
        
        if k == 0:
            
            return "6"
        
        else:
            
            return "4"
    
    
    # get stuff seen today
    
    all_chunks = []
    
    VOC_COMMAND = """SELECT vocab_id FROM course_vocab
    WHERE course_id=%s AND counts>5"""
    
    cur.execute(VOC_COMMAND, (course_id,))
    vocab_ids = [x[0] for x in cur.fetchall()]
    
    vocab_ids = random.sample(vocab_ids, min(13, len(vocab_ids)))
    
    CHUNK_COMMAND = """SELECT chunk_id FROM chunk_vocab cv
    INNER JOIN chunks c
    ON c.id=cv.chunk_id
    WHERE vocab_id=%s AND source=%s
    """
    
    random.shuffle(vocab_ids)
    
    for vocab_id in vocab_ids:

        cur.execute(CHUNK_COMMAND, (vocab_id, source_list[0]))
        r = cur.fetchall()

        if r:
            chunk_ids = random.sample(r,5)


        all_chunks.append([next_chunk(cur, user_id, vocab_id, chunk_id, options={"interaction_mode": get_interaction_mode(vocab_id, k)}) for (k, chunk_id) in enumerate(chunk_ids)])
        
    WD_COMMAND = """SELECT word FROM vocab
    WHERE id=%s
    """
    new_all_chunks = [[], [], [], [], []]
    words = []
    
    idx_dict = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3, 10: 3, 11: 3, 12: 3}
    for idx, v in enumerate(vocab_ids):
        
        cur.execute(WD_COMMAND, (v,))
        words.append(cur.fetchall()[0][0])
        
        for j in range(5):
            if j >= idx_dict[idx]:
                new_all_chunks[j].append(all_chunks[idx][j-idx_dict[idx]])
    
    for j in range(5):
        newj = new_all_chunks[j][:]
        random.shuffle(newj)
        new_all_chunks[j] = newj
    
    return {"allChunks": new_all_chunks, "words": words, "name": "Smart session"}
