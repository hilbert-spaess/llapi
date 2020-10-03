# log warnings if things go wrong

from config import WARNING_FILE

def log_warning(params):

    with open(WARNING_FILE, 'a') as warningfile:
        warningfile.write(" ".join([":".join([str(a),str(params[a])]) for a in params.keys()]) + "\n")
