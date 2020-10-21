from connect import connect

# check for words in the user_vocab that don't have many counts.

def no_counts(cur, user_id, level, course_id):
    
    WD_COMMAND = """SELECT word FROM vocab WHERE id=%s"""
    
    print("\nNEW AND UNHINGED")
    
    COMMAND = """SELECT uv.vocab_id, uv.level, uv.definition FROM user_vocab uv
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (user_id,))
    records = cur.fetchall()
    
    for instance in records:
        
        if not instance[2]:
        
            cur.execute(WD_COMMAND, (instance[0],))
            wd = cur.fetchall()[0][0]

            print(wd)
            print("Level: " + str(instance[2]))
        
    
    COMMAND = """SELECT uv.vocab_id, cv.counts, uv.level FROM user_vocab uv
    INNER JOIN course_vocab cv
    ON cv.vocab_id = uv.vocab_id
    WHERE uv.user_id=%s AND cv.counts < 5 AND uv.level < %s AND cv.course_id=%s
    """
    cur.execute(COMMAND, (user_id, level + 2, course_id))
    records = cur.fetchall()
    
    print("\nNOT ENOUGH SENTENCES FOR")
    
    WD_COMMAND = """SELECT word FROM vocab WHERE id=%s"""
    
    for instance in records:
        
        cur.execute(WD_COMMAND, (instance[0],))
        wd = cur.fetchall()[0][0]
        
        print("Word: " + wd)
        print("Level: " + str(instance[2]))
        print("Counts: " + str(instance[1]))
        print("\n")
    

def no_words(cur, user_id):
    
    pass

# check if there aren't enough words.

conn, cur = connect()

COMMAND = """SELECT id FROM users"""
cur.execute(COMMAND)
user_ids = [x[0] for x in cur.fetchall()]

for user_id in user_ids:
    
    COMMAND = """SELECT level, email, course_id FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    level, email, course_id = cur.fetchall()[0]
    
    print(level, email)
    print("\n")
    
    no_counts(cur, user_id, level, course_id)

cur.close()
conn.commit()
conn.close()