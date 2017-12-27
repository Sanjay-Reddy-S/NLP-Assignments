from collections import defaultdict
import math
POS_WORD=["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]
NEG_WORD=["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]

def PMI(filename="test2.txt"): #Reads file and create count dictionaries
	fp=open(filename,'r')
	word_counts=defaultdict(float)
	context_counts=defaultdict(float)
	word_context_counts=defaultdict(float)
	line_count=0.0
	for line in fp:
		line=line.replace('\n','')
		text=line.split(' ')
		text=set(text)
		line_count+=1
		for w in text:
			if w in POS_WORD or w in NEG_WORD or '@' in w or '#' in w:
				continue
			word_counts[w]+=1
		for i in POS_WORD:
			if i in line:
				context_counts["POS_WORD"]+=1
				for w in text:
					if w in POS_WORD or w in NEG_WORD or '@' in w or '#' in w:
						continue
					word_context_counts[w+",POS_WORD"]+=1
				break
		for i in NEG_WORD:
			if i in line:
				context_counts["NEG_WORD"]+=1
				for w in text:
					if w in POS_WORD or w in NEG_WORD or '@' in w or '#' in w:
						continue
					word_context_counts[w+",NEG_WORD"]+=1
				break
	fp.close()
	print "No. of tweets: "+str(line_count)
	return (word_context_counts,word_counts,context_counts,line_count)

def top_polarities_PPMI(filename='test2.txt',num=50,flag=1,assume=1): 
	#Flag=0 remove with count<500
	#Assume=1 ALL -ve values of PMI are made 0. Assume=1 ONLY when count is 0, PMI is made 0
	word_context_counts,word_counts,context_counts,line_count=PMI(filename)
	polarity=set()
	fp=open(filename,'r')
	count1=0
	count2=0
	for line in fp:
		line=line.replace('\n','')
		text=line.split(' ')
		count1+=1
		for w in text:
			pos_term=0
			neg_term=0
			if flag==0 and word_counts[w]<500:
				continue
			if w in POS_WORD or w in NEG_WORD or '@' in w or '#' in w:
				continue
			if w+",POS_WORD" in word_context_counts:
				pos_term=math.log(word_context_counts[w+",POS_WORD"]*line_count/(word_counts[w]*context_counts["POS_WORD"]))
				if assume==1 and (pos_term<0):
					pos_term=0
			if w+",NEG_WORD" in word_context_counts:
				neg_term=math.log(word_context_counts[w+",NEG_WORD"]*line_count/(word_counts[w]*context_counts["NEG_WORD"]))
				if assume==1 and (neg_term<0):
					neg_term=0
			polarity.add((w,pos_term-neg_term))
			count2+=1
	sorted_count=sorted(polarity,key=lambda (k,v):v, reverse=True)
	#print "Len: "+str(len(sorted_count))
	#print "Len: "+str(len(polarity))
	#print count1
	#print count2
	fp.close()
	return sorted_count[:num],sorted_count[-1*num:]

def F1_F2_measures(filename,word_context_counts):
	f1=set()
	f2=set()
	fp=open(filename,'r')
	tot_words=0
	line_count=0
	sent_len=[]
	for line in fp:
		line=line.replace('\n','')
		text=line.split(' ')
		line_count+=1.0
		for w in text:
			if w in POS_WORD or w in NEG_WORD or '@' in w or '#' in w:
				continue
			tot_words+=1
			if w+",POS_WORD" not in word_context_counts:
				f1.add(w)
			if w+",NEG_WORD" not in word_context_counts:
				f2.add(w)
	#print "Avg. words per sentence: "+str(tot_words/line_count)
	#print list(f1)[:10]
	#print list(f2)[:10]
	return math.ceil((len(f1)+len(f2))/(tot_words/line_count))

def top_polarities_Laplace(filename='test2.txt',num=50,assume=1,flag=1,smooth=0.5): 
	#Flag=0 remove with count<500. 
	#Assume=0 implies dont add extra denominator term
	word_context_counts,word_counts,context_counts,line_count=PMI(filename)
	polarity=set()
	fp=open(filename,'r')
	count1=0
	count2=0
	f1=F1_F2_measures(filename,word_context_counts)
	for line in fp:
		line=line.replace('\n','')
		text=line.split(' ')
		count1+=1
		for w in text:
			pos_term=0
			neg_term=0
			if flag==0 and word_counts[w]<500:
				continue
			if w in POS_WORD or w in NEG_WORD or '@' in w or '#' in w:
				continue
			if w+",POS_WORD" in word_context_counts:
				if assume==1:
					pos_term=(word_context_counts[w+",POS_WORD"]*1.0)/(line_count+f1*smooth)
				else:
					pos_term=(word_context_counts[w+",POS_WORD"]*1.0)/(line_count)
			else:
				if assume==1:
					pos_term=(smooth)/(line_count+f1*smooth)
				else:
					pos_term=(smooth)/(line_count)
			if w+",NEG_WORD" in word_context_counts:
				if assume==1:
					neg_term=(word_context_counts[w+",NEG_WORD"]*1.0)/(line_count+f1*smooth)
				else:
					neg_term=(word_context_counts[w+",NEG_WORD"]*1.0)/(line_count)
			else:
				if assume==1:
					neg_term=(smooth)/(line_count+f1*smooth)
				else:
					neg_term=(smooth)/(line_count)
			polar_measure=math.log((pos_term*context_counts["NEG_WORD"])/(neg_term*context_counts["POS_WORD"]))
			polarity.add((w,pos_term-neg_term))
			count2+=1
	sorted_count=sorted(polarity,key=lambda (k,v):v, reverse=True)
	#print "Len: "+str(len(sorted_count))
	#print "Len: "+str(len(polarity))
	#print count1
	#print count2
	fp.close()
	return sorted_count[:num],sorted_count[-1*num:]

"""

pos_words,neg_words=top_polarities_PPMI(filename="tweets.txt",flag=1,assume=1)
print "With NO thresholding. Using PPMI"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

pos_words,neg_words=top_polarities_PPMI(filename="tweets.txt",flag=1,assume=0)
print "With NO thresholding. Using PPMI Variant"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

pos_words,neg_words=top_polarities_Laplace(filename="tweets.txt",flag=1,assume=1)
print "With NO thresholding. Using Laplace"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

pos_words,neg_words=top_polarities_Laplace(filename="tweets.txt",flag=1,assume=0)
print "With NO thresholding. Using Laplace variant"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

pos_words,neg_words=top_polarities_PPMI(filename="tweets.txt",flag=0,assume=0)
print "With thresholding. Using PPMI Variant"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

pos_words,neg_words=top_polarities_PPMI(filename="tweets.txt",flag=0,assume=1)
print "With thresholding. Using PPMI"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

pos_words,neg_words=top_polarities_Laplace(filename="tweets.txt",flag=0,assume=1)
print "With thresholding. Using Laplace"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

pos_words,neg_words=top_polarities_Laplace(filename="tweets.txt",flag=0,assume=0)
print "With thresholding. Using Laplace Variant"
print "Positive Terms: "+str([i[0] for i in pos_words])
print "Negative Terms: "+str([i[0] for i in neg_words])

"""
