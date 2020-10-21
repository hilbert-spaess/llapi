def get_permissions(cur, user_id):
    
    COMMAND = """SELECT course_id FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    course_id = cur.fetchall()[0][0]
    
    if course_id == 7:
        
        return ["b"]
    
    return []