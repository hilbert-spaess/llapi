def get_permissions(cur, user_id):
    
    COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    return []