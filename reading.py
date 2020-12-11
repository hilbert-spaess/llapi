from flask import Flask, request, make_response, jsonify, _request_ctx_stack, redirect
from flask_cors import CORS, cross_origin
import pickle
import csv
import numpy as np
import json
import pandas as pd
import psycopg2
from api_helpers import choose_next_chunk, next_chunk, get_all_chunks, load_tutorial, get_today_progress, get_level_progress
import on_review
from connect import connect
import threading
import reviews_over
import my_vocab, my_progress, new_user_choices, read_for_fun
from tests import log_in_test_alex, step_time_test_user_alex
import reading_analysis
import new_vocab_add
from config import API_AUDIENCE
import random
import json
import lists
import reading

import permissions

from six.moves.urllib.request import urlopen
from functools import wraps
from jose import jwt

import sys

def daily_reading(cur, conn, user_id, req):
    
    out = {}

   # analysischunks = [{"mechanism": "analysis", "text": "Jim bought a Capybara from the corner shop.", "question": "What did Jim buy from the corner shop?"}]

    #improvechunks = [{"mechanism": "improve", "text": "Jim bought a Capybara from the corner shop", "interaction": {"type": "choose", "question": "Improve this sentence using a word you've learned this session.", "options": ["acquired", "suffered", "imbued", "relented"]}}]

    out["allChunks"] = reading_analysis.getchunks()

    out["today_progress"] = {"yet": len(out["allChunks"]), "done": 0}

    res = make_response(jsonify(out))

    return res
    
    if req["answeredCorrect"] == "-1":
        print("HEMLO this is the first chumk")
        return get_first_chunk(cur, user_id)

    if req["first"] == 1:

        on_review.on_review(cur, user_id, req)

        cur.close()
        conn.commit()
        conn.close()

        conn, cur = connect()

    if req["done"]:

        x = threading.Thread(target=reviews_over.reviews_over, args=(user_id,))
        x.start()
        print("Starting the background scheduling thread.")

        out["status"] = "done"

        COMMAND = """SELECT word FROM vocab v
        INNER JOIN user_vocab_log l 
        ON v.id = l.vocab_id
        WHERE l.user_id=%s AND EXTRACT(DAY FROM l.time) = EXTRACT(DAY FROM NOW()) 
        """
        cur.execute(COMMAND, (user_id,))

        words = cur.fetchall()

        out["words"] = [x[0] for x in words]


    cur.close()
    conn.commit()
    conn.close()

    res = make_response(jsonify(out))

    return res

def get_first_chunk(cur, user_id):
    
    chunk_id = choose_next_chunk(cur, user_id)
    print("chunk id: ", chunk_id)
    
    out = {}
    
    if chunk_id:
        allchunks = get_all_chunks(cur, user_id)
        allchunks = get_firsts(cur, user_id, allchunks)
        if len(allchunks) < 20:
            allchunks = supplement(cur, user_id, allchunks)
            
        out["allChunks"] = allchunks
    else:
        out["allChunks"] = [0]
        out["status"] = "done"
        
    out["today_progress"] = {"yet": len(out["allChunks"]), "done": 0}
    
    out["permissions"] = permissions.get_permissions(cur, user_id)
    
    print(out["today_progress"])
    
    res = make_response(jsonify(out))
    
    return res

def get_firsts(cur, user_id, allchunks):
    
    # look for firsts. if there are firsts, get the corresponding fluff.
    
    fluffchunks = []
    
    for chunk in allchunks:
        
        if chunk["interaction"][chunk["keyloc"]]["streak"] == 0:
            
            fluffchunks.append(read_for_fun.next_chunk(cur, user_id, chunk["interaction"][chunk["keyloc"]]["v"] , chunk["chunkid"], options={"interaction_mode": "6"}))
            fluffchunks[-1]["first"] = 0

    for chunk in allchunks:
            
                fluffchunks.append(chunk)
    
    return fluffchunks

def supplement(cur, user_id, allchunks):

    # for now: completely randomly decide on supplementing up to 20

    r = 20 - len(allchunks)

    newchunks = read_for_fun.read_for_fun(cur, user_id, options={"new_no": r, "interaction_mode": "6"})

    for chunk in newchunks:
        allchunks.insert(random.randrange(len(allchunks)+1), chunk)

    return allchunks

    

        
