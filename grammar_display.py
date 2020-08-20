import numpy as np
import spacy
import re
from grammar_cambridge import *
for key  in grammardict.keys():
    if key not in confounders.keys():
        confounders[key] = (1, [])
        
import dill as pickle

grammar_ids = {}

for (i, idx) in enumerate(sorted(list(grammardict.keys()))):
    grammar_ids[i] = idx
    
def grammar_analyse(sentence):
    keys = sorted(list(grammardict.keys()))
    n = len(sentence)
    masks = []
    for i,key in enumerate(keys):
        newmask = i * grammardict[key](sentence)
        if np.sum(newmask) > 0:
            masks.append(newmask)
    mask = [[(int(x[k]), keys[int(x[k])]) for x in masks if x[k] != 0] for k in range(n)]
    return mask, 
    
    
