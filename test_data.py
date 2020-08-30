import psycopg2
import csv
import pickle
import random

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
        cur.execute(COMMAND)

        return cur.fetchall()[0][0]
    
    def get_test_vocab():
    
        vocab = []

        # get test vocab

        sentence_command = """
        SELECT first_sentence FROM chunk_vocab
        WHERE chunk_id=%s AND vocab_id=%s
        """
        cur.execute(sentence_command, (next_chunk, vocab_id))
        sentence = cur.fetchall()[0][0]

        vocab.append((vocab_id, sentence, 1))

        # get aux vocab

        sentence_breaks = get_sentence_breaks()

        sentence_no = len(sentence_breaks.split(","))

        # choose a vocab item from each sentence

        for sen in range(sentence_no):

            if sen != sentence:

                # some random element so not flooded with chunks, probably dependent on sentence_no

                new_vocab = choose_new(sen)

                if new_vocab:

                    vocab.append((potential[0], sen, 0))

        return sorted(vocab, key = lambda x: x[1])
    
    def get_sentence_breaks():
    
        sentence_breaks_command = """
        SELECT sentence_breaks FROM chunks
        WHERE chunk_id=%s
        """
        cur.execute(sentence_breaks_command, (next_chunk,))
        return cur.fetchall()[0][0]
    
    def get_interaction_mode(item):
    
        # will need code here once I figure out what good interactions look like

        return "3"
    
    def get_location(v_id):
    
        COMMAND = """
        SELECT locations FROM chunk_vocab
        WHERE chunk_id = %s AND vocab_id=%s
        """
        cur.execute(COMMAND, (next_chunk, v_id))
        location = cur.fetchal()[0][0].split(",")[0]
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
        WHERE c.chunk_id = %s AND c.first_sentence = %s
        """
        cur.execute(COMMAND, (next_chunk, sen))
        potential = cur.fetchall()

        if potential:
            potential = sorted(potential, key = lambda x: abs(x[1] - user_level))[0]

        return potential
    
    test_data = {}
    
    # a JSON to into the user_nextchunk database for ease of loading.
    
    test_vocab = get_test_vocab()
    
    for i, item in enumerate(test_vocab):
        
        test_data[str(i)] = {}
        test_data[str(i)]["v"] = item[0]
        test_data[str(i)]["key"] = str(item[2])
        
        if item[2]:
            key_location = str(i)
    
    # find locations, lengths for all vocab items
    
    sentence_breaks = get_sentence_breaks()
    
    for i, item in enumerate(test_vocab):
        
        test_data[str(i)]["location"] = get_location(item[0])
        test_data[str(i)]["length"] = sentence_breaks[item[1]]
    
    # get streak
    
    test_data[key_location]["streak"] = get_streak()

    # choose interaction methodology for each (based on streak data)
    
    for i, item in enumerate(test_vocab):
        
        test_data[str(i)]["mode"] = get_interaction_mode(item)
    
    return test_data