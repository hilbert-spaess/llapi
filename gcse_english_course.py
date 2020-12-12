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

main_questions = ["Describe how Sherlock feels about Irene Adler.", "What do we learn about Sherlock's work as a detective?", "What do you learn about Sherlock in this text?"]

question1 = {'id': 1, 't': 0, 'q': "What words does Sherlock use to describe Irene Adler?", 'a': "He thinks that she \"eclipses\" and \"predominates\" all other women. In fact, he always refer to her as simply \"the woman\".", 'i': {4 : {'mode': 'text', 'a': 'eclipses', 'data': {'loc': 23}, 'id': 1}, 6: {'mode': 'text', 'a': 'predominates', 'data': {'loc': 25}, 'id': 2}}}

question2 = {'id': 2, 't': 0, 'q': "What does this tell us about how Sherlock feels about her?", 'a': "Sherlock feels that Irene is special.", 'i': {5: {'mode': 'choose', 'id': 3, 'a': 'special.', 'choices': ['special', 'intelligent', 'beautiful', 'crazy']}}}

question3 = {'id': 3, 't': 0, 'q': "Complete your answer to the question. Do you think he cares much about other women?", 'a': 'Sherlock feels that Irene is special, and that she "eclipses" and "predominates" her sex. She is unique to him, and .', 'i': {16: {'mode': 'choose', 'a': 'unique', 'id': 4, 'choices': ['helpful', 'respectful', 'unique', 'indignant']}, 20 : {'mode': 'free', 'id': 5}}}

question4 = {'id':4, 't': 0, 'q': "When Watson writes that \"All emotions, and that one particularly, were abhorrent...\", which emotion is he referring to as \"that one\"?", 'a': 'Love', 'i': {0: {'mode': 'fill', 'a': 'Love', 'id': 6}}}

question5 = {'id': 5, 't': 0, 'q': "This shows us that Sherlock is not very interested in romantic relationships, but is much more interested in his detective work. Can you use the following pieces of evidence to support this claim: \"a gibe and a sneer\", \"abhorrent\", \"intrusions\"", 'a': 'Sherlock is not interested in romantic feelings. The phrase \"a gibe and a sneer\" indicates . The words \"abhorrent\" and \"intrusions\" tell us . ', 'i': {15: {'mode': 'free', 'id': 7}, 23: {'mode': 'free', 'id': 8}}}


question6 = {'id': 6, 't': 0, 'q': "Here is the answer we've constructed together:", 'm': 'summary', 'a': 'Sherlock feels that Irene is special, and that she "eclipses" and "predominates" her sex. She is unique to him, and . He is not interested in romantic feelings. The phrase "a gibe and a sneer" indicates . The words "abhorrent" and "intrusions" tell us .', 'i': {20: {'mode': 'filled', 'id': 5}, 36: {'mode': 'filled', 'id': 7}, 44: {'mode': 'filled', 'id': 8}}}

question7 = {'id': 7, 't': 1, 'q': "What adjectives does Watson use to describe Sherlock's mind? Complete the statement below.", 'a': 'Watson describes Sherlock\'s mind as cold and precise, but also .', 'i': {5: {'mode': 'text', 'a': 'cold', 'id': 12}, 7: {'mode': 'text', 'a': 'precise,', 'id': 13}, 10: {'mode': 'text', 'a': 'balanced.', 'id': 14}}}

question8 = {'id': 8, 't': 1, 'q': "Sherlock is described as being like a certain object- how is he described? What literary technique is this an example of?", 'a': 'He is compared to a . This is an example of a .', 'i': {5: {'a': 'perfect reasoning and observing machine', 'mode': 'text', 'id': 15}, 12: {'a': 'metaphor', 'id': 16, 'mode': 'choose', 'choices': ['metaphor', 'simile', 'personification', 'synopsis']}}}

question9 = {'id': 9, 't': 1, 'q': "Explain what this metaphor tells us about him.", 'a': "He is a careful and logical detective, who is likely very intelligent.", 'i': {3: {'a': 'careful', 'id': 17, 'mode': 'choose', 'choices': ['careful', 'brash', 'excitable', 'nervous']}, 5: {'a': 'logical', 'mode': 'choose', 'id': 18, 'choices': ['ruthless', 'knowledgeable', 'logical', 'harsh']}, 13: {'a': 'intelligent.', 'id': 19, 'mode': 'choose', 'choices': ['rude', 'intelligent', 'deaf', 'brave']}}}

question10 = {'id': 10, 't': 1, 'q': "The narrator mentions two items used by Sherlock, which give us more information about him. Complete your answer below:", 'a': 'Watson describes Sherlock\'s mind as "cold" and "precise", but also "balanced". He is described as a "perfect reasoning and observing machine". This is an example of a metaphor. The metaphor illustrates that he is a careful and logical detective, who is likely very intelligent. The phrases "sensitive instrument" and "high-power lenses" tell us about the tools he uses. This . his .', 'i': {59: {'id': 20, 'mode': 'choose', 'choices': ['energises', 'emphasises', 'empties', 'elevates'], 'a': 'emphasises'}, 61: {'id': 21, 'mode': 'free'}}}

question11 = {'id': 11, 't': 2, 'm': 'summary',  'q': "We've helped you put your answers together. Feel free to make some changes, and then submit your final answer below", 'a': 'Sherlock feels that Irene is special, and that she "eclipses" and "predominates" her sex. She is unique to him, and . He is not interested in romantic feelings. The phrase "a gibe and a sneer" indicates . The words "abhorrent" and "intrusions" tell us . \n\nWatson describes Sherlock\'s mind as "cold" and "precise", but also "balanced". He is described as a "perfect reasoning and observing machine". This is an example of a metaphor. The metaphor illustrates that he is a careful and logical detective, who is likely very intelligent. The phrases "sensitive instrument" and "high-power lenses" tell us about the tools he uses. This emphasises his .', 'i': {20: {'mode': 'filled', 'id': 5}, 36: {'mode': 'filled', 'id': 7}, 44: {'mode': 'filled', 'id': 8}, 106: {'id': 21, 'mode': 'filled'}}}


questions = [[question1, question2, question3], [question4, question5], [question6], [question7, question8, question9], [question10], [question11]]

day1.append({"mechanism": "analysis", "text": text, "questions": questions, "main_questions": main_questions})

# day 1 devices questions

text1 = "He was, I take it, the most perfect reasoning and observing machine that the world has seen."

question1 = {'q': 'The author uses the metaphor "reasoning and observing machine" when describing Sherlock.', 'i': {4: {'mode': 'fill'}}}

text2 = "It was a rimy morning, and very damp. I had seen the damp lying on the outside of my little window, as if some goblin had been crying there all night, and using the window for a pocket-handkerchief."

question2 = {'q': 'In this extract the author employs an absurd simile. He writes that the window is "damp ... as if some goblin had been crying there all night".', 'i': {8: {'mode': 'fill'}}}

"""
for k in [{"mechanism": "device", "text": text1, "question": question1}, {"mechanism": "device", "text": text2, "question": question2}]:

    day1.append(k)
"""

#

days.append(day1)

### day 2

