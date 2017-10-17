from __future__ import division
import sys,re,random
from collections import defaultdict
from pprint import pprint
import pickle
import re
##########################
# Stuff you will use

import vit_starter  # your vit.py from part 1
OUTPUT_VOCAB = set(""" ! # $ & , @ A D E G L M N O P R S T U V X Y Z ^ """.split())

##########################
# Utilities

def dict_subtract(vec1, vec2):
    """treat vec1 and vec2 as dict representations of sparse vectors"""
    out = defaultdict(float)
    out.update(vec1)
    for k in vec2: out[k] -= vec2[k]
    return dict(out)

def dict_scalarprod(d,num):
    for key in d.keys():
        d[key]=d[key]*num
    return d

def dict_argmax(dct):
    """Return the key whose value is largest. In other words: argmax_k dct[k]"""
    return max(dct.iterkeys(), key=lambda k: dct[k])

def dict_dotprod(d1, d2):
    """Return the dot product (aka inner product) of two vectors, where each is
    represented as a dictionary of {index: weight} pairs, where indexes are any
    keys, potentially strings.  If a key does not exist in a dictionary, its
    value is assumed to be zero."""
    smaller = d1 if len(d1)<len(d2) else d2  # BUGFIXED 20151012
    total = 0
    for key in smaller.iterkeys():
        total += d1.get(key,0) * d2.get(key,0)
    return total

def read_tagging_file(filename):
    """Returns list of sentences from a two-column formatted file.
    Each returned sentence is the pair (tokens, tags) where each of those is a
    list of strings.
    """
    sentences = open(filename).read().strip().split("\n\n")
    ret = []
    for sent in sentences:
        lines = sent.split("\n")
        pairs = [L.split("\t") for L in lines]
        tokens = [tok for tok,tag in pairs]
        tags = [tag for tok,tag in pairs]
        ret.append( (tokens,tags) )
    return ret
###############################

## Evaluation utilties you don't have to change

def do_evaluation(examples, weights):
    num_correct,num_total=0,0
    for tokens,goldlabels in examples:
        N = len(tokens); assert N==len(goldlabels)
        predlabels = predict_seq(tokens, weights)
        num_correct += sum(predlabels[t]==goldlabels[t] for t in range(N))
        num_total += N
    print "%d/%d = %.4f accuracy" % (num_correct, num_total, num_correct/num_total)
    return num_correct/num_total

def fancy_eval(examples, weights):
    confusion = defaultdict(float)
    bygold = defaultdict(lambda:{'total':0,'correct':0})
    for tokens,goldlabels in examples:
        predlabels = predict_seq(tokens, weights)
        for pred,gold in zip(predlabels, goldlabels):
            confusion[gold,pred] += 1
            bygold[gold]['correct'] += int(pred==gold)
            bygold[gold]['total'] += 1
    goldaccs = {g: bygold[g]['correct']/bygold[g]['total'] for g in bygold}
    for gold in sorted(goldaccs, key=lambda g: -goldaccs[g]):
        print "gold %s acc %.4f (%d/%d)" % (gold,
                goldaccs[gold],
                bygold[gold]['correct'],bygold[gold]['total'],)

def show_predictions(tokens, goldlabels, predlabels):
    print "%-20s %-4s %-4s" % ("word", "gold", "pred")
    print "%-20s %-4s %-4s" % ("----", "----", "----")
    for w, goldy, predy in zip(tokens, goldlabels, predlabels):
        out = "%-20s %-4s %-4s" % (w,goldy,predy)
        if goldy!=predy:
            out += "  *** Error"
        print out

###############################

## YOUR CODE BELOW

def train(examples, stepsize=1, numpasses=10, do_averaging=False, devdata=None):
    """
    IMPLEMENT ME !
    Train a perceptron. This is similar to the classifier perceptron training code
    but for the structured perceptron. Examples are now pairs of token and label
    sequences. The rest of the function arguments are the same as the arguments to
    the training algorithm for classifier perceptron.
    """

    weights = defaultdict(float)
    weightsums = defaultdict(float)
    t = 0

    def get_averaged_weights():
        # IMPLEMENT ME!
        #avg_weights=defaultdict(float)
        #avg_weights={idx: weights[idx]-((1.0/t)*value) for idx,value in weightsums.iteritems()}
        #return avg_weights
        avg_weights=defaultdict(float)
        for idx,value in weightsums.iteritems():
            avg_weights[idx]= weights[idx]-((1.0/t)*value)
        return avg_weights

    for pass_iteration in range(numpasses):
        print "Training iteration %d" % pass_iteration
        # IMPLEMENT THE INNER LOOP!
        # Like the classifier perceptron, you may have to implement code
        # outside of this loop as well!

        for tokens,goldlabels in examples:
            predlabels = predict_seq(tokens, weights)
            gradient = dict_subtract(features_for_seq(tokens, goldlabels), features_for_seq(tokens, predlabels))
            for idx,value in gradient.iteritems():
                weights[idx]=weights[idx]+(value*stepsize)
                weightsums[idx]=weightsums[idx]+((t-1)*value*stepsize)
            t += 1

        # Evaluation at the end of a training iter
        print "TR  RAW EVAL:",
        do_evaluation(examples, weights)
        if devdata:
            print "DEV RAW EVAL:",
            do_evaluation(devdata, weights)
        if devdata and do_averaging:
            print "DEV AVG EVAL:",
            do_evaluation(devdata, get_averaged_weights())

    print "Learned weights for %d features from %d examples" % (len(weights), len(examples))
    # NOTE different return value then classperc.py version.
    return weights if not do_averaging else get_averaged_weights()

def predict_seq(tokens, weights):
    """
    IMPLEMENT ME!
    takes tokens and weights, calls viterbi and returns the most likely
    sequence of tags
    """
    # once you have Ascores and Bscores, could decode with
    # predlabels = greedy_decode(Ascores, Bscores, OUTPUT_VOCAB)
    (A_factor,B_factors)=calc_factor_scores(tokens,weights)
    predlabels=vit_starter.viterbi(A_factor, B_factors, OUTPUT_VOCAB)
    return predlabels

def greedy_decode(Ascores, Bscores, OUTPUT_VOCAB):
    """Left-to-right greedy decoding.  Uses transition feature for prevtag to curtag."""
    N=len(Bscores)
    if N==0: return []
    out = [None]*N
    out[0] = dict_argmax(Bscores[0])
    for t in range(1,N):
        tagscores = {tag: Bscores[t][tag] + Ascores[out[t-1], tag] for tag in OUTPUT_VOCAB}
        besttag = dict_argmax(tagscores)
        out[t] = besttag
    return out

def local_emission_features(t, tag, tokens):
    """
    Feature vector for the B_t(y) function
    t: an integer, index for a particular position
    tag: a hypothesized tag to go at this position
    tokens: the list of strings of all the word tokens in the sentence.
    Retruns a set of features.
    """
    curword = tokens[t]
    feats = {}
    feats["tag=%s_biasterm" % tag] = 1
    feats["tag=%s_curword=%s" % (tag, curword)] = 1
    
    """
    if (t>1):
        feats["tag=%s_wordtoleft=%s" % (tag, tokens[t-1])] = 1
    """
    """
    suffixes=['ing','ly','ance','ness','able'] #ing for verb, ly for adverb, ness and able for nouns
    for suffix in suffixes:
        if suffix in curword:
            feats["tag=%s_suffix=%s" % (tag, suffix)] = 1    
    """
    """ 
    if(len(curword) <= 5):
        feats["tag=%s_length=%s" % (tag, len(curword))] = 1
    else:
        feats["tag=%s_length=6+" % tag] = 1
    if(curword[0].isupper()):
        feats["tag=%s_upperchar=%s"%(tag,curword[0])]=1
    """
    """
    if(curword[0]=='@' or curword[0]=='#'):
        feats["tag=%s_firstchar=%s"%(tag,curword[0])]=1
    if '.com'in curword or 'http://' in curword:
        feats["tag=%s_url=1"%tag]=1 
    """
    """ #Number is reducing accuracy
    if curword.isdigit():
        feats["tag=%s_number=%s" % (tag, curword)] = 1
    elif '.' in curword:
        lst=curword.split('.')
        if len(lst)==2 and lst[0].isdigit() and (lst[1].isdigit() or len(lst[1]==0)):
            feats["tag=%s_number=%s" % (tag, curword)] = 1
    """
    return feats

def features_for_seq(tokens, labelseq):
    """
    IMPLEMENT ME!

    tokens: a list of tokens
    labelseq: a list of output labels
    The full f(x,y) function. Returns one big feature vector. This is similar
    to features_for_label in the classifier peceptron except here we aren't
    dealing with classification; instead, we are dealing with an entire
    sequence of output tags.

    This returns a feature vector represented as a dictionary.
    """
    feat_vec = defaultdict(float)
    for i in range(len(tokens)):
        feats_emission=local_emission_features(i,labelseq[i],tokens)
        for i in feats_emission.keys():
            if i in feat_vec.keys():
                feat_vec[i]+=feats_emission[i] #Biasterm gets increasing vals!!
            else:
                feat_vec[i]=1.0
    feats_transition={}
    for i in range(1,len(tokens)):
        key="trans_%s_%s" % (labelseq[i-1],labelseq[i])
        if key not in feats_transition.keys():
            feats_transition[key] = 1.0
        else:
            feats_transition[key] += 1.0
    feat_vec.update(feats_transition)
    return feat_vec

def calc_factor_scores(tokens, weights):
    """
    IMPLEMENT ME!

    tokens: a list of tokens
    weights: perceptron weights (dict)

    returns a pair of two things:
    Ascores which is a dictionary that maps tag pairs to weights
    Bscores which is a list of dictionaries of tagscores per token
    """
    N = len(tokens)
    # MODIFY THE FOLLOWING LINE
    Ascores = { (tag1,tag2): weights["trans_%s_%s" % (tag1,tag2)] for tag1 in OUTPUT_VOCAB for tag2 in OUTPUT_VOCAB }
    Bscores = []
    for i in range(N):
        Bscores.append(defaultdict(float))
    for t in range(N):
        # IMPLEMENT THE INNER LOOP
        #tagscore=defaultdict(float)
        #Bscores.append({tag:}) 
        #local_emission_features(t, tag, tokens)
        for tag in OUTPUT_VOCAB:
            tagscore=dict_dotprod(weights,local_emission_features(t,tag,tokens))
            Bscores[t][tag]+=tagscore
    assert len(Bscores) == N
    return Ascores, Bscores

if __name__ == '__main__':
    # You may implement your code here
    """
    ret=read_tagging_file("oct27.dev")
    tags_count={}
    max_count=['@',0]
    total_count=0.0
    for i in ret:
        for j in i[1]:
            if j in tags_count.keys():
                tags_count[j]+=1
                if tags_count[j]>max_count[1]:
                    max_count[0]=j
                    max_count[1]=tags_count[j]
            else:
                tags_count[j]=1
            total_count+=1
    print max_count
    #print tags_count
    print "Base accuracy: "+str(max_count[1]/total_count)
    
    print local_emission_features(2, 'V', "I went running".split())
    features=features_for_seq("I went running".split(), ['P','V','V'])
    print features
    Ascores, Bscores=calc_factor_scores("I went running".split(),features)
    print Ascores,Bscores
    #print calc_factor_scores("I went running".split(), {})
    """
    train_examples=read_tagging_file('oct27.train')
    test_examples=read_tagging_file('oct27.dev')
    try:
        weights=pickle.load(open( "weights.p", "rb" ) )
    except IOError:
        weights=train(train_examples, do_averaging=True, devdata=test_examples)
        pickle.dump( weights, open( "weights.p", "wb" ) )        
    #weights=train(train_examples, do_averaging=True, devdata=test_examples)
    #pickle.dump( weights, open( "weights.p", "wb" ) )
    #weights=pickle.load(open( "weights.p", "rb" ) )
    fancy_eval(test_examples,weights)
    show_predictions(test_examples[0][0], test_examples[0][1], predict_seq(test_examples[0][0], weights))
    show_predictions(test_examples[1][0], test_examples[1][1], predict_seq(test_examples[1][0], weights))    
