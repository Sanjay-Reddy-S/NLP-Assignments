from pprint import pprint

grammar_rules = []
lexicon = {}
probabilities = {}
possible_parents_for_children = {}


def populate_grammar_rules():
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO Fill in your implementation for processing the grammar rules.
    fp=open("pcfg_grammar_modified",'r')
    for line in fp:
        line=line.strip()
        line=line.replace('\n','')
        if not line.strip(): continue
        try:
            left, right_tup = line.split("->")
        except ValueError:
            print line
            print "Here"
            break
        left = left.strip()
        children = right_tup.split()
        if len(children)==3:
            rule = (left, tuple(children[:-1]))
            grammar_rules.append(rule)
            probabilities[rule]=float(children[-1])
        elif len(children)==2:
            if left in lexicon:
                lexicon[left].add(children[0])
            else:
                lexicon[left]=set([children[0]])
            probabilities[(left,tuple([children[0]]) )]=float(children[-1])
            #probabilities[(left,(children[0]) )]=children[-1]
        else:
            print "Something Fishy..."

    #print grammar_rules

    for parent, (leftchild, rightchild) in grammar_rules:
        if (leftchild, rightchild) not in possible_parents_for_children:
            possible_parents_for_children[leftchild, rightchild] = []
        possible_parents_for_children[leftchild, rightchild].append(parent)

    #Error Checking
    all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
    for par, (leftchild, rightchild) in grammar_rules:
        if leftchild not in all_parents:
            assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
        if rightchild not in all_parents:
            assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

    print "Grammar rules in tuple form:"
    pprint(grammar_rules)
    print "Rule parents indexed by children:"
    pprint(possible_parents_for_children)
    print "probabilities"
    pprint(probabilities)
    print "Lexicon"
    pprint(lexicon)

def pcky_agree(sentence):
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    non_terminals=set()
    for tup in grammar_rules:
        non_terminals.add(tup[0])
        non_terminals.add(tup[1][0])
        non_terminals.add(tup[1][1])
    non_terminals=list(non_terminals)
    print non_terminals
    N = len(sentence)
    cells = {}
    #back=[]
    back={}
    for i in range(N):
        temp=[]
        for j in range(i + 1, N + 1):
            cells[(i, j)] = [0]*len(non_terminals)
            back[(i,j)] = [0]*len(non_terminals)
            #temp.append([0]*len(non_terminals))
        #print "Here..."
        #print temp
        #back.append(temp)

    #print len(back)
    #print len(back[0])
    #print (back[0][0])
    #pprint (back)

    for j in range(1,N+1):
        word=sentence[j-1]
        for key in lexicon:
            if word in lexicon[key]:
                #print "Fill lexicon: "+str(j-1)+","+str(j)+" '"+word+"' with: "+key
                idx=non_terminals.index(key)
                cells[(j-1,j)][idx]=float(probabilities[(key,tuple([word]))])
                back[(j-1,j)][idx]=(key,word)
        for i in range(j-2,-1,-1):
            for k in range(i+1,j):
                for rule_tup in grammar_rules:
                    idx_b=non_terminals.index(rule_tup[1][0])
                    idx_c=non_terminals.index(rule_tup[1][1])
                    idx_a=non_terminals.index(rule_tup[0])
                    if cells[(i,k)][idx_b]<=0 or cells[(k,j)][idx_c]<=0:
                        continue
                    try:
                        prob_value=probabilities[rule_tup]*cells[(i,k)][idx_b]*cells[(k,j)][idx_c]
                    except TypeError:
                        print "Error..."
                        print rule_tup
                        print probabilities[rule_tup]
                        print cells[(i,k)][idx_b]
                        print cells[(k,j)][idx_c]
                        return None
                    if cells[(i,j)][idx_a] <prob_value:
                        #print "Fil grammar: "+str(i)+","+str(j)+" with: "+str(rule_tup)
                        cells[(i,j)][idx_a]=prob_value
                        back[(i,j)][idx_a]=(k,idx_b,idx_c)
    pprint(cells)
    #pprint(back)
    idx_S=non_terminals.index('S')
    #print idx_S
    if cells[(0,N)][idx_S]>0:
        #ans=back_track(back,cells,idx_S,0,N,non_terminals)
        #ans=[]
        return True
    else:
        return False

def back_track(back,cells,idx_key,idx1,idx2,non_terminals):
    tup=back[(idx1,idx2)][idx_key]
    #lst_0=[idx[0] for idx in cells[(idx1,idx2)]]
    #idx=lst_0.index(key)
    #tup=cells[(idx1,idx2)][idx]
    #ans.append(((idx1,idx2),tup))
    if len(tup)==3:
        ans=[]
        ans.append(non_terminals[idx_key])
        ans_left=back_track(back,cells,tup[1],idx1,tup[0],non_terminals) #Here stopped thinking of multiple answers
        ans_right=back_track(back,cells,tup[2],tup[0],idx2,non_terminals)
        ans.append(ans_left)
        ans.append(ans_right)
        return ans
    else:
        #tup1=cells[(idx1,tup[1])]
        #tup2=cells[(tup[1],idx2)]

        return [tup[0],tup[1]]

        
def pcky_parse(sentence):
    # Return the most probable legal parse for the sentence
    # If nothing is legal, return None.
    # This will be similar to cky_parse(), except with probabilities.
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO complete the implementation
    
    non_terminals=set()
    for tup in grammar_rules:
        non_terminals.add(tup[0])
        non_terminals.add(tup[1][0])
        non_terminals.add(tup[1][1])
    for key in lexicon:
        non_terminals.add(key)
    non_terminals=list(non_terminals)
    print non_terminals
    N = len(sentence)
    cells = {}
    #back=[]
    back={}
    for i in range(N):
        temp=[]
        for j in range(i + 1, N + 1):
            cells[(i, j)] = [0]*len(non_terminals)
            back[(i,j)] = [0]*len(non_terminals)
            #temp.append([0]*len(non_terminals))
        #print "Here..."
        #print temp
        #back.append(temp)

    #print len(back)
    #print len(back[0])
    #print (back[0][0])
    #pprint (back)

    for j in range(1,N+1):
        word=sentence[j-1]
        for key in lexicon:
            if word in lexicon[key]:
                #print "Fill lexicon: "+str(j-1)+","+str(j)+" '"+word+"' with: "+key
                idx=non_terminals.index(key)
                cells[(j-1,j)][idx]=float(probabilities[(key,tuple([word]))])
                back[(j-1,j)][idx]=(key,word)
        for i in range(j-2,-1,-1):
            for k in range(i+1,j):
                for rule_tup in grammar_rules:
                    idx_b=non_terminals.index(rule_tup[1][0])
                    idx_c=non_terminals.index(rule_tup[1][1])
                    idx_a=non_terminals.index(rule_tup[0])
                    if cells[(i,k)][idx_b]<=0 or cells[(k,j)][idx_c]<=0:
                        continue
                    try:
                        prob_value=probabilities[rule_tup]*cells[(i,k)][idx_b]*cells[(k,j)][idx_c]
                    except TypeError:
                        print "Error..."
                        print rule_tup
                        print probabilities[rule_tup]
                        print cells[(i,k)][idx_b]
                        print cells[(k,j)][idx_c]
                        return None
                    if cells[(i,j)][idx_a] <prob_value:
                        #print "Fil grammar: "+str(i)+","+str(j)+" with: "+str(rule_tup)
                        cells[(i,j)][idx_a]=prob_value
                        back[(i,j)][idx_a]=(k,idx_b,idx_c)
    pprint(cells)
    #pprint(back)
    idx_S=non_terminals.index('S')
    #print idx_S
    if cells[(0,N)][idx_S]>0:
        print "Probability is: "+str(cells[(0,N)][idx_S])
        ans=back_track(back,cells,idx_S,0,N,non_terminals)
        #ans=[]
        return ans
    else:
        return False


populate_grammar_rules()
#pprint (pcky_parse(['include' ,'this', 'book']))
#pprint(pcky_parse(['book','the', 'flight', 'through', 'Houston']))
#pprint(pcky_parse(['the', 'the']))