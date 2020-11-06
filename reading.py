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
    
    if req["answeredCorrect"] == "-1":
        print("HEMLO this is the first chumk")
        return get_first_chunk(cur, user_id)

    if req["first"] == 1:
        on_review.set_first(cur, user_id, req)

        cur.close()
        conn.commit()
        conn.close()

        conn, cur = connect()

    if req["first"] == 0 or (req["interaction"][req["keyloc"]]["streak"] > 0 and int(req["answers"][int(req["keyloc"])]) == 1):
        print("REVIEW")
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
        allchunks = []
        newallchunks = get_all_chunks(cur, user_id)
        print("newallchunks", newallchunks)
        for chunk in newallchunks:
            print(chunk)
            if chunk["first"]:
                allchunks.append(chunk)
        random.shuffle(allchunks)
        for chunk in newallchunks:
            if not chunk["first"]:
                allchunks.append(chunk)
        out["allChunks"] = allchunks
        print(out["allChunks"])
    else:
        out["allChunks"] = [0]
        out["status"] = "done"
        print("NOTHING LEFT")
        
    yet, done = get_today_progress(cur, user_id)
    out["today_progress"] = {"yet": yet, "done": done}
    
    out["permissions"] = permissions.get_permissions(cur, user_id)
    
    print(out["today_progress"])
    
    res = make_response(jsonify(out))
    
    return res
        