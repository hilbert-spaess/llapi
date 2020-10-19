from flask import Flask, request, make_response, jsonify, _request_ctx_stack
from flask_cors import CORS, cross_origin
import pickle
import csv
import numpy as np
import json
import pandas as pd
import psycopg2
from api_helpers import choose_next_chunk, next_chunk, get_all_chunks, load_tutorial, get_today_progress, get_level_progress
from lesson_helpers import get_all_lessons
import on_review
from connect import connect
import threading
import reviews_over
import my_vocab, my_progress, new_user_choices
import new_vocab_add
from config import API_AUDIENCE
import random

from six.moves.urllib.request import urlopen
from functools import wraps
from jose import jwt

import sys
sys.path.append('/var/www/html/llapi')
sys.path.append('/home/ubuntu/.local/lib/python3.5/site-packages')

AUTH0_DOMAIN = "accounts.ricecake.ai"
ALGORITHMS = ["RS256"]

app = Flask(__name__)
CORS(app)

class AuthError(Exception):
    
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        print("HI")
        print(list(request.form.keys()))
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read().decode('utf-8'))
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

@app.route('/api/firstchunk', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_first_chunk():
    
    print("HEMLO")
    print(_request_ctx_stack.top.current_user['sub'])
    
    print(request)
    req = request.get_json()
    conn, cur = connect()
    out = {}
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    user_id = cur.fetchall()[0][0]
    
    chunk_id = choose_next_chunk(cur, user_id)
    print("chunk id: ", chunk_id)
    
    if chunk_id:
        out = next_chunk(cur, user_id, chunk_id)
    else:
        out["displayType"] = "done"
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()
    
    return res

def get_first_chunk1(cur, user_id, req):
    
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
        out["displayType"] = "done"
        print("NOTHING LEFT")
        
    yet, done = get_today_progress(cur, user_id)
    out["today_progress"] = {"yet": yet, "done": done}  
    
    res = make_response(jsonify(out))
    
    return res
        

@app.route('/api/getchunk', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_text_chunk():
    
    req = request.get_json()
    conn, cur = connect()
    out = {}
    
    print(req)
    
    COMMAND = """SELECT id, tutorial FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    # possibly a new user
    
    if not a:
        out["displayType"] = "newUser"
        
        res = make_response(jsonify(out))

        cur.close()
        conn.commit()
        conn.close()

        return res
    
    user_id = a[0][0]
    
    # possibly just a log
           
    if req == {}:
        return make_response(jsonify({}))
    
    if req["answeredCorrect"] == "-1":
        print("HEMLO this is the first chumk")
        return get_first_chunk1(cur, user_id, req)
    
    else:
        
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
            
            out["displayType"] = "done"
            
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
    
@app.route('/api/getlessons', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_lessons():
    
    req = request.get_json()
    conn, cur = connect()
    out = {}
    
    COMMAND = """SELECT id, tutorial FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    # possibly a new user
    
    if not a:
        out["displayType"] = "newUser"
        
        res = make_response(jsonify(out))

        cur.close()
        conn.commit()
        conn.close()

        return res
    
    user_id = a[0][0]
    
    COMMAND = """SELECT 1 FROM user_vocab uv 
    INNER JOIN users u
    ON u.id = uv.user_id
    WHERE u.id=%s AND uv.level <= u.level AND active=0"""
    
    cur.execute(COMMAND, (user_id,))
    
    if cur.fetchall():
        out["displayType"] = "lessons"
        all_lessons = get_all_lessons(cur, user_id)
        out["all_lessons"] = all_lessons
    
    return out
    
    
    
@app.route('/api/newuser', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def new_user():
    
    req = request.get_json()
    conn, cur = connect()
    out = {}
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    print(req)
    
    if req == {}:
        
        print("BEMLO")
        
        
        
        COMMAND = """SELECT * FROM courses"""
        cur.execute(COMMAND)
        records = cur.fetchall()
        
        options = {}
        for instance in records:
            options[instance[0]] = {"name": instance[1]}
            
        out["choices"] = options
        
        print(out)
        
        res = make_response(jsonify(out))
        
        return res
    
    a = cur.fetchall()
    
    if not a:
        
        
        course_id = req["course"]
        print("course choice", course_id)
        
        if course_id in [1, "1"]:
            vlevel = '4'
            tutorial=0
            message = "This is the Core TOEFL course. If you want to change the difficulty, or if you have any questions, get in touch."
        if course_id in [2, "2"]:
            vlevel = '1.5'
            tutorial=0
            message = """This is the Core GRE course. If you want to change the difficulty, if you have specific words/topics you want to see, or if you have any questions, get in touch."""
        
        
        COMMAND = """INSERT INTO users(name, vlevel, course_id, email, tutorial, message, level)
        VALUES(%s, %s, %s, %s, %s, %s, 1)
        RETURNING id"""
        cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'], vlevel, course_id, req["email"], tutorial, message))
        user_id = cur.fetchall()[0][0]
        print("id", user_id)
        
        cur.close()
        conn.commit()
        conn.close()
        
        new_vocab_add.new_course(user_id, course_id)
        
        res = make_response(jsonify(out))

        return res

        
        
        
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()
    
    return res

@app.route('/api/loadvocab', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def load_vocab():

    conn, cur = connect()
    req = request.get_json()
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    if not a:
        out = {}
        out["displayType"] = "newUser"
        
        res = make_response(jsonify(out))
    
        cur.close()
        conn.commit()
        conn.close()

        return res  
    
    user_id = a[0][0]
    
    out = my_vocab.load_vocab(cur, user_id, req)
    
    print(out)
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()

    return res

@app.route('/api/newvocabword', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def new_vocab_word():
    
    req = request.get_json()
    conn, cur = connect()
    
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    user_id = cur.fetchall()[0][0]
    
    if req["type"] == "submit":
        
        print(req["payload"])
        print("SUBMITTED")
        
        out = my_vocab.new_word(cur, req["payload"], user_id)
        
    elif req["type"] == "confirm":
        
        my_vocab.confirm_new_word(cur, req["payload"], user_id)
        
        out = {"state": "null"}
        
    else:
        
        out= {"state": "null"}
        
    cur.close()
    conn.commit()
    conn.close()
    
    res = make_response(jsonify(out))
    
    return res
    

@app.route('/api/getdata', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_data():

    conn, cur = connect()
    req = request.get_json()
    
    user_id = req["userId"]
    
    out = api_helpers.get_data(cur, req)
    
    print(out)
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()

    return res

@app.route('/api/todayprogress', methods=['POST', 'GET'])
@cross_origin(origin='*')
@requires_auth
def get_today_review_progress():
    
    conn, cur = connect()
    req = request.get_json()
    out = {}
    
    COMMAND = """SELECT id, level FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    a = cur.fetchall()
    
    user_id = a[0][0]
    level = a[0][1]
    
    COMMAND = """SELECT c.chunk, uv.vocab_id, c.id FROM chunks c
    INNER JOIN user_vocab_log uv
    ON uv.chunk_id = c.id
    WHERE user_id=%s AND DATE(uv.time) = DATE(NOW())
    """
    cur.execute(COMMAND, (user_id,))
    
    records = cur.fetchall()
    
    todaychunks = []
    
    for instance in records:
        todaychunks.append([instance[0], instance[1], instance[2]])
        
    LOC_COMMAND = """SELECT locations FROM chunk_vocab
    WHERE chunk_id=%s AND vocab_id=%s
    """
    
    WD_COMMAND = """SELECT word FROM vocab
    WHERE id=%s
    """
    
    for i, instance in enumerate(todaychunks):
        cur.execute(LOC_COMMAND, (instance[2], instance[1]))
        location = cur.fetchall()[0][0].split(",")[0]
        
        todaychunks[i].append(location)
        
        cur.execute(WD_COMMAND, (instance[1],))
        wd = cur.fetchall()[0][0]
        
        todaychunks[i].append(wd)
    
    out["todaychunks"] = todaychunks
    
    COMMAND = """SELECT v.word, uv.streak FROM user_vocab uv
    INNER JOIN vocab v
    ON uv.vocab_id = v.id
    WHERE uv.user_id=%s AND uv.vocab_id=%s
    """
    words = []
    for i, instance in enumerate(todaychunks):
        
        cur.execute(COMMAND, (user_id, instance[1]))
        x = cur.fetchall()[0]
        words.append({"w": x[0], "s": x[1]})

    out["words"] = words
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()
    
    return res
    
    
@app.route('/api/todaywords', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_today_words():
    
    conn, cur = connect()
    req = request.get_json()
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    a = cur.fetchall()
    
    user_id = a[0][0]
    
    COMMAND = """SELECT word FROM vocab v
    INNER JOIN user_vocab_log l 
    ON v.id = l.vocab_id
    WHERE l.user_id=%s AND EXTRACT(DAY FROM l.time) = EXTRACT(DAY FROM NOW()) 
    """
    cur.execute(COMMAND, (user_id,))
    
    words = cur.fetchall()
    
    out = {}
    out["words"] = list(set([x[0] for x in words]))
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()
    
    return res


@app.route('/api/coursevocab', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def course_vocab():
    
    out = {}
    conn, cur = connect()
    req = request.get_json()
    
    COMMAND = """INSERT INTO users(name, vlevel, course_id, email, tutorial, message, level)
    VALUES(%s, %s, %s, %s, %s, %s, 1)
    RETURNING id"""
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'], 0, req["course"], req["email"], 0, ""))
    user_id = cur.fetchall()[0][0]
    
    out["course_vocab"] = new_user_choices.course_vocab_samples(cur, user_id)
    
    print(out["course_vocab"])
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()
    
    return res

@app.route('/api/coursevocabsubmit', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def course_vocab_submit():
    
    out = {}
    conn, cur = connect()
    req = request.get_json()
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    a = cur.fetchall()
    
    user_id = a[0][0]
    
    words = req["words"]
    
    new_user_choices.course_vocab_submit(user_id, words)
    
    cur.close()
    conn.commit()
    conn.close()
    
    res = make_response(jsonify(out))
    
    return res
    

@app.route('/api/loadprogress', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def load_progress():

    conn, cur = connect()
    req = request.get_json()
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    if not a:
        out = {}
        out["displayType"] = "newUser"
        
        res = make_response(jsonify(out))
    
        cur.close()
        conn.commit()
        conn.close()

        return res  
        
    user_id = a[0][0]
    
    out = my_progress.load_progress(cur, user_id)
    
    print(out)
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()

    return res    

@app.route('/api/launchscreen', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def launch_screen():

    conn, cur = connect()
    req = request.get_json()
    
    COMMAND = """SELECT id, tutorial, message, level FROM users
    WHERE name=%s
    """
    
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    if not a:
        out = {}
        out["displayType"] = "newUser"
        
        res = make_response(jsonify(out))
    
        cur.close()
        conn.commit()
        conn.close()

        return res  
    
    out = {}
        
    user_id = a[0][0]
    tutorial = a[0][1]
    message = a[0][2]
    level = a[0][3]
    out["tutorial"] = tutorial
    
    out["read_notification"] = get_today_progress(cur, user_id)[0]
    
    out["level"] = level
    
    COMMAND = """SELECT * FROM user_vocab uv 
    INNER JOIN users u
    ON u.id = uv.user_id
    WHERE u.id=%s AND uv.level <= u.level AND active=0"""
    cur.execute(COMMAND, (user_id,))
    
    out["lessons_notification"] = len(cur.fetchall())
    
    out["message"] = message
    
    out["levelprogress"] = get_level_progress(cur, user_id, level)
    
    COMMAND = """SELECT v.word, uv.streak FROM user_vocab uv
    INNER JOIN vocab v
    ON uv.vocab_id = v.id
    WHERE uv.user_id=%s AND uv.level=%s
    """
    cur.execute(COMMAND, (user_id, level))
    out["levelwords"] = [{"w": x[0], "s": x[1]} for x in cur.fetchall()]
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()

    return res    

    # Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

# /server.py

