from __future__ import print_function
import pandas as pd
import os
from string import ascii_uppercase
from numpy.random import shuffle

workDir = os.getcwd()
sep = os.sep
fname = '8letterWordsFromElexicon'
words=pd.read_csv('words_from_databases'+sep+fname+'.csv')
wordsHalfAsManyLtrs = pd.read_csv('words_from_databases'+sep+'4letterWordsFromElexicon.csv')

uppercase = [char for char in ascii_uppercase]

#words.to_pickle(fname+'.pickle')
#words = pd.read_pickle(fname+'.pickle')
if type(words['Word'].irow(-1)) is not str: #sometimes last row is bad, probably because carriage return at end
    words = words[:-1]
    
numLtrs = words['Length'][0] 
halfNumLtrs = int(numLtrs/2)
#print('words=',words)
words['Word'][:halfNumLtrs+1]
words['firstHalf'] = words['Word'].str[0:halfNumLtrs]
words['secondHalf'] = words['Word'].str[halfNumLtrs:numLtrs]

print(words)
properNouns =[word for word in words['Word'] if  word[0] in uppercase]

#remove properNouns (or words with initial capital letters) from words

properNounBoolean = words['Word'].isin(properNouns) #single logical column df of len(words) where a cell is True if the word is in properNouns

properNounBooleanInvert = ~properNounBoolean #reverse that, we only want the words that aren't in properNouns

words = words[properNounBooleanInvert]
words = words.reset_index(drop=True) #otherwise the indexes have gaps where the properNouns were removed

words.to_csv(path_or_buf=workDir+sep+'words.csv')




print('words.head=',words.head())
print('words.tail=',words.tail())
#print(properNouns)
if type(wordsHalfAsManyLtrs['Word'].irow(-1)) is not str: #sometimes last row is bad, probably because carriage return at end
    wordsHalfAsManyLtrs = wordsHalfAsManyLtrs[:-1]
#print('words3ltrs.head()=',wordsHalfAsManyLtrs)
#For each  word, check if both firsthalf and second half is a word
ngrams = wordsHalfAsManyLtrs['Word'].astype(str)
ngrams = list(ngrams)
ngrams = [ x.upper() for x in ngrams ]
#print('ngrams=',ngrams)
validWords = []
validWordsFreq = []
#print('words with both halves legal:')
for i in range(len(words)):
    firstHalf = words['firstHalf'][i].upper()
    #print('firstHalf=',firstHalf)
    secondHalf = words['secondHalf'][i].upper()
    if i==0:
        print('example firstHalf=',firstHalf,' secondHalf=',secondHalf)
    if firstHalf in ngrams and secondHalf in ngrams:
        #print(words['Word'][i])
        validWords.append(firstHalf+secondHalf)
        #validWordFreq.append(words['frequency'][i])
print(len(validWords),' valid words')

#freqCriterion = 3
#validWordFreq > freqCriterion 

wordsForNotCompound = wordsHalfAsManyLtrs[~wordsHalfAsManyLtrs['Word'].isin(words['firstHalf']) | ~wordsHalfAsManyLtrs['Word'].isin(words['secondHalf'])]
wordsForNotCompound = wordsForNotCompound.reset_index(drop=True)

wordsForNotCompound = wordsForNotCompound[~wordsForNotCompound['Word'].str[0].isin(uppercase)]
wordsForNotCompound = wordsForNotCompound.reset_index(drop=True)

wordsForNotCompound = wordsForNotCompound[wordsForNotCompound['Log_Freq_HAL']>5] #mean log HAL is ~8, SD is ~ 2, don't want low freq words in list
wordsForNotCompound = wordsForNotCompound.reset_index(drop=True)

idxShuffled = range(len(wordsForNotCompound))

shuffle(idxShuffled)

print(idxShuffled)

wordsForNotCompound = wordsForNotCompound.iloc[idxShuffled,]
wordsForNotCompound = wordsForNotCompound.reset_index(drop=True)
print(wordsForNotCompound)

print(wordsForNotCompound['Word'][0:len(wordsForNotCompound)/2])



FirstPseudo = pd.DataFrame(wordsForNotCompound['Word'][0:len(wordsForNotCompound)/2])
SecondPseudo = pd.DataFrame(wordsForNotCompound['Word'][len(wordsForNotCompound)/2:len(wordsForNotCompound)])


##NOT WORKING FROM HERE ON
pseudoCompounds = FirstPseudo.merge(SecondPseudo, how='left')


print(pseudoCompounds)
#print(wordsForNotCompound)