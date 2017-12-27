import random

def no_of_functions(text):
	return text.count("public static")

def no_of_single_comments(text):
	lines=text.split('\n')
	count=0
	len_comments=[]
	for line in lines:
		if '//' in line:
			count+=1
			idx=line.find('//')
			len_comments.append(len(line)-(idx+2))
	return (count,len_comments)

def no_of_multiple_comments(text):
	lines=text.split('\n')
	count=0
	lines_modified=[]
	comment_len=[]
	i=0
	print text
	while(i <(len(lines))):
		if '/*' not in lines[i]:
			lines_modified.append(lines[i])
		else:
			#print "Before anything..."
			#print lines_modified
			lines_modified.append(lines[i])
			i+=1
			while('*/' not in lines[i]):
				lines_modified[-1]+=(" "+lines[i])
				i+=1
			lines_modified[-1]+=(lines[i])
		i+=1
	for line in lines_modified:
		print line
	
	for line in lines_modified:
		if '/*' in line:
			count+=1
			comment_len.append(len(line))
	return (count,comment_len)


def average_variable_length(text):
	lines=text.split('\n')
	total_len=0
	count_variables=0
	#for line in lines:

fp=open('sample_code_3.txt',"r")
text=""
for line in fp:
	text+=(line)

print no_of_multiple_comments(text)
print no_of_single_comments(text)