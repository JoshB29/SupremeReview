from __future__ import print_function
import re
import sys
import math
import os
import numpy as np
import openpyxl
#import statsmodels.api as sm # recommended import according to the docs
#import pandas as pandas

#Printing with interpolation
def p(my_string):
	print(my_string.format(**globals()),end="",sep="")

#String interpolation
#def i(my_string):
#        return ({my_string}.format(**globals()))
def chomp(L):
    L=L.rstrip()
    return L
#Split a string based on the seperator
#e.g v=split(L,"\t")
#will split L based on tabs
def split(L,sep):
    v=L.split(sep)
    return v
#Join an array to a string
def sjoin (v,sep):
	v_s=sep.v.join()
	return(v_s)

#Substitue part of a string for another (i.e. string replacement)
#a[4]=s(a[4],".pdb","")
#will replae ".pdb" with nothing
#*args can contain an optional argument, which is how many maximum do you want to replace
#e.g. L=s(L,"\t","-",1); will substitue the first occurance only of tab
def s(L,string,substitute,*args):

    L=str.replace(L,string,substitute,*args);
    return L

#Printing with interpolation
#e.g. p("{v[0]}\t{v[1]}\t{v[0]}\\n")
#Note that for this function all variables must have braces ({}) around them (e.g. {v[1]}). Also new line must be "\\n", not "\n"
def p(my_string):
    my_string=my_string.format(**globals())
    print(my_string,end="",sep="")

#get rownames of data frame
def rownames(data_frame):
	returnlist(data_frame.index)

#import modules/functions from a file
def source (file_1):
	exec(open(file_1).read())
	return

#get the intersection between two lists
def intersection(list_1,list_2):
	return(list(set(list_1) & set(list_2)))

#given two lists, return the members of the first list not in the second list
def setdiff(list_1,list_2):
	return(list(set(list_1)-set(list_2)))

#assign names to a list in an R sort of fashion (named lists)
def names(list,names):
    return(pandas.Series(list_1,index=list_2))

#Does the variable exist? returns 1 if yes and 0 if not
def exists(var):
	output=1
	try:
		var
	except NameError:	
		output=0

#is the variable equal to None, not the same as doe not exist
def isnone(var):
	output=0
	if not var:
		output=1
	return(output)
#def shift(list_1):
#	list_1.pop[0]
#	return(list_1)

#translate lowercase to upercase
def lowerupper (string_1):
	trantab = maketrans("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	return(string_1.translate(trantab))
#translate lowercase to upercase
def upperlower (string_1):
	trantab = maketrans("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	return(string_1.translate(trantab))

#retrun a numeric vector
def as_numeric (list_1):
	list_1 = list(map(int, list_1))
	return(list_1)

#This function calculates the maximum information gain between a list given a gold standard, It calculates if for all the potential split points and returns split point that gives the maximum information.
#list 1 is a namedList where the names are names and the value is the value of each instance
#list 2 is the gold standard (which will be given a label of 1)
def informationGain(list_1,list_2):
	#sort the data from heighest to lowest
	values=unique(sorted(list_1,reverse=1))
	gold_standard_data=intersection(list_1.names,list_2.names)
	gold_standard_data=namedList(gold_standard_data)
	gold_standard_data.names=gold_standard_data
	gold_standard_length=len(gold_standard_data)
	dict_1=dict(zip(list_1.names, list_1))
	#Get values for gold standard
	gold_standard_data.data = itemgetter(*gold_standard_data.names)(dict_1)
	negative_set_data=setdiff(list_1.names,gold_standard_data.names)
	negative_set_data=namedList(negative_set_data)
	negative_set_data.names=negative_set_data
	negative_set_data.data=itemgetter(*negative_set_data.names)(dict_1)


	gold_standard_length=len(gold_standard_data)
	negative_standard_length=len(negative_set_data)
	total_length=len(list_1)
	negative_set_data_A = np.array(negative_set_data.data)
	gold_standard_data_A=np.array(gold_standard_data.data)
	information_gain_old=0
	information_gain_max=0
	split_point=max(values)
	#now for each value point, find the information gain
	for i in range(len(values)):
	
		neg_up=np.sum(negative_set_data_A >= values[i])
		gold_up=np.sum(gold_standard_data_A >= values[i])
		total_up=neg_up+gold_up
		prob_neg_up=neg_up/total_up
		prob_gold_up=gold_up/total_up
		#I add a very small to the probabilities to that we are not taking a log of zero
		prob_gold_up=prob_gold_up+.000000000001
		prob_neg_up=prob_neg_up+.000000000001
		prob_gold_down=((gold_standard_length-gold_up)/total_length)+.000000000001
		prob_neg_down=((negative_standard_length-neg_up)/total_length)+.000000000001
		#prob_gold_down=abs(1-prob_gold_up)
		#prob_neg_down=abs(1-prob_neg_up)
		my_information_gain=-1*((prob_gold_up*math.log(prob_gold_up,2)+prob_neg_up*math.log(prob_neg_up,2))+ (prob_gold_down*math.log(prob_gold_down,2)+prob_neg_down*math.log(prob_neg_down,2)))
		#print(my_information_gain)
		if my_information_gain > information_gain_max:
			information_gain_max=my_information_gain
			split_point=values[i]
			#This is the split point that gives the highest information.
			split_point_index=i
	
	#you can also modify this to return the split point/index. The split point is the point within the feature that splits to the best information.		
	#print(split_point)
	return(information_gain_max)


#Remove non-unique from list, equivelent to bash uniq
def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def cd(directory):
	os.chdir(directory)
	return

#perform a system command
def bash(string_1):
	os.system(string_1)
	return
#Get ecdf from list
def plot_ecdf (list_1):
	ecdf = sm.distributions.ECDF(list_1)
	x = np.linspace(min(list_1), max(list_1))
	y = ecdf(x)
	plt.step(x, y)
	plt.show()

#read in dataframe from text file with no header
def readdataframe_noheader(file_1):
	df=pandas.read_table(file_1,header=None)
	return(df)

#read in dataframe from text file with no header
def readdataframe_header(file_1):
	df=pandas.read_table(file_1)
	return(df)
#reverse a string, so that "josh" becomes "hsoj"
def reverse_string(string_1):
	string_1=string_1[::-1]
	return(string_1)

#given a list, remove elements that are comments (ie., start with a "#")
def remove_comment_line(list_1):
	list_to_return=[]
	for i in list_1:
		i=str(i)
		m=re.search(r'^\s*#',i)
		if m:
			continue
		list_to_return.append(i)
	return(list_to_return)
#aliases
#f is float
f=float

#given an openpyxl excel workbook of a sheet and a column name, (e.g. 'A', return a column as a list
def return_list_from_excel_column(work_sheet,column_letter):
	list_to_return=[]
	list_1=work_sheet[column_letter]
	#print(list_1)
	#y=0
	for x in range(len(list_1)-1):
		#print(x)
		list_to_return.append(list_1[x].value)
		#y=y+1 
	return(list_to_return)

# A Dynamic Programming based Python program for edit
# distance problem
# This code is contributed by Bhavya Jain, I got based it on from http://www.geeksforgeeks.org/dynamic-programming-set-5-edit-distance/
def editDistDP(str1, str2):
	#str2 (n) is the columns, str1 (m) is the rows
    m=len(str1)
    n=len(str2)
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    #print(dp)
    # Fill d[][] in bottom up manner
    for i in range(m+1):
        for j in range(n+1):
            # If first string is empty, only option is to
            # isnert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    #print(dp)
    list_to_return=[dp[i][j],dp]
   
    return dp[m][n]
    #return list_to_return
    #return dp

#This is also the edit distance, except that it finds the edit distance of for a local match (i.e. substring)
#In this function:
#x=editDistLocalMatch("josuaboyde","mynameisjoshuabroyde")
#x will equal 2 (i.e. the "h" and "r")
#Note that in this function, str1 must be shorter than str2
def editDistLocalMatch(str1, str2):
	#str2 (n) is the columns, str1 (m) is the rows
    m=len(str1)
    n=len(str2)
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    #print(dp)
    # Fill d[][] in bottom up manner
    for i in range(m+1):
        for j in range(n+1):
            # If first string is empty, only option is to
            # isnert all characters of second string
            if i == 0:
                dp[i][j]=0 #jb added initializes the 
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    #print(dp)
    #list_to_return=[dp[i][j],dp]
   
    return min(dp[m])
    #return list_to_return


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')