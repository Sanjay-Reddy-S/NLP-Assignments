from __future__ import division
from collections import defaultdict

import os
import random
random.seed(777)
# Global class labels.
POS_LABEL = 'pos'
NEG_LABEL = 'neg'

# Path to dataset - FILL IN THE FOLLOWING LINE
PATH_TO_DATA = "large_movie_review_dataset"
TRAIN_DIR = os.path.join(PATH_TO_DATA, "train")
TEST_DIR = os.path.join(PATH_TO_DATA, "test")

###################################
# Utilities

def dict_subtract(vec1, vec2):
    """treat vec1 and vec2 as dict representations of sparse vectors"""
    out = defaultdict(float)
    out.update(vec1)
    for k in vec2: out[k] -= vec2[k]
    return dict(out)

def dict_argmax(dct):
    """Return the key whose value is largest. In other words: argmax_k dct[k]"""
    return max(dct.iterkeys(), key=lambda k: dct[k])

def dict_scalarprod(d,num):
    for key in d.keys():
        d[key]=d[key]*num
    return d

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

def tokenize_doc(doc):
    """
    Tokenize a document and return its bag-of-words representation.
    doc - a string representing a document.
    returns a dictionary mapping each word to the number of times it appears in doc.
    """

    bow = defaultdict(float)
    tokens = doc.split()
    lowered_tokens = map(lambda t: t.lower(), tokens)
    for token in lowered_tokens:
        bow[token] += 1.0
    return bow

def construct_dataset(train=True):
    """
    Build a dataset. If train is true, build training set otherwise build test set.
    The training set is a list of training examples. A training example is a tuple
    containing a dictionary (that represents features of the training example) and
    a label for that training instance (either 1 or -1).
    """

    dataset = []
    DATA_DIR = TRAIN_DIR if train == True else TEST_DIR
    pos_path = os.path.join(DATA_DIR, POS_LABEL)
    neg_path = os.path.join(DATA_DIR, NEG_LABEL)

    num_inst = 1000
    print "[constructing dataset...]"
    for (p, label) in [ (pos_path, POS_LABEL), (neg_path, NEG_LABEL) ]:
        numeric_label = 1 if p == pos_path else -1
        print "\treading data from %s" % p
        for f in sorted(os.listdir(p))[:num_inst]:
        #for f in sorted(os.listdir(p)):
            with open(os.path.join(p,f),'r') as doc:
                content = doc.read()
                bow = tokenize_doc(content)
                dataset.append((bow, numeric_label))
    print "[dataset constructed.]"
    return dataset

###############################
# YOUR CODE GOES BELOW

def features_for_label(bow, label):
    """
    !! MAKE SURE YOU UNDERSTAND WHAT IS GOING ON HERE                     !!
    !! You will need to implement/use a function very similar to this for !!
    !! the structured perceptron code.                                    !!

    The full f(x,y) function. Pass in the bag-of-words for one document
    (represented as a dictionary) and a string label. Returns one big feature
    vector.  The space of keys for this feature vector is used for all classes.
    But for any single call to this function, half of all the features have to be zero.
    """
    feat_vec = defaultdict(float)
    for word, value in bow.iteritems():
        feat_vec["%s_%s" % (label, word)] = value
    return feat_vec

def predict_multiclass(bow, weights):
    """
    Takes a set of features represented as a dictionary and a weight vector that contains
    weights for features of each label (represented as a dictionary) and
    performs perceptron multi-class classification (i.e., finds the class with the highest
    score under the model.

    You may find it peculiar that the name of this function has to do with multiclass
    classification or that we are making predictions in this relatively complicated way
    given the binary classification setting. You are correct; this is a bit weird. But,
    this code looks a lot like the code for multiclass perceptron and the structured
    perceptron (i.e., making the next part of this homework easier).
    """
    pos_feat_vec = features_for_label(bow, "1")
    neg_feat_vec = features_for_label(bow, "-1")
    scores = { 1: dict_dotprod(pos_feat_vec, weights),
               -1: dict_dotprod(neg_feat_vec, weights) }
    return dict_argmax(scores)

def train(examples, stepsize=1, numpasses=10, do_averaging=False, devdata=None):
    """
    Trains a perceptron.
      examples: list of (featvec, label) pairs; featvec is a dictionary and label is a string
      stepsize: hyperparameter; this affects how the weights are updated
      numpasses: the number of times to loop through the dataset during training
      do_averaging: boolean that determines whether to use averaged perceptron
      devdata: the test set of examples

    returns a dictionary containing the vanilla perceptron accuracy on the train set and test set
    and the averaged perceptron's accuracy on the test set.
    """

    weights = defaultdict(float)
    weightsums=defaultdict(float)
    train_acc = []
    test_acc = []
    avg_test_acc = []
    t=0
    def get_averaged_weights():
        # IMPLEMENT ME when you get to this part
        
        #avg_weights=dict_subtract(weights,dict_scalarprod(weightsums,1.0/numpasses))
        #return avg_weights
        avg_weights=defaultdict(float)
        for idx,value in weightsums.iteritems():
            avg_weights[idx]= weights[idx]-((1.0/t)*value)
        return avg_weights

    print "[training...]"
    for pass_iteration in range(numpasses):
        print "\tTraining iteration %d" % pass_iteration
        #random.seed(700)
        random.shuffle(examples)
        for bow, goldlabel in examples:
            predlabel = predict_multiclass(bow, weights)
            if predlabel != goldlabel:
                # IMPLEMENT ME
                # you might also need to add some additional code to this function
                # but the majority of what you need to write goes here
                
                #rev_gradient=dict_subtract(features_for_label(bow,predlabel),features_for_label(bow,goldlabel))
                #weights=dict_subtract(weights,rev_gradient)
                #mult_rev_gradient=dict_scalarprod(rev_gradient,pass_iteration)
                #weightsums=dict_subtract(weightsums,mult_rev_gradient)

                gradient=dict_subtract(features_for_label(bow,goldlabel),features_for_label(bow,predlabel))
                for idx,value in gradient.iteritems():
                    weights[idx]=weights[idx]+value*stepsize
                    weightsums[idx]=weightsums[idx]+((t-1)*value*stepsize)
            t+=1

        print "TR RAW EVAL:",
        train_acc.append(do_evaluation(examples, weights))

        if devdata:
            print "DEV RAW EVAL:",
            test_acc.append(do_evaluation(devdata, weights))

        if devdata and do_averaging:
            print "DEV AVG EVAL:",
            avg_test_acc.append(do_evaluation(devdata, get_averaged_weights()))
            #print get_averaged_weights()
            #print weights

    print "[learned weights for %d features from %d examples.]" % (len(weights), len(examples))

    return { 'train_acc': train_acc,
             'test_acc': test_acc,
             'avg_test_acc': avg_test_acc,
             'weights': weights if not do_averaging else get_averaged_weights() }


def do_evaluation(examples, weights):
    """
    Compute the accuracy of a trained perceptron.
    """
    num_correct, num_total = 0, 0
    for feats, goldlabel in examples:
        predlabel = predict_multiclass(feats, weights)
        if predlabel == goldlabel:
            num_correct += 1.0
        num_total += 1.0
    print "%d/%d = %.4f accuracy" % (num_correct, num_total, num_correct/num_total)
    return num_correct/num_total

def plot_accuracy_vs_iteration(train_acc, test_acc, avg_test_acc, naive_bayes_acc):
    """
    IMPLEMENT ME!

    Plot the vanilla perceptron accuracy on the trainning set and test set
    and the averaged perceptron accuracy on the test set.
    """
    from matplotlib import pyplot as plt # moved into this function only so it doesnt slow down the overall script if this function doesnt get called
    plt.plot(train_acc,'r--',label='Training accuracy')
    plt.plot(test_acc, 'bs',label='Test accuracy (Vanilla perceptron)') 
    plt.plot(avg_test_acc, 'g^',label='Test accuracy (Avg. perceptron)')
    plt.plot(naive_bayes_acc, 'k',label='Naive Bayes')
    plt.title('Accuracy for vanilla perceptron, average perceptron, Naive Bayes')
    plt.xlabel("No. of passes over data: ")
    plt.ylabel("Accuracy (Out of 1)...")
    plt.legend(loc='lower right')
    plt.show()

if __name__=='__main__':
    training_set = construct_dataset(train=True)
    test_set = construct_dataset(train=False)
    #sol_dict = train(training_set, do_averaging=False, devdata=test_set)
    sol_dict = train(training_set, do_averaging=True, devdata=test_set)
    plot_accuracy_vs_iteration(sol_dict['train_acc'], sol_dict['test_acc'], sol_dict['avg_test_acc'],[0.8388 for i in range(len(sol_dict['train_acc']))])
