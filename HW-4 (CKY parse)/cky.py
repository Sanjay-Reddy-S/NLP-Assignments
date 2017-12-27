from pprint import pprint

# The productions rules have to be binarized.

grammar_text = """
S -> NP VPp
S -> NPp VPs
S -> NP VP
NP -> Det Noun
NPp -> Det NounP
VP -> Verb NP
VPs -> VerbS NP
VPp -> VerbP NP
PP -> Prep NP
NP -> NP PP
VP -> VP PP
"""

lexicon = {
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'NounP':set(['cats','dogs']),
    'Verb': set(['attacked', 'saw', 'loved', 'hated']),
    'VerbS':set(['attack']),
    'VerbP':set(['attacks']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the', 'a']),
}

# Process the grammar rules.  You should not have to change this.
grammar_rules = []
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    left = left.strip()
    children = right.split()
    rule = (left, tuple(children))
    grammar_rules.append(rule)
possible_parents_for_children = {}
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)
# Error checking
all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
for par, (leftchild, rightchild) in grammar_rules:
    if leftchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    if rightchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

#print "Grammar rules in tuple form:"
#pprint(grammar_rules)
# print "Rule parents indexed by children:"
# pprint(possible_parents_for_children)


def cky_acceptance(sentence):
    # return True or False depending whether the sentence is parseable by the grammar.
    global grammar_rules, lexicon

    # Set up the cells data structure.
    # It is intended that the cell indexed by (i,j)
    # refers to the span, in python notation, sentence[i:j],
    # which is start-inclusive, end-exclusive, which means it includes tokens
    # at indexes i, i+1, ... j-1.
    # So sentence[3:4] is the 3rd word, and sentence[3:6] is a 3-length phrase,
    # at indexes 3, 4, and 5.
    # Each cell would then contain a list of possible nonterminal symbols for that span.
    # If you want, feel free to use a totally different data structure.
    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    # TODO replace the below with an implementation
    #for cell_tup in cells:
    #    for word in sentence[cell_tup[0]:cell_tup[1]]:
    #        for key in lexicon:
    #            if word in lexicon[key]:
    #                cells[cell_tup].append(key) #NOT worrying if word not in lexicon. I think it was already handled
    #                break
    # for i in range(N):
    #     word=sentence[i]
    #     for key in lexicon:
    #         if word in lexicon[key]:
    #             cells[(i,i+1)]=[key]
    #             break

    for j in range(1,N+1):
        word=sentence[j-1]
        for key in lexicon:
            if word in lexicon[key]:
                #print "Fill lexicon: "+str(j-1)+","+str(j)+" '"+word+"' with: "+key
                cells[(j-1,j)].append(key)
        for i in range(j-2,-1,-1):
            for k in range(i+1,j):
                for rule_tup in grammar_rules:
                    if (rule_tup[1][0] in cells[(i,k)]) and (rule_tup[1][1] in cells[(k,j)]):
                        #print "Fil grammar: "+str(i)+","+str(j)+" with: "+str(rule_tup)
                        cells[(i,j)].append(rule_tup[0])

    pprint(cells)
    if 'S' in cells[(0,N)]:
        return True
    else:
        return False


def cky_parse(sentence):
    # Return one of the legal parses for the sentence.
    # If nothing is legal, return None.
    # This will be similar to cky_acceptance(), except with backpointers.
    global grammar_rules, lexicon

    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    # TODO replace the below with an implementation
    for j in range(1,N+1):
        word=sentence[j-1]
        for key in lexicon:
            if word in lexicon[key]:
                #print "Fill lexicon: "+str(j-1)+","+str(j)+" '"+word+"' with: "+key
                cells[(j-1,j)].append((key,0,'',word))
        for i in range(j-2,-1,-1):
            for k in range(i+1,j):
                for rule_tup in grammar_rules:
                    lst0_1=[idx[0] for idx in cells[(i,k)]]
                    lst0_2=[idx[0] for idx in cells[(k,j)]]
                    if (rule_tup[1][0] in lst0_1) and (rule_tup[1][1] in lst0_2):
                        #print "Fil grammar: "+str(i)+","+str(j)+" with: "+str(rule_tup)
                        cells[(i,j)].append((rule_tup[0],k,rule_tup[1][0],rule_tup[1][1]))
                        #print cells[(i,j)]

    pprint(cells)
    lst_0=[idx[0] for idx in cells[(0,N)]]
    if 'S' not in lst_0:
        return None
    else:
        #idx=lst_0.index('S')
        #ans=back_track_bfs(cells,'S',[],0,N)
        #ans=back_track(cells,'S',[],0,N)
        ans=back_track(cells,'S',0,N)
        #pprint(ans)
        #sol=data_clean(ans,sentence)
        #return ans
        #print ans
        return ans

def back_track(cells,key,idx1,idx2):
    lst_0=[idx[0] for idx in cells[(idx1,idx2)]]
    idx=lst_0.index(key)
    tup=cells[(idx1,idx2)][idx]
    #ans.append(((idx1,idx2),tup))
    if tup[2]=='':
        return [tup[0],tup[3]]
    else:
        #tup1=cells[(idx1,tup[1])]
        #tup2=cells[(tup[1],idx2)]
        ans=[]
        ans.append(tup[0])
        ans_left=back_track(cells,tup[2],idx1,tup[1]) #Here stopped thinking of multiple answers
        ans_right=back_track(cells,tup[3],tup[1],idx2)
        ans.append(ans_left)
        ans.append(ans_right)
        return ans

## some examples of calling these things...
## you probably want to call only one sentence at a time to help debug more easily.

#print cky_acceptance(['the','cat','attacked','the','food'])
#print cky_parse(['the','cat','attacked','the','food'])
#print cky_acceptance(['the','cats','attack','the','dog'])
#print cky_parse(['the','cats','attack','the','dog'])
#pprint (cky_parse(['the','cat','with','the','food','on','a','dog','attacks','the','dog']))
#print cky_acceptance(["the", "the"])
#print cky_parse(["the", "table", "attacked", "a", "dog"])
#print cky_acceptance(["the", "cat"])

# pprint( cky_parse(['the','cat','attacked','the','food']))
# pprint( cky_acceptance(['the','the']))
# pprint( cky_parse(['the','the']))
# print cky_acceptance(['the','cat','attacked','the','food','with','a','dog'])
# pprint( cky_parse(['the','cat','attacked','the','food','with','a','dog']) )
# pprint( cky_parse(['the','cat','with','a','table','attacked','the','food']) )
#

def back_track_bfs(cells,key,ans,idx1,idx2):
    lst_0=[idx[0] for idx in cells[(idx1,idx2)]]
    idx=lst_0.index(key)
    tup=cells[(idx1,idx2)][idx]
    queue=[((idx1,idx2),tup,0)]
    count=0
    while(len(queue)>0):
        peek=queue[0]
        queue.pop(0)
        ans.append(peek)
        
        if peek[1][2]!='':
            lst_0=[idx[0] for idx in cells[(peek[0][0],peek[1][1])]]
            try:
                idx=lst_0.index(peek[1][2])
            except ValueError:
                print queue
                print "Left Side: "
                break
            tup=cells[(peek[0][0],peek[1][1])][idx]
        
            queue.append(((peek[0][0],peek[1][1]),tup,peek[2]+1))

        if peek[1][3]!='':
            #print cells[(peek[1][1],peek[0][1])]
            lst_0=[idx[0] for idx in cells[(peek[1][1],peek[0][1])]]
            try:
                idx=lst_0.index(peek[1][3])
            except ValueError:
                print queue
                print "Right Side: "
                break
            tup=cells[(peek[1][1],peek[0][1])][idx]

            queue.append(((peek[1][1],peek[0][1]),tup,peek[2]+1))

    return ans

def data_clean(ans,sentence):
    idx=0
    sol=[]
    sol_dict={}
    for tup in ans:
        sol.append((tup[1][0],tup[2]))
        if tup[1][2]=='':
            sol.append((sentence[idx],tup[2]+1))
            idx+=1
    print sol
    print 
    return sol
