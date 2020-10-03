import psycopg2
import csv
import pickle
import random
from pyinflect import InflectionEngine
import numpy as np


def get_vocab_data(cur, vocab_id, user_id, next_chunk, v_context):
    
    # locations
    
    COMMAND = """
    SELECT c.locations FROM vocab v
    INNER JOIN chunk_vocab c
    ON c.vocab_id = v.id
    WHERE c.chunk_id = %s AND c.first_sentence = %s
    """ 
    
    # choose interaction
    
    # for a particular vocab id, find location, interaction mechanism, length after the interaction


def get_test_data(cur, vocab_id, user_id, next_chunk):
    
    def get_streak():
    
        COMMAND = """
        SELECT streak FROM user_vocab
        WHERE user_id=%s AND vocab_id=%s
        """
        cur.execute(COMMAND, (user_id, vocab_id))
        r = cur.fetchall()
        if r:
            return r[0][0]
        else:
            return "0"
    
    def get_test_vocab():
    
        vocab = []
        
        # get test vocab

        sentence_command = """
        SELECT first_sentence FROM chunk_vocab
        WHERE chunk_id=%s AND vocab_id=%s
        """
        cur.execute(sentence_command, (next_chunk, vocab_id))
        sentence = cur.fetchall()[0][0]

        vocab.append((vocab_id, int(sentence), 1))

        # get aux vocab

        sentence_breaks = get_sentence_breaks()

        sentence_no = len(sentence_breaks.split(","))

        # choose a vocab item from each sentence

        for sen in range(sentence_no):

            if sen != int(sentence):

                # some random element so not flooded with chunks, probably dependent on sentence_no

                new_vocab = choose_new(sen)

                if new_vocab:

                    vocab.append((new_vocab[0], sen, 0))

        return sorted(vocab, key = lambda x: x[1])
    
    def get_sentence_breaks():
    
        sentence_breaks_command = """
        SELECT sentence_breaks FROM chunks
        WHERE id=%s
        """
        cur.execute(sentence_breaks_command, (next_chunk,))
        return cur.fetchall()[0][0]
    
    def get_sense():
        
        sense_command = """
        SELECT sense FROM chunk_vocab
        WHERE chunk_id=%s AND vocab_id=%s
        """
        cur.execute(sense_command, (next_chunk, vocab_id))
        r = cur.fetchall()
        if r:
            return r[0][0]
        else:
            return None
    
    def get_interaction_mode(item):
    
        # will need code here once I figure out what good interactions look like
        if item[2]:
            if not get_streak():
                return "6"
            else:
                return "4"
        else:
            return "3"
    
    def get_location(v_id):
    
        COMMAND = """
        SELECT locations FROM chunk_vocab
        WHERE chunk_id = %s AND vocab_id=%s
        """
        cur.execute(COMMAND, (next_chunk, v_id))
        location = cur.fetchall()[0][0].split(",")[0]
        return location
    
    def choose_new(sen):
    
        COMMAND = """
        SELECT vlevel FROM users
        WHERE id=%s
        """
        cur.execute(COMMAND,(user_id,))
        user_level = cur.fetchall()[0][0]

        COMMAND = """
        SELECT v.id, v.zipf FROM vocab v
        INNER JOIN chunk_vocab c
        ON c.vocab_id = v.id
        WHERE c.chunk_id = %s AND c.first_sentence = %s AND v.zipf > 0
        """
        cur.execute(COMMAND, (next_chunk, str(sen)))
        potential = cur.fetchall()

        if potential:
            potential = sorted(potential, key = lambda x: abs(x[1] - user_level))[0]

        return potential
    
    def get_lower_upper(sentence_breaks, key_location):
        
        sb = [-1] + [int(k) for k in sentence_breaks]
        lower_cap = sb[int(key_location)] + 1
        upper_cap = sb[int(key_location)+1]+1
        
        return [lower_cap, upper_cap]
    
    test_data = {}
    
    # a JSON to into the user_nextchunk database for ease of loading.
    
    test_vocab = get_test_vocab()
    print(test_vocab)
    
    for i, item in enumerate(test_vocab):
        
        test_data[str(i)] = {}
        test_data[str(i)]["v"] = item[0]
        test_data[str(i)]["key"] = str(item[2])
        
        if item[2]:
            key_location = str(i)
    
    # find locations, lengths for all vocab items
    
    sentence_breaks = get_sentence_breaks().split(",")
    
    for i, item in enumerate(test_vocab):
        
        test_data[str(i)]["location"] = get_location(item[0])
        test_data[str(i)]["length"] = str(int(sentence_breaks[item[1]]) + 1)
        
    # get streak
    
    test_data[key_location]["streak"] = get_streak()
    test_data[key_location]["sense"] = get_sense()
    test_data[key_location]["lower_upper"] = get_lower_upper(sentence_breaks, key_location)
    
    print("lower-upper", test_data[key_location]["lower_upper"])

    # choose interaction methodology for each (based on streak data)
    
    for i, item in enumerate(test_vocab):
        
        test_data[str(i)]["mode"] = get_interaction_mode(item)
        
        if get_interaction_mode(item) in ["4", "6"]:
            
            COMMAND = """
            SELECT v.pos, v.zipf, v.word, cv.tags FROM vocab v
            INNER JOIN chunk_vocab cv
            ON cv.vocab_id = v.id
            WHERE v.id = %s AND chunk_id=%s
            """
            cur.execute(COMMAND, (item[0], next_chunk))
            out = cur.fetchall()[0]
            pos = out[0]; zipf = out[1]; wd = out[2]; tag = out[3].split(",")[0]
            
            alternatives = []
            
            altdict = InflectionEngine().getAllInflections(wd)
            
            for t in altdict.values():
                for z in t:
                    alternatives.append(z)
           
            
            test_data[str(i)]["alternatives"] = alternatives
   
        if get_interaction_mode(item) in ["3", "6"]:
            
            COMMAND = """
            SELECT v.pos, v.zipf, v.word, cv.tags FROM vocab v
            INNER JOIN chunk_vocab cv
            ON cv.vocab_id = v.id
            WHERE v.id = %s AND chunk_id=%s
            """
            cur.execute(COMMAND, (item[0], next_chunk))
            out = cur.fetchall()[0]
            pos = out[0]; zipf = out[1]; wd = out[2]; tag = out[3].split(",")[0]
            
            first_letter = wd[0].lower()
            
            COMMAND = """
            SELECT word, zipf FROM vocab
            WHERE pos=%s AND LEFT(word,1)=%s AND id != %s
            """
            cur.execute(COMMAND, (pos, first_letter, item[0]))
            options = [list(a) for a in cur.fetchall() if a[1] > 0]
            options.sort(key=lambda x: np.abs(x[1] - zipf) + np.abs(len(wd) - len(x[0])))
            y = options[:min(len(options), 3):]
            
            print("YMCA",  y)
            y.append([wd, zipf])

            for idc in range(len(y)):
                print(y[idc][0])
                print(tag)
                a = InflectionEngine().getInflection(y[idc][0].split(" ")[0], tag)
                if a:
                    y[idc][0] = a[0]
                
            random.shuffle(y)
            
            print(wd)
            print("YMCA", y)
            
            for j, sen in enumerate(y):
                
                print(test_data)
            
                test_data[str(i)][str(j)] = {'s': sen[0]}
                
                print(test_data["0"])


    
    return test_data