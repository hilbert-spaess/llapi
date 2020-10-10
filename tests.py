# TESTS OF THE CURRENT SETUP

TST = "auth0|5f8055e3d94ca10071bb1a90"
# test account

import psycopg2

from connect import connect

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
        
    
    
    

# RUN-TESTS
# put an account in a certain state and check that important functions still work

##

print("Log in test.")
log_in_test()