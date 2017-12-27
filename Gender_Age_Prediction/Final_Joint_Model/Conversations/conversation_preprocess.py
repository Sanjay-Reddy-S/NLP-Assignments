import xml.etree.ElementTree as ET
import os
import nltk
import enchant

d1=enchant.Dict("en_US")

age_dict={'10s\r':'13-17','10s':'13-17','20s\r':'23-27','20s':'23-27','30s\r':'33-37','30s':'33-37'}

def xml_to_txt():
	files=[]
	fp_0=open('files_labels.txt','r')
	for file in fp_0:
		file=file.replace('\n','')
		if file.endswith(".xml"):
			files.append(file)
		
	gt_file="truth.txt"

	ground_truth={}
	fp=open(gt_file,'r')
	for line in fp:
		if len(line)<3:
			continue
		line=line.replace('\n','')
		text=line.split(':::')
		if '\r' in text[2]:
			text[2]=text[2].replace('\r','')
		if len(text)>=4 and '\r' in text[3]:
			text[3]=text[3].replace('\r','')
		try:
			if len(text)>=4:
				ground_truth[text[0]+'.xml']=[text[1],age_dict[text[2]],text[3]]
			else:
				ground_truth[text[0]+'.xml']=[text[1],age_dict[text[2]]]
		except:
			print line
			print text
			return

	text=[]
	age=[]
	gender=[]
	file_names=[]
	criminal=[]
	file_count_var=0

	fp1=open("text.txt",'a')
	fp2=open("gender.txt",'a')
	fp3=open("age.txt",'a')
	fp4=open("file_names.txt",'a')
	fp5=open("criminal.txt",'a')

	for file in files:
		file_count_var+=1
		#if file_count_var>=116830:
		#	break
		if file_count_var%100==0:
			for i in range(len(text)):
				text[i]=text[i].replace('\t','')
				sent=text[i].encode('utf-8')
				fp1.write(sent+'\n')
				fp2.write(gender[i]+'\n')
				fp3.write(age[i]+'\n')
				fp4.write(file_names[i]+'\n')
				fp5.write(criminal[i]+'\n')
			text=[]
			gender=[]
			age=[]
			file_names=[]
			criminal=[]

		print str(file_count_var)+' : '+file
		tree = ET.parse('en/'+file)
		root=tree.getroot()
		count=int(root[0].attrib['count'])
		file_short=file.split('_')[0]
		for i in range(count):
			text_add=root[0][i].text
			if text_add==None or len(text_add)<3:
				break
			if '<' in text_add or '>' in text_add:
				break
			text_add=text_add.replace('\n','.')
			text_add=text_add.replace('\r','.')
			text.append(text_add)
			gender.append(ground_truth[file_short+'.xml'][0])
			age.append(ground_truth[file_short+'.xml'][1])
			if len(ground_truth[file_short+'.xml'])>=3:
				criminal.append(ground_truth[file_short+'.xml'][2])
			else:
				criminal.append("None")
			file_names.append(file)
	
	if file_count_var%100!=0:
		for i in range(len(text)):
			text[i]=text[i].replace('\t','')
			sent=text[i].encode('utf-8')
			fp1.write(sent+'\n')
			fp2.write(gender[i]+'\n')
			fp3.write(age[i]+'\n')
			fp4.write(file_names[i]+'\n')
			fp5.write(criminal[i]+'\n')
		text=[]
		gender=[]
		age=[]
		file_names=[]
		criminal=[]	

	fp1.close()
	fp2.close()
	fp3.close()
	fp4.close()
	fp5.close()
#116830
def no_of_punc_line(line):
	count=0
	punc=['.',',','!','?',':']
	for i in line:
		if i in punc:
			count+=1
	return count

def count_wrong(text):
	count=0
	for word in text:
		if d1.check(word)==False:
			count+=1
	return count

def pos_statistics(pos_text):
	tag_fd = nltk.FreqDist(tag for (word, tag) in pos_text)
	dict_col={'adjectives':0,'punc':1,'adverb':2,'noun':3,'verb':4,'interjection':5,'preposition':6,'article':7,'pronoun':8}
	stats=[0]*len(dict_col)
	for tup in tag_fd.most_common():
		if 'RB' in tup[0]:
			stats[dict_col['adverb']]+=tup[1]
		elif 'NN' in tup[0]:
			stats[dict_col['noun']]+=tup[1]
		elif '.' in tup[0]:
			stats[dict_col['punc']]+=tup[1]
		elif 'JJ' in tup[0]:
			stats[dict_col['adjectives']]+=tup[1]
		elif 'VB' in tup[0]:
			stats[dict_col['verb']]+=tup[1]
		elif 'UH' in tup[0]:
			stats[dict_col['interjection']]+=tup[1]
		elif 'IN' in tup[0]:
			stats[dict_col['preposition']]+=tup[1]
		elif 'PRP' in tup[0] or 'WP' in tup[0]:
			stats[dict_col['pronoun']]+=tup[1]
		elif 'DT' in tup[0]:
			stats[dict_col['article']]+=tup[1]
	return stats

fet_names=['Total Chars','Total Words','Incorrect Words']#'POS_Ones(Variable)'

def f_measure(pos_stats):
	dict_col={'adjectives':0,'punc':1,'adverb':2,'noun':3,'verb':4,'interjection':5,'preposition':6,'article':7,'pronoun':8}
	nouns=pos_stats[dict_col['noun']]
	adjectives=pos_stats[dict_col['adjectives']]
	prep=pos_stats[dict_col['preposition']]
	article=pos_stats[dict_col['article']]
	pro=pos_stats[dict_col['pronoun']]
	verb=pos_stats[dict_col['verb']]
	adv=pos_stats[dict_col['adverb']]
	inter=pos_stats[dict_col['interjection']]
	return 0.5*((nouns+adjectives+prep+article)-(pro+verb+adv+inter)+100)

def words_to_fet():
	fp1=open('text.txt','r')
	fp2=open('features.txt','w')
	for line in fp1:
		if line=='\n':
			continue
		fet_values=[0]*len(fet_names)
		line=line.replace('\n','')
		# gender=fp2.readline()
		# gender.replace('\n','')
		# age=fp3.readline()
		# age.replace('\n','')
		text=nltk.word_tokenize(line)
		pos_text=nltk.pos_tag(text)
		for i in range(len(fet_names)):
			if i==0:
				fet_values[i]=len(line)
			elif i==1:
				fet_values[i]=len(pos_text)
			elif i==2:
				fet_values[i]=count_wrong(text)
				print fet_values[i]
		pos_stats=pos_statistics(pos_text)
		for i in pos_stats:
			fet_values.append(i)
		F_measure=f_measure(pos_stats)
		fet_values.append(F_measure)
		for i in range(len(fet_values)):
			fp2.write(str(fet_values[i]))
			if i!=len(fet_values)-1:
				fp2.write(",")
			else:
				fp2.write("\n")
	fp2.close()

xml_to_txt()