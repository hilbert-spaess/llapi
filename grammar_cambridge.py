# %%
import numpy as np
import spacy

# %%
#nlp = spacy.load("en_core_web_md")

# %%
grammardict = {}
confounders = {}

# %%
def structureless_phrase(phrase):
    def get_phrase(a):
        n = len(phrase.split(" "))
        phr = phrase.split(" ")
        mask = np.zeros(len(a))
        for i,x in enumerate(a[n-1:]):
            for j in range(n):
                if a[n-1+i-j].lower_ != phr[-1-j].lower():
                    break
            else:
                for j in range(n):
                    mask[n-1+i-j] = 1
        return mask
    
    return lambda x: get_phrase(x)

# %%
# CONSTANTS

time_nouns = sorted(list(set(["time", "morning", "afternoon", "weekend","evening", "second", "moment", "minute", "hour", "day", "week", "night", "season", "month", "year", "decade", "century"])))

# %%
def a_bit(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.text in ["a", "an"] and x.head.lemma_=="bit":
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["A bit"] = a_bit
confounders["A bit"] = (1,)

# %%
# as written above, as noted above, as stated above

def as_written_above(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.text=="," and a[i-1].lower_=="above" and a[i-2].tag_=="VBN" and a[i-3].lower_=="as":
            mask[i-1]=1
    return mask

grammardict["As written above"] = lambda x: as_written_above(x)
confounders["As written above"] = (1,)

# override usual as, above

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/according-to

def according_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.text=="to" and a[i-1].lower_ == "according" and "pobj" in [y.dep_ for y in x.subtree]:
            mask[i]=1
            mask[i-1]=1
    return mask

grammardict["According to"] = according_to
confounders["According to"] = (1,)

# override usual to

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/actual-and-actually

def actually(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="actually" and x.dep_=="advmod": mask[i]=1
    return mask

grammardict["Actually"] = actually
confounders["Actually"] = (0,)

# override usual adverb

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/adjective-phrases-functions

def adjective_after_pronoun(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.pos_=="ADJ" and a[i-1].lower_ in ["anyone", "anybody", "anything", "anywhere", "everyone", "everybody", "everything", "everywhere", "no one", "nobody", "nothing", "nowhere", "someone", "somebody", "something", "somewhere"]:
            mask[i]=1
            mask[i-1]=1
    return mask

# override usual stuff

grammardict["Adjective after pronoun"] = adjective_after_pronoun
confounders["Adjective after pronoun"] = (1,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/age

def at_the_age_of(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.lower_ == "of" and a[i-1].lower_=="age" and a[i-1].head.lower_=="at":
            mask[i]=1
            mask[i-1]=1
            mask[a[i-1].head.i]=1
    return mask

def is_years_old(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.lower_ == "old" and a[i-1].lemma_ in time_nouns and x.head.lemma_=="be":
            mask[i]=1
            mask[i-1]=1
            mask[a[i-1].head.i]=1
    return mask

def is_years_of_age(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.lower_ == "age" and a[i-1].lower_=="of" and a[i-2].lemma_ in time_nouns and a[i-2].head.lemma_=="be":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
            mask[a[i-2].head.i]=1
    return mask

def how_old(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_ == "old" and a[i-1].lower_=="how":
            mask[i-1]=1
            mask[i]=1
    return mask

def what_age(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_ == "age" and a[i-1].lower_=="what":
            mask[i-1]=1
            mask[i]=1
    return mask

grammardict["At the age of"] = at_the_age_of
grammardict["Is years old"] = is_years_old
grammardict["Is years of age"] = is_years_of_age
grammardict["How old"] = how_old
grammardict["What age"] = what_age

confounders["At the age of"] = (1,)
confounders["Is years old"] = (1,)
confounders["Is years of age"] = (1,)
confounders["How old"] = (1,)
confounders["What age"] = (1,)

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/alike

def alike_adj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="alike" and x.pos_=="ADJ":
            mask[i]=1
    return mask

grammardict["Alike: adjective"] = alike_adj
confounders["Alike: adjective"] = (0,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/all

def all_det(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ =="all" and x.pos_ in ["DET", "PDT"] and x.tag_ in ["DT", "PDT"]:
            mask[i] = 1
    return mask

def all_of_pp(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_ =="of" and a[i-1].lower_=="all" and a[i+1].pos_=="PRON":
            mask[i] = 1
            mask[i-1]=1
            mask[i+1]=1
    return mask

def all_together(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="together" and a[i-1].lower_=="all":
            mask[i] = 1
            mask[i-1]=1
    return mask

grammardict["All (determiner)"] = all_det
grammardict["All of + pronoun"] = all_of_pp
grammardict["All together"] = all_together

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/also-as-well-or-too

def as_well(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="well" and x.dep_=="advmod" and a[i-1].lower_=="as":
            mask[i] = 1
            mask[i-1]=1
    return mask

grammardict["As well"] = as_well

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/alternate-ly-alternative-ly

def every_other(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 1 and x.lemma_ in time_nouns and a[i-1].lower_=="other" and a[i-2].lower_=="every":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["Every other + time"] = every_other

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/although-or-though

def as_though(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="though" and a[i-1].lower_=="as":
            mask[i] = 1
            mask[i-1]=1
    return mask

def as_if(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="though" and a[i-1].lower_=="as":
            mask[i] = 1
            mask[i-1]=1
    return mask

grammardict["As though"] = as_though
grammardict["As if"] = as_if

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/always

def always_doing(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 1 and x.tag_=="VBG" and a[i-1].lower_=="always" and a[i-2].lemma_=="be":
            mask[i] = 1
            mask[i-1]=1
            mask[i-2]=1
    return mask

# overwrite always and normal present

def can_always(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="always" and a[i-1].lemma_ in ["can", "could"]:
            mask[i] = 1
            mask[i-1]=1
    return mask

def as_always(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="always" and a[i-1].lower_=="as":
            mask[i] = 1
            mask[i-1]=1
    return mask

def all_the_time(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 1 and x.lower_=="time" and a[i-1].lower_=="the" and a[i-2].lower_=="all":
            mask[i] = 1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["Always doing"] = always_doing
grammardict["Can always"] = can_always
grammardict["As always"] = as_always
grammardict["All the time"] = all_the_time

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/amount-of-number-of-or-quantity-of

def amount_of(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_=="of" and a[i-1].lower_=="amount" and "NOUN" in [y.pos_ for y in x.subtree]:
            mask[i] = 1
            mask[i-1]=1
            for y in x.subtree:
                if y.pos_=="NOUN": mask[y.i]=1
    return mask

def number_of(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="of" and a[i-1].lower_=="number" and "NOUN" in [y.pos_ for y in x.subtree]:
            mask[i] = 1
            mask[i-1]=1
            for y in x.subtree:
                if y.pos_=="NOUN": mask[y.i]=1
    return mask

def quantity_of(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="of" and a[i-1].lower_=="quantity" and "NOUN" in [y.pos_ for y in x.subtree]:
            mask[i] = 1
            mask[i-1]=1
            for y in x.subtree:
                if y.pos_=="NOUN": mask[y.i]=1
    return mask

grammardict["Amount of"] = amount_of
grammardict["Number of"] = number_of
grammardict["Quantity of"] = quantity_of

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/and

def go_and_do(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 1 and x.tag_=="VB" and a[i-1].lower_=="and" and a[i-2].lemma_.lower()=="go":
            mask[i] = 1
            mask[i-1]=1
            mask[i-2]=1
    return mask

def come_and_do(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 1 and x.tag_=="VB" and a[i-1].lower_=="and" and a[i-2].lemma_.lower()=="come":
            mask[i] = 1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["Go and do"] = go_and_do
grammardict["Come and do"] = come_and_do

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/any

def any_det(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if x.lower_=="any" and x.dep_=="det":
            mask[i] = 1
    return mask

grammardict["Any (determiner)"] = any_det
confounders["Any (determiner)"] = (0,)

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/any-more-or-anymore

def any_more_adj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="more" and x.dep_=="amod" and a[i-1].lower_=="any":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def any_more_adv(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="more" and x.dep_=="advmod" and a[i-1].lower_=="any":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def some_more_adj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="more" and x.dep_=="amod" and a[i-1].lower_=="some":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def some_more_adv(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="more" and x.dep_=="advmod" and a[i-1].lower_=="some":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Any more (adjective)"] = any_more_adj
grammardict["Some more (adjective)"] = some_more_adj
grammardict["Any more (adverb)"] = any_more_adv
grammardict["Some more (adverb)"] = some_more_adv

# %%
def anyone_body_thing(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if x.lower_ in ["anyone", "anybody", "anything"]:
            mask[i] = 1
    return mask

grammardict["Anyone / anybody / anything"] = anyone_body_thing
confounders["Anyone / anybody / anything"] = (0,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/anyway

def anyway_discourse(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if x.text=="Anyway" and a[i+1].text==",":
            mask[i] = 1
    return mask

grammardict["Anyway, ... (discourse)"] = anyway_discourse

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/apart-from-or-except-for

def apart_from(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="from" and a[i-1].lower_=="apart":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def except_for(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_=="for" and a[i-1].lower_=="except":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Apart from"] = apart_from
grammardict["Except for"] = except_for

# always override these with phrasals

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/appear

def appear_subject(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if x.lemma_=="appear" and x.pos_=="VERB" and ((a[i+1].lower_=="as" and a[i+2].lower_ in ["if", "though"]) or (a[i+1].lower_=="that")):
            mask[i] = 1
            mask[i+1] = 1
    return mask

grammardict["Appears as if / appears that"] = appear_subject

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/approximations-around-four-o-clock

number_approximations = ["about", "roughly", "almost", "around", "approximately", "as many as", "in the region of", "up to", "at or around"]

def number_approximation(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.pos_=="NUM" and a[i-1].lower_ in number_approximations:
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Number approximation"] = number_approximation

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/as-as

def as_as(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 1 and x.lower_=="as" and a[i-2].lower_=="as" and a[i-1].pos_ in ["ADV", "ADJ"]:
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2]=1
    return mask

def as_much(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ in ["much", "many"] and a[i-1].lower_=="as":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def as_long_as(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 1 and x.lower_=="as" and a[i-2].lower_=="as" and a[i-1].lower_=="long":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2]=1
    return mask

grammardict["As ... as"] = as_as
grammardict["As much / many"] = as_much
grammardict["As long as"] = as_long_as

# overwrite as ... as with as long as 

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/as-if-and-as-though

def as_if_though(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ in ["if", "though"] and a[i-1].lower_=="as":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["As if / as though"] = as_if_though

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/away-and-away-from

def away_from(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ =="from" and a[i-1].lower_=="away":
            mask[i] = 1
            mask[i-1] = 1
            for y in x.subtree:
                if y.dep_=="pobj": mask[y.i]=1
    return mask

grammardict["Preposition: away from"] = away_from

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/at

def at_adj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ == "at" and a[i-1].pos_=="ADJ" and "pcomp" in [y.dep_ for y in x.subtree]:
            mask[i] = 1
            mask[i-1] = 1
    return mask

def at_all(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ == "all" and a[i-1].lower_=="at":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Adjective + at (eg good at)"] = at_adj
grammardict["At all"] = at_all

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/be-expressions-be-able-to-be-due-to

be_expressions = ["about", "able", "due", "likely", "meant", "supposed", "unlikely"]
be_expressions = sorted(list(set(be_expressions)))

def be_exp(a, exp):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_== exp and a[i+1].tag_=="TO" and ((x.head.lemma_ == "be") or ("be" in [y.lemma_ for y in x.subtree])):
            mask[i]=1
            mask[i+1]=1
            mask[x.head.i]=1
    return mask
for exp in be_expressions:
    grammardict["Be " + exp + " to"] = (lambda pre: lambda x: be_exp(x, pre))(exp)

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/because-because-of-and-cos-cos-of

def because_of(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ =="of" and a[i-1].lower_=="because":
            mask[i] = 1
            mask[i-1] = 1
            for y in x.subtree:
                if y.dep_=="pobj": mask[y.i]=1
    return mask

def just_because(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ =="because" and a[i-1].lower_=="just":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Preposition: because of"] = because_of
grammardict["Just because"] = just_because

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/before

def just_before(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ =="before" and a[i-1].lower_=="just":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def shortly_before(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if i > 0 and x.lower_ =="before" and a[i-1].lower_=="shortly":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Just before"] = just_before
grammardict["Shortly before"] = shortly_before

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/between-or-among

def between_and(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
         if x.lower_ =="between" and "and" in [y.text for y in x.subtree] and "pobj" in [y.dep_ for y in x.subtree]:
            mask[i] = 1
            for y in x.subtree:
                if y.text=="and" or y.dep_=="pobj": mask[y.i]=1
    return mask

def among_others(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 1 and x.text == "," and a[i-1].lower_ == "others" and a[i-2].lower_=="among":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
    return mask

def among_other_things(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.text == "," and a[i-1].lower_=="things" and a[i-2].lower_=="other" and a[i-3].lower_=="among":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
            mask[i-3] = 1
    return mask

grammardict["Between . and ."] = between_and
grammardict["Among others, "] = among_others
grammardict["Among other things,"] = among_other_things

# %%
def beyond_belief(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_=="belief" and a[i-1].lower_ == "beyond":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def beyond_doubt(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_=="doubt" and a[i-1].lower_ == "beyond":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Beyond belief"] = beyond_belief
grammardict["Beyond doubt"] = beyond_doubt

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/both

def both_det(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="both" and x.pos_ in ["DET", "PDT"]:
            mask[i] = 1
    return mask

grammardict["Both (determiner)"] = both_det
confounders["Both (determiner)"] = (0,)

# %%
def neither_of(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_=="of" and a[i-1].lower_ == "neither":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["Neither of"] = neither_of

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/but

def and_conj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="and" and x.dep_=="cc":
            mask[i] = 1
    return mask

def but_conj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="but" and x.dep_=="cc":
            mask[i] = 1
    return mask

def or_conj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="or" and x.dep_=="cc":
            mask[i] = 1
    return mask

def but_for(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.lower_=="for" and a[i-1].lower_=="but":
            mask[i] = 1
            mask[i-1]=1
    return mask

def all_but(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.tag_=="VBN" and a[i-1].lower_=="but" and a[i-2].lower_=="all":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
    return mask

def either_or_conj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="either" and x.dep_=="preconj":
            for y in a[i+1:]:
                if y.text==".": break
                if y.lower_=="or" and y.dep_=="cc":
                    mask[i]=1
                    mask[y.i]=1
                    break
    return mask

def neither_nor_conj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="neither":
            for y in a[i+1:]:
                if y.text==".": break
                if y.lower_=="nor" and y.dep_=="cc":
                    mask[i]=1
                    mask[y.i]=1
                    break
    return mask

def both_and_conj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="both":
            for y in a[i+1:]:
                if y.text=="." or y.pos_=="VERB": break
                if y.lower_=="and" and y.dep_=="cc":
                    mask[i]=1
                    mask[y.i]=1
                    break
    return mask

grammardict["and (conjunction)"] = and_conj
grammardict["but (conjunction)"] = but_conj
grammardict["but for"] = but_for
grammardict["all but"] = all_but
grammardict["or (conjuction)"] = or_conj
grammardict["either ... or ..."] = either_or_conj
grammardict["neither ... nor ..."] = neither_nor_conj
grammardict["both ... and ..."] = both_and_conj

for z in ["and (conjuction)", "but (conjuction)", "or (conjuction)"]:
    confounders[z] = (0,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/by

def by_day_night(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["day", "night"] and a[i-1].lower_=="by":
            mask[i] = 1
            mask[i-1] = 1
    return mask

grammardict["by day / by night"] = by_day_night

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/can

def can(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_.lower()=="can" and x.pos_=="VERB" and x.head.pos_=="VERB":
            mask[i]=1
            mask[x.head.i]=1
    return mask

def can_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if (i > 0 and x.lower_=="n't" and a[i-1].lower_=="ca"):
            mask[i]=1
            mask[x.head.i]=1
        elif x.lower_=="cannot":
            mask[i] =1
    return mask

# trivial overriding to be done here

grammardict["can (ability)"] = can
grammardict["can (negative)"] = can_negative

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/commands-and-instructions

def command_positive(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.dep_ in ["ROOT", "advcl"] and x.tag_ == "VB" and ((i > 0 and a[i-1].text in [".", "'", "\""]) or (i==0)):
            mask[i] = 1
    return mask

def command_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 1 and x.tag_ == "VB" and a[i-1].lower_ in ["n't", "not"] and a[i-2].lower_ == "do" and ((i > 2 and a[i-1].text in [".", "'", "\""]) or (i==2)):
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
    return mask

def just_command(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and (i==1 or a[i-2].is_punct) and a[i-1].lower_=="just" and x.dep_ in ["ROOT", "advcl"] and x.tag_ == "VB":
            mask[i] = 1
    return mask

grammardict["command (positive)"] = command_positive
grammardict["command (negative)"] = command_negative
grammardict["Just + command"] = just_command

# %%
comparative_modifiers = ["more", "less", "fewer"]
superlative_modifiers = ["most", "least"]

def comparative_form(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.pos_ in ["ADJ", "ADV"] and a[i-1].lower_ in comparative_modifiers:
            mask[i] = 1
            mask[i-1] = 1
        elif x.tag_ in ["JJR", "RBR"] and x.lower_ not in comparative_modifiers:
            mask[i] = 1
    return mask


def superlative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.pos_=="ADJ" and a[i-1].lower_ in superlative_modifiers:
            mask[i] = 1
            mask[i-1] = 1
        if x.tag_ in ["JJS", "RBS"] and x.lower_ not in superlative_modifiers:
            mask[i] = 1
    return mask

# irregular comparatives + superlatives

def better(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="better" and x.tag_=="JJR":
            mask[i] = 1
    return mask

def best(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="best" and x.tag_=="JJS":
            mask[i] = 1
    return mask

def worse(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="worse" and x.tag_=="JJR":
            mask[i] = 1
    return mask

def worst(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="worst" and x.tag_=="JJS":
            mask[i] = 1
    return mask
    

def further(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="further" and x.tag_=="JJR":
            mask[i] = 1
    return mask

    
def furthest(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="furthest" and x.tag_=="JJS":
            mask[i] = 1
    return mask

def much_comparative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 1 and x.pos_ in ["ADJ", "ADV"] and a[i-1].lower_ in comparative_modifiers and a[i-2].lower_=="much":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
        elif i>0 and x.tag_ in ["JJR", "RBR"] and a[i-1].lower_=="much":
            mask[i] = 1
            mask[i-1] = 1
    return mask

def a_lot_comparative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.pos_ in ["ADJ", "ADV"] and a[i-1].lower_ in comparative_modifiers and a[i-2].lower_=="lot" and a[i-3].lower=="a":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
            mask[i-3] = 1
        elif i>0 and x.tag_ in ["JJR", "RBR"] and a[i-1].lower_=="lot" and a[i-2].lower_=="a":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
    return mask

def er_and_er(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.tag_ in ["JJR", "RBR"] and x.lower_ == a[i-2].lower_ and a[i-1].lower_=="and":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] =1
    return mask

def more_and_more(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>2 and x.pos_ in ["ADJ", "ADV"] and a[i-1].lower_ in comparative_modifiers and a[i-1].lower_==a[i-3].lower_ and a[i-2].lower_=="and":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] =1
            mask[i-3] = 1
    return mask

def by_far_superlative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>2 and x.tag_ in ["JJS", "RBS"] and a[i-1].lower_=="the" and a[i-2].lower_ =="far" and a[i-3].lower_=="by":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] =1
            mask[i-3]=1
    return mask

def easily_superlative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>2 and x.tag_ in ["JJS", "RBS"] and a[i-1].lower_=="the" and a[i-2].lower_ =="easily":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] =1
    return mask

def superlative_of_all(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["JJS", "RBS"] and x.head.pos_=="NOUN" and "of" in [y.lower_ for y in x.head.subtree] and "all" in [y.lower_ for y in x.head.subtree]:
            for y in x.head.subtree:
                if y.i > 0 and y.lower_=="all" and a[y.i - 1].lower_=="of":
                    mask[i]=1
                    mask[y.i]=1
                    mask[y.i-1]=1
    return mask

def superlative_infinitive(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["JJS", "RBS"] and x.head.pos_=="NOUN" and "TO" in [y.tag_ for y in x.head.subtree]:
            for y in x.head.subtree:
                if y.tag_=="TO":
                    mask[i]=1
                    mask[y.i]=1
                    mask[y.head.i]=1
    return mask

def the_er_the_er(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.tag_ in ["JJR", "RBR"] and a[i-1].lower_=="the" and x.head.lemma_=="be" and x.head.dep_=="ccomp" and (("RBR" in [y.tag_ for y in x.head.head.subtree]) or ("JJR" in [y.tag_ for y in x.head.head.subtree])):
            for y in x.head.head.subtree:
                if y.i > 0 and y.i != x.i and y.tag_ in ["JJR", "RBR"] and a[y.i - 1].lower_=="the":
                    mask[i]=1
                    mask[i-1]=1
                    mask[y.i]=1
                    mask[y.i - 1]=1
    return mask
# obvious overrides to look at

noun_comparatives = ["more", "less", "fewer"]

def comparative_noun(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.pos_=="NOUN" and a[i-1].lower_ in noun_comparatives:
            mask[i]=1
            mask[i-1]=1
    return mask

grammardict["Comparative form"] = comparative_form
grammardict["Superlative"] = superlative

confounders["Comparative form"] = (0,)
confounders["Superlative"] = (0,)

grammardict["better"] = better
grammardict["best"] = best
grammardict["worse"] = worse
grammardict["worst"] = worst
grammardict["further"] = further
grammardict["furthest"] = furthest
grammardict["much + comparative"] = much_comparative
grammardict["a lot + comparative"] = a_lot_comparative
grammardict["-er and -er"] = er_and_er
grammardict["more and more (etc)"] = more_and_more
grammardict["by far superlative"] = by_far_superlative
grammardict["easily superlative"] = easily_superlative
grammardict["superlative of all"] = superlative_of_all
grammardict["superlative + infinitive"] = superlative_infinitive
grammardict["the -er, the -er"] = the_er_the_er
grammardict["comparative noun"] = comparative_noun

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/conditionals-if

def zero_conditional(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["VBP", "VBZ"] and ("if" in [y.lower_ for y in list(x.subtree)]) and ('VBP' in [y.tag_ for y in list(x.subtree)] or 'VBZ' in [y.tag_ for y in list(x.subtree)]):
            for k in list(x.subtree):
                if (k.tag_ in ["VBP", "VBZ"] and "if" in [x.lower_ for x in list(k.subtree)]):
                    mask[i] = 1
                    mask[k.i] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "if": mask[l.i]=1
    return mask

def first_conditional(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["VB"] and ("if" in [y.lower_ for y in list(x.subtree)]) and ("will" in [y.lower_ for y in list(x.subtree)] or "'ll" in [y.lower_ for y in list(x.subtree)]) and ('VBP' in [y.tag_ for y in list(x.subtree)] or 'VBZ' in [y.tag_ for y in list(x.subtree)]):
            for k in list(x.subtree):
                if (k.tag_ in ["VBP", "VBZ"] and "if" in [x.lower_ for x in list(k.subtree)]):
                    mask[i] = 1
                    mask[k.i] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "if": mask[l.i]=1
                elif k.lower_ in ["will", "'ll"]:
                    mask[k.i] = 1
    return mask


def second_conditional(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.head.tag_ in ["VB"] and x.lower_ in ["'d", "would"] and ("if" in [y.lower_ for y in list(x.head.subtree)]) and ('VBD' in [y.tag_ for y in list(x.head.subtree)]):
            for k in list(x.head.subtree):
                if (k.tag_ in ["VBD"] and "if" in [y.lower_ for y in list(k.subtree)]):
                    mask[i] = 1
                    mask[x.head.i]
                    mask[k.i] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "if": mask[l.i]=1
    return mask

def third_conditional(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["VBN"] and (i > 2) and a[i-1].lower_ in ["'ve", "have"] and (a[i-2].tag_=="MD" or a[i-2].lemma_=="would") and ("if" in [y.lower_ for y in list(x.subtree)]) and ('VBN' in [y.tag_ for y in list(x.subtree)]):
            for k in list(x.subtree):
                if (k.tag_ in ["VBN"] and a[k.i -1].lower_ in ["had", "'d"] and "if" in [y.lower_ for y in list(k.subtree)]):
                    mask[i-2]=1
                    mask[i-1] = 1
                    mask[i] = 1
                    mask[k.i] = 1
                    mask[k.i-1] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "if": mask[l.i]=1
    return mask

def zero_conditional_unless(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["VBP", "VBZ"] and ("unless" in [y.lower_ for y in list(x.subtree)]) and ('VBP' in [y.tag_ for y in list(x.subtree)] or 'VBZ' in [y.tag_ for y in list(x.subtree)]):
            for k in list(x.subtree):
                if (k.tag_ in ["VBP", "VBZ"] and "unless" in [x.lower_ for x in list(k.subtree)]):
                    mask[i] = 1
                    mask[k.i] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "unless": mask[l.i]=1
    return mask

def first_conditional_unless(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["VB"] and ("unless" in [y.lower_ for y in list(x.subtree)]) and ("will" in [y.lower_ for y in list(x.subtree)] or "'ll" in [y.lower_ for y in list(x.subtree)]) and ('VBP' in [y.tag_ for y in list(x.subtree)] or 'VBZ' in [y.tag_ for y in list(x.subtree)]):
            for k in list(x.subtree):
                if (k.tag_ in ["VBP", "VBZ"] and "unless" in [x.lower_ for x in list(k.subtree)]):
                    mask[i] = 1
                    mask[k.i] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "unless": mask[l.i]=1
                elif k.lower_ in ["will", "'ll"]:
                    mask[k.i] = 1
    return mask


def second_conditional_unless(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.head.tag_ in ["VB"] and x.lower_ in ["'d", "would"] and ("unless" in [y.lower_ for y in list(x.head.subtree)]) and ('VBD' in [y.tag_ for y in list(x.head.subtree)]):
            for k in list(x.head.subtree):
                if (k.tag_ in ["VBD"] and "unless" in [y.lower_ for y in list(k.subtree)]):
                    mask[i] = 1
                    mask[x.head.i]
                    mask[k.i] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "unless": mask[l.i]=1
    return mask

def third_conditional_unless(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["VBN"] and (i > 2) and a[i-1].lower_ in ["'ve", "have"] and a[i-2].tag_=="MD" and ("unless" in [y.lower_ for y in list(x.subtree)]) and ('VBN' in [y.tag_ for y in list(x.subtree)]):
            for k in list(x.subtree):
                if (k.tag_ in ["VBN"] and a[k.i -1].lower_ in ["had", "'d"] and "unless" in [y.lower_ for y in list(k.subtree)]):
                    mask[i-2]=1
                    mask[i-1] = 1
                    mask[i] = 1
                    mask[k.i] = 1
                    mask[k.i-1] = 1
                    for l in list(k.subtree):
                        if l.lower_ == "unless": mask[l.i]=1
    return mask


def if_should(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="if":
            for y in a[i:]:
                if y.pos_=="VERB" and y.lower_ != "should":
                    break
                if y.lower_=="should":
                    mask[i]=1
                    mask[y.i]=1
                    break
    return mask

def should_you(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="should":
            print("henlo")
            for y in a[i+1:]:
                if y.pos_=="VERB": 
                    if y.tag_ != "VB": 
                        break
                    else:
                        mask[i] = 1
                        mask[y.i]=1
                        break
                    
    return mask

def should_you(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="should":
            for y in a[i+1:]:
                if y.pos_=="VERB": 
                    if y.tag_ != "VB": 
                        break
                    else:
                        if "nsubj" in [z.dep_ for z in a[i:y.i]]:
                            mask[i] = 1
                            mask[y.i]=1
                            break
                    
    return mask

def had_you(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="had":
            for y in a[i+1:]:
                if y.pos_=="VERB": 
                    if y.tag_ in ["VBN", "VBD"] and "nsubj" in [z.dep_ for z in a[i:y.i]]: 
                        mask[i] = 1
                        mask[y.i]=1
                        break
                    else:
                        break
                    
    return mask

grammardict["Zero conditional"] = zero_conditional
grammardict["First conditional"] = first_conditional
grammardict["Second conditional"] = second_conditional
grammardict["Third conditional"] = third_conditional
grammardict["If you should..."] = if_should
grammardict["Zero conditional unless"] = zero_conditional_unless
grammardict["First conditional unless"] = first_conditional_unless
grammardict["Second conditional unless"] = second_conditional_unless
grammardict["Third conditional unless"] = third_conditional_unless
grammardict["Should you"] = should_you
grammardict["Had you"] = had_you

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/conjunctions-adding

def in_addition_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 1 and x.lower_=="to" and a[i-1].lower_=="addition" and a[i-2].lower_=="in":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["In addition to"] = in_addition_to

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/conjunctions-causes-reasons-results-and-purpose

def so(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="so" and x.dep_=="mark":
            mask[i]=1
    return mask

def so_that(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.lower_=="that" and a[i-1].lower_=="so" and a[i-1].dep_=="mark":
            mask[i]=1
            mask[i-1]=1
    return mask

def in_order_that(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.lower_=="that" and a[i-1].lower_=="order" and a[i-2].lower_=="in":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["So (conj)"] = so
confounders["So (conj)"] = (0,)
grammardict["So that"] = so_that
grammardict["In order that"] = in_order_that

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/conjunctions-contrasting

def even_though(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.lower_=="though" and a[i-1].lower_=="even":
            mask[i]=1
            mask[i-1]=1
    return mask

def even_if(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.lower_=="if" and a[i-1].lower_=="even":
            mask[i]=1
            mask[i-1]=1
    return mask

grammardict["Even though"] = even_though
grammardict["Even if"] = even_if

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/conjunctions-time

def as_soon_as(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.lower_=="as" and a[i-1].lower_=="soon" and a[i-2].lower_=="as":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["As soon as"] = as_soon_as

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/contrasts

def on_one_hand_other_hand(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>2 and x.lower_=="hand" and a[i-1].lower_=="one" and a[i-2].lower_=="the" and a[i-3].lower_=="on":
            for y in a[i+1:]:
                if y.lower_=="hand" and a[y.i-1].lower_=="other" and a[y.i-2].lower_=="the" and a[y.i-3].lower_=="on":
                    mask[i]=1
                    mask[i-1]=1
                    mask[i-2]=1
                    mask[i-3]=1
                    mask[y.i]=1
                    mask[y.i-1]=1
                    mask[y.i-2]=1
                    mask[y.i-3]=1

    return mask

def on_the_other_hand(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>2 and x.lower_=="hand" and a[i-1].lower_=="other" and a[i-2].lower_=="the" and a[i-3].lower_=="on":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
            mask[i-3]=1

    return mask

def on_the_contrary(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.lower_=="contrary" and a[i-1].lower_=="the" and a[i-2].lower_=="on":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1

    return mask


grammardict["On the one hand ... on the other hand"] = on_one_hand_other_hand
grammardict["On the other hand"] = on_the_other_hand
grammardict["On the contrary"] = on_the_contrary

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/could

def could_affirmative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.tag_ == "VB" and a[i-1].lower_ in ["could"]:
            mask[i] = 1
            mask[i-1] = 1
    return mask

def could_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 1 and x.tag_ == "VB" and a[i-1].lower_ in ["n't", "not"] and a[i-2].lower_ == "could":
            mask[i] = 1
            mask[i-1] = 1
            mask[i-2] = 1
    return mask

def could_have(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="could" and x.head.tag_=="VBN" and a[x.head.i-1].lower_=="have":
            mask[i] = 1
            mask[x.head.i]=1
            mask[x.head.i-1]=1
    return mask

grammardict["Could (affirmative)"] = could_affirmative
grammardict["Could (negative)"] = could_negative
grammardict["Could have"] = could_have

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/discourse-markers-so-right-okay

disc_marker = ["So ,", "Anyway ,", "Firstly ,", "Secondly ,", "In addition ,", "Moreover ,", "In conclusion ,", "In sum ,"]

for disc in disc_marker:
    grammardict[disc + " ... (discourse marker)"] = structureless_phrase(disc)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/do

def do_emphatic(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and i < len(a) - 1 and x.lemma_=="do" and a[i+1].dep_ != "neg" and (not a[i+1].is_punct) and x.head.pos_ in ["VERB", "INTJ"] and ("dobj" not in [y.dep_ for y in x.subtree]):
            mask[i]=1
            mask[x.head.i]=1
    return mask

# override the question and irregular verb stuff

grammardict["Do (emphatic)"] = do_emphatic

# %%
def do_noun(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_=="do" and "dobj" in [y.dep_ for y in x.subtree]:
            mask[i]=1
            for y in x.subtree:
                if y.head == x and y.dep_=="dobj":
                    mask[y.i]=1
    return mask

grammardict["Do + noun"] = do_noun

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/dummy-subjects

def there_is(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="there" and x.tag_=="EX" and x.head.lemma_=="be":
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["There is / there are"] = there_is

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/downtoners

def a_little(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i> 0 and x.lower_=="little" and x.dep_=="npadvmod" and a[i-1].lower_=="a":
            mask[i]=1
            mask[i-1]=1
    return mask

def only_just(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and  x.lower_=="just" and x.dep_ in ["npadvmod", "advmod"] and a[i-1].lower_=="only":
            mask[i]=1
            mask[i-1]=1
    return mask

grammardict["A little (downtoner)"] = a_little
grammardict["Only just (downtoner)"] = only_just

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/each

grammardict["Each of"] = structureless_phrase("each of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/each-other-one-another

grammardict["Each other"] = structureless_phrase("each other")
grammardict["One another"] = structureless_phrase("one another")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/either

grammardict["Either of"] = structureless_phrase("either of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/else

else_words = ["anybody", "anyone", "anywhere", "everybody", "everyone", "everywhere", "nobody", "no one", "nowhere", "somebody", "somewhere", "someone"]

def anything_else(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_=="else" and a[i-1].lower_ in else_words:
            mask[i]=1
            mask[i-1]=1
    return mask

def wh_else(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.lower_=="else" and a[i-1].tag_ in ["WRB", "WP"]:
            mask[i]=1
            mask[i-1]=1
    return mask

grammardict["Anything else / ... else"] = anything_else
grammardict["Who else / ..."] = wh_else

grammardict["Or else"] = structureless_phrase("or else")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/enough

grammardict["Enough of"] = structureless_phrase("enough of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/even

grammardict["Even so"] = structureless_phrase("even so")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/ever

grammardict["Ever so"] = structureless_phrase("ever so")
grammardict["Ever such"] = structureless_phrase("ever such")

def as_as_ever(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.pos_ in ["ADJ", "ADV"] and a[i-1].lower_=="as" and "ever" in [y.lower_ for y in x.subtree]:
            for y in x.subtree:
                if y.lower_=="ever" and y.i > 0 and a[y.i-1].lower_=="as":
                    mask[y.i]=1
                    mask[i]=1
                    mask[i-1]=1
                    mask[y.i-1]=1
    return mask

grammardict["As ... as ever"] = as_as_ever

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/exclamations

def exclamation_what(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if (i == 0 or a[i-1].is_punct) and x.lower_=="what":
            for j in a[i:]:
                if j.is_punct:
                    if j.text == "!":
                        mask[i]=1
                        mask[j.i]=1
                        break
                    else:
                        break
    return mask

def exclamation_how(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if (i == 0 or a[i-1].is_punct) and x.lower_=="how":
            for j in a[i:]:
                if j.is_punct:
                    if j.text == "!":
                        mask[i]=1
                        mask[j.i]=1
                        break
                    else:
                        break
    return mask


grammardict["What ... ! (exclamation)"] = exclamation_what
grammardict["How ... ! (exclamation)"] = exclamation_how

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/far-or-a-long-way

grammardict["A long way"] = structureless_phrase("a long way")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/finally-at-last-lastly-or-in-the-end

grammardict["At last"] = structureless_phrase("at last")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/finally-at-last-lastly-or-in-the-end

grammardict["In the end"] = structureless_phrase("in the end")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/first-firstly-or-at-first

grammardict["At first"] = structureless_phrase("at first")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/following-or-the-following

grammardict["The following"] = structureless_phrase("the following")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/from

def from_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="from":
            for y in a[i+1:]:
                if y.lower_=="to" and y.dep_=="prep":
                    mask[i]=1
                    for z in x.subtree:
                        if z.dep_=="pobj": mask[z.i]=1
                    mask[y.i]=1
                    for z in y.subtree:
                        if z.dep_=="pobj": mask[z.i]=1
                if y not in x.subtree or y.pos_=="VERB":
                    break
    return mask

grammardict["From ... to ..."] = from_to

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/now

grammardict["Right now"] = structureless_phrase("right now")
grammardict["Just now"] = structureless_phrase("just now")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/future-continuous-i-will-be-working

def future_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["will", "'ll", "wo"] and x.head.tag_=="VBG" and ("be" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_=="be": mask[y.i]=1
    return mask

grammardict["Future continuous"] = future_continuous
confounders["Future continuous"] = (0, ["Future simple"])

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/future-perfect-continuous-i-will-have-been-working-here-ten-years

def future_perfect_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["will", "'ll", "wo"] and x.head.tag_=="VBG" and ("have" in [y.lower_ for y in x.head.subtree]) and ("been" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_ in ["have", "been"]: mask[y.i]=1
    return mask

grammardict["Future perfect continuous"] = future_perfect_continuous
confounders["Future perfect continuous"] = (0,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/future-perfect-simple-i-will-have-worked-eight-hours

def future_perfect(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["will", "'ll", "wo"] and x.head.tag_=="VBN" and ("have" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_ == "have": mask[y.i]=1
    return mask

grammardict["Future perfect"] = future_perfect
confounders["Future perfect"] = (0,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/future-be-going-to-i-am-going-to-work

def be_going_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.tag_=="VB" and a[i-1].tag_=="TO" and a[i-2].lower_=="going" and a[i-3].lemma_=="be":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
            mask[i-3]=1
    return mask

grammardict["Be going to (future)"] = be_going_to

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/future-will-and-shall

def future_simple(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["will", "'ll", "wo"] and x.pos_ == "VERB" and x.tag_ == "MD":
            mask[i] = 1
            mask[x.head.i]=1
    return mask

grammardict["Future simple"] = future_simple
confounders["Future simple"] = (0,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/get

def get_adj(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_=="get" and "ADJ" in [y.pos_ for y in x.subtree]:
            for y in x.subtree:
                if y.pos_=="ADJ" and y.head==x:
                    mask[i]=1
                    mask[y.i]=1
    return mask

def got_event(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="got" and x.head.tag_=="VBN" and x.head != x:
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Get + adjective"] = get_adj
grammardict["Got + event"] = got_event

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/had-better

def had_better(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.lower_=="better" and a[i-1].lower_ in ["had", "'d"] and x.head.tag_=="VB":
            mask[i]=1
            mask[x.head.i]=1
            mask[i-1]=1
    return mask

grammardict["Had better"] = had_better

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/hardly-ever-rarely-scarcely-seldom

grammardict["Hardly ever"] = structureless_phrase("hardly ever")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/have-got-and-have

def have_got(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_=="have" and x.pos_=="AUX" and x.head.lemma_=="get":
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Have got"] = have_got

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/here-and-there

grammardict["Around here"] = structureless_phrase("around here")
grammardict["Over there"] = structureless_phrase("over there")
grammardict["In here"] = structureless_phrase("in here")
grammardict["here you are"] = structureless_phrase("here you are")
grammardict["there you go"] = structureless_phrase("there you go")

def here_it_is(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.is_punct and a[i-1].lower_ in ["is", "am", "are"] and a[i-3].lower_=="here":
            mask[i-3]=1
            mask[i-1]=1
    return mask

grammardict["Here it is"] = here_it_is

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/how

def how_extent(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.pos_ in ["ADJ", "ADV"] and a[i-1].lower_=="how":
            mask[i]=1
            mask[i-1]=1
    return mask

grammardict["How: extent"] = how_extent

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/how-is-or-what-is-like

def how_condition(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.lemma_=="be" and a[i-1].lower_=="how":
            mask[i]=1
            mask[i-1]=1
    return mask

def what_is_like_question(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>0 and x.lemma_=="be" and a[i-1].lower_=="what":
            for t,j in enumerate(a[i+1:]):
                if j.text=="?" and a[i+t].lower_=="like":
                    mask[i]=1
                    mask[i-1]=1
                    mask[j.i]=1
                    mask[j.i - 1]=1
    return mask

grammardict["How: condition"] = how_condition
grammardict["What is ... like?"] = what_is_like_question

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/how-is-or-what-is-like

def ever_pronoun(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["however", "whatever", "whichever", "whenever", "wherever", "whoever"]:
            mask[i]=1
    return mask

grammardict["Ever pronoun"] = ever_pronoun
confounders["Ever pronoun"] = (0,)

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/if

grammardict["If possible"] = structureless_phrase("if possible")
grammardict["If necessary"] = structureless_phrase("if necessary")
grammardict["If so"] = structureless_phrase("if so")
grammardict["Even if"] = structureless_phrase("even if")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/if-only

grammardict["If only"] = structureless_phrase("if only")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/in-fact

grammardict["In fact"] = structureless_phrase("in fact")

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/imperative-clauses-be-quiet

def lets(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.tag_=="VB" and a[i-1].lower_=="'s" and a[i-2].lower_=="let":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
    return mask

def lets_not(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>2 and x.tag_=="VB" and a[i-1].dep_=="neg" and a[i-2].lower_=="'s" and a[i-3].lower_=="let":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
            mask[i-3]=1
    return mask

grammardict["Let's"] = lets
grammardict["Let's not"] = lets_not

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/in-case-of

grammardict["In case"] = structureless_phrase("in case")
grammardict["In case of"] = structureless_phrase("in case of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/in-front-of

grammardict["In front of"] = structureless_phrase("in front of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/in-order-to

def in_order_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 1 and x.lower_=="to" and a[i-1].lower_=="order" and a[i-2].lower_=="in" and x.head.dep_=="acl":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
            mask[x.head.i]=1
    return mask

def in_order_not_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 2 and x.lower_=="to" and a[i-1].lower_=="not" and a[i-2].lower_=="order" and a[i-3].lower_=="in" and x.head.dep_=="acl":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
            mask[i-3]=1
            mask[x.head.i]=1
    return mask
grammardict["In order to"] = in_order_to
grammardict["In order not to"] = in_order_not_to

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/in-spite-of-and-despite

grammardict["In spite of"] = structureless_phrase("in spite of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/in-the-way-or-on-the-way

grammardict["In the way"] = structureless_phrase("in the way")
grammardict["On the way"] = structureless_phrase("on the way")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/invitations

def would_like(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_.lower()=="would" and x.head.lower_=="like":
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Would like"] = would_like

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/it-s-time

grammardict["It's time"] = structureless_phrase("it 's time")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/kind-of-and-sort-of

grammardict["Kind of"] = structureless_phrase("kind of")
grammardict["Sort of"] = structureless_phrase("sort of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/long

grammardict["No longer"] = structureless_phrase("no longer")

# %%
# # https://dictionary.cambridge.org/grammar/british-grammar/long

def look_forward_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.lower_=="to" and a[i-1].lower_=="forward" and a[i-2].lemma_=="look":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["Look forward to"] = look_forward_to

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/lots-a-lot-plenty

grammardict["lots of"] = structureless_phrase("lots of")
grammardict["a lot of"] = structureless_phrase("a lot of")
grammardict["plenty of"] = structureless_phrase("plenty of")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/many

grammardict["As many as"] = structureless_phrase("as many as")

# %%
#https://dictionary.cambridge.org/grammar/british-grammar/matter

def doesnt_matter(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_.lower() in ["do", "would"] and x.head.lower_=="matter":
            mask[i]=1
            mask[x.head.i]=1
    return mask

def it_matters_to(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.lower_=="to" and a[i-1].lower_=="matters" and "it" in [y.lower_ for y in a[i-1].subtree]:
            for y in a[i-1].subtree:
                if y.lower_=="it" and y.head==a[i-1]:
                    mask[i]=1
                    mask[i-1]=1
                    mask[y.i]=1
    return mask

def whats_the_matter(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.lower_=="matter" and a[i-1].lower_=="the" and a[i-2].lower_=="'s":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
            for y in x.subtree:
                if y.lower_=="with": mask[y.i]=1
    return mask

def no_matter(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i>1 and x.tag_ in ["WP", "WRB"] and a[i-1].lower_=="matter" and a[i-2].lower_=="no":
            mask[i]=1
            mask[i-1]=1
            mask[i-2]=1
    return mask

grammardict["As a matter of fact"] = structureless_phrase("as a matter of fact")


grammardict["Doesn't matter"] = doesnt_matter
grammardict["It matters to"] = it_matters_to
grammardict["What's the matter"] = whats_the_matter

grammardict["No matter what"] = no_matter

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/may

def may(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="may" and x.pos_=="VERB" and x.head.pos_ in ["VERB", "AUX"]:
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["May (affirmative)"] = may

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/may

def may_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i> 0 and x.dep_=="neg" and a[i-1].lower_=="may" and a[i-1].pos_=="VERB" and a[i-1].head.pos_ in ["VERB", "AUX"]:
            mask[i]=1
            mask[i-1]=1
            mask[a[i-1].head.i]=1
    return mask

grammardict["May as well"] = structureless_phrase("May as well")
grammardict["Might as well"] = structureless_phrase("Might as well")
grammardict["May just as well"] = structureless_phrase("May just as well")
grammardict["Might just as well"] = structureless_phrase("Might just as well")

grammardict["May (negative)"] = may_negative

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/might

def might(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="might" and x.pos_=="VERB" and x.head.pos_ in ["VERB", "AUX"]:
            mask[i]=1
            mask[x.head.i]=1
    return mask

def might_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i> 0 and x.dep_=="neg" and a[i-1].lower_=="might" and a[i-1].pos_=="VERB" and a[i-1].head.pos_ in ["VERB", "AUX"]:
            mask[i]=1
            mask[i-1]=1
            mask[a[i-1].head.i]=1
    return mask

grammardict["Might (negative)"] = might_negative
grammardict["Might"] = might

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/mind

def dont_mind(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_.lower() in ["do", "would"] and x.head.lower_=="mind":
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Don't mind"] = dont_mind

grammardict["Never mind"] = structureless_phrase("never mind")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/more-or-less

grammardict["More or less"] = structureless_phrase("more or less")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/much-a-lot-lots-a-good-deal-adverbs

grammardict["Too much"] = structureless_phrase("too much")
grammardict["So much"] = structureless_phrase("so much")
grammardict["A lot"] = structureless_phrase("a lot")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/must

def must(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="must" and x.pos_=="VERB" and x.head.pos_ in ["VERB", "AUX"]:
            mask[i]=1
            mask[x.head.i]=1
    return mask

def must_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i> 0 and x.dep_=="neg" and a[i-1].lower_=="may" and a[i-1].pos_=="VERB" and a[i-1].head.pos_ in ["VERB", "AUX"]:
            mask[i]=1
            mask[i-1]=1
            mask[a[i-1].head.i]=1
    return mask


grammardict["Must"] = must
grammardict["Must negative"] = must_negative

# %%
def by_agent(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="by" and x.dep_=="agent":
            mask[i]=1
    return mask

grammardict["By (agent)"] = by_agent

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/need

def need(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_=="need" and x.pos_=="VERB" and x.head.pos_ in ["VERB", "AUX"]:
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Need (affirmative)"] = need

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/next

grammardict["Next to"] = structureless_phrase("next to")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/no-doubt-or-without-doubt

grammardict["No doubt"] = structureless_phrase("no doubt")
grammardict["Without doubt"] = structureless_phrase("without doubt")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/no-more-not-any-more

grammardict["No more"] = structureless_phrase("no more")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/no-sooner

grammardict["No sooner"] = structureless_phrase("no sooner")

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/no-none-and-none-of

grammardict["None of"] = structureless_phrase("none of")

# %%
def not_only_but_also(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i> 0 and x.lower_=="only" and a[i-1].lower_=="not" and a[i-1].dep_=="preconj":
            for y in a[i+1:]:
                if y.text==".": break
                if y.lower_=="but" and y.dep_=="cc":
                    mask[i]=1
                    mask[y.i]=1
                    break
    return mask

grammardict["Not only ... but (also)"] = not_only_but_also

# %%
grammardict["Now that"] = structureless_phrase("now that")

# %%
def cardinal_no(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_=="CD":
            mask[i]=1
    return mask

grammardict["Number (cardinal)"] = cardinal_no

# %%
# https://dictionary.cambridge.org/grammar/british-grammar/of-course

grammardict["Of course"] = structureless_phrase("of course")

# %%
grammardict["Out of"] = structureless_phrase("out of")

# %%
grammardict["All over"] = structureless_phrase("all over")

# %%
grammardict["So far"] = structureless_phrase("so far")

# %%
def present_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["am", "are", "is", "'m", "'s", "'re"] and x.head.tag_ == "VBG":
            mask[i] = 1
            mask[x.head.i] = 1
        elif x.lower_=="'s" and x.head.head.tag_=="VBG":
            mask[i]=1
            mask[x.head.head.i]=1
    return mask

grammardict["Present continuous"] = present_continuous
confounders["Present continuous"] = (0,)

# %%
def present_perfect_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["have", "has", "'ve", "'s"] and x.head.tag_=="VBG" and ("been" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_=="been": mask[y.i]=1
    return mask

grammardict["Present perfect continuous"] = present_perfect_continuous
confounders["Present perfect continuous"] = (0,)

# confounder: present_continuous

# %%
def present_perfect(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["have", "has", "'ve", "'s"] and x.head.tag_=="VBN":
            mask[i] = 1
            mask[x.head.i] = 1
    return mask

grammardict["Present perfect"] = present_perfect
confounders["Present perfect"] = (0,)

# %%
def present_simple(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.pos_ == "VERB" and x.tag_ in ["VBP", "VBZ"] and x.dep_ not in ['aux', 'auxpass']:
            mask[i] = 1
    return mask

grammardict["Present simple"] = present_simple

def present_simple_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i >0 and x.dep_=="neg" and a[i-1].lower_ in ["do", "does"] and a[i-1].head.tag_=="VB":
            mask[i] = 1
            mask[i-1]=1
            mask[a[i-1].head.i]=1
    return mask

grammardict["Present simple negative"] = present_simple_negative

def present_simple_question(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["do", "does"] and x.head.tag_=="VB" and "?" in [y.text for y in x.head.subtree]:
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Present simple question"] = present_simple_question

for z in ["Present simple", "Present simple negative", "Present simple question"]:
    confounders[z] = (0,)

# %%
def past_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["was", "were"] and x.head.tag_ == "VBG":
            mask[i] = 1
            mask[x.head.i] = 1
    return mask

def past_perfect_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["had", "'d"] and x.head.tag_=="VBG" and ("been" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_=="been": mask[y.i]=1
    return mask

def past_perfect(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["had", "'d"] and x.head.tag_ == "VBN":
            mask[i] = 1
            mask[x.head.i] = 1
    return mask

def past_simple(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.pos_ == "VERB" and x.tag_ == "VBD":
            mask[i] = 1
    return mask

def past_simple_negative(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i >0 and x.dep_=="neg" and a[i-1].lower_ in ["did"] and a[i-1].head.tag_=="VB":
            mask[i] = 1
            mask[i-1]=1
            mask[a[i-1].head.i]=1
    return mask


def past_simple_question(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["did"] and x.head.tag_=="VB" and "?" in [y.text for y in x.head.subtree]:
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Past continuous"] = past_continuous
grammardict["Past perfect continuous"] = past_perfect_continuous
grammardict["Past pefect"] = past_perfect
grammardict["Past simple"] = past_simple
grammardict["Past simple question"] = past_simple_question
grammardict["Past simple negative"] = past_simple_negative

for z in ["Past continuous", "Past perfect continuous", "Past perfect", "Past simple", "Past simple question", "Past simple negative"]:
    confounders[z] = (0,)

# %%
def passive_present_simple(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["am", "are", "is", "'m", "'re", "'s"] and x.dep_=="auxpass" and x.head.tag_=="VBN":
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Passive present simple"] = passive_present_simple
confounders["Passive present simple"] = (0,)

def passive_present_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["am", "are", "is", "'m", "'re", "'s"] and x.head.tag_=="VBN" and ("being" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_=="being": mask[y.i]=1
    return mask

grammardict["Passive present continuous"] = passive_present_continuous
confounders["Passive present continuous"] = (0,)

def passive_past_simple(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["were", "was"] and x.head.tag_=="VBN":
            mask[i]=1
            mask[x.head.i]=1
    return mask

grammardict["Passive past simple"] = passive_past_simple
confounders["Passive past simple"] = (0,)

def passive_past_continuous(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["was", "were"] and x.head.tag_=="VBN" and ("being" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_=="being": mask[y.i]=1
    return mask

grammardict["Passive past continuous"] = passive_past_continuous
confounders["Passive past continuous"] = (0,)


def passive_present_perfect(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["has", "have", "'s", "'ve"] and x.head.lower_ != "been" and x.head.tag_=="VBN" and ("been" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree: 
                if y.lower_=="been": mask[y.i]=1
    return mask

grammardict["Passive present perfect"] = passive_present_perfect
confounders["Passive present perfect"] = (0,)

def passive_past_perfect(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["had", "'d"] and x.head.tag_=="VBN" and ("been" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree: 
                if y.lower_=="been": mask[y.i]=1
    return mask

grammardict["Passive past perfect"] = passive_past_perfect
confounders["Passive past perfect"] = (0,)

def passive_future_simple(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["will", "'ll"] and x.head.tag_=="VBN" and ("be" in [y.lower_ for y in x.head.subtree]):
            mask[i]=1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_=="be": mask[y.i]=1
    return mask

grammardict["Passive future simple"] = passive_future_simple
confounders["Passive future simple"] = (0,)

def passive_future_perfect(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ in ["will", "'ll"] and x.head.tag_=="VBN" and ("have" in [y.lower_ for y in x.head.subtree] and "been" in [y.lower_ for y in x.head.subtree]):
            mask[i] = 1
            mask[x.head.i]=1
            for y in x.head.subtree:
                if y.lower_ in ["been", "have"]: mask[y.i]=1
    return mask

grammardict["Passive future perfect"] = passive_future_perfect
confounders["Passive future perfect"] = (0,)

# %%
def proper_noun(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.pos_=="PROPN":
            mask[i]=1
    return mask

grammardict["Proper noun"] = proper_noun

# %%
grammardict["Such as"] = structureless_phrase("such as")

# %%
grammardict["By the time"] = structureless_phrase("by the time")

# %%
grammardict["Just in time"] = structureless_phrase("just in time")

# %%
def direct_question(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.tag_ in ["WRB", "WP"] and x.head.dep_=="ROOT":
            mask[i] = 1
    return mask

grammardict["Direct question"] = direct_question
confounders["Direct question"] = (0,)

# %%
def yes_no_question(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.dep_=="aux" and "?" in [y.text for y in x.head.subtree] and ((i==0) or (a[i-1].is_punct)):
            mask[i] = 1
    return mask

grammardict["Yes/no question"] = yes_no_question

# %%
def infinitive_intention(a):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.pos_ in ["VERB", "AUX"] and a[i-1].lower_=="to" and x.head.pos_=="VERB":
            mask[i]=1
            mask[i-1]=1
            mask[x.head.i]=1
    return mask

grammardict["Infinitive (intention)"] = infinitive_intention

# %%


# %%
"""specific prepositions."""

preps = ['about', 'above', 'against', 'among', 'amongst','across', 'after', 'along', 'alongside', 'as','at', 'around', 'round',
         'before', 'beyond', 'near','over','despite', 'opposite', 'towards', 'onto', 'into','beside', 'like','inside','besides', 'since', 'down', 'behind', 'below', 'beneath', 'by', 'during', 'for', 'from', 'in', 'of', 'on', 'to', 'under', 'with', 'within', 'without', 'except']
preps = sorted(list(set(preps)))
print(preps)

def prep(a, pre):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if (x.lower_==pre) and (x.dep_== "prep") and ("pobj" in [y.dep_ for y in x.subtree]):
            mask[i]=1
            for y in x.subtree:
                if y.dep_=="pobj": mask[y.i]=1
    return mask

for pr in preps:
    grammardict["Preposition: " + pr] = (lambda pre: lambda x: prep(x, pre))(pr)
    confounders["Preposition: " + pr] = (-1,)

# %%
"""specific determiners"""
dets = ["some", "this", "that", "those", "these", "my", "your", "his", "her", "its", "our", "their", "few", "little", "some", "any", "enough",
       "another", "several", "each", 'many',"either", 'other', 'few',"enough", "half"]
dets = sorted(list(set(dets)))
print(dets)

def det(a, dt):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if (x.lower_==dt) and x.tag_ in ["DT", "PDT"]:
            mask[i]=1
    return mask

for dtt in dets:
    grammardict["Determiner: " + dtt] = (lambda pre: lambda x: det(x, pre))(dtt)
    confounders["Determiner: " + dtt] = (0,)

# %%
"""prep/adverb + gerund"""

gerund_preps = ["although", "before", "though", "by", "of", "for"]
gerund_preps = sorted(list(set(gerund_preps)))
                      
def gerund_prep(a, pre):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if i > 0 and x.tag_=="VBG" and a[i-1].lower_==pre:
            mask[i]=1
            mask[i-1]=1
    return mask

for pr in gerund_preps:
    grammardict[pr + " + gerund"] = (lambda pre: lambda x: gerund_prep(x,pre))(pr)
    confounders[pr + " + gerund"] = (-1,)
    
# overwrites normal adverb/prep phrase

# %%
"""specific adverbs."""

adverbs = ['about', 'abroad', 'again', 'afterwards', 'beforehand', 'ago', 'alike', 'back', 'almost', 'already', 'also', 'altogether', 'always', 'anyway', 'around', 'away', 'before', 'below',
           'nearly', 'early', 'so','most', 'outside', 'out', 'never', 'throughout', 'once', 'often', 'nowadays', 'next','only','nearby','much','mostly','perhaps', 'maybe','extremely', 'very', 'highly', 'late', 'lately','largely', 'greatly', 'widely', 'just', 'rather','absolutely', 'completely', 'too', 'totally', 'utterly', 'really', 'inside','first', 'rarely', 'hopefully', 'now', 'scarcely', 'seldom', 'hardly','today','hard', 'half', 'soon','lastly', 'fairly', 'far', 'finally', 'even', 'ever', 'eventually', 'previously', 'especially','enough', 'either','downwards', 'somewhat', 'hardly', 'barely', 'slightly','beyond', 'down','still', 'though', 'tonight', 'beneath', 'besides']
adverbs = sorted(list(set(adverbs)))
print(adverbs)

def adverb(a, adverb):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if (x.dep_ in ["advmod", "npadvmod", "prt"] or (x.pos_=="ADV" and x.dep_=="neg")) and x.lower_==adverb:
            mask[i]=1
    return mask

for adverbb in adverbs:
    grammardict["Adverb: " + adverbb] = (lambda adv: lambda x: adverb(x, adv))(adverbb)
    confounders["Adverb: " + adverbb] = (-1,)

# %%
adverb_clause_starters = ["when", "with", "finally", "inside", "lastly", "after", "during", "even", "that", "because", "as", "if", "until", "while", "whenever", "since", "although", "unless", "before", "supposing", "whether", "once", "now"]
adverb_clause_starters = sorted(list(adverb_clause_starters))

def adverb_clause(a, adverb):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lower_ == adverb and "advcl" in [y.dep_ for y in x.ancestors]:
            mask[i]=1
            for y in x.ancestors:
                if y.dep_=="advcl": mask[y.i]=1
    return mask

for adverbb in adverb_clause_starters:
    grammardict["Adverb clause: " + adverbb] = (lambda adv: lambda x: adverb_clause(x, adv))(adverbb)

# %%
"""Irregular verbs"""

irregular_verbs = ["do", "get", "be", "have"]

def irregular_verb(base):
    def recognise(a):
        mask = np.zeros(len(a))
        for i,x in enumerate(a):
            if x.lemma_==base and x.pos_ in ["VERB", "AUX"]:
                mask[i]=1
        return mask
    
    return lambda x: recognise(x)

for irreg in irregular_verbs:
    grammardict["Irregular verb: "+ irreg] = irregular_verb(irreg)
    confounders["Irregular verb: "+ irreg] = (-1,)

# %%
"""verb + infinitive"""

vfs = ["appear", "ask", "dare", "enable", "have", "need"]
vfs = sorted(list(set(vfs)))

def vf(a, verb):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_==verb and x.pos_ in ["VERB", "AUX"] and a[i+1].tag_=="TO":
            mask[i]=1
            mask[i+1]=1
            mask[a[i+1].head.i]=1
    return mask

for verbb in vfs:
    grammardict[verbb + " + infinitive"] = (lambda verb: lambda a: vf(a, verb))(verbb)
    confounders[verbb + " + infinitive"] = (0,)

# %%
"""verb-object-infinitive"""

vofs = ["permit", "allow", "ask", "consider", "dare", "enable"]
vofs = sorted(list(vofs))

def vof(a, verb):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_ == verb:
            for t,y in enumerate(a[i:]):
                if y.dep_ in ["nsubj", "dobj"] and a[i:][t+1].tag_=="TO": 
                    mask[i]=1
                    mask[y.i]=1
                    mask[y.i + 1]=1
                    mask[a[i:][t+1].head.i]=1
                    break
    return mask

for voff in vofs:
    grammardict[voff + " object and infinitive"] = (lambda vf: lambda x: vof(x, vf))(voff)

# %%
"""verb-object-zero-infinitive"""

vozfs = ["let"]
vozfs = sorted(list(vozfs))

def vozf(a, verb):
    mask = np.zeros(len(a))
    for i,x in enumerate(a):
        if x.lemma_ == verb:
            for t,y in enumerate(a[i:]):
                if y.dep_ in ["nsubj", "dobj"] and a[i:][t+1].tag_=="VB": 
                    mask[i]=1
                    mask[y.i]=1
                    mask[y.i + 1]=1
                    break
    return mask

for vozff in vozfs:
    grammardict[vozff + " object do something"] = (lambda vf: lambda x: vozf(x, vf))(vozff)

# %%
"""phrasals"""
import csv

# load idioms

phrasals = []

with open("phrasal_verbs.csv", newline='') as csvfile:
    idiomreader = csv.reader(csvfile)
    next(idiomreader)
    for row in idiomreader:
        phrasals.append(row[0])

"""phrasals = ["be afraid of", "act against", "advise against", "argue against", "be against", "campaign against", "decide against", "demonstrate against", "discriminate against", "fight against", "go against", "guard against", "protest against", "react against",
           "rebel against", "ask for", "speak out against", "struggle against", "testify against", "vote against", "have something against", "come along", "bring along",
           "choose between", "differentiate between", "fall down", "distinguish between", "divide between", "consist of", "could be", "could get"]
phrasals = sorted(list(set(phrasals)))
"""

phrasals = sorted(list(set(phrasals)))

def phrasal(a, phrasal):
    m = len(phrasal.split(" ")) - 1
    main= phrasal.split(" ")[0]
    mask = np.zeros(len(a))
    l = phrasal.split(" ")[1:]
    for i, x in enumerate(a):
        if (i < len(a)-(m-1)) and (x.head.lemma_ == main) and x.lower_==l[0]:
            for n in range(m-1):
                if not (a[i+1+n].lower_==l[n+1]):
                    break
            else:
                for n in range(m):
                    mask[i+n]=1
                mask[x.head.i]=1
    return mask

for phr_grd in phrasals:
    grammardict["Phrasal verb: " + phr_grd] = (lambda p: lambda x: phrasal(x, p))(phr_grd)
# overwrite normal preposition

# %%
"""Idioms"""

# load idioms

idioms = []

ignore = ["one's", "oneself", ","]

with open("idioms.csv", newline='') as csvfile:
    idiomreader = csv.reader(csvfile)
    next(idiomreader)
    for row in idiomreader:
        idioms.append(row[0])

def idiom_spotter(phrase):
    def classify_idiom(a):
        n = len(phrase.split(" "))
        phr = phrase.split(" ")
        mask = np.zeros(len(a))
        for i,x in enumerate(a[n-1:]):
            for j in range(n):
                if (a[n-1+i-j].lemma_.lower() != phr[-1-j].lower()) and (phr[-1-j] not in ignore):
                    break
            else:
                for j in range(n):
                    mask[n-1+i-j] = 1
        return mask
    return lambda a: classify_idiom(a)

for idiom in idioms:
    grammardict["Idiom: " + idiom] = idiom_spotter(idiom)

# %%
"""phrasal + gerund """

phrasal_gerunds = ["afraid of"]
phrasal_gerunds = sorted(list(set(phrasal_gerunds)))

def phrasal_gerund(a, phrasal):
    main, particle = phrasal.split(" ")[0], phrasal.split(" ")[1]
    mask = np.zeros(len(a))
    for i, x in enumerate(a):
        if (i < len(a)-1) and (x.lemma_ == main) and (a[i+1].lower_==particle) and ("VBG" in [y.tag_ for y in a[i+1].children]):
            mask[i]=1
            mask[i+1]=1
            for y in a[i+1].children: 
                mask[y.i]=1
    return mask

for phr_grd in phrasal_gerunds:
    grammardict["Phrasal verb + gerund: " + phr_grd] = (lambda p: lambda x: phrasal_gerund(x, p))(phr_grd)

# Overwrites normal phrasal.

# %%
"""phrasal + infinitive"""

phrasal_infinitives = ["carry on", "have got"]
phrasal_infinitives = sorted(list(set(phrasal_infinitives)))

def phrasal_infinitive(a, phrasal):
    main, particle = phrasal.split(" ")[0], phrasal.split(" ")[1]
    mask = np.zeros(len(a))
    for i, x in enumerate(a):
        if (i < len(a)-1) and (x.lemma_ == main) and (a[i+1].lower_==particle) and a[i+2].tag_=="TO":
            mask[i]=1
            mask[i+1]=1
            mask[i+2]=1
            mask[a[i+2].head.i]=1
    return mask

for phr_grd in phrasal_infinitives:
    grammardict["Phrasal verb + infinitive: " + phr_grd] = (lambda p: lambda x: phrasal_infinitive(x, p))(phr_grd)

# Overwrites normal phrasal.

# %%
def analyse(sentence):
    sentence = nlp(sentence)
    print(sentence)
    print("\n")
    for k in grammardict.keys():
        mask = grammardict[k](sentence)
        if np.sum(mask) > 0:
            print(k)
            print(mask)

# %%
import dill as pickle

pickle.dump(grammardict, open("grammardict.txt", 'wb'))

# %%
