# add vocab from a config file to a particular course

# robust checking that the vocab is in a state we want to see
# robust checking that not been added yet

import os
from config import COURSE_DIRECTORY, COURSE_NO, API_DIRECTORY

from connect import connect

import csv

VOCABFILE = os.path.join(COURSE_DIRECTORY, COURSE_NO, "vocab.txt")

# load vocab.
# vocabfile: word:definition:POS

def add_vocab(cur):

    def get_data(line):
        
        word = line[0].strip()
        if not word.isalpha():
            raise Exception(word + " is not a word")
            
        definition = line[1].strip()
        if not isinstance(definition, str):
            raise Exception(definition + " is not a string")
        
        pos = line[2].strip()
        if not pos in ["noun", "verb", "adjective", "adverb"]:
            raise Exception(pos + " is not a POS")
            
        return word, definition, pos
    
    def get_rank(word):
    
        with open("wordlist.csv", 'r') as rankfile:
            
            reader = csv.reader(rankfile, delimiter=":")
            
            for row in reader:
                
                if row[0] == word:
                    
                    return row[7].replace(",", "")
    
    def get_vocab_id(word, pos):
        
        COMMAND = """SELECT id FROM vocab
        WHERE word=%s AND pos=%s
        """
        
        cur.execute(COMMAND, (word, pos))
        r = cur.fetchall()
        
        if r:
            return r[0][0]
            
        if not r:
            
            rank = get_rank(word)
            print(word)
            print(rank)
            INS_COMMAND = """INSERT INTO vocab(word, pos, rank)
            VALUES(%s, %s, %s)
            RETURNING id"""
            
            cur.execute(INS_COMMAND, (word, pos, rank))
            l = cur.fetchall()[0][0]
            
            return l

    with open(VOCABFILE, 'r') as vocabfile:

        lines = vocabfile.readlines()
        lines = [x.split(":") for x in lines if len(x.split(":")) == 3]
        
    CHK_COMMAND = """SELECT * FROM course_vocab
    WHERE course_id=%s AND vocab_id=%s
    """
        
    COMMAND = """INSERT INTO course_vocab(course_id, vocab_id, definition, counts)
    VALUES(%s, %s, %s, 0)
    """

    for item in lines:

        word, definition, pos = get_data(item)
        
        vocab_id = get_vocab_id(word, pos)
        
        cur.execute(CHK_COMMAND, (COURSE_NO, vocab_id))
        
        if not cur.fetchall():
            
            print("INSERTING " + word)
            
            cur.execute(COMMAND, (COURSE_NO, vocab_id, definition))

conn, cur = connect()

add_vocab(cur)

cur.close()
conn.commit()
conn.close()

