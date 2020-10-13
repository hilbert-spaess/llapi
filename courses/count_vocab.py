import os
from config import COURSE_DIRECTORY, COURSE_NO, API_DIRECTORY

from connect import connect

import csv

def count_vocab(cur):
    
    def get_course_source():
        
        with open(os.path.join(COURSE_DIRECTORY, "course_source.txt"), 'r') as CSFILE:
            
            lines = CSFILE.readlines()
            
        course_source = {x.split(":")[0].strip():[y.strip() for y in x.split(":")[1].split(",")] for x in lines}
    
        return course_source
    
    def get_vocab_ids(course):
        
        COMMAND = """SELECT vocab_id FROM course_vocab
        WHERE course_id=%s
        """
        cur.execute(COMMAND, (course,))
        
        return [x[0] for x in cur.fetchall()]
    
    def count(vocab_id, source_list):
        
        print("v", vocab_id)
        print("s", source_list)
        
        # count # of occurrences
        
        COMMAND = """SELECT cv.chunk_id from chunk_vocab cv
        INNER JOIN chunks c
        ON c.id = cv.chunk_id
        WHERE cv.vocab_id=%s AND c.source=%s
        """
        
        count = 0
        for source in source_list:
            print(source)
            cur.execute(COMMAND, (vocab_id, source))
            count += len(cur.fetchall())
        
        return count
    
    def update_count(vocab_id, course_id, count):
        
        COMMAND = """UPDATE course_vocab
        SET counts=%s
        WHERE vocab_id=%s AND course_id=%s
        """
        
        cur.execute(COMMAND, (count, vocab_id, course_id))
    
    course_source = get_course_source()
    
    for course, source_list in course_source.items():
        
        print(course)
        
        vocab_ids = get_vocab_ids(course)
        
        for vocab_id in vocab_ids:
            
            vcount = count(vocab_id, source_list)
            
            print(vcount)
            
            update_count(vocab_id, course, vcount)
    
    print(course_source)
    
conn, cur = connect()

count_vocab(cur)

cur.close()
conn.commit()
conn.close()