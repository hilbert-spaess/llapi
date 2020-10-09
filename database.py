from connect import connect

#general wrappers for interfacing with the database

# not the responsibility of this code to open connection to the database

def select(cur, data):
    
    table = data["table"]
    keys = data["keys"]
    conditions = [x.split(" ") for x in data["conditions"]]
    
    def get_condition(condition):
        
        if condition[0] == "equal":
            
            return "=".join([condition[1], "%s"])
        
        else:
            
            return None
        
    def get_value(condition):
        
        if condition[0] == "equal":
            
            return condition[2]
        
        else:
            
            return None
        
    def keyify(instance):
        
        out_dict = {}
        
        for i, key in enumerate(keys):
            
            out_dict[key] = instance[i]
        
        return out_dict
            
    
    # table is a tuple containing the tables to be chosen from.
    
    table = data["table"]
    keys = data["keys"]
    conditions = [x.split(" ") for x in data["conditions"]]
    
    print(conditions)
    
    keys_string = ",".join(keys)
    
    conditions_string = " AND ".join([get_condition(condition) for condition in conditions if get_condition(condition)])
    
    values = tuple([get_value(condition) for condition in conditions if get_value(condition)])
    
    COMMAND = "SELECT " + keys_string + " FROM " + table + " WHERE " + conditions_string
    
    cur.execute(COMMAND, values)
    
    records = cur.fetchall()
    
    return [keyify(instance) for instance in records]
    
def select_join(data):
    
    pass

conn, cur = connect()
a = select(cur, {"table": "user_vocab", "keys": {"streak", "levelled"}, "conditions": ["equal user_id 39", "equal level 2"]})
print(a)