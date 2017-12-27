import random
import os
import numpy as np
def avg_length(PATH):
	tot_sum=0
	count=0
	fp=open(PATH,'r')
	lengths=[]
	for line in fp:
		length=int(line.split(',')[0])
		lengths.append(length)
		#if count<10:
		#	#print length
		tot_sum+=length
		count+=1.0
	print "Max Length: "+str(max(lengths))
	print "Min Length: "+str(min(lengths))
	print "Median Length: "+str(np.median(lengths))
	print "1st Quartile: "+str(np.percentile(np.array(lengths),25,axis=0))
	print "2nd Quartile: "+str(np.percentile(np.array(lengths),50,axis=0))
	print "3rd Quartile: "+str(np.percentile(np.array(lengths),75,axis=0))
	return str(tot_sum/count)

print "Conversation: "+avg_length("/home/sanjay/NLP_Project/Conversation/features3.txt")
print
print "Hotel Review: "+avg_length("/home/sanjay/NLP_Project/Hotel/features3.txt")
print
print "Twitter: "+avg_length("/home/sanjay/NLP_Project/Twitter/untitled folder/features3.txt")
