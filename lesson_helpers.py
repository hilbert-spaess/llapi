import psycopg2
import csv
import pickle
import random
from connect import connect
import test_data
import json

from warning import log_warning
import time

def get_lesson(cur, user_id, vocab_id):
    
    def get_lesson_data():
        
        COMMAND = """SELECT v.word, uv.definition FROM user_vocab uv
        INNER JOIN vocab v
        ON v.id = uv.vocab_id
        WHERE uv.user_id=%s AND uv.vocab_id=%s
        """
        cur.execute(COMMAND, (user_id, vocab_id))
        data = cur.fetchall()
        
        lesson_data = {'w': data[0][0], 'def': data[0][1]}
        
        return lesson_data

def get_all_lessons(cur, user_id):
    
    def get_lesson_vocab():
        
        COMMAND = """SELECT uv.vocab_id FROM user_vocab uv
        INNER JOIN users u
        ON u.id = uv.user_id
        WHERE u.id=%s AND active=0 AND uv.level <= u.level"""
        cur.execute(COMMAND, (user_id,))
        
        records = cur.fetchall()
        
        return [x[0] for x in records]
    
    # get the lesson for each vocab id
    
    lesson_vocab = get_lesson_vocab()
    
    lessons = {}
    
    for vocab_id in lesson_vocab:
        
        lessons[vocab_id] = get_lesson(cur, user_id, vocab_id)
        
    return lessons
        
    
    