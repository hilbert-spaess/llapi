from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import pickle
import csv
import numpy as np
import json
import pandas as pd
import spacy
import psycopg2
import api_helpers
import on_review
from connect import connect

app = Flask(__name__)

# utility function: sample from an arbitrary discrete distribution

def sample_discrete(weights):

    weights = weights/np.sum(weights)

    x = np.random.rand()
    sum = weights[0]
    i = 0

    while sum < x:
        sum += weights[i+1]
        i += 1

    return i
        

# compute the correct probability values

# utility function: load a word from a CSV with a score in a particular range.

def word_range(lower, upper):
    print(lower)
    with open("vocab2.csv", 'r') as vocabfile:
        reader = list(csv.reader(vocabfile))
        for i,line in enumerate(reader[1:]):
            if float(line[2]) < upper:
                upperid = i
                break
        for i,line in enumerate(reader[upperid+1:]):
            if float(line[2]) < lower:
                print(line[2])
                lowerid = i
                break
        print("lowerid")
        print(lowerid)
        print("upperid")
        print(upperid)
        n = np.random.randint(1+upperid, 1+lowerid+upperid)
        return reader[n][0], reader[n][2]
                

def word_computation(data):

    if data["number"] == 0:
        N = np.random.randint(19000)
    
        with open("vocab2.csv", 'r') as vocabfile:
            reader = csv.reader(vocabfile)
            line = next((x for i, x in enumerate(reader) if i == N), None)

        
        word = line[0]
        score = line[2]

    else:
        with open("temp_data.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = []
            sortedlist = sorted(reader, key=lambda x: x[2])
            for row in sortedlist:
                if row[0] == data["userId"]:
                    rows.append(row)

        scores = np.array([float(row[2]) for row in rows])
        answered = np.array([float(row[3]) for row in rows])

        vals = np.zeros(len(scores)+1)
        weights = []
        for j in range(1,8):
            newanswered = []
            for i,answer in enumerate(answered):
                if scores[i] < j:
                    newanswered.append(1 - answer)
                else: newanswered.append(answer)
            newanswered = np.array(newanswered)
            newanswered = 0.8*newanswered + 0.2*(1-newanswered)
            weights.append(np.prod(newanswered))
        x = sample_discrete(weights) + 1

        #changes = [19297, 19025, 15396, 7101, 1524, 138, 12]
        # optimise this later
        


        # divide into integer sections. compute likelihood of falling into each integer section, and
        # sample accordingly (using the direct values).

        
        word, score = word_range(x, x+1)

    return word, score

def select_word(stuff):

    word, score = word_computation(stuff)

    return word, score

@app.route('/api/getword', methods=["POST", "GET"])
def get_word():

    req = request.get_json()

    if req["number"] > 0:
        with open("temp_data.csv", 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([req["userId"], req["word"], req["score"], req["answered"]])

    new_word, new_score = select_word(req)

    res = make_response(jsonify({"word": new_word, "score": new_score}))

    return res

@app.route('/api/getchunk', methods=["POST", "GET"])
def get_text_chunk():
    
    conn, cur = connect()

    req = request.get_json()
    
    userid = req["userId"]
    
    print("correct?", req["answeredCorrect"])
    
    if req["answeredCorrect"] == -1:
        out = api_helpers.next_chunk(userid, cur)
        
    else:
        
        # record the results
        
        on_review.on_review(cur, req)
        out = api_helpers.next_chunk(userid, cur)
            
    print(out)
    res = make_response(jsonify(out))
    
    cur.close()
    conn.commit()
    conn.close()

    return res

@app.route('/api/dumpresult', methods=["POST", "GET"])
def dump_result():
    req = request.json

    with open("temp_data", 'wb') as dumpfile:
        pickle.dump(req, dumpfile)

    res = make_response()

    return res

if __name__=='__main__':
    
    app.run()
