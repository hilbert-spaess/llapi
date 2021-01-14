import random

days = []

# define the reading comprehension question for the first day

day1 = []

text = ' '.join("""To Sherlock Holmes she is always “the” woman. I have seldom heard him
mention her under any other name. In his eyes she eclipses and
predominates the whole of her sex. It was not that he felt any emotion
akin to love for Irene Adler. All emotions, and that one particularly,
were abhorrent to his cold, precise but admirably balanced mind. He
was, I take it, the most perfect reasoning and observing machine that
the world has seen, but as a lover he would have placed himself in a
false position. He never spoke of the softer passions, save with a gibe
and a sneer. They were admirable things for the observer—excellent for
drawing the veil from men’s motives and actions. But for the trained
reasoner to admit such intrusions into his own delicate and finely
adjusted temperament was to introduce a distracting factor which might
throw a doubt upon all his mental results. Grit in a sensitive
instrument, or a crack in one of his own high-power lenses, would not
be more disturbing than a strong emotion in a nature such as his. And
yet there was but one woman to him, and that woman was the late Irene
Adler, of dubious and questionable memory.""".split())

main_questions = ["Describe how Sherlock feels about Irene Adler.", "What do we learn about Sherlock's work as a detective?", "What can we learn about Sherlock from this paragraph?"]

question0 = {'id': 0, 't': 2, 'm': 'filler', 'q': "We can divide our answer into two parts:\n1. Sherlock's attitude towards Irene Adler and romantic feelings.\n2. What he is like as a detective.\n\nWe will answer the question by paying attention to key evidence in the text, and you will be guided into making points, embedding quotes, and developing your answer. You will form a complete answer to the question above.\nPress the arrow in the top-right to continue.", 'i': {}, 'a':""}

question1 = {'id': 1, 't': 0, 'q': "Evidence: What two words does Sherlock use to describe Irene Adler?", 'a': "He thinks that she \"eclipses\" and \"predominates\" all other women.", 'i': {4 : {'mode': 'text', 'a': 'eclipses', 'data': {'loc': 23}, 'id': 1}, 6: {'mode': 'text', 'a': 'predominates', 'data': {'loc': 25}, 'id': 2}}}

question2 = {'id': 2, 't': 0, 'q': "Point: What does this tell us about how Sherlock feels about her?", 'a': "Sherlock feels that Irene is special.", 'i': {5: {'mode': 'choose', 'id': 3, 'a': 'special.', 'choices': ['special', 'intelligent', 'beautiful', 'crazy']}}}

question3 = {'id': 3, 't': 0, 'q': "We combine the Point and Evidence, and can add some explanation below. Here are some thoughts that might help you develop your answer:\nWhat does this tell us about how Sherlock feels about other women?\nCan they even be compared to her?", 'a': 'Sherlock feels that Irene is special, since she "eclipses" and "predominates" her sex. This shows us that she is unique to him, and she is .', 'i': {19: {'mode': 'choose', 'a': 'unique', 'id': 4, 'choices': ['helpful', 'respectful', 'unique', 'indignant']}, 25 : {'mode': 'free', 'id': 5, 'a': "probably the only woman he cares much about."}}}

question4 = {'id':4, 't': 0, 'q': "When Watson writes that \"All emotions, and that one particularly, were abhorrent...\", which emotion is he referring to as \"that one\"?", 'a': 'Love', 'i': {0: {'mode': 'fill', 'a': 'Love', 'id': 6}}}

question5 = {'id': 5, 't': 0, 'd': "These are our synonyms. You can use them in your answer later.", 'q': "This shows us that Sherlock is not very interested in romantic relationships, but is much more interested in his detective work. Here is some evidence that we could use to prove this point: \"a gibe and a sneer\", \"abhorrent\", and \"intrusions\". First, write some synonyms or explanations for these words.", 'a': "1. \"a gibe and a sneer\": . 2. \"abhorrent\": . 3. \"intrusions\": . ", 'i': {6: {'mode': 'free', 'id': 22, 'a': 'mocking/dismissive remarks, noises'}, 9: {'mode': 'free', 'id': 23, 'a': 'repulsive, detestable'}, 12: {'mode': 'free', 'id': 24, 'a': '(unwelcome) disturbances'}}}

question55 = {'t': 0, 'q': "To use these pieces of evidence in an explanation, we could highlight what these words show about his attitude towards love. One example has been given. Try and do the same for the other two:", 'a': "He . interested in romantic feelings. The phrase \"a gibe and a sneer\" indicates that he is dismissive toward love. The words \"abhorrent\" and \"intrusive\" .", 'i': {1: {'mode': 'choose', 'a': 'is not', 'id': 25, 'choices': ['is', 'is not']}, 25: {'mode': 'free', 'id': 7, 'a': 'tell us that he finds such feelings repulsive and sees them as distractions to his work.'}}}

question57 = {'id': 0, 't': 2, 'm': 'filler', 'q': "We can divide our answer into two parts:\n1. Sherlock's attitude towards Irene Adler and romantic feelings.\n2. What he is like as a detective.\n\nIn this session we will work on the second point.", 'i': {}, 'a':""}

question6 = {'id': 6, 't': 0, 'q': "Here is the answer we've constructed together:", 'm': 'summary', 'a': 'Sherlock feels that Irene is special, since she "eclipses" and "predominates" her sex. This shows us that she is unique to him, and . He is not interested in romantic feelings. The phrase "a gibe and a sneer" indicates that he is dismissive towards love. The words "abhorrent" and "intrusions" tell us .', 'i': {23: {'mode': 'filled', 'id': 5}, 52: {'mode': 'filled', 'id': 7}}}

question7 = {'id': 7, 't': 1, 'q': "What adjectives does Watson use to describe Sherlock's mind? Complete the statement below.", 'a': 'Watson describes Sherlock\'s mind as cold and precise, but also .', 'i': {5: {'mode': 'text', 'a': 'cold', 'id': 12}, 7: {'mode': 'text', 'a': 'precise,', 'id': 13}, 10: {'mode': 'text', 'a': 'balanced.', 'id': 14}}}

question8 = {'id': 8, 't': 1, 'q': "Sherlock is compared to a certain object- how is he described? What literary technique is this an example of?", 'a': 'He is compared to a . This is an example of a .', 'i': {5: {'a': 'perfect reasoning and observing machine', 'mode': 'text', 'id': 15}, 12: {'a': 'metaphor', 'id': 16, 'mode': 'choose', 'choices': ['metaphor', 'simile', 'personification', 'synopsis']}}}

question9 = {'id': 9, 't': 1, 'q': "Explain what this metaphor tells us about him.", 'a': "He is a careful and logical detective, who is likely very intelligent.", 'i': {3: {'a': 'careful', 'id': 17, 'mode': 'choose', 'choices': ['careful', 'brash', 'excitable', 'nervous']}, 5: {'a': 'logical', 'mode': 'choose', 'id': 18, 'choices': ['ruthless', 'knowledgeable', 'logical', 'harsh']}, 11: {'a': 'intelligent.', 'id': 19, 'mode': 'choose', 'choices': ['rude', 'intelligent', 'deaf', 'brave']}}}

question10 = {'id': 10, 't': 1, 'q': "The narrator mentions two items used by Sherlock, which give us more information about him. Complete your answer below:", 'a': 'Watson describes Sherlock\'s mind as "cold" and "precise", but also "balanced". He is described as a "perfect reasoning and observing machine". This is an example of a metaphor. The metaphor illustrates that he is a careful and logical detective, who is likely very intelligent. The phrases "sensitive instrument" and "high-power lenses" tell us about the tools he uses. This . his .', 'i': {59: {'id': 20, 'mode': 'choose', 'choices': ['energises', 'emphasises', 'empties', 'elevates'], 'a': 'emphasises'}, 61: {'id': 21, 'mode': 'free', 'a': 'care and attention to detail, which gives us the impression that he is a thorough and effective detective.'}}}

question11 = {'id': 11, 't': 2, 'm': 'summary',  'q': "We've helped you put your answers together. Feel free to make some changes, and then submit your final answer below", 'a': 'We are first told about how he feels about Irene Adler. Sherlock feels that Irene is special, and that she "eclipses" and "predominates" her sex. She is unique to him, and . He is not interested in romantic feelings. The phrase "a gibe and a sneer" indicates that he is dismissive towards love. The words "abhorrent" and "intrusions" tell us . \n\nIn fact, Sherlock is much more focused on his work. Watson describes Sherlock\'s mind as "cold" and "precise", but also "balanced". He is described as a "perfect reasoning and observing machine". This is an example of a metaphor. The metaphor illustrates that he is a careful and logical detective, who is likely very intelligent. The phrases "sensitive instrument" and "high-power lenses" tell us about the tools he uses. This emphasises his .', 'i': {31: {'mode': 'filled', 'id': 5}, 60: {'mode': 'filled', 'id': 7}, 44: {'mode': 'filled', 'id': 8}, 132: {'id': 21, 'mode': 'filled'}}}

print(question11['a'].split().index('emphasises'))


questions = [question0, question1, question2, question3, question4, question5, question55, question6, question7, question8, question9, question10, question11]

day1comp = [question0, question1, question2, question3, question4, question5, question55, question6]

day2comp = [question57, question7, question8, question9, question10, question11]

# day 1 devices questions

text1 = "He was, I take it, the most perfect reasoning and observing machine that the world has seen."

question1 = {'id': 2000, 'q': 'The author uses the metaphor "reasoning and observing machine" when describing Sherlock.', 'a': 'metaphor', 'i': {4: {'mode': 'devicefill'}}}

text2 = "It was a rimy morning, and very damp. I had seen the damp lying on the outside of my little window, as if some goblin had been crying there all night, and using the window for a pocket-handkerchief."

question2 = {'id': 2001, 'q': 'In this extract the author employs an absurd simile. He writes that the window is "damp ... as if some goblin had been crying there all night".', 'a': 'simile',  'i': {8: {'mode': 'devicefill'}}}

text3 = "The moonbeams danced on the surface of the water."

question3 = {'id': 2002, 'q': 'Here the author uses personification: the technique of describing an inanimate object as behaving like a human', 'a': 'personification', 'i': {4: {'mode': 'devicefill'}}}

question4 = {'id': 2003, 'q': 'I wanted to see the world. Accordingly, I left my home with just a bag on my back.', 'a': 'Accordingly', 'i': {6: {'mode': 'choose', 'choices': ['In contrast', 'Furthermore', 'Accordingly', 'In conclusion']}}}

question5 = {'id': 2004, 'q': 'The speaker refuted all of his opponent\'s points. Furthermore, he pleased the audience while doing so.', 'a': 'Furthermore', 'i': {8: {'mode': 'choose', 'choices': ['Instead', 'Similarly', 'Nevertheless', 'Furthermore']}}}

question6 = {'id': 2005, 'q': 'The chess player stared at the board. Her opponent did likewise.', 'a': 'likewise', 'i': {10: {'mode': 'choose', 'choices': ['Likewise', 'Nevertheless', 'Hence', 'Consequently']}}}

question7 = {'id': 2006, 'q': 'The book was written many years ago. The language is therefore often unfamiliar.', 'a': 'therefore', 'i': {10: {'mode': 'choose', 'choices': ['furthermore', 'therefore', 'similarly', 'thereby']}}}

question8 = {'id': 2007, 'q': 'The author conveys an atmosphere of supreme solitude and melancholy.', 'a': 'conveys', 'i': {2: {'mode': 'choose', 'choices': ['depicts', 'contrasts', 'combines', 'conveys']}}}

question9 = {'id': 2008, 'q': 'The style of the dance epitomises the care-free attitude of the era.', 'a': 'epitomises', 'i': {5: {'mode': 'choose', 'choices': ['epitomises', 'employs', 'hints', 'insinuates']}}}

question10 = {'id': 2009, 'q': 'The portrayal of his grandfather is a crude caricature of a stereotypical old man.', 'a': 'caricature', 'i': {8: {'mode': 'choose', 'choices': ['effigy', 'caricature', 'display', 'employment']}}}

day1vocab= [{"mechanism": "device", "text": text1, "question": question1}, {"mechanism": "device", "text": text2, "question": question2}, {"mechanism": "device", "text": text3, "question": question3}, {"mechanism": "device", "question": question4}, {"mechanism": "device", "question": question5}, {"mechanism": "device", "question": question6}, {"mechanism": "device", "question": question7}, {"mechanism": "device", "question": question8}, {"mechanism": "device", "question": question9}, {"mechanism": "device", "question": question10}]

day1writing = [{"mechanism": "writing", "id": 1001, "prompt": {"title": "Creative Writing Task: You can finish this over the next two days.", "text": "Sherlock occasionally dresses up as a beggar in order to observe strangers without being noticed. We know that he is very careful, and his disguises are usually very good.\nSee if you can carry on using the voice of the narrator and describe Sherlock disguised as a beggar on the side of the road. The start of the paragraph has been given. Feel free to change it. Here are some things you could pay attention to:\n-His clothes\n-His posture\n-Possible accessories\n-His interaction with passers-by\nIf you find this difficult, just write a few sentences and we will go through this in the lesson"}}]
random.shuffle(day1vocab)

day1 = {"Comprehension": [{"mechanism": "analysis", "text": text, "questions": day1comp, "main_questions": main_questions}], "Vocabulary": day1vocab, "Writing": day1writing}

##

text1 = 'A man entered who could hardly have been less than six feet six inches in height, with the chest and limbs of a Hercules.'

question1 = {'id': 2010, 'def': 'Make reference to something', 'q': 'In this extract, the author alludes to the Roman hero Hercules.', 'a': 'alludes', 'i': {5: {'mode': 'choose', 'choices': ['augments', 'alludes', 'anticipates', 'answers']}}}

text2 = 'April is the cruellest month, breeding Lilacs out of the dead land'

question2 = {'id': 2011, 'q': 'The stark juxtaposition of "Lilacs" and the "dead land" evokes an unsettling mood.', 'a': 'juxtaposition', 'i': {2: {'mode': 'devicefill'}}}

# simile question

text3 = "Now, I saw the damp lying on the bare hedges and spare grass, like a coarser sort of spiders' webs; hanging itself from twig to twig and blade to blade."

question3 = {'id': 2012, 'q': 'Dickens uses personification to bring the mist to life, writing that it is "hanging itself from twig to twig"', 'a': 'personification', 'i': {2: {'mode': 'devicefill'}}}

# metaphor question

text4 = "He was a bag of bones, a floppy doll, a broken stick, a maniac."

question4 = {'id': 2013, 'q': 'In this extract, Kerouac uses the emphatic technique of asyndeton: listing nouns without any conjuctions.', 'a': 'asyndeton', 'i': {9: {'mode': 'devicefill'}}}

text5 = "Still young and healthy, he was blooming like a flower in season."

question5 = {'id': 2014, 'q': 'The comparison of the boy to a flower is an example of a simile.', 'a': 'simile', 'i': {13: {'mode': 'devicefill'}}}

text6 = "The stars were thousands of gems sprinkled across the night sky."

question6 = {'id': 2015, 'q': 'The author uses the metaphor of stars as "gems", evoking the excitement of the night sky.', 'a': 'metaphor', 'i': {4: {'mode': 'devicefill'}}}

# furthermore: 7

question7 = {'id': 2016, 'q': "I'm not interested in what you have to offer, and furthermore, I refuse to be contacted again.", 'a': 'furthermore', 'i': {10: {'mode': 'choose', 'choices': ['furthermore', 'generally', 'nevertheless', 'in contrast']}}}

# accordingly: 8

question8 = {'id': 2017, 'q': "The author writes for a young audience, and accordingly he uses simple words with an exciting plot.", 'a': 'accordingly', 'def': 'As such; it follows that ...', 'i': {8: {'mode': 'choose', 'choices': ['furthermore', 'accordingly', 'undeniably', 'relentlessly']}}}

day2vocab= [{"mechanism": "device", "text": text1, "question": question1}, {"mechanism": "device", "text": text2, "question": question2}, {"mechanism": "device", "text": text3, "question": question3}, {"mechanism": "device", "question": question4, "text": text4}, {"mechanism": "device", "question": question5, "text": text5}, {"mechanism": "device", "question": question6, "text": text6}, {"mechanism": "device", "question": question7}, {"mechanism": "device", "question": question8}]

day2 = {"Comprehension": [{"mechanism": "analysis", "text": text, "questions": day2comp, "main_questions": main_questions}], "Writing": day1writing, "Vocabulary": day2vocab}


days.append(day1)
days.append(day2)

### day 2

### day 3

text = ' '.join("""Dorothy lived in the midst of the great Kansas prairies, with Uncle
Henry, who was a farmer, and Aunt Em, who was the farmer’s wife. Their
house was small, for the lumber to build it had to be carried by wagon
many miles. There were four walls, a floor and a roof, which made one
room; and this room contained a rusty looking cookstove, a cupboard for
the dishes, a table, three or four chairs, and the beds. Uncle Henry
and Aunt Em had a big bed in one corner, and Dorothy a little bed in
another corner. There was no garret at all, and no cellar—except a
small hole dug in the ground, called a cyclone cellar, where the family
could go in case one of those great whirlwinds arose, mighty enough to
crush any building in its path. It was reached by a trap door in the
middle of the floor, from which a ladder led down into the small, dark
hole.

When Dorothy stood in the doorway and looked around, she could see
nothing but the great grey prairie on every side. Not a tree nor a
house broke the broad sweep of flat country that reached to the edge of
the sky in all directions. The sun had baked the plowed land into a
grey mass, with little cracks running through it. Even the grass was
not green, for the sun had burned the tops of the long blades until
they were the same grey colour to be seen everywhere. Once the house had
been painted, but the sun blistered the paint and the rains washed it
away, and now the house was as dull and grey as everything else.""".split())

main_questions = ["What impressions do we get of Dorothy's home and surroundings?", "What do we learn from their home and belongings?", "How do their surroundings contribute to the impression that they are poor?"]

question0 = {"t": 0, "m": "filler", "q": "We can think about her home and surroundings separately, but we can draw similar inferences from the two.", 'i': {}, 'a': ""}

question1 = {"t": 1, "q": "Point: The writer makes a list in the first paragraph: \"four walls, a floor ... the beds\".What can we infer from this list?", "a": "The list of things in Dorothy's home . them as a . family.", 'i': {7: {"mode": "choose", "a": "depicts", "choices": ["installs", "depicts", "regards", "evokes"], "id": 30}, 11: {"mode": "choose", "a": "poor", "choices": ["foolish", "wealthy", "poor", "wise"], "id": 31}}}

question2 = {"t": 1, "q": "Evidence: Build on your answer by filling in the gaps.", "a": "It appears the writer has listed everything they have - \"a rusty cookstove ... dishes ... beds\", and it is . that they have very few possessions.", "i": {20: {"mode": "choose", "choices": ["implied", "inferred", "described", "related"], "a": "implied", "id": 32}, 26: {"mode": "choose", "a": "possessions", "choices": ["windows", "chores", "possessions", "pets"], "id": 33}}}

question = {"t": 1, "q": "", "a": "", "i": {20: {"mode": "choose", "choices": ["", "", "", ""], "a": "", "id": 32}, 26: {"mode": "choose", "a": "", "choices": ["", "", "", ""], "id": 33}}}

question3 = {"t": 1, "q": "Explanation: We can develop this explanation further. Isn’t it odd that the writer explicitly mentions the walls, roof and floor? Is he trying to emphasise something?", "a": "The writer () highlights the \"walls\", \"floor\" and \"roof\", which () .", "i": {2: {"mode": "choose", "choices": ["even", "yet", "furthermore", "alternatively"], "a": "even", "id": 34}, 10: {"mode": "choose", "a": "reinforces", "choices": ["depicts", "emphasises", "reinforces", "elucidates"], "id": 35}, 11: {"mode": "free", "id": 36, "a": "the simplicity of the things that are important to them, and make up their home."}}}

question4 = {"t": 1, "m": "summary", "q": "Here's our answer to the question so far.", "a": "The list of things in Dorothy's home depicts them as a poor family. It appears the writer has listed everything they have - \"a rusty cookstove ... dishes ... beds\", and it is implied that they have very few possessions. The writer () highlights the \"walls\", \"floor\" and \"roof\", which . .", "i": {42: {"mode": "filled", "id": 34}, 50: {"mode": "filled", "id": 35}, 51: {"mode": "filled", "id": 36}}}

question5 = {"t": 2, "q": "Point. What can you deduce about their surroundings? Try and complete the sentence below:", "a": "It is obvious that they live in a . and . place.", "i": {8: {"mode": "choose", "choices": ["crowded", "friendly", "remote", "tropical"], "a": "remote", "id": 37}, 10: {"mode": "choose", "a": "dangerous", "choices": ["useful", "dangerous", "peaceful", "bustling"], "id": 38}}}

question6 = {"t": 2, "q": "Evidence. Here are quotes that support your point. Fill in the key words to start building on your answer:", "a": "The presence of a “cyclone cellar” (indicates) that the area may experience these “great whirlwinds” from time to time, which tells us that it’s a (hostile) place to live.", "i": {6: {"mode": "choose", "choices": ["indicates", "infers", "refutes", "suspects"], "a": "indicates", "id": 39}, 25: {"mode": "choose", "a": "hostile", "choices": ["peaceful", "hostile", "deadly", "robust"], "id": 40}}}

question7 = {"t": 2, "q": "Explanation. Think about why they would live here (it’s probably not their choice!)", "a": "(Since) no family would willingly live in such a (desolate) place, we can infer that this family must be quite (desperate) and .", "i": {0: {"mode": "choose", "choices": ["despite", "since", "whatever", "nevertheless"], "a": "since", "id": 41}, 9: {"mode": "choose", "a": "desolate", "choices": ["desolate", "differentiated", "dubious", "deniability"], "id": 42}, 20: {"mode": "choose", "a": "desperate", "choices": ["replete", "bespoke", "desperate", "betrayed"], "id": 43}, 22: {"mode": "free", "id": 44, "a": "had no choice but to settle there."}}}

question8 = {"t": 2, "m": "summary", "q": "Here's your answer to the question so far.", "a": "The list of things in Dorothy's home depicts them as a poor family. It appears the writer has listed everything they have - \"a rusty cookstove ... dishes ... beds\", and it is implied that they have very few possessions. The writer () highlights the \"walls\", \"floor\" and \"roof\", which . . \n\nIt is obvious that they live in a remote and dangerous place. The presence of a \"cyclone cellar\" indicates that the area may experience these \"great whirlwinds\" from time to time, which tells us that it's a hostile place to live. Since no family would willingly live in such a desolate place, we can infer that this family must be quite desperate and .", "i": {42: {"mode": "filled", "id": 34}, 50: {"mode": "filled", "id": 35}, 51: {"mode": "filled", "id": 36}, 115: {"mode": "filled", "id": 44}}}

question9 = {"t": 2, "q": "What word is repeated three times in the second paragraph?", "a": "Grey", "i": {0: {"mode": "fill", "a": "Grey", "id": 45}}}

question10 = {"t": 2, "q": "Consider the effect of this repetition.", "a": "The repetition of the word “grey” and the fact that it was to be \"seen everywhere\" highlights the (dullness) of their surroundings. The colour (epitomises) the remoteness and the . of where they live. This adds to the bleak atmosphere and (reinforces) the image of a poor family.", "i": {18: {"mode": "choose", "choices": ["energy", "retention", "dullness", "disparity"], "a": "dullness", "id": 46}, 24: {"mode": "choose", "a": "epitomises", "choices": ["elucidates", "epitomises", "evokes", "estranges"], "id": 47}, 29:{"mode": "choose", "a": "uniformity", "choices": ["hilarity", "uniqueness", "untidiness", "uniformity"], "id": 48}, 41: {"mode": "choose", "a": "reinforces", "choices": ["engenders", "reinforces", "illustrates", "highlights"], "id": 49}}}

question11 = {"t": 0, 'm': "summary", "q": "Here is your complete answer to the question!", "a": "The list of things in Dorothy's home depicts them as a poor family. It appears the writer has listed everything they have - \"a rusty cookstove ... dishes ... beds\", and it is implied that they have very few possessions. The writer () highlights the \"walls\", \"floor\" and \"roof\", which . . \n\nIt is obvious that they live in a remote and dangerous place. The presence of a \"cyclone cellar\" indicates that the area may experience these \"great whirlwinds\" from time to time, which tells us that it's a hostile place to live. Since no family would willingly live in such a desolate place, we can infer that this family must be quite desperate and . The repetition of the word “grey” and the fact that it was to be \"seen everywhere\" highlights the (dullness) of their surroundings. The colour epitomises the remoteness and the uniformity of where they live. This adds to the bleak atmosphere and reinforces the image of a poor family", "i": {42: {"mode": "filled", "id": 34}, 50: {"mode": "filled", "id": 35}, 51: {"mode": "filled", "id": 36}, 115: {"mode": "filled", "id": 44}}}

print(question10["a"].split().index('(reinforces)'))

day3comp = [{"text": text, "mechanism": "analysis", "questions": [question0, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11], "main_questions": main_questions}]

day3writing = [{"mechanism": "writing", "id": 1002, "prompt": {"title": "Creative Writing Task: You can have a look at this now, but there is no comprehension on day 4.", "text": "We know that Dorothy’s family is poor, and that their home is remote. Write the next paragraph of this narrative, and talk about some of the things that Dorothy spends her time doing. Here are some ideas that might help:\n\nThere are fields all around her home, are there things for her to do in them?\nWe know that the nearest forest is miles away, can she venture that far?\nYou could make up a stream near her home perhaps.\nThink about how her surroundings change with the seasons, and whether her activities would adjust accordingly.\n\nPay attention to the atmosphere you are creating—what kind of life is she living? Is it a simple life, is she happy or content? It’s up to you to decide, you could include some more detailed descriptions of her surroundings to contribute to the atmosphere."}}]

# juxtaposition

text1 = 'Merry and tragical? Tedious and brief?; That is hot ice, and wondrous strange snow!; How shall we find the concord of this discord?'

question1 = {'id': 2020, 'q': 'With the close positioning of \"hot\" and \"ice\", \"concord\" and \"discord\", this extract features repeated use of juxtaposition.', 'def': 'two things placed close together with contrasting effect', 'a': 'juxtaposition', 'i': {17: {'mode': 'devicefill'}}}

# asyndeton

text2 = 'An empty stream, a great silence, an impenetrable forest. The air was thick, warm, heavy, sluggish.'

question2 = {'id': 2021, 'q': 'The author uses the asyndeton "thick, warm, heavy, sluggish", to convey a stultifying and oppressive atmosphere.', 'def': 'a list without conjunctions', 'a': 'asyndeton', 'i': {4: {'mode': 'devicefill'}}}

# personification

text3 = 'The mouth of the cave yawned open before him.'

question3 = {'id': 2022, 'q': 'By writing that the cave mouth \"yawned\", the author uses personification to bring his description to life.', 'def': 'attributing human characteristics to an inanimate object', 'a': 'personification', 'i': {10: {'mode': 'devicefill'}}}

# interjection

question4 = {'id': 2023, 'q': 'The teacher made a sharp interjection, rebuking the pupil for their actions and demanding that they return to their seat.', 'a': 'interjection', 'def': 'an abrupt remark, an exclamation', 'i': {5: {'mode': 'choose', 'choices': ['addendum', 'interjection', 'retention', 'suspicion']}}}

# allude

question8 = {'id': 2028, 'q': 'The so-called "Goldilocks zone" is the region of space in which planetary conditions are just right for life to occur. The name alludes to the famous fairy tale of Goldilocks and the three bears.', 'a': 'alludes', 'def': 'refer to, make reference to', 'i': {22: {'mode': 'definition'}}}

# systematic

question5 = {'id': 2024, 'q': 'The subject of anatomy refers to the systematic study of the human body and its constituent parts.', 'a': 'systematic', 'def': 'done or acting according to a fixed plan or system', 'i': {7: {'mode': 'choose', 'choices': ['systematic', 'reductive', 'materialistic', 'salacious']}}}

# catalyst

question5 = {'id': 2025, 'q': 'The war had the effect of acting as a catalyst for the growth of many different industries.', 'a': 'catalyst', 'def': 'something that causes or accelerates change', 'i': {9: {'mode': 'choose', 'choices': ['analogy', 'refactoring', 'catalyst', 'deployment']}}}

# hypothesise

question6 = {'id': 2026, 'q': 'The theory of relativity was first hypothesised by Einstein in the early twentieth century.', 'a': 'hypothesised', 'def': 'conjecture, make a guess, put forward a hypothesis', 'i': {6: {'mode': 'choose', 'choices': ['hypnotised', 'heralded', 'haunted', 'hypothesised']}}}

# dubious

question7 = {'id': 2027, 'q': 'The evidence that he was the culprit is dubious at best.', 'a': 'dubious', 'def': 'not to be relied on, suspicious', 'i': {8: {'mode': 'choose', 'choices': ['derived', 'dubious', 'daunting', 'deterred']}}}
# The evidence that he was the culprit is dubious at best. 

question9 = {'id': 2029, 'q': 'When interviewed, the artist found it impossible to convey his sweeping ideas in simple terms.', 'a': 'convey', 'a': 'convey', 'def': 'make an idea known and understandable', 'i': {8: {'mode': 'choose', 'choices': ['confer', 'convey', 'confide', 'correlate']}}}

#When interviewed, the artist found it impossible to convey his sweeping ideas in simple terms.

day3vocab = [{"text": text1, "question": question1, "mechanism": "device"}, {"text": text2, "question": question2, "mechanism": "device"}, {"text": text3, "question": question3, "mechanism": "device"}, {"question": question4, "mechanism": "device"},  {"question": question5, "mechanism": "device"},  {"question": question6, "mechanism": "device"},  {"question": question7, "mechanism": "device"},  {"question": question8, "mechanism": "device"}, {"question": question9, "mechanism": "device"}]

day3 = {"Comprehension": day3comp, "Vocabulary": day3vocab, "Writing": day3writing}

day4 = {"Comprehension": day3comp, "Vocabulary": day3vocab, "Writing": day3writing}

days.append(day3)

days.append(day4)

text = """"By the way, Doctor, I shall want your co-operation.”
“I shall be delighted.”
“You don’t mind breaking the law?”
“Not in the least.”
“Nor running a chance of arrest?”
“Not in a good cause.”
“Oh, the cause is excellent!”
“Then I am your man.”
“I was sure that I might rely on you.”
“But what is it you wish?”
“When Mrs. Turner has brought in the tray I will make it clear to you. Now,” he said as he turned hungrily on the simple fare that our landlady had provided, “I must discuss it while I eat, for I have not much time. It is nearly five now. In two hours we must be on the scene of action. Miss Irene, or Madame, rather, returns from her drive at seven. We must be at Briony Lodge to meet her.”
"""

main_questions = ["How does the writer use form and structure to portray the relationship between the two people?"]

question1 = {"t": 0, "q": "**What are some of your first impressions about the relationship between these people? Note down a few ideas, you do not have to explain your answers.", "a": ". . . . .", 'i': {0: {'mode': 'free', 'id': 50}, 1: {'mode': 'free', 'id': 51}, 2: {'mode': 'free', 'id': 52}, 3: {'mode': 'free', 'id': 53}}}

question2 = {"t": 0, "q": "We thought they seemed *friendly* and *trusting*. Let's examine how *form* and *structure* contribute to these impressions.\n\nWhat is the form of this text?", "a": ".", 'i': {0: {'mode': 'fill', 'id': 54, 'a': 'A conversation'}}}

question3 = {"t": 0, "q": "**What do you notice about the way they talk to each other? Does this give us any information about their relationship?", "a": "The form of this text is a conversation, and we can infer from their casual conversation style that they are good friends. This is apparent from how Sherlock directly “wants” a favour from Watson without greeting him, and that Sherlock says,”I was sure that I might rely on you”. This shows that not only do they know each other well, but are also on amiable terms with each other.", 'i': {11: {'mode': 'choose', 'id': 55, 'a': 'infer', 'choices': ['indicate', 'imply', 'infer', 'introduce']}, 14: {'mode': 'choose', 'id': 56, 'a': 'casual', 'choices': ['casual', 'formal', 'mundane', 'descriptive']}, 24: {'mode': 'choose', 'id': 57, 'a': 'apparent', 'choices': ['suspicious', 'aware', 'apparent', 'apt']}, 29: {'mode': 'choose', 'id': 58, 'a': '"wants"', 'choices': ['"wants"', '"minds"', '"relies"', '"desires"']}, 64: {'mode': 'choose', 'id': 59, 'a': 'amiable', 'choices': ['antagonistic', 'adversarial', 'amiable', 'avaracious']}}}

question4 = {"t": 0, "q": "**What do you notice about the sentences, are they long? Think about the effect this creates.", "a": "The sentences are short and (create) the feel of a (quick) conversation. This (highlights) Watson’s decisiveness in agreeing to help, since he does not take time to (hesitate). He immediately agrees to . and expresses that he (doesn’t) mind breaking the law. Watson’s quick responses also (implies) that he trusts Sherlock, because he knows Sherlock wouldn't ask him to break the law (unless) it was for a good cause.", 'i': {5: {'mode': 'choose', 'id': 60, 'a': 'create', 'choices': ['enact', 'create', 'disrupt', 'envision']}, 10: {'mode': 'choose', 'id': 61, 'a': 'quick', 'choices': ['quick', 'slow', 'steady']}, 13: {'mode': 'choose', 'id': 62, 'a': 'highlights', 'choices': ['predicts', 'disseminates', 'highlights', 'corrupts']}, 27: {'mode': 'choose', 'id': 63, 'a': 'hesitate.', 'choices': ['harangue', 'haughty', 'headlong', 'hesitate']}, 32: {'mode': 'textsyn', 'id': 64,'a': 'cooperate', 's': 'go along with it'}, 37: {'mode': 'choose', 'id': 65, 'a': 'doesn\'t', 'choices': ['does', 'doesn\'t']}, 46: {'mode': 'choose', 'a': 'implies', 'id': 66, 'choices': ['imply', 'insinuate', 'infer', 'impede']}, 62: {'mode': 'choose', 'a': 'unless', 'id': 67, 'choices': ['until', 'always', 'unless', 'without']}}}

question5 = {"t": 0, "q": "From their conversation we can already infer that they are unreserved and unguarded towards each other. Let’s explore how structure—in this case, the chronology/order of events— emphasises that Watson trusts Sherlock.\nThis is a more subtle point. Complete the answer below:", "a": "Notice the structure of the conversation and chronology of events, which reinforces this theme of trust. Watson agrees to not only help Sherlock but also to break the law before knowing what the mission is. This would be unlikely unless he completely trusted him.", "i": {13: {"mode": "choose", "id": 68, "a": "theme", "choices": ["theory", "theme", "thesis", "theology"]}, 29: {"mode": "choose", "id": 69, "a": "before", "choices": ["before", "after"]}, 41: {"mode": "choose", "id": 70, "a": "completely", "choices": ["partially", "completely", "implicitly", "repeatedly"]}}}

question6 = {"t": 0, "m": "summary", "q": "Here is our final answer structured around the themes of friendship and trust:", "a": "The form of this text is a conversation, and we can infer from their casual conversation style that they are good friends. Their verbal exchange is casual because Sherlock directly asks Watson for a favour without greeting him, and we know that they are acquantied because Sherlock says,”I was sure that I might rely on you”. This shows that they know each other well and are on amiable terms with each other. The sentences are short and create the feel of a quick conversation. This highlights Watson’s decisiveness in agreeing to help, since he does not take time to hesitate. He immediately agrees to to “cooperate” and expresses that he doesn't mind breaking the law.\n\nWatson’s quick responses also imply that he trusts Sherlock, because he knows Sherlock wouldn't ask him to break the law unless it was for a good cause. Notice the structure of the conversation and chronology of events, which reinforces this theme of trust. Watson agrees to not only help Sherlock but also to break the law before knowing what the mission is. This would be unlikely unless he completely trusted him.", 'i': {}}

print(question5["a"].split().index("completely"))

day5comp = [{"text": text, "mechanism": "analysis", "questions": [question1, question2, question3, question4, question5, question6], "main_questions": main_questions}]

question1 = {'id': 2040, 'q': 'The development of radar was the first major step towards the creation of more systematic methods of tracking objects in the sky.', 'a': 'systematic', 'def': 'done or acting according to a fixed plan or system', 'i': {14: {'mode': 'choose', 'choices': ['systematic', 'seductive', 'materialistic', 'solipsistic']}}}

# catalyst

question2 = {'id': 2041, 'q': 'One major catalyst for the rapid spread of ideas was the internet, which made information sharing much easier.', 'a': 'catalyst', 'def': 'something that causes or accelerates change', 'i': {2: {'mode': 'choose', 'choices': ['coefficient', 'conductor', 'catalyst', 'deployment']}}}

# hypothesise

question3 = {'id': 2042, 'q': 'Many historians reject the Marxist theory of class struggle and hypothesise instead that the French Revolution was largely driven by economic factors.', 'a': 'hypothesise', 'def': 'conjecture, make a guess, put forward a hypothesis', 'i': {10: {'mode': 'choose', 'choices': ['hypothesise', 'hallucinate', 'haunted', 'heterodox']}}}

# dubious

question4 = {'id': 2043, 'q': 'The anthropological consensus is that religion, at least in its organised form, began when early humans tried to explain natural phenomena.', 'a': 'consensus', 'def': 'agreement, shared opinion', 'i': {2: {'mode': 'choose', 'choices': ['corrective', 'consensus', 'commission', 'cephalopod']}}}

question5 = {'id': 2044, 'q': 'The scientific evidence in favour of the existence of ghosts and other paranormal phenomena is dubious at best.', 'a': 'dubious', 'def': 'disputable, untrustworthy', 'i': {15: {'mode': 'choose', 'choices': ['distracting', 'dubious', 'divisive', 'dismissive']}}}


day5vocab = [{"question": question1, "mechanism": "device"}, {"question": question2, "mechanism": "device"}, {"question": question3, "mechanism": "device"},{"question": question4, "mechanism": "device"}, {"question": question5, "mechanism": "device"}]

day5 = {"Comprehension": day5comp, "Writing": [], "Vocabulary": day5vocab}

days.append(day5)

text= " ".join("""It was a rimy morning, and very damp. I had seen the damp lying on the outside of my little

window, as if some goblin had been crying there all night, and using the window for a pocket-
handkerchief. Now, I saw the damp lying on the bare hedges and spare grass, like a coarser

sort of spiders' webs; hanging itself from twig to twig and blade to blade. On every rail and gate,
wet lay clammy; and the marsh-mist was so thick, that the wooden finger on the post directing
people to our village—a direction which they never accepted, for they never came there—was
invisible to me until I was quite close under it. Then, as I looked up at it, while it dripped, it
seemed to my oppressed conscience like a phantom devoting me to the Hulks.""".split())

main_questions = ["How does the writer use language to create atmosphere?"]

question0 = {"t": 0, "m": "filler", "q": "It is possible to describe the atmosphere in many ways, in this question we will encourage you to choose two impressions and give reasons for them.", 'i': {}, 'a': ""}

question1 = {"t": 0, "q": "What words could you use to describe the atmosphere? Write some down and we will suggest some of the ones we came up with.", "d": "Here are some that we came up with. Feel free to use them later.", "a": ".", "i": {0: {"id": 80, "mode": "free", "a": "Sombre, mysterious, frightening/spine-chilling/creepy, dangerous..."}}}

question2 = {"t": 0, "m": "noanswer", "q": "Descriptive adjectives: Sombre, mysterious, frightening/spine-chilling/creepy, dangerous\nChoose one of the adjectives and find two quotes to use as evidence for this feeling. Try to explain why the phrases give you this feeling.", "a": "Mood/atmosphere: . Evidence: . How do the quotes make you feel and why do they have this effect? . ", "i": {1: {"id": 81, "mode": "free", "a": ""}, 3: {"id": 82, "mode": "free"}, 18: {"id": 83, "mode": "free"}}}

question3 = {"t": 0, "m": "noanswer", "q": "Descriptive adjectives: Sombre, mysterious, frightening/spine-chilling/creepy, dangerous\nNow do the same thing for another adjective.", "a": "Mood/atmosphere: . Evidence: . How do the quotes make you feel and why do they have this effect? . ", "i": {1: {"id": 84, "mode": "free", "a": ""}, 3: {"id": 85, "mode": "free"}, 18: {"id": 86, "mode": "free"}}}

question4 = {"t": 0, "m": "noanswer", "q": "Now try to join your answers using appropriate connectives to form a free-flowing paragraph. Here are some phrases/words you may find helpful:\n\nActive verbs: • ...shows/creates/portrays... • ...evokes/instills a sense of... • A/An...image is depicted through/by...", "a": "Mood/atmosphere: . Evidence: . How do the quotes make you feel and why do they have this effect? . .Mood/atmosphere: . Evidence: . How do the quotes make you feel and why do they have this effect? . .", "i": {1: {"id": 81, "mode": "filled", "a": ""}, 3: {"id": 82, "mode": "filled"}, 18: {"id": 83, "mode": "filled"}, 20: {"id": 84, "mode": "filled"}, 22: {"id": 85, "mode": "filled"}, 37: {"id": 86, "mode": "filled"}, 38: {"id": 87, "mode": "free", "freelines": 4}}}

question5 = {"t": 0, "m": "noanswer", "q": "Charles Dickens employed pathetic fallacy in his work. You could think of this as a special case of personification where human emotions are attributes to objects or nature/weather etc. It is often used to reflect the mood of a character, in this case the narrator Pip. Judging by the mood the writer has created, how could you describe Pip’s mood?", "a": ".", "i": {0: {"mode": "free", "id": 88}}}

day6comp = [{"main_questions": main_questions, "text": text, "mechanism": "analysis", "questions": [question0, question1, question2, question3, question4, question5]}]

# consensus def

question1 = {'id': 2050, 'q': 'The scientific community ultimately reached a consensus that animal testing was unacceptable and should only be used as last resort for absolutely critical drug trials .', 'a': 'consensus', 'def': 'general agreement', 'i': {6: {'mode': 'definition'}}}

# hypothesise def

question2 = {'id': 2051, 'q': 'Gravity was well - studied and extensively discussed in Newton \'s time , yet the relationship between gravity and light was first hypothesised by Einstein with his special theory of relativity .', 'a': 'hypothesised', 'def': 'form a guess, make a theory', 'i': {22: {'mode': 'definition'}}}

# catalyst def

question3 = {'id': 2052, 'q': 'The atmosphere created by these new ideas served as a catalyst for the period of intellectual brilliance that was seventeenth - century England .', 'a': 'catalyst', 'def': 'something that makes change occur faster', 'i': {10: {'mode': 'definition'}}}

# maxim choose

question4 = {'id': 2053, 'q': 'The maxim "All men are created equal" was used to argue that it was illegitimate to own another person , and that slavery should be made illegal .', 'a': 'maxim', 'def': 'a short statement expressing general truth', 'i': {1: {'mode': 'choose', 'choices': ['maxim', 'mango', 'mixer', 'medic']}}}

# dichotomy choose

question5 = {'id': 2054, 'q': 'Conversations with poets and scientists revealed the dichotomy between intuitive and rational thought processes .', 'a': 'dichotomy', 'def': 'a division between two opposite things', 'i': {7: {'mode': 'choose', 'choices': ['detergent', 'dichotomy', 'deference', 'diligence']}}}


# plausible choose

question6 = {'id': 2055, 'q': 'The argument may be plausible , but the history of mathematics reveals that without formal proof , our everyday intuition is not to be trusted when it comes to infinite sets .', 'a': 'plausible', 'def': 'reasonable, probable (of an idea, argument)', 'i': {4: {'mode': 'choose', 'choices': ['plausible', 'pragmatic', 'premature', 'primitive']}}}


# paramount choose

question7 = {'id': 2056, 'q': 'It was of paramount importance that the protesters remain non - violent , or the police would surely have license to intervene .', 'a': 'paramount', 'def': 'most important, of supreme importance', 'i': {3: {'mode': 'choose', 'choices': ['perpetual', 'paramount', 'plentiful', 'pertinent']}}}


# correlate choose

question8 = {'id': 2057, 'q': 'They found that the number of hours a student spent watching television a day correlated with their academic performance , even when confounding factors such as exercise levels were taken into account .', 'a': 'correlated', 'def': 'have a dependent relationship with; change along with', 'i': {14: {'mode': 'choose', 'choices': ['cooperated', 'circulated', 'correlated', 'cultivated']}}}

day6vocab = [{"question": question1, "mechanism": "device"}, {"question": question2, "mechanism": "device"}, {"question": question3, "mechanism": "device"},{"question": question4, "mechanism": "device"}, {"question": question5, "mechanism": "device"}, {"question": question6, "mechanism": "device"}, {"question": question7, "mechanism": "device"}, {"question": question8, "mechanism": "device"}]

random.shuffle(day6vocab)

day6 = {"Comprehension": day6comp, "Vocabulary": day6vocab}

days.append(day6)

## day 7

day7writing = [{"mechanism": "writing", "id": 1003, "prompt": {"title": "Creative Writing Task", "text": "In the next part of the story, she goes to a very elaborate ball and has an excellent time. Try to write a piece of text describing this event and her experience. The key thing is to develop more detail about a few important things. Think about the following:\n\nSetting the scene and describing the ball (there are many things you could write about, choose two or three and try to add as much detail as possible)\n\nWhat she does at the ball and how she enjoyed it (you could describe her feelings or communicate how she feels through describing her actions)\n\nYou have been provided with the text, feel free to look at it for inspiration or even use little bits you really like. Otherwise please try and use your own words."}}]

# day 7 vocab

# maxim def

q1 = {'id': 2060, 'q': 'The antecedents to the modern theory of modal realism , summarised by the maxim " Whatever can exist , does exist " , can be found centuries earlier with the work of the ancient Greek philosopher Plato .', 'a': 'maxim', 'def': 'a short statement expressing general truth', 'i': {13: {'mode': 'definition'}}}

# dichotomy def

q2 = {'id': 2061, 'q': 'The Nature vs. Nurture debate is an old one , with a long history of scientific investigation giving evidence for both sides of the dichotomy .', 'a': 'dichotomy', 'def': 'a division between two opposite things', 'i': {24: {'mode': 'definition'}}}

# plausible def

q3 = {'id': 2062, 'q': 'His refutation of my conjecture , dismissed outhand during the lecture , seemed more and more plausible as I reflected on it later .', 'a': 'plausible', 'def': 'reasonable, probable (of an idea, argument)', 'i': {16: {'mode': 'definition'}}}

# paramount def

q4 = {'id': 2063, 'q': 'The importance of the king within his realm was second to that of the Pope , whose influence over matters theological ( and often political ) was paramount .', 'a': 'paramount', 'def': 'most important, of supreme importance', 'i': {27: {'mode': 'definition'}}}

# correlate def

q5 = {'id': 2064, 'q': 'The amount of trade between two nations correlates closely with the amount of diplomatic contact .', 'a': 'correlates', 'def': 'have a dependent relationship with; change along with', 'i': {7: {'mode': 'definition'}}}

# aspect c

q6 = {'id': 2065, 'q': 'The goal was to modernise various aspects of the house without changing its essential character , which required , for example , finding ways to restore the old floorboards to their original condition .', 'a': 'aspects', 'def': 'a particular part or feature of something', 'i': {6: {'mode': 'choose', 'choices': ['accesses', 'aspects', 'authors', 'agencies']}}}

# implicit c

q7 = {'id': 2066, 'q': 'The idea of the existence of a soul is implicit in the ideology of many early religions . It is often understood that the soul is eternal and separates from the body after death .', 'a': 'implicit', 'def': 'suggested but not directly expressed', 'i': {9: {'mode': 'choose', 'choices': ['imperial', 'integral', 'inherent', 'implicit']}}}

# arbitrary c

q8 = {'id': 2067, 'q': 'The university , despite being an institution of scholarship , seems to set completely arbitrary grade boundaries every term .', 'a': 'arbitrary', 'def': 'based on random choice rather than reason', 'i': {14: {'mode': 'choose', 'choices': ['alternate', 'arbitrary', 'ambiguous', 'authentic']}}}

# simile

# metaphor

# alliteration

# hyperbole

day7vocab = [{"question": q1, "mechanism": "device"}, {"question": q2, "mechanism": "device"}, {"question": q3, "mechanism": "device"},{"question": q4, "mechanism": "device"}, {"question": q5, "mechanism": "device"}, {"question": q6, "mechanism": "device"}, {"question": q7, "mechanism": "device"}, {"question": q8, "mechanism": "device"}]

text = """
The girl was one of those pretty and charming young creatures who sometimes are born, as if by a slip of fate, into a family of clerks. She had no dowry, no expectations, no way of being known, understood, loved, married by any rich and distinguished man; so she let herself be married to a little clerk of the Ministry of Public Instruction.
She dressed plainly because she could not dress well, but she was unhappy as if she had really fallen from a higher station; since with women there is neither caste nor rank, for beauty, grace and charm take the place of family and birth. Natural ingenuity, instinct for what is elegant, a supple mind are their sole hierarchy, and often make of women of the people the equals of the very greatest ladies.
Mathilde suffered ceaselessly, feeling herself born to enjoy all delicacies and all luxuries. She was distressed at the poverty of her dwelling, at the bareness of the walls, at the shabby chairs, the ugliness of the curtains. All those things, of which another woman of her rank would never even have been conscious, tortured her and made her angry. The sight of the little Breton peasant who did her humble housework aroused in her despairing regrets and bewildering dreams. She thought of silent antechambers hung with Oriental tapestry, illumined by tall bronze candelabra, and of two great footmen in knee breeches who sleep in the big armchairs, made drowsy by the oppressive heat of the stove. She thought of long reception halls hung with ancient silk, of the dainty cabinets containing priceless curiosities and of the little coquettish perfumed reception rooms made for chatting at five o'clock with intimate friends, with men famous and sought after, whom all women envy and whose attention they all desire.
"""

main_questions = ["The Diamond Necklace", "Interpretation Question", "Things we learn about the main character"]

q0 = {"t": 0, "m": "filler", "q": "We will be thinking about what we learn about the girl being described. This time I will still guide you with some topics, but first let's look at some key words and phrases.", "a": "", "i": {}}

q1 = {"t": 1, "q": "Try to explain what the following word/phrase means in your own words.", "a": "Clerk: .", "i": {1: {"mode": "free", "id": 90, "a": "Basic office worker."}}}

q2 = {"t": 1, "q": "Try to explain what the following word/phrase means in your own words.", "a": "\"a higher station\" (paragraph 2): .", "i": {5: {"mode": "free", "id": 91, "a": "A higher social class."}}}

q3 = {"t": 1, "q": "Try to explain what the word in asterisks (**) means in your own words.", "a": "**For** beauty, grace, and charm take the place of family and birth: .", "i": {12: {"mode": "free", "id": 92, "a": "Since/Because"}}}

q4 = {"t": 1, "q": "Try to explain what the following word/phrase means in your own words.", "a": "Shabby (paragraph 3): .", "i": {3: {"mode": "free", "id": 93, "a": "Scruffy, worn down"}}}

q5 = {"t": 1, "q": "Try to explain what the following word/phrase means in your own words.", "a": "Tapestry (paragraph 3): .", "i": {3: {"mode": "free", "id": 94, "a": "Heavy hanging fabrics, such as curtains or hanging rugs"}}}

q6 = {"t": 2, "m": "noanswer", "q": "Write down a few key points and find some evidence for each point. You DO NOT need to explain your answer", "a": "(1 of 4) What is her position in life? .", "i": {9: {"mode": "free", "id": 95, "a": "Heavy hanging fabrics, such as curtains or hanging rugs", "freelines": 4}}}

q7 = {"t": 2, "m": "noanswer", "q": "Write down a few key points and find some evidence for each point. You DO NOT need to explain your answer", "a": "(2 of 4) What do we learn about her appearance? .", "i": {10: {"mode": "free", "id": 96, "a": "Heavy hanging fabrics, such as curtains or hanging rugs", "freelines": 4}}}

q8 = {"t": 2, "m": "noanswer", "q": "Write down a few key points and find some evidence for each point. You DO NOT need to explain your answer", "a": "(3 of 4) How does she feel about her situation in life? .", "i": {12: {"mode": "free", "id": 97, "a": "Heavy hanging fabrics, such as curtains or hanging rugs", "freelines": 4}}}

q9 = {"t": 2, "m": "noanswer", "q": "Write down a few key points and find some evidence for each point. You DO NOT need to explain your answer", "a": "(4 of 4) What kind of life does she want? .", "i": {10: {"mode": "free", "id": 98, "a": "Heavy hanging fabrics, such as curtains or hanging rugs", "freelines": 4}}}

day7comp = [{"text": text, "mechanism": "analysis", "questions": [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9], "main_questions": main_questions}]

day7 = {"Writing": day7writing, "Vocabulary": day7vocab, "Comprehension": day7comp}

days.append(day7)

day7writing = [{"mechanism": "writing", "id": 1003, "prompt": {"title": "Creative Writing Task", "text": "In the next part of the story, she goes to a very elaborate ball and has an excellent time. Try to write a piece of text describing this event and her experience. The key thing is to develop more detail about a few important things. Think about the following:\n\nSetting the scene and describing the ball (there are many things you could write about, choose two or three and try to add as much detail as possible)\n\nWhat she does at the ball and how she enjoyed it (you could describe her feelings or communicate how she feels through describing her actions)\n\nYou have been provided with the text, feel free to look at it for inspiration or even use little bits you really like. Otherwise please try and use your own words."}}]



##

text = """On his bench in Madison Square Soapy moved uneasily. When wild geese honk high of nights, and when women without sealskin coats grow kind to their husbands, and when Soapy moves uneasily on his bench in the park, you may know that winter is near at hand. 

A dead leaf fell in Soapy's lap. That was Jack Frost's card. Jack is kind to the regular denizens of Madison Square, and gives fair warning of his annual call. At the corners of four streets he hands his pasteboard to the North Wind, footman of the mansion of All Outdoors, so that the inhabitants thereof may make ready. 

Soapy's mind became cognisant of the fact that the time had come for him to resolve himself into a singular Committee of Ways and Means to provide against the coming rigour. And therefore he moved uneasily on his bench. 

The hibernatorial ambitions of Soapy were not of the highest. In them there were no considerations of Mediterranean cruises, of soporific Southern skies drifting in the Vesuvian Bay. Three months on the Island was what his soul craved. Three months of assured board and bed and congenial company, safe from Boreas and bluecoats, seemed to Soapy the essence of things desirable. 

For years the hospitable Blackwell's had been his winter quarters. Just as his more fortunate fellow New Yorkers had bought their tickets to Palm Beach and the Riviera each winter, so Soapy had made his humble arrangements for his annual hegira to the Island. And now the time was come. On the previous night three Sabbath newspapers, distributed beneath his coat, about his ankles and over his lap, had failed to repulse the cold as he slept on his bench near the spurting fountain in the ancient square. So the Island loomed big and timely in Soapy's mind. He scorned the provisions made in the name of charity for the city's dependents. In Soapy's opinion the Law was more benign than Philanthropy. There was an endless round of institutions, municipal and eleemosynary, on which he might set out and receive lodging and food accordant with the simple life. But to one of Soapy's proud spirit the gifts of charity are encumbered. If not in coin you must pay in humiliation of spirit for every benefit received at the hands of philanthropy. As Caesar had his Brutus, every bed of charity must have its toll of a bath, every loaf of bread its compensation of a private and personal inquisition. Wherefore it is better to be a guest of the law, which though conducted by rules, does not meddle unduly with a gentleman's private affairs."""

main_questions = ["See if you can infer what the following word/phrase means.", "Try and answer this interpretation question.", "Soapy tries to get caught by police six times but he fails. Can you summarise each of the attempts?"]

q1 = {"t": 0, "m": "noanswer", "q": "Women without sealskin coats", "a": ".", "i": {0: {"mode": "free", "id": 100}}}

q2 = {"t": 0, "m": "noanswer", "q": "Denizen", "a": ".", "i": {0: {"mode": "free", "id": 101}}}

q3 = {"t": 0, "m": "noanswer", "q": "Cognisant", "a": ".", "i": {0: {"mode": "free", "id": 102}}}

q4 = {"t": 0, "m": "noanswer", "q": "Hibernatorial", "a": ".", "i": {0: {"mode": "free", "id": 103}}}

q5 = {"t": 1, "m": "noanswer", "q": "Who is Soapy?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "id": "104"}}}

q6 = {"t": 1, "m": "noanswer", "q": "What is the issue that Soapy is about to face?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "id": "105"}}}

q7 = {"t": 1, "m": "noanswer", "q": "What kind of place is Blackwell's?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "id": "106"}}}

q8 = {"t": 1, "m": "noanswer", "q": "What was his attitude towards charity?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "id": "107"}}}

day8qs = [q1, q2, q3, q4, q5, q6, q7, q8]

for i in range(6):

    day8qs.append({"t": 2, "m": "noanswer", "q": "Attempt " + str(i+1), "a": ".", "i": {0: {"mode": "free", "freelines": 4, "id": 108+i}}})

day8comp = [{"text": text, "mechanism": "analysis", "questions": day8qs, "main_questions": main_questions}]

day8 = {"Comprehension": day8comp}

days.append(day8)

day9writing = [{"mechanism": "writing", "id": 1005, "prompt": {"title": "Explore the idea that appearances can be deceptive in The Cop and the Anthem", "text": "We touched on the themes of poverty and social class, and introduced the idea that a lot of the characters were surprising when it came to their identity and intellect.\n\nWe will use this opportunity to practise forming a cohesive thesis in a longer piece of writing. By considering the context, answer the question above. Think of O'Henry's idea that all four million inhabitants in New York were worth knowing, not just \"the 400\"."}}]

day9 = {"Writing": day9writing}

days.append(day9)

## day 10 stuff

text = """
I
Half a league, half a league,
Half a league onward,
All in the valley of Death
   Rode the six hundred.
“Forward, the Light Brigade!
Charge for the guns!” he said.
Into the valley of Death
   Rode the six hundred.

II
“Forward, the Light Brigade!”
Was there a man dismayed?
Not though the soldier knew
   Someone had blundered.
   Theirs not to make reply,
   Theirs not to reason why,
   Theirs but to do and die.
   Into the valley of Death
   Rode the six hundred.

III
Cannon to right of them,
Cannon to left of them,
Cannon in front of them
   Volleyed and thundered;
Stormed at with shot and shell,
Boldly they rode and well,
Into the jaws of Death,
Into the mouth of hell
   Rode the six hundred.

IV
Flashed all their sabres bare,
Flashed as they turned in air
Sabring the gunners there,
Charging an army, while
   All the world wondered.
Plunged in the battery-smoke
Right through the line they broke;
Cossack and Russian
Reeled from the sabre stroke
   Shattered and sundered.
Then they rode back, but not
   Not the six hundred.

V
Cannon to right of them,
Cannon to left of them,
Cannon behind them
   Volleyed and thundered;
Stormed at with shot and shell,
While horse and hero fell.
They that had fought so well
Came through the jaws of Death,
Back from the mouth of hell,
All that was left of them,
   Left of six hundred.

VI
When can their glory fade?
O the wild charge they made!
   All the world wondered.
Honour the charge they made!
Honour the Light Brigade,
   Noble six hundred!
"""

main_questions = ["Explore how Tennyson creates excitement in \'The Charge of the Light Brigade\'"]

q1 = {"t": 0, "m": "filler", "q": "This is a war poem written by English poet Lord Alfred Tennyson. It describes a group of men on horses charging at cannons. The charge was the result of a mistake made by another soldier. The poem is moving and breathless, and evokes the excitement of charging horses.\n\nIn this question we'll work through some important aspects of the poem.\n\nThe poem is fun to read out loud!", "a": "", "i": {}}

q2 = {"t": 0, "q": "First, let's look at some details of the poem.\n\nHow many horsemen are there? .", "a": ".", "i": {0: {"mode": "fill", "a": "600", "id": 120}}}

q3 = {"t": 0, "q": "Who are they charging at? .", "a": ".", "i": {0: {"mode": "fill", "a": "Russian soldiers and cannons", "id": 121}}}

q4 = {"t": 0, "m": "noanswer", "q": "Find evidence in the text for the following events:\n\nSomeone makes a mistake when ordering them to charge.", "a": ".", "i": {0: {"mode": "free", "a": "Russian soldiers and cannons", "id": 122}}}

q5 = {"t": 0, "m": "noanswer", "q": "Find evidence in the text for the following events:\n\nThe cannons completely surround the horsemen.", "a": ".", "i": {0: {"mode": "free", "a": "Russian soldiers and cannons", "id": 123}}}

q6 = {"t": 0, "m": "noanswer", "q": "Find evidence in the text for the following events:\n\nLots of the horsemen die.", "a": ".", "i": {0: {"mode": "free", "a": "Russian soldiers and cannons", "id": 124}}}

q7 = {"t": 0, "m": "noanswer", "q": "Tennyson uses rhyme to enhance the excitement. Find two examples of rhymes in the text, and write briefly about what effect they create.", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "Russian soldiers and cannons", "id": 125}}}

q8 = {"t": 0, "m": "noanswer", "q": "Tennyson repeats lots of small phrases. Find two examples of repetition. What do they sound like when you say them outloud? What effect do they create?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "Russian soldiers and cannons", "id": 126}}}

q9 = {"t": 0, "m": "noanswer", "q": "Tennyson uses metaphors and personification involving death. Find two examples: why do they create tension?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "Russian soldiers and cannons", "id": 127}}}

q10 = {"t": 0, "m": "noanswer", "q": "Let's consider the ways in which the last verse is different from the others. Make a few notes for each topic:", "a": "Length: . Rhyming: .", "i": {1: {"mode": "free", "a": "Russian soldiers and cannons", "id": 128}, 3: {"mode": "free", "id": 129}}}

q11 = {"t": 0, "m": "noanswer", "q": "Let's consider the ways in which the last verse is different from the others. Make a few notes for each topic:", "a": "Punctuation: . Tone/mood: .", "i": {1: {"mode": "free", "a": "Russian soldiers and cannons", "id": 130}, 3: {"mode": "free", "id": 131}}}

q12 = {"t": 0, "m": "noanswer", "q": "Here's a space for you to leave any last notes about the poem.", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "Russian soldiers and cannons", "id": 132}}}


day10comp = [{"text": text, "mechanism": "analysis", "questions": [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12], "main_questions": main_questions}]

q1 = {"t": 0, "m": "noanswer", "q": "Women without sealskin coats", "a": ".", "i": {0: {"mode": "free", "id": 100}}}

q3 = {"t": 0, "m": "noanswer", "q": "Cognisant", "a": ".", "i": {0: {"mode": "free", "id": 102}}}

q4 = {"t": 0, "m": "noanswer", "q": "Hibernatorial", "a": ".", "i": {0: {"mode": "free", "id": 103}}}

q5 = {"t": 1, "m": "noanswer", "q": "Who is Soapy?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "id": "104"}}}

day10 = {"Comprehension": day10comp}

days.append(day10)

## day 11

text = """

I

They throw in Drummer Hodge, to rest
     Uncoffined—just as found:
His landmark is a kopje-crest
     That breaks the veldt around;
And foreign constellations west
     Each night above his mound.
 

II

Young Hodge the Drummer never knew—
     Fresh from his Wessex home—
The meaning of the broad Karoo,
     The Bush, the dusty loam,
And why uprose to nightly view
     Strange stars amid the gloam.
 

III

Yet portion of that unknown plain
     Will Hodge for ever be;
His homely Northern breast and brain
     Grow up a Southern tree,
And strange-eyed constellations reign
     His stars eternally.

"""

main_questions = ["What effect does the poem have on the reader, and how does the poet accomplish these effects?"]

q1 = {"t": 0, "m": "filler", "q": "Hardy's poem describes the grave of a soldier, (a drummer), who fought and died in South Africa. It contrasts the landscape of his foreign grave with the home he came from.", "a": "", "i": {}}

q2 = {"t": 0, "m": "noanswer", "q": "Hardy deliberately uses difficult foreign words. Look up the definitions of the following words, and write them in your own words.\n\nKopje", "a": ".", "i": {0: {"mode": "free", "a": "", "id": 140}}}

q3 = {"t": 0, "m": "noanswer", "q": "Hardy deliberately uses difficult foreign words. Look up the definitions of the following words, and write them in your own words.\n\nveldt", "a": ".", "i": {0: {"mode": "free", "a": "", "id": 141}}}

q4 = {"t": 0, "m": "noanswer", "q": "Hardy deliberately uses difficult foreign words. Look up the definitions of the following words, and write them in your own words.\n\nKaroo", "a": ".", "i": {0: {"mode": "free", "a": "", "id": 142}}}

q5 = {"t": 0, "m": "noanswer", "q": "Hardy deliberately uses difficult foreign words. Look up the definitions of the following words, and write them in your own words.\n\ngloam", "a": ".", "i": {0: {"mode": "free", "a": "", "id": 143}}}

q6 = {"t": 0, "m": "noanswer", "q": "What does the use of foreign words reveal?", "a": ".",  "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 144}}}

q7 = {"t": 0, "m": "noanswer", "q": "Find some quotes in the text that refer to the theme of: isolation", "a": ".",  "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 145}}}

q8 = {"t": 0, "m": "noanswer", "q": "Find some quotes in the text that refer to the theme of: nature.", "a": ".",  "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 146}}}

q9 = {"t": 0, "m": "noanswer", "q": "How do the stanzas start and end? What effect does this create.", "a": ".",  "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 147}}}

q10 = {"t": 0, "m": "noanswer", "q": "Find a quote in which Hardy personifies the stars. How does he present them?", "a": ".",  "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 148}}}

q11 = {"t": 0, "m": "noanswer", "q": "Find some examples of alliteration or interesting sounds in the poem.", "a": ".",  "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 149}}}

q12 = {"t": 0, "m": "noanswer", "q": "What is the rhyme scheme of the poem. What does it remind you of?", "a": ".",  "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 150}}}

q13 = {"t": 0, "m": "noanswer", "q": "Here's a space for you to leave any last notes about the poem.", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "Russian soldiers and cannons", "id": 151}}}

day11comp = [{"text": text, "mechanism": "analysis", "questions": [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13], "main_questions": main_questions}]

day11 = {"Comprehension": day11comp}

days.append(day11)

text = """
We stood by a pond that winter day,
And the sun was white, as though chidden of God,
And a few leaves lay on the starving sod;
– They had fallen from an ash, and were gray.

Your eyes on me were as eyes that rove
Over tedious riddles of years ago;
And some words played between us to and fro
On which lost the more by our love.

The smile on your mouth was the deadest thing
Alive enough to have strength to die;
And a grin of bitterness swept thereby
Like an ominous bird a-wing….

Since then, keen lessons that love deceives,
And wrings with wrong, have shaped to me
Your face, and the God curst sun, and a tree,
And a pond edged with grayish leaves. 
"""

main_questions = ["How does the poet depict his relationship in this poem?"]

q1 = {"t": 0, "m": "noanswer", "q": "Let's build some paragraphs as part of an answer.\n\nHow is the theme of death presented in the context of the relationship?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 160}}}

q2 = {"t": 0, "m": "noanswer", "q": "Let's build some paragraphs as part of an answer.\n\nHow do body parts represent the fate of the relationship as a whole?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 161}}}

q3 = {"t": 0, "m": "noanswer", "q": "Let's build some paragraphs as part of an answer.\n\nHow are time and change relevant to the relationship?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 162}}}

q4 = {"t": 0, "m": "noanswer", "q": "What do you think was the fate of the relationship? How would you summarise the depiction of the relationship as a whole?", "a": ".", "i": {0: {"mode": "free", "freelines": 4, "a": "", "id": 163}}}

day12comp = [{"text": text, "mechanism": "analysis", "questions": [q1, q2, q3, q4], "main_questions": main_questions}]

day12 = {"Comprehension": day12comp}

days.append(day12)

# day 8 vocab

# aspect def

# catalyst def

# implicit def

# arbitrary def

# consensus def

# rudimentary c

# myriad c

# critique c

# personification

# juxtaposition

# asyndeton

# alliteration

# hyperbole

##

# day 9 vocab

# rudimentary def

# myriad d

# critique d

# dichotomy d

# plausible d

# paramount d

# correlate d

# capitalise c

# corroborate c

# sybillance

# metaphor

