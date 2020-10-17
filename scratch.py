# add course to all vocabulary currently in circulation.

from connect import connect


def add_course(cur, user_id):
    
    COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    COMMAND = """UPDATE user_vocab
    SET course_id=%s
    WHERE user_id=%s
    """
    cur.execute(COMMAND, (course_id, user_id))

def get_all_ids(cur):
    
    COMMAND = """SELECT id FROM users"""
    cur.execute(COMMAND)
    
    ids = [x[0] for x in cur.fetchall()]
    
    return ids

conn,cur = connect()

user_ids = get_all_ids(cur)

for user_id in user_ids:
    
    print(user_id)
    
    add_course(cur, user_id)

cur.close()
conn.commit()
conn.close()