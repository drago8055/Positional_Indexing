# coding: utf-8

# In[1]:


import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from collections import defaultdict
import copy


# In[2]:


def preprocessing(textFile):
    tokenizer = RegexpTokenizer(r'\w+')  # Tokenizing and punctuation removal
    tokens = normalization(tokenizer.tokenize(textFile))
    listOfWords = lemmatization(tokens)
    return listOfWords


# In[3]:


def lemmatization(words):
    lemmatizer = WordNetLemmatizer()
    listOfWords = []
    for x in words:
        listOfWords.append(lemmatizer.lemmatize(x))
    return listOfWords


# In[4]:


def normalization(words):
    listOfwords = []
    for word in words:
        listOfwords.append(word.lower())

    return listOfwords


# In[5]:


positional_index = defaultdict(dict)
dir1 = "20_newsgroups2/"
mainDir = os.listdir(dir1)
allDocs = []
docIds = {}
id = 0
for subDir in mainDir:
    dir2 = dir1 + subDir + "/"
    fileList = os.listdir(dir2)
    for file in fileList:
        id += 1
        allDocs.append(id)
        dir3 = dir2 + file
        docIds[id] = dir3
        fileContent = open(dir3, 'r', encoding='latin-1').read()
        words = preprocessing(fileContent)
        docAndPosition = defaultdict(list)
        for i in range(len(words)):
            if positional_index[words[i]].get(id) == None:
                new = []
                new.append(int(i))
                positional_index[words[i]][id] = new
            else:
                positional_index[words[i]][id].append(i)

# In[6]:


lemmatizer = WordNetLemmatizer()
query = input("Phrase query:")
tokenizer = RegexpTokenizer(r'\w+')  # Tokenizing and punctuation removal
x = normalization(tokenizer.tokenize(query))
q = lemmatization(x)

# In[7]:


if len(q) == 1:
    flag = 0
    count = 0
    for key in positional_index[q[0]]:
        count += 1
        flag = 1
    if flag == 0:
        print("No document found.")
    else:
        print(count)
else:
    candidate = []
    for idx in positional_index[q[0]]:
        for idy in positional_index[q[1]]:
            if idx == idy:
                for pos in positional_index[q[0]][idx]:
                    if (pos + 1) in positional_index[q[1]][idx]:
                        d = []
                        e = []
                        d.append(idx)
                        e.append(pos)
                        e.append(pos + 1)
                        d.append(e)
                        candidate.append(d)

# In[8]:


for i in range(2, len(q)):
    temp = copy.deepcopy(candidate)
    for j in temp:
        if positional_index[q[i]].get(j[0]) == None:
            del candidate[candidate.index(j)]
        else:
            if j[1][-1] + 1 in positional_index[q[i]][j[0]]:
                candidate[candidate.index(j)][1].append(j[1][-1] + 1)
            else:
                del candidate[candidate.index(j)]

# In[11]:


print(len(candidate), candidate)
