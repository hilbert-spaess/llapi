import numpy as np
from flask import Flask, request, make_response, jsonify, _request_ctx_stack, redirect
from gcse_english_course import days

def load_data(cur, user_id, req):

    answers = {}

    out = {}

    if "data" in req.keys() and "mode" in req["data"].keys() and req["data"]["mode"] == "tutor":

        COMMAND = """SELECT * FROM tutee_course
        WHERE user_id=%s AND course_id=%s"""
        cur.execute(COMMAND, (req["data"]["user_id"], 1))
        r = cur.fetchall()

        for item in r:

            answers[item[2]] = item[3]

    else:

        COMMAND = """SELECT * FROM tutee_course
        WHERE user_id=%s AND course_id=%s"""
        cur.execute(COMMAND, (user_id, 1))
        r = cur.fetchall()

        for item in r:

            answers[item[2]] = item[3]
        

    

    out["answers"] = answers

    print(out["answers"])

    if "data" in req.keys():
        out["data"] = req["data"]
    else:
        out["data"] = {}

    i = int(req["id"])

    print(i)

    out["allChunks"] = days[i-1]

    out["today_progress"] = {"yet": len(out["allChunks"]), "done": 0}

    out["course_id"] = 1 # gcse english reading course

    res = make_response(jsonify(out))

    return res
