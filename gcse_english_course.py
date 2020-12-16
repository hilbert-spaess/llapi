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

text1 = 'A man entered who could hardly have been less than six feet six inchesin height, with the chest and limbs of a Hercules.'

question1 = {'id': 2010, 'q': 'In this extract, the author alludes to the Roman hero Hercules.', 'a': 'alludes', 'i': {5: {'mode': 'choose', 'choices': ['augments', 'alludes', 'anticipates', 'answers']}}}

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

question8 = {'id': 2017, 'q': "The author writes for a young audience, and accordingly he uses simple words with an exciting plot.", 'a': 'accordingly', 'i': {8: {'mode': 'choose', 'choices': ['furthermore', 'accordingly', 'undeniably', 'relentlessly']}}}

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

day3 = {"Comprehension": day3comp, "Vocabulary": [], "Writing": day3writing}

days.append(day3)

print(text)


