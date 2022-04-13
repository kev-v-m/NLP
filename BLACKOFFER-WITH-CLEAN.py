#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import os
import re
from textblob import TextBlob
import numpy as np
import re


# In[2]:


driver = webdriver.Chrome('C:/Users/Kevin/Downloads/chromedriver_win32/chromedriver.exe')


# In[3]:


df=pd.read_csv('C:\\Users\Kevin\Desktop\BLACKOFFER\Input.csv')
df.describe()


# In[4]:


Tit=[]
Cont=[]
idx=0


# In[5]:


os.chdir('C:\\Users\Kevin\Desktop\BLACKOFFER')


# In[6]:


idx=0
for i in df["URL"]:
    idx+=1
    if idx>1:
        break
    driver.get(i)
    a = driver.find_element_by_class_name("td-post-content").text
    a = a.encode('utf-8').decode('ascii', 'ignore')
    #a = a.format(r"\r\n\\ ")
    f = open('{}.txt'.format(idx), 'w')
    f.write(driver.title)            
    f.write("\n")
    f.write("\n")
    f.write("\n")    
    f.write(a)
    f.close()

 


# In[7]:


from textblob import TextBlob
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
import re
import string


# In[8]:


def data_clean(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    #text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text


# In[9]:


def break_sentences(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return list(doc.sents)
 


# In[10]:


#for i in range(170):
 #   f = open('{}.txt'.format(idx), 'r',encoding='utf-8')
f = open('1.txt').read()
f=data_clean(f)
#f=f.lower()
#import string
#f=f.translate(str.maketrans('','',string.punctuation))
#f=f.split()



# In[11]:


score=SIA().polarity_scores(f)
print(score)


# In[12]:



def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# In[13]:


getSubjectivity(f)


# In[14]:


def avg_words_sentence(text):
    res = re.split('\! |\.|-|!|\?', text)
    #print(res)
    sentence_len=0
    for i in res:
        i=i.split(" ")
        for j in i:
            if j!="":
                sentence_len+=1
                #print(j,sentence_len,len(res))
    return (sentence_len/(len(res)-1))
ans = avg_words_sentence(f) 
print(ans)


# In[15]:


def avg_sentence_len(text):
    res = re.split('\! |\.|-|!|\?', text)
    sentence_len=0
    for i in res:
        i=i.split(" ")
        #print(i)
        for j in i:
            if j!="":
                #print(j)
                sentence_len+=len(j)
                #print(sentence_len)

    return (sentence_len/(len(res)-1))
ans = avg_sentence_len(f) 
print(ans)


# In[16]:


def avgwordlength(f):
    word=f.split()
    sum=0

    for i in word:
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:len(i)-1]
        sum+=len(i)
        #print(sum)
    #print("avg",sum/len(word))
    return sum/len(word)

avgwordlength(f)


# In[17]:


def wordcount(f):
    word=f.split()
    sum=0

    for i in word:
        sum+=1
    #print(sum)
    return sum
words=wordcount(f)


# In[18]:


import spacy
from textstat.textstat import textstatistics,legacy_round


# In[19]:



def syllables_count(word):
    return textstatistics().syllable_count(word)
 
syllable=syllables_count(f)
print(syllable)


# In[20]:


print(syllable/words)


# In[21]:


def difficult_words(text):
     
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    # Find all words in the text
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [str(token) for token in sentence]
 
    # difficult words are those with syllables >= 2
    # easy_word_set is provide by Textstat as
    # a list of common words
    diff_words_set = set()
     
    for word in words:
        syllable_count = syllables_count(word)
        if word not in nlp.Defaults.stop_words and syllable_count >= 2:
            diff_words_set.add(word)
 
    return len(diff_words_set)
print(difficult_words(f))


# In[22]:


def total_sentences(f):
    res = re.split('\! |\.|-|!|\?', f)
    #print(res)
    return len(res) - 1
total_sentences(f)


# In[23]:


def fog(f):
    diff=difficult_words(f)
    wc=wordcount(f)
    return 0.4*(100*(diff/wc) + (wc/total_sentences(f)))


# In[24]:


fog(f)


# In[25]:


def percdiffwords(f):
    #print(difficult_words(f),wordcount(f))
    return (difficult_words(f)/wordcount(f))
percdiffwords(f)


# In[26]:


def perspro(f):
    pronounRegex = re.compile(r'I|we|my|ours|us',re.I)
    pronouns = pronounRegex.findall(f)
    return len(pronouns)
perspro(f)


# In[ ]:




