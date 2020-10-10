from connect import connect

# total usage

# who's been on today

# anything left unscheduled today?

def close(conn, cur):
    
    cur.close()
    conn.commit()
    conn.close()

def display_users():
    
    conn, cur = connect()
    
    print("###")
    print("CURRENT USERS")
    print("email, course, level")
    print("###")
    print("\n\n")
    
    cur.execute("select email, course_id, level from users")
    
    records = cur.fetchall()
    
    for instance in records:
        
        print(", ".join([str(x) for x in instance]))
        
    print("\n\n")
    
def unscheduled():
    
    conn, cur = connect()
    
    print("###")
    print("UNSCHEDULED REVIEWS")
    print("user_id, course, level")
    print("###")
    print("\n\n")
    
    cur.execute("select user_id, vocab_id from user_vocab where active=1 and scheduled=0")
    records = cur.fetchall()
    
    for instance in records:
        
        print(", ".join([str(x) for x in instance]))
         
    print("\n\n")
    
def users_work_today():
    
    conn, cur = connect()
    
    print("###")
    print("USERS WORK TODAY")
    print("###")
    
    cur.execute("select user_id from user_vocab_log where DATE(time) = DATE(NOW())")
    records = list(set(cur.fetchall()))
    
    for instance in records:
        
        user_id = instance[0]
        
        COMMAND = """SELECT email FROM users WHERE id=%s"""
        cur.execute(COMMAND, (user_id,))
        
        email = cur.fetchall()[0][0]
        
        print("User " + email + "!!")
        
def recent_usage(user_id):
    
    conn, cur = connect()
    
    COMMAND = "SELECT email from users where id=%s"
    cur.execute(COMMAND, (user_id,))
    email = cur.fetchall()[0][0]
    
    print("###")
    print("Recent work of " + email)
    
    COMMAND = """SELECT vocab_id FROM user_vocab_log
    WHERE user_id = %s AND DATE(time) = DATE(NOW() - %s * INTERVAL '1 day')
    """
    
    for i in range(10):
        
        cur.execute(COMMAND, (user_id, str(i)))
        
        print(str(i) + " days ago: " + str(len(cur.fetchall())))
        
def all_recent_usage():
    
    conn, cur = connect()
    
    print("###")
    print("PROGRESS OF USERS FROM THE LAST THREE DAYS")
    print("###\n\n")
    
    COMMAND = """SELECT user_id FROM user_vocab_log
    WHERE DATE(time) >= DATE(NOW() - 5 * INTERVAL '1 day')
    """
    cur.execute(COMMAND)
    records = list(set(cur.fetchall()))
    
    for instance in records:
        
        recent_usage(instance[0])
        
        print("\n\n")
        
def all_diagnostics():
    
    display_users()
    unscheduled()
    users_work_today()
    all_recent_usage()

all_diagnostics()
    
    