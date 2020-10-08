import connect
from wordfreq import zipf_frequency
import numpy as np

from connect import connect

conn, cur = connect()

# load vocab with definitions to the vocab database

def load_vocab():

    with open("./vocab.txt", 'r') as vocabfile:
        vocab = [x.split(":") for x in vocabfile.readlines() if len(x.split(":")) >= 3]

    THERE_COMMAND = """SELECT * FROM vocab
    WHERE word=%s AND pos=%s
    """

    INS_COMMAND = """INSERT INTO vocab(word, pos, zipf) 
    VALUES(%s, %s, %s)
    RETURNING id
    """

    with open("./vocab1.txt", 'w') as outfile:

        for item in vocab:

            if len(item) != 3:
                outfile.write(":".join(item))

            else:

                cur.execute(THERE_COMMAND, (item[0].strip(), item[2].strip()))
                r = cur.fetchall()

                if not r:

                    cur.execute(INS_COMMAND, (item[0].strip(), item[2].strip(), zipf_frequency(item[0].strip(), 'en')))
                    r = cur.fetchall()

                item = [x.strip() for x in item]
                item.append(str(r[0][0]) + "\n")
                outfile.write(":".join(item))
                
def add_to_curriculum():
    
    with open("./curriculum.txt", 'r') as currentfile:
        curriculum = [x.split(":") for x in currentfile if x.strip()]
    
    curriculum_words = [x[0] for x in curriculum]
    levels = [x[4] for x in curriculum]
    level = max(levels)
    print(level)
    newlevel = str(int(level) + 1)
    
    with open("./vocab1.txt", 'r') as vocabfile:
        vocab = [x.split(":") for x in vocabfile.readlines() if len(x.split(":")) >= 3 and x.split(":")[0] not in curriculum_words]
        print(vocab)
    
    with open("./curriculum.txt", 'a') as outfile:
        if len(vocab) >= 15:
            z = np.random.randint(11, 15)
            for item in vocab[:z]:
                outfile.write(item[0].strip() + ":" + "x" + ":" + item[1].strip() + ":" + item[3].strip() + ":" + newlevel +  ":" + item[2].strip() + "\n")

        
    
    
load_vocab()
add_to_curriculum()

cur.close()
conn.commit()
conn.close()

    
# load them to the curriculum- choose levels- find vocab IDs

# separate function for live-changing the curricula for people