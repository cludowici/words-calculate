from __future__ import print_function
import pandas as pd
import os

#This program will find all the compound words in a long list of words, by
#taking the lexicon of all half-as-many-letters words and checking them against 
#the long list.

print(os.getcwd()) #os.chdir() If using within psychopy, might start out in wrong directory
dir='words_from_databases/'
fname = '8letterWordsFromElexicon'
#Read in all the words (downloaded before from Elexicon
words=pd.read_csv(dir+fname+'.csv')
#Read in all the words with half as many letters
wordsHalfAsManyLtrs = pd.read_csv(dir+'4letterWordsFromElexicon.csv')

#words.to_pickle(fname+'.pickle')
#words = pd.read_pickle(fname+'.pickle')
if type(words['Word'].irow(-1)) is not str: #sometimes last row is bad, probably because carriage return at end
    words = words[:-1]
    
wordsList =  words['Word'].astype(str) #put them into a list
wordsList = list( wordsList )
wordsList = [ x.upper() for x in wordsList ] #change to upper case

numLtrs = words['Length'][0] 
halfNumLtrs = int(numLtrs/2)
print('words=',words)
words['firstHalf'] = 'ZZZZZ'
words['secondHalf'] = 'ZZZZZ'
#Loop through all words, dividing them into first half and second half
#Add first and second half to same pandas dataframe
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
print('words.head=',words.head())
#print('words.tail=',words.tail())

if type(wordsHalfAsManyLtrs['Word'].irow(-1)) is not str: #sometimes last row is bad, probably because carriage return at end
    wordsHalfAsManyLtrs = wordsHalfAsManyLtrs[:-1] #remove last item

#For each  word, find out whether both firsthalf and second half is a word
halfLengthWords = wordsHalfAsManyLtrs['Word'].astype(str)
halfLengthWords = list(halfLengthWords)
halfLengthWords = [ x.upper() for x in halfLengthWords ] #change to upper case
print('halfLengthWords=',halfLengthWords)
validWords = []
validWordsFreq = []
print('words with both halves legal:')
for i in range(len(words)):
    firstHalf = words['firstHalf'][i].upper()
    #print('firstHalf=',firstHalf)
    secondHalf = words['secondHalf'][i].upper()
    if i==0:
        print('example firstHalf=',firstHalf,' secondHalf=',secondHalf)
    if firstHalf in halfLengthWords and secondHalf in halfLengthWords:
        print(words['Word'][i])
        validWords.append(firstHalf+secondHalf)
        #validWordFreq.append(words['frequency'][i])
print(len(validWords),' valid words')

#freqCriterion = 3
#validWordFreq > freqCriterion 

#check whether the half words can be combined in either order to form a legal word
reverseWords = []
print('words whose half-word can be put in either order to form a legal word:')
for i in range(len(words)):
    firstHalf = words['firstHalf'][i].upper()
    #print('firstHalf=',firstHalf)
    secondHalf = words['secondHalf'][i].upper()
    reversed = secondHalf + firstHalf
    if reversed in wordsList and (firstHalf != secondHalf):
        reverseWords.append(reversed)
        print(reversed)
    if i==0:
        print('example reversed=',reversed)
print(len(reverseWords),' valid reverse words')

