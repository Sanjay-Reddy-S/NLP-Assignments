from __future__ import division
import sys,json,math
import os
import numpy as np
from collections import defaultdict
import math
from gensim.models import Word2Vec

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict


def cosine(dict1,dict2):
    smaller=dict1 if len(dict1)<len(dict2) else dict2
    total=0
    for key in dict1.iterkeys():
        total+=dict1.get(key,0)*dict2.get(key,0)
    sum1=0
    sum2=0
    for val in dict1.values():
        sum1+=val*val
    for val in dict2.values():
        sum2+=val*val
    return total/(math.sqrt(sum1)*math.sqrt(sum2))

def cosine_np(dict1,dict2):
    assert len(dict1)==len(dict2)
    total=0
    sum1=0
    sum2=0
    for i in range(len(dict1)):
        total+=dict1[i]*dict2[i]
        sum1+=dict1[i]*dict1[i]
        sum2+=dict2[i]*dict2[i]
    return total/(math.sqrt(sum1)*math.sqrt(sum2))

#data=load_contexts("nytcounts.university_cat_dog")
#print "University and cat: "+str(cosine(data['university'],data['cat']))
#print "University and dog: "+str(cosine(data['university'],data['dog']))
#print "dog and cat: "+str(cosine(data['dog'],data['cat']))

def linear_expression(dict1,dict2,dict3):
    lst=[]
    for i in range(len(dict1)):
        lst.append(dict1[i]-dict2[i]+dict3[i])
    return lst

def NN(word,dict_context,func='cosine',dict2=None):
    lst=[]
    count=0
    for key in dict_context:
        if key==word:
            continue
        if word!=None:
            lst.append([word,key,func(dict_context[key],dict_context[word])])
        else:
            lst.append([word,key,func(dict_context[key],dict2)])
        #if count%100==0:
        #    #print "At tis stage: "+str(count)
        count+=1
    lst2=sorted(lst,key= lambda x: x[2],reverse=True)
    #print lst2[:20]
    words=[]
    for i in lst2[:20]:
        words.append(i[1])
    return words

#print "stock: "+str(NN("sleep",data,cosine))
#print "yellow: "+str(NN("edward",data,cosine))
#print "sleep: "+str(NN('saved',data,cosine))
#print "oats: "+str(NN('red',data,cosine))
#print "improve: "+str(NN('improve',data,cosine))
#print "beautiful: "+str(NN('beautiful',data,cosine))

#data=load_word2vec("nyt_word2vec.4k")
#print "better: "+str(NN("better",data,cosine_np))