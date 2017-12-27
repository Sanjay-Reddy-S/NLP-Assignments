from bs4 import BeautifulSoup
import urllib2
import xml.etree.ElementTree as ET
import os

import warnings
warnings.filterwarnings("ignore")

"""
url="https://twitter.com/AntonGBR/status/426120567146573824"
content=urllib2.urlopen(url).read()
soup=BeautifulSoup(content)
print soup.title.string


files=[]
for file in os.listdir('.'):
	if file.endswith(".xml"):
		files.append(file)
	if file=='truth.txt':
		gt_file=file

ground_truth={}
fp=open(gt_file,'r')
for line in fp:
	line=line.replace('\n','')
	text=line.split(':::')
	ground_truth[text[0]+'.xml']=[text[1],text[2]]

text=[]
file_names=[]
files=["0a9e35fd6f123137d585a482f2484d8e.xml"]
for file in files:
	tree = ET.parse(file)
	root=tree.getroot()
	count=int(root[0].attrib['count'])
	print count
	for i in range(count):
		url=str(root[0][i].attrib['url'])
		print "URL: "+url
		content=urllib2.urlopen(url).read()
		soup=BeautifulSoup(content,"lxml")
		sent=soup.title.string
		print sent
		text.append(sent)
		file_names.append(file)

for i in range(len(text)):
	print text[i]
"""
def xml_to_txt():
	files=[]
	for file in os.listdir('.'):
		if file.endswith(".xml"):
			files.append(file)
		if file=='truth.txt':
			gt_file=file

	ground_truth={}
	fp=open(gt_file,'r')
	for line in fp:
		line=line.replace('\n','')
		text=line.split(':::')
		ground_truth[text[0]+'.xml']=[text[1],text[2]]

	text=[]
	age=[]
	gender=[]
	file_names=[]

	# for file in files:
	# 	tree = ET.parse(file)
	# 	root=tree.getroot()
	# 	count=int(root[0].attrib['count'])
	# 	for i in range(count):
	# 		text.append(root[0][i].text)
	# 		gender.append(ground_truth[file][0])
	# 		age.append(ground_truth[file][1])
	# 		file_names.append(file)
	fp1=open("text.txt",'a+')
	fp2=open("gender.txt",'a+')
	fp3=open("age.txt",'a+')
	fp4=open("file_names.txt",'a+')
	file_count_var=0
	for file in files:
		print str(file_count_var)+' : '+file
		tree = ET.parse(file)
		root=tree.getroot()
		count=int(root[0].attrib['count'])
		#print count
		for i in range(count):
			if i>100:
				print i
				for i in range(len(text)):
					sent=text[i].encode('utf-8')
					idx1=sent.find(':')
					sent=sent.replace('\n',' ')
					sent=sent[idx1+3:-1]+'\n'
					fp1.write(sent)
					fp2.write(gender[i]+'\n')
					fp3.write(age[i]+'\n')
					fp4.write(file_names[i]+'\n')
				text=[]
				age=[]
				gender=[]
				file_names=[]
				break
			elif i%10==0:
				print i
				for i in range(len(text)):
					sent=text[i].encode('utf-8')
					idx1=sent.find(':')
					sent=sent.replace('\n',' ')
					sent=sent[idx1+3:-1]+'\n'
					fp1.write(sent+'\n')
					fp2.write(gender[i]+'\n')
					fp3.write(age[i]+'\n')
					fp4.write(file_names[i]+'\n')
				text=[]
				age=[]
				gender=[]
				file_names=[]
			try:
				url=str(root[0][i].attrib['url'])
			except:
				break
			#print "URL: "+url
			try:
				content=urllib2.urlopen(url).read()
			except urllib2.HTTPError:
				print "FileName:"+str(i)+" "+str(file)
				#continue
				break
			soup=BeautifulSoup(content,"lxml")
			sent=soup.title.string
			#print sent

			text.append(sent)
			gender.append(ground_truth[file][0])
			age.append(ground_truth[file][1])
			file_names.append(file)
		file_count_var+=1
	
	fp1.close()
	fp2.close()
	fp3.close()
	fp4.close()

xml_to_txt()