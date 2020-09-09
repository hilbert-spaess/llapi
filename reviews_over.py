import psycopg2
import csv
import pickle
import random
from connect import connect
import scheduler
import new_vocab_add

def get_new_word_no(cur, user_id):
    
    return 5

def reviews_over(user_id):
    
    conn, cur = connect()

    word_no = get_new_word_no(cur, user_id)
    new_vocab_add.new_vocab_add(cur, user_id, word_no)
    
    cur.close()
    conn.commit()
    conn.close()
    
    scheduler.schedule(user_id)