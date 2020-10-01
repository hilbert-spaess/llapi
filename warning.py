# log warnings if things go wrong

from config import WARNING_FILE

def log_warning(params):

    with open(WARNING_FILE, 'a') as warningfile:
        warningfile.write(" ".join([":".join([a,params[a]]) for a in params.keys()]) + "\n")
