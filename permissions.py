TST = ["auth0|5f8055e3d94ca10071bb1a90", "auth0|5f96f26c7539d10068acec2b"]

def get_permissions(cur, user_id):
    
    COMMAND = """SELECT course_id, name FROM users
    WHERE id=%s
    """
    cur.execute(COMMAND, (user_id,))
    records = cur.fetchall()
    course_id = records[0][0]
    name = records[0][1]
    
    if course_id == 7:
        
        return ["b"]
    
    if name in TST:
        
        return ["s", "r"]
    
    return []