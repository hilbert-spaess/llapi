# TESTS OF THE CURRENT SETUP

TST = "auth0|5f8055e3d94ca10071bb1a90"
# test account

import psycopg2
import random
import json

from connect import connect

from new_vocab_add import new_course
from scheduler import schedule

def close(conn, cur):
    
    cur.close()
    conn.commit()
    conn.close()

def delete_test_user():
    
    print("Deleting test user")
    
    conn, cur = connect()
    
    COMMAND = """DELETE FROM users
    WHERE name=%s"""
    cur.execute(COMMAND, (TST,))
    
    close(conn, cur)
    
    print("Test user deleted")
    
def insert_test_user(data):
    
    conn, cur = connect()
    
    print(data)
    
    COMMAND = """INSERT INTO users(name, email, vlevel, course_id, tutorial, level)
    VALUES(%s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    cur.execute(COMMAND, (TST, "test@gmail.com", data["vlevel"], data["course_id"], "0", data["level"]))
    
    user_id = cur.fetchall()[0][0]
                                                                      
    close(conn, cur)
    
    print("Test user added.")
    
    return user_id

def reset_user(cur, user_id):
    
    COMMAND = """DELETE FROM user_nextchunk
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))
    
    print("deleted pre-scheduled stuff")
    
    COMMAND = """UPDATE user_vocab
    SET active=0, next=NOW(), scheduled=0
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))
    
    print("set all to inactive")
    
def delete_all(cur, user_id):

    COMMAND = """DELETE FROM user_vocab
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))
    
    COMMAND = """DELETE FROM user_nextchunk
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))
    
    COMMAND = """DELETE FROM user_vocab_log
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))


# INTERACT-TESTS
# put an account in a certain state and allow me to interact with it

# account logging in for the first time, and doing first reviews.
# account doing reviews

#

def log_in_test():
    
    response = ""
    
    while response != "y":
    
        delete_test_user()

        print("Try logging in with test@gmail.com")

        response = input(">")
        
    
def random_day_lvl1(data):
    
    data["level"] = "1"
    
    delete_test_user()
    
    user_id = insert_test_user(data)
    
    new_course(user_id, data["course_id"])
    
    conn, cur = connect()
    
    reset_user(cur, user_id)
    
    # set active for the right stuff
    
    COMMAND = """SELECT vocab_id 
    FROM user_vocab
    WHERE user_id=%s AND level=1"""
    cur.execute(COMMAND, (user_id,))
    vocab_ids = [x[0] for x in cur.fetchall()]
    
    active_ids = random.sample(vocab_ids, 4)
    
    COMMAND = """UPDATE user_vocab
    SET active=1, streak=%s
    WHERE user_id=%s AND vocab_id=%s
    """
    
    for vocab_id in active_ids:
        
        streak = str(random.randint(0,3))
        
        cur.execute(COMMAND, (streak, user_id, vocab_id))
        
        print("Set " + str(vocab_id) + " active. Streak " + streak)
        
    close(conn, cur)
        
    schedule(user_id)
        
    print("Scheduled today's reviews for test user.")
    # set streaks for the right stuff
    
    r = input("Now do today's reviews.")
    
    # check to see if everything scheduled
    
    conn, cur = connect()
    
    COMMAND = """SELECT vocab_id, scheduled, next, streak, levelled
    FROM user_vocab
    WHERE user_id=%s and active=1"""
    cur.execute(COMMAND, (user_id,))
    
    records = cur.fetchall()
    
    for instance in records:
        
        print("Vocab ID: " + str(instance[0]))
        print("Scheduled: " + str(instance[1]))
        print("Streak: " + str(instance[3]))
        print("Scheduled for: " + str(instance[2]))
        print("Levelled up? " + str(instance[4]))
    
# level-up test

def level_up(data):
    
    delete_test_user()
    
    user_id = insert_test_user(data)
    
    new_course(user_id, data["course_id"])
    
    conn, cur = connect()
    
    reset_user(cur, user_id)
    
    COMMAND = """UPDATE user_vocab
    SET active=1, next=NOW(), streak=3
    WHERE user_id=%s AND level=%s
    """
    cur.execute(COMMAND, (user_id, data["level"]))
    
    close(conn, cur)
    
    schedule(user_id)
    
    r = input("Level yourself up now.")
    
    # let the test user level up
    
    conn, cur = connect()
    
    COMMAND = """SELECT level FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    
    lvl = cur.fetchall()[0][0]
    
    print("Level: " + str(lvl))
    
    COMMAND = """SELECT vocab_id, scheduled, next, streak, levelled, level
    FROM user_vocab
    WHERE user_id=%s and active=1
    """
    cur.execute(COMMAND, (user_id,))
    
    records = cur.fetchall()
    
    for instance in records:
        
        print("Vocab ID: " + str(instance[0]))
        print("Level: " + str(instance[5]))
        print("Scheduled: " + str(instance[1]))
        print("Streak: " + str(instance[3]))
        print("Scheduled for: " + str(instance[2]))
        print("Levelled up? " + str(instance[4]))
    
    # check that the test user has indeed levelled up

# simulate a real user test

def simulate(simulated_user_id):
    
    delete_test_user()
    
    conn, cur = connect()
    
    COMMAND = """SELECT vlevel, course_id, level FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (simulated_user_id,))
    r = cur.fetchall()[0]
    
    data = {"vlevel": r[0], "course_id": r[1], "level": r[2]}
    
    user_id = insert_test_user(data)
    
    delete_all(cur, user_id)
    
    COMMAND = """SELECT * FROM user_vocab
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (simulated_user_id,))
    
    INS_COMMAND = """INSERT INTO user_vocab(user_id, vocab_id, sense, definition, active, scheduled, next, streak, level, levelled)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    records = cur.fetchall()
    
    for instance in records:
        
            cur.execute(INS_COMMAND, (user_id, instance[1], instance[2], instance[3], instance[4], instance[5], instance[6], instance[7], instance[8], instance[9]))
            
    print("simulated user_vocab")
    
    COMMAND = """SELECT * FROM user_nextchunk
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (simulated_user_id,))
    
    INS_COMMAND = """INSERT INTO user_nextchunk(user_id, chunk_id, next, test_data, first, unknown_vocab, unknown_grammar, vocab_id)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    records = cur.fetchall()
    
    for instance in records:
        
        cur.execute(INS_COMMAND, (user_id, instance[1], instance[2], json.dumps(instance[3]), instance[4], instance[5], instance[6], instance[7]))
        
    print("simulated user_nextchunk")
        
    COMMAND = """SELECT * FROM user_vocab_log
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (simulated_user_id,))
    
    INS_COMMAND = """INSERT INTO user_vocab_log(user_id, vocab_id, chunk_id, time, result)
    VALUES(%s, %s, %s, %s, %s)
    """
    records = cur.fetchall()
    
    for instance in records:
        
        cur.execute(INS_COMMAND, (user_id, instance[1], instance[2], instance[3], instance[4]))
        
    print("simulated user_vocab_log")
    
    close(conn, cur)
            
def step_time_test_user():
    
    conn, cur = connect()
    
    COMMAND = """SELECT id FROM users
    WHERE name=%s
    """
    cur.execute(COMMAND, (TST,))
    user_id = cur.fetchall()[0][0]
    
    COMMAND = """UPDATE user_nextchunk
    SET next = next - INTERVAL '1 day'
    WHERE user_id=%s
    """
    
    cur.execute(COMMAND, (user_id,))
    
    close(conn, cur)
    
    
    
    

# RUN-TESTS
# put an account in a certain state and check that important functions still work

##

"""
print("Log in test.")
log_in_test()

print("Level 1 test.")
data = {"vlevel": "1.5", "course_id": "2"}
random_day_lvl1(data)

print("Level up test.")
data = {"vlevel": "1.5", "course_id": "2", "level": "1"}
level_up(data)
"""

log_in_test()
