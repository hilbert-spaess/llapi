from connect import connect
import numpy as np
import random

conn, cur = connect()

def list_words():

    CMD = """SELECT v.word FROM vocab v 
    INNER JOIN course_vocab cv
    ON cv.vocab_id = v.id
    WHERE cv.course_id=6"""

    cur.execute(CMD)

    print(cur.fetchall())

def load_sentence():

    while True:

        word = input(">")

        CMD = """SELECT id, definition FROM vocab
        WHERE word=%s
        """
        cur.execute(CMD, (word,))
        vocab_id, definition  = cur.fetchall()[0]

        CMD = """SELECT * FROM chunk_vocab
        WHERE vocab_id=%s
        """
        cur.execute(CMD, (vocab_id,))
        r = cur.fetchall()

        no = input(str(len(r)) + " > ")

        if no == "q":

            break

        CMD = """SELECT chunk FROM chunks
        WHERE id=%s
        """
        chunk_id = r[int(no)][0]
        cur.execute(CMD, (chunk_id,))
        text = cur.fetchall()[0][0]

        idx = input("id: ")

        options = input("option: ")


        if options == "def":

            COMMAND = """
            SELECT v.pos, v.rank, v.word, cv.locations FROM vocab v
            INNER JOIN chunk_vocab cv
            ON cv.vocab_id = v.ID
            WHERE v.id = %s AND cv.chunk_id=%s
            """
            cur.execute(COMMAND, (vocab_id,chunk_id))
            out = cur.fetchall()[0]
            pos = out[0]; rank = out[1]; wd = out[2]; loc = out[3];

            print("{'id': " + idx + ", 'q': '" + " ".join(text.split("#")) + "', 'a': '" + text.split("#")[int(loc)] + "', 'def': '" + definition + "', 'i': {" + str(loc) + ": {'mode': 'definition'}}}")

        if options == "c":

            COMMAND = """
            SELECT v.pos, v.rank, v.word, cv.locations FROM vocab v
            INNER JOIN chunk_vocab cv
            ON cv.vocab_id = v.ID
            WHERE v.id = %s AND cv.chunk_id=%s
            """
            cur.execute(COMMAND, (vocab_id,chunk_id))
            out = cur.fetchall()[0]
            pos = out[0]; rank = out[1]; wd = out[2]; loc = out[3];

            COMMAND = """
            SELECT word, rank FROM vocab
            WHERE pos=%s AND LEFT(word,1)=%s AND id != %s AND rank > 0
            """
            cur.execute(COMMAND, (pos, wd[0], vocab_id))
            wdoptions = [list(a) for a in cur.fetchall() if a[1] > 0]
            print(wd)
            print(rank)
            if rank:
                wdoptions.sort(key=lambda x: np.abs(np.log(x[1]) - np.log(rank)) + np.abs(len(wd) - len(x[0])))
            else:
                wdoptions.sort(key=lambda x: np.abs(np.log(x[1]) - np.log(user_level)) + np.abs(len(wd) - len(x[0])))
            y = wdoptions[:min(len(wdoptions), 3)]
            y = [x[0] for x in y]
            y.append(wd)
            random.shuffle(y)
            

            print("{'id': " + idx + ", 'q': '" + " ".join(text.split("#")) + "', 'a': '" + text.split("#")[int(loc)] + "', 'def': '" + definition + "', 'i': {" + str(loc) + ": {'mode': 'choose', 'choices': " + str(y) + "}}}")

def load_device():

    wd = input("wd: ")
    definition = input("def: ")
    answer = input("ans: ")
    idx = input("id: ")
    loc = int(answer.split().index(wd))

    print("{'id': " + idx + ", 'q': '" + answer + "', 'a': '" + wd + "', 'def': '" + definition + "', 'i': {" + str(loc) + ": {'mode': 'devicefill'}}}")
    
    
list_words()

opt = input("Sentence or Device? ")
if opt == "s":
    load_sentence()
if opt == "d":
    load_device()
