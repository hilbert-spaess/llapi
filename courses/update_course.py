from connect import connect

def update_course(cur, user_id):
    
    # get active lvl
    
    LVL_COMMAND = """SELECT level FROM users
    WHERE id=%s
    """
    cur.execute(LVL_COMMAND, (user_id,))
    level = cur.fetchall()[0][0]
    
    cutoff = level + 2
    
    DEL_COMMAND = """DELETE FROM user_vocab
    WHERE user_id = %s AND level >= %s
    """
    cur.execute(DEL_COMMAND, (user_id, str(cutoff)))
    
    # delete everything beyond the one up level
    
def update_vocab_level(cur, course_id):
    
    if course_id == 1:
        vlevel = "10000"
    if course_id == 2:
        vlevel = "30000"
    
    COMMAND = """UPDATE users
    SET vlevel=%s WHERE course_id=%s
    """
    cur.execute(COMMAND, (vlevel, str(course_id)))
    
def update_message(cur, message, course_id):
    
    COMMAND = """UPDATE users
    SET message=%s WHERE course_id=%s
    """
    cur.execute(COMMAND, (message, course_id))
    
def update_all_courses(cur):
    
    COMMAND = """SELECT id, course_id, email FROM users"""
    cur.execute(COMMAND)
    
    records = cur.fetchall()
    
    for instance in records:
        
        user_id, course_id, email = instance
        
        print("updating " + email)
        
        update_course(cur, user_id)
        
        update_vocab_level(cur, course_id) 
    
    
conn, cur = connect()

update_all_courses(cur)

cur.close()
conn.commit()
conn.close()