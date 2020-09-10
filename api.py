from flask import Flask, request, make_response, jsonify, _request_ctx_stack
from flask_cors import CORS, cross_origin
import pickle
import csv
import numpy as np
import json
import pandas as pd
import spacy
import psycopg2
from api_helpers import choose_next_chunk, next_chunk
import api_helpers
import on_review
from connect import connect
import threading
import reviews_over
import my_vocab
import new_vocab_add

from six.moves.urllib.request import urlopen
from functools import wraps
from jose import jwt

import sys
sys.path.append('/var/www/html/llapi')
sys.path.append('/home/ubuntu/.local/lib/python3.5/site-packages')

AUTH0_DOMAIN = "dev-yt8x5if8.eu.auth0.com"
API_AUDIENCE="http://localhost:5000"
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
        jwks = json.loads(jsonurl.read())
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
    
    if chunk_id:
        out = next_chunk(cur, user_id, chunk_id)
    else:
        out = {}
        out["displayType"] = "done"
    
    res = make_response(jsonify(out))
    
    return res
        

@app.route('/api/getchunk', methods=["POST", "GET"])
@cross_origin(origin='*')
@requires_auth
def get_text_chunk():
    
    print("HENLO there sir")
    
    req = request.get_json()
    conn, cur = connect()
    out = {}
    
    print(req)
    print("HEMLO")
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'],))
    
    a = cur.fetchall()
    
    print(a)
    
    if not a:
        out["displayType"] = "newUser"
        
        res = make_response(jsonify(out))

        cur.close()
        conn.commit()
        conn.close()

        return res
    
    user_id = a[0][0]
    
    if req["answeredCorrect"] == "-1":
        print("HEMLO this is the first chumk")
        return get_first_chunk1(cur, user_id, req)
    
    else:
        
        print(req['keyloc'])

        on_review.on_review(cur, user_id, req)

        cur.close()
        conn.commit()
        conn.close()

        conn, cur = connect()

        chunk_id = choose_next_chunk(cur, user_id)

        if chunk_id:
            out = next_chunk(cur, user_id, chunk_id)
        else:
            out["displayType"] = "done"
            new_conn, new_cur = connect()
            x = threading.Thread(target=reviews_over.reviews_over, args=(user_id,))
            x.start()
            print("Starting the background scheduling thread.")

        res = make_response(jsonify(out))

        cur.close()
        conn.commit()
        conn.close()

        return res
    
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
    
    a = cur.fetchall()
    
    if not a:
        
        course_id = req["courseChoice"]
        print("course choice", course_id)
        
        COMMAND = """INSERT INTO users(name, vlevel)
        VALUES(%s, %s)
        RETURNING id"""
        cur.execute(COMMAND, (_request_ctx_stack.top.current_user['sub'], '4.5'))
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
    user_id = a[0][0]
    
    out = my_vocab.load_vocab(cur, user_id, req)
    
    print(out)
    
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()

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

