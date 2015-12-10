from __future__ import print_function
import pandas as pd
import os
fname = '6letterWordsFromElexicon'
words=pd.read_csv(fname+'.csv')
wordsHalfAsManyLtrs = pd.read_csv('3letterWordsFromElexicon.csv')

#words.to_pickle(fname+'.pickle')
#words = pd.read_pickle(fname+'.pickle')
if type(words['Word'].irow(-1)) is not str: #sometimes last row is bad, probably because carriage return at end
    words = words[:-1]
    
numLtrs = words['Length'][0] 
halfNumLtrs = int(numLtrs/2)
print('words=',words)
words['Word'][:halfNumLtrs+1]
words['firstHalf'] = 'ZZZZZ'
words['secondHalf'] = 'ZZZZZ'
#words['firstHalf'][1] = 'N'
for i in  range( len(words) ):
    thisWord = words['Word'][i]
    #print('thisWord=',thisWord)
    #print('thisWord[:halfNumLtrs]=',thisWord[:3])
    try:
        words['firstHalf'][i] = thisWord[:halfNumLtrs]
    except Exception,e:
        print(e)
        print('i=',i)
    words['secondHalf'][i] = thisWord[halfNumLtrs:]
#str(words['Word'])
print('words.head=',words.head())
print('words.tail=',words.tail())

if type(wordsHalfAsManyLtrs['Word'].irow(-1)) is not str: #sometimes last row is bad, probably because carriage return at end
    wordsHalfAsManyLtrs = wordsHalfAsManyLtrs[:-1]
print('words3ltrs.head()=',wordsHalfAsManyLtrs)
#For each  word, check if both firsthalf and second half is a word
ngrams = wordsHalfAsManyLtrs['Word'].astype(str)
ngrams = list(ngrams)
ngrams = [ x.upper() for x in ngrams ]
print('ngrams=',ngrams)
validWords = []
validWordsFreq = []
print('words with both halves legal:')
for i in range(len(words)):
    firstHalf = words['firstHalf'][i].upper()
    #print('firstHalf=',firstHalf)
    secondHalf = words['secondHalf'][i].upper()
    if i==0:
        print('example firstHalf=',firstHalf,' secondHalf=',secondHalf)
    if firstHalf in ngrams and secondHalf in ngrams:
        print(words['Word'][i])
        validWords.append(firstHalf+secondHalf)
        #validWordFreq.append(words['frequency'][i])
print(len(validWords),' valid words')

#freqCriterion = 3
#validWordFreq > freqCriterion 



