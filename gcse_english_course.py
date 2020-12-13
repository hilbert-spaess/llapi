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


question6 = {'id': 6, 't': 0, 'q': "Here is the answer we've constructed together:", 'm': 'summary', 'a': 'Sherlock feels that Irene is special, since she "eclipses" and "predominates" her sex. This shows us that she is unique to him, and . He is not interested in romantic feelings. The phrase "a gibe and a sneer" indicates that he is dismissive towards love. The words "abhorrent" and "intrusions" tell us .', 'i': {23: {'mode': 'filled', 'id': 5}, 52: {'mode': 'filled', 'id': 7}}}

question7 = {'id': 7, 't': 1, 'q': "What adjectives does Watson use to describe Sherlock's mind? Complete the statement below.", 'a': 'Watson describes Sherlock\'s mind as cold and precise, but also .', 'i': {5: {'mode': 'text', 'a': 'cold', 'id': 12}, 7: {'mode': 'text', 'a': 'precise,', 'id': 13}, 10: {'mode': 'text', 'a': 'balanced.', 'id': 14}}}

question8 = {'id': 8, 't': 1, 'q': "Sherlock is described as being like a certain object- how is he described? What literary technique is this an example of?", 'a': 'He is compared to a . This is an example of a .', 'i': {5: {'a': 'perfect reasoning and observing machine', 'mode': 'text', 'id': 15}, 12: {'a': 'metaphor', 'id': 16, 'mode': 'choose', 'choices': ['metaphor', 'simile', 'personification', 'synopsis']}}}

question9 = {'id': 9, 't': 1, 'q': "Explain what this metaphor tells us about him.", 'a': "He is a careful and logical detective, who is likely very intelligent.", 'i': {3: {'a': 'careful', 'id': 17, 'mode': 'choose', 'choices': ['careful', 'brash', 'excitable', 'nervous']}, 5: {'a': 'logical', 'mode': 'choose', 'id': 18, 'choices': ['ruthless', 'knowledgeable', 'logical', 'harsh']}, 11: {'a': 'intelligent.', 'id': 19, 'mode': 'choose', 'choices': ['rude', 'intelligent', 'deaf', 'brave']}}}

question10 = {'id': 10, 't': 1, 'q': "The narrator mentions two items used by Sherlock, which give us more information about him. Complete your answer below:", 'a': 'Watson describes Sherlock\'s mind as "cold" and "precise", but also "balanced". He is described as a "perfect reasoning and observing machine". This is an example of a metaphor. The metaphor illustrates that he is a careful and logical detective, who is likely very intelligent. The phrases "sensitive instrument" and "high-power lenses" tell us about the tools he uses. This . his .', 'i': {59: {'id': 20, 'mode': 'choose', 'choices': ['energises', 'emphasises', 'empties', 'elevates'], 'a': 'emphasises'}, 61: {'id': 21, 'mode': 'free'}}}

question11 = {'id': 11, 't': 2, 'm': 'summary',  'q': "We've helped you put your answers together. Feel free to make some changes, and then submit your final answer below", 'a': 'Sherlock feels that Irene is special, and that she "eclipses" and "predominates" her sex. She is unique to him, and . He is not interested in romantic feelings. The phrase "a gibe and a sneer" indicates . The words "abhorrent" and "intrusions" tell us . \n\nWatson describes Sherlock\'s mind as "cold" and "precise", but also "balanced". He is described as a "perfect reasoning and observing machine". This is an example of a metaphor. The metaphor illustrates that he is a careful and logical detective, who is likely very intelligent. The phrases "sensitive instrument" and "high-power lenses" tell us about the tools he uses. This emphasises his .', 'i': {20: {'mode': 'filled', 'id': 5}, 36: {'mode': 'filled', 'id': 7}, 44: {'mode': 'filled', 'id': 8}, 106: {'id': 21, 'mode': 'filled'}}}


questions = [question0, question1, question2, question3, question4, question5, question55, question6, question7, question8, question9, question10, question11]

day1comp = [question0, question1, question2, question3, question4, question5, question55, question6]

day2comp = [question7, question8, question9, question10, question11]

# day 1 devices questions

text1 = "He was, I take it, the most perfect reasoning and observing machine that the world has seen."

question1 = {'q': 'The author uses the metaphor "reasoning and observing machine" when describing Sherlock.', 'a': 'metaphor', 'i': {4: {'mode': 'devicefill'}}}

text2 = "It was a rimy morning, and very damp. I had seen the damp lying on the outside of my little window, as if some goblin had been crying there all night, and using the window for a pocket-handkerchief."

question2 = {'q': 'In this extract the author employs an absurd simile. He writes that the window is "damp ... as if some goblin had been crying there all night".', 'a': 'simile',  'i': {8: {'mode': 'devicefill'}}}

text3 = "The moonbeams danced on the surface of the water."

question3 = {'q': 'Here the author uses personification: the technique of describing an inanimate object as behaving like a human', 'a': 'personification', 'i': {4: {'mode': 'devicefill'}}}

question4 = {'q': 'I wanted to see the world. Accordingly, I left my home with just a bag on my back.', 'a': 'Accordingly', 'i': {6: {'mode': 'choose', 'choices': ['In contrast', 'Furthermore', 'Accordingly', 'In conclusion']}}}

question5 = {'q': 'The speaker refuted all of his opponent\'s points. Furthermore, he pleased the audience while doing so.', 'a': 'Furthermore', 'i': {8: {'mode': 'choose', 'choices': ['Instead', 'Similarly', 'Nevertheless', 'Furthermore']}}}

day1vocab= [{"mechanism": "device", "text": text1, "question": question1}, {"mechanism": "device", "text": text2, "question": question2}, {"mechanism": "device", "text": text3, "question": question3}, {"mechanism": "device", "question": question4}, {"mechanism": "device", "question": question5}]

day1writing = [{"mechanism": "writing", "id": 1001, "prompt": {"title": "Creative Writing Task: You can start this today and finish it tomorrow!", "text": "Sherlock occasionally dresses up as a beggar in order to observe strangers without being noticed. We know that he is very careful, and his disguises are usually very good.\nSee if you can carry on using the voice of the narrator and describe Sherlock disguised as a beggar on the side of the road. The start of the paragraph has been given. Feel free to change it. Here are some things you could pay attention to:\n-His clothes\n-His posture\n-Possible accessories\n-His interaction with passers-by\nIf you find this difficult, just write a few sentences and we will go through this in the lesson"}}]
random.shuffle(day1vocab)

day1 = {"Comprehension": [{"mechanism": "analysis", "text": text, "questions": day1comp, "main_questions": main_questions}], "Vocabulary": day1vocab, "Writing": day1writing}

day2 = {"Comprehension": [{"mechanism": "analysis", "text": text, "questions": day2comp, "main_questions": main_questions}], "Writing": day1writing}


days.append(day1)
days.append(day2)

### day 2

