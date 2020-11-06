from read_for_fun import next_chunk
from config import COURSE_DIRECTORY
import os
import random

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
    
    print("read list " + str(data["id"]))
    
    list_id = data["id"]
    
      
    CRS_COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(CRS_COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    with open(os.path.join(COURSE_DIRECTORY, 'course_source.txt'), 'r') as CSFILE:
        
         lines = CSFILE.readlines()
            
    course_source = {x.split(":")[0].strip():[y.strip() for y in x.split(":")[1].split(",")] for x in lines}
    
    source_list = course_source[str(course_id)]
    
    def get_all_chunks():
        
        all_chunks = []
        
        VOC_COMMAND = """SELECT vocab_id FROM list_vocab
        WHERE list_id=%s
        """
        cur.execute(VOC_COMMAND, (list_id,))
        vocab_ids = [x[0] for x in cur.fetchall()]
        
        CHUNK_COMMAND = """SELECT chunk_id FROM chunk_vocab cv
        INNER JOIN chunks c
        ON c.id=cv.chunk_id
        WHERE vocab_id=%s AND source=%s
        """
        
        for vocab_id in vocab_ids:
            
            cur.execute(CHUNK_COMMAND, (vocab_id, source_list[0]))
            r = cur.fetchall()
            
            if r:
                chunk_id = random.sample(r,1)[0]
                
        
            all_chunks.append(next_chunk(cur, user_id, vocab_id, chunk_id))
            
        return all_chunks
    
    allChunks = get_all_chunks()
    
    return {"allChunks": allChunks, "today_progress": {"yet": len(allChunks), "done": 0}}