from flask import Flask, request, make_response, jsonify, _request_ctx_stack, redirect
from flask_cors import CORS, cross_origin
import pickle
import csv
import numpy as np
import json
import pandas as pd
import psycopg2
from api_helpers import choose_next_chunk, next_chunk, get_all_chunks, load_tutorial, get_today_progress, get_level_progress
from gcse_english_course import days
import on_review
from connect import connect
import threading
import reviews_over
import my_vocab, my_progress, new_user_choices, read_for_fun, course_data
from tests import log_in_test_alex, step_time_test_user_alex
import new_vocab_add
from config import API_AUDIENCE, DIRECTORY
import random
import json
import lists
import reading

import permissions

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

@app.route('/api/register', methods=["POST", "GET"])
@cross_origin(origin='*')
def redirect_to_verify():
    
    req = request.query_string.decode()
    
    return redirect("http://ricecake.ai/register?" + req, code=302)

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

@app.route('/api/readforfun', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def read_for_fun_api(cur, user_id):
    
    out = {}
    
    out["allChunks"] = read_for_fun.read_for_fun(cur, user_id)
    
    out["today_progress"] = {"yet": len(out["allChunks"]), "done": 0}
    
    out["displayType"] = "readforfun"
    
    res = make_response(jsonify(out))
    
    return res
        

@app.route('/api/startreading', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_text_chunk():
    
    req = request.get_json()
    conn, cur = connect()
    out = {}

    print("rquest")
    print(req)
    
    COMMAND = """SELECT id, tutorial FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    # possibly a new user
    
    if not a:
        out["status"] = "newUser"
        
        res = make_response(jsonify(out))

        cur.close()
        conn.commit()
        conn.close()

        return res
    
    user_id = a[0][0]
    
    # possibly just a log

    if req == {}:
        return make_response(jsonify({}))
    
    if "type" in req.keys() and req["type"] == "daily_reading":
        
        print("hihi nigaa")
        
        return reading.daily_reading(cur, conn, user_id, req)
    
    return make_response(jsonify({}))
    
    
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
    
    elif req["type"] == "submit_choice":
        
        my_vocab.submit_choice(cur, user_id, req["payload"])
        
        out = {"state": "null"}
        
    elif req["type"] == "delete":
        
        my_vocab.delete_word(cur, user_id, req["payload"]["data"])
        
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
        if instance[1] not in [x[1] for x in todaychunks]:
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
    
    out["permissions"] = permissions.get_permissions(cur, user_id)
    
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
    
    out["course_vocab"] = new_user_choices.course_vocab_samples(cur, req["course"])
    
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
    
    print(req)
    
    COMMAND = """INSERT INTO users(name, vlevel, course_id, email, tutorial, message, level)
    VALUES(%s, %s, %s, %s, %s, %s, 1)
    RETURNING id"""
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'], 0, req["course"], req["email"], 0, ""))
    user_id = cur.fetchall()[0][0]
    
    words = req["words"]
    course_id = req["course"]
    
    cur.close()
    conn.commit()
    conn.close()
    
    new_user_choices.course_vocab_submit(user_id, course_id, words)
    
    res = make_response(jsonify(out))
    
    return res



@app.route('/api/resetaccount', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def reset_account():
    
    conn, cur = connect()
    
    req = request.get_json()
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    user_id = a[0][0]
    
    log_in_test_alex()
    
    return make_response(jsonify({}))

@app.route('/api/steptime', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def step_time():
    
    conn, cur = connect()
    
    req = request.get_json()
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    user_id = a[0][0]
    
    step_time_test_user_alex()
    
    return make_response(jsonify({}))
     

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
    
    out["read_data"] = reading.daily_reading(cur, conn, user_id, {}).get_json()
    
    out["vocab_data"] = my_vocab.load_vocab(cur, user_id, req)
    
    COMMAND = """SELECT * FROM user_vocab
    WHERE user_id=%s AND streak > 0"""
    cur.execute(COMMAND, (user_id,))
    lightbluewords = len(cur.fetchall())
    
    COMMAND = """SELECT * FROM user_vocab
    WHERE user_id=%s AND streak > 4"""
    cur.execute(COMMAND, (user_id,))
    darkbluewords = len(cur.fetchall())
    
    lightbluewords = lightbluewords - darkbluewords
    
    out["wordnos"] = [lightbluewords, darkbluewords]
    
    
    
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

@app.route('/api/loadlists', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def load_lists():

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
    
    user_id = a[0][0]
    
    out = {}
    
    out["lists"] = lists.load_lists(cur, user_id)
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()

    return res 

@app.route('/api/newlist', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def new_list():
    
    req = request.get_json()
    conn, cur = connect()
    
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    user_id = cur.fetchall()[0][0]
    
    out = {}
    
    if req["payload"] == {}:
        
        res = make_response(jsonify(out))
        return res
    
    if req["type"] == "read":
        
        out["read_data"] = lists.read_list(cur, user_id, req["payload"])
        out["state"] = "read"
        out["list_id"] = req["payload"]["id"]
    
    else:
        out= {"state": "null"}
    
    cur.close()
    conn.commit()
    conn.close()
    
    res = make_response(jsonify(out))
    
    return res

@app.route('/api/loglist', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def log_list():
    
    req = request.get_json()
    conn, cur = connect()
    
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    user_id = cur.fetchall()[0][0]
    
    out = {}
    
    if "status" in req.keys() and req["status"] == "alive":
        
        lists.register_score(cur, user_id, req)
        
    cur.close()
    conn.commit()
    conn.close()
    
    res = make_response(jsonify({}))
    return res

@app.route('/api/coursedata', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_course_data():

    req = request.get_json()
    conn, cur = connect()

    print("hemlo")
    print(req)

    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    user_id = cur.fetchall()[0][0]

    return course_data.load_data(cur, user_id, req)

@app.route('/api/coursedays', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_course_days():

    req = request.get_json()
    conn, cur = connect()

    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    user_id = cur.fetchall()[0][0]

    out = {}

    out["days"] = 7
    out["notifications"] = []

    comp_dict = {0: 7, 1: 21, 2: 49, 3: 49, 4: -1, 5: -1, 6: -1}

    for i in range(out["days"]):

        COMP_CMD = """SELECT * FROM tutee_course
        WHERE course_id=1 AND user_id=%s AND answer_id=%s
        """
        cur.execute(COMP_CMD, (user_id, comp_dict[i]))
        r = cur.fetchall()
        print(r)
        if r:
            read = 0
        else:
            read = 1

        write = 1

        VOC_CMD = """SELECT answer_id FROM tutee_course
        WHERE course_id=1 AND user_id=%s AND answer_id > 1999 AND answer_id < 3000"""
        cur.execute(VOC_CMD, (user_id,))
        answers = [x[0] for x in cur.fetchall()]

        poss = [x["question"]['id'] for x in days[i]["Vocabulary"]]

        print("poss", poss)
        print("answers", answers)

        rem = list(set(poss) - set(answers))

        out["notifications"].append({"C": read, "V": len(rem), "W": write})

    return make_response(jsonify(out))
    

@app.route('/api/analysislog', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def log_analysis():

    req = request.get_json()
    conn, cur = connect()


    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    user_id = cur.fetchall()[0][0]

    CHK_COMMAND = """SELECT * FROM tutee_course
    WHERE user_id=%s AND answer_id=%s AND course_id=%s"""
    
    INS_COMMAND = """INSERT INTO tutee_course(text, user_id, answer_id, course_id)
    VALUES(%s, %s, %s, %s)
    """

    UPD_COMMAND = """UPDATE tutee_course
    SET text=%s
    WHERE user_id=%s AND answer_id=%s AND course_id=%s
    """

    for item in req["answers"].items():

        cur.execute(CHK_COMMAND, (user_id, item[0], req["course_id"]))
        if not cur.fetchall():
        
            cur.execute(INS_COMMAND, (item[1], user_id, item[0], req["course_id"]))

        else:

            cur.execute(UPD_COMMAND, (item[1], user_id, item[0], req["course_id"]))

    cur.close()
    conn.commit()
    conn.close()

    print(req)
    print("hemlo")

    return make_response(jsonify({}))


@app.route('/api/tutorview', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_tutors():

    req = request.get_json()
    conn, cur = connect()

    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    user_id = cur.fetchall()[0][0]

    print(req)
    print("hemlo")


    out = {"users": [{'user_id': '609', 'email':'test@gmail.com'}, {'user_id': '596', 'email': 'albertdaitt@gmail.com'}, {'user_id': '613', 'email': 'charlotte.bev@gmail.com'}, {'email': 'cyl070716@gmail.com', 'user_id': '615'}, {'email': 'guoyudong20060126@outlook.com', 'user_id': '614'}, {'user_id': '616', 'email': 'lukejiang@yandex.com'}]}

    return make_response(jsonify(out))




@app.route('/api/jobs', methods=["POST", "GET"])
@cross_origin(origin='*')
def load_jobs():

    req = request.get_json()

    out = {}

    outjobs = []

    with open(DIRECTORY + "/jobs/stem_jobs.txt", 'r') as jobfile:

        joblines = jobfile.read()
        jobs = joblines.split("##")[1:]
        jobs = [x for x in jobs if x.strip()]

    for job in jobs:

        new = {}

        for x in job.split("\n"):

            if x.strip():

                x = x.strip()

                print(x.split())

                new[x.split()[0].strip()] = " ".join(x.split()[1:]).strip()

        outjobs.append(new)

    out["jobs"] = outjobs

    res = make_response(jsonify(out))

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

