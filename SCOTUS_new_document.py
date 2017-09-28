
import sqlite3
from bs4 import BeautifulSoup
import re
import sys
import math
import os
import optparse
import json
import time
import matplotlib.pylab as plt
import requests
import pandas as pandas
import numpy
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn import metrics
import sklearn
import pickle
import random
import math
import seaborn
import statistics
import nltk

exec(open("/Users/joshuabroyde/Scripts/Modules/myFunctions.py").read())
#get the new input file
file_1=sys.argv[1]
#file_1="/Users/joshuabroyde/dummy_example/137980.pdf"
the_model="/Users/joshuabroyde/Projects/Supreme_Court_Data/All_Decisions/SCOTUS-notebook/other_notebook/finalized_model.sav"
features_to_use_location="/Users/joshuabroyde/Projects/Supreme_Court_Data/All_Decisions/SCOTUS-notebook/other_notebook/features_to_use.txt"
tf_idf_location="/Users/joshuabroyde/Projects/Supreme_Court_Data/All_Decisions/SCOTUS-notebook/other_notebook/tf_idf_scores.txt"
tf_idf_scores=pickle.load(open(tf_idf_location,'rb'))
features_to_use=pickle.load(open(features_to_use_location,'rb'))
loaded_model = pickle.load(open(the_model, 'rb'))

#iris = load_iris()
df=readdataframe_header("/Users/joshuabroyde/Projects/Supreme_Court_Data/All_Decisions/SCOTUS_certiorari_short.tsv")
#for now, exclue cases with a column labal=2, these are remanded cases
df=df[df.label != 2]
df[df["label"].isnull()]
df=df.dropna()
#remove nulls


#process the file
os.system("pdftotext {file_1}   input_to_script.txt".format(**locals()))
df2=pandas.DataFrame(columns=df.columns)
df2.loc[1,"ID"]=11111
df2.loc[1,"label"]=0
df2.loc[1,"file_location"]="input_to_script.txt"
df=df2

#merge the query with the new documents
#df=pandas.concat([df,df2],ignore_index=True)

#create feature data frame, that has the same number of rows as the first data frame
#df_features = pandas.DataFrame(index=df.index)
df_features=pandas.DataFrame(0,columns=features_to_use.columns,index=df.index)

#start adding features row by row
#df_features["Decision_length"] = np.nan
#get the length of the decision
for index,row in df.iterrows():
	file_location=row[2]
	#print(file_location)
	#get decision length
	f= open(file_location, 'r',encoding="ISO-8859-1").read()
	#word count
	decision_length=len(f.split())
	df_features.loc[index,"Decision_length"]=decision_length
	#df_features.loc[index] = pandas.Series({"Decision_length" : decision_length})
	#print(str(index))

#does the opinion have the word "disagree", indicating possible disagreement with precident. 1 means it uses the phrase
#df_features["disagree_left"] = np.nan
for index,row in df.iterrows():
	file_location=row[2]
	#print(file_location)
	f= open(file_location, 'r',encoding="ISO-8859-1").read()	#word 
	m=re.search("disagree",f)
	add=0
	if m:
		add=1
	df_features.loc[index,"disagree_left"] = add
	#print(str(index))

for index,row in df.iterrows():
	file_location=row[2]
	#print(file_location)
	f= open(file_location, 'r',encoding="ISO-8859-1").read()	#word 
	m=re.search("dissent",f)
	add=0
	if m:
		add=1
	df_features.loc[index,"dissent_others"] = add
	#print(str(index))


#get all unigrams from the text
all_text=""
for index,row in df.iterrows():
    file_location=row[2]
    #print(file_location)
    f= open(file_location, 'r',encoding="ISO-8859-1").read()	#word 
    text =f
    all_text=all_text+text
   #print(index)

#get unigram word tokens
all_text_list=list()
for index,row in df.iterrows():
    file_location=row[2]
    #print(file_location)
    f= open(file_location, 'r',encoding="ISO-8859-1").read()	#word 
    text =f
    all_text_list.append(text)
    #print(index)

#unigrams = nltk.word_tokenize(all_text)
#unigram_count=nltk.Counter(unigrams)


#perform TF-IDF on the corpus of the text
vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(
                        use_idf=True, 
                        norm=None, 
                        smooth_idf=False, 
                        sublinear_tf=False, 
                        binary=False,
                        min_df=1, max_df=1.0, max_features=None,
                        strip_accents='unicode', # retira os acentos
                        ngram_range=(1,1), preprocessor=None,              stop_words=None, tokenizer=None, vocabulary=None
             )

tf_idf_result = vectorizer.fit_transform(all_text_list)
idf = vectorizer.idf_
#print (dict(zip(vectorizer.get_feature_names(), idf)))

tf_idf_scores_local=dict(zip(vectorizer.get_feature_names(), idf))

#convert the tfidf resultsto the feature dataframe
tf_idf_matrix=tf_idf_result.todense()
df_tfidf=pandas.DataFrame(tf_idf_matrix)

#append these features to the feature 
df_tfidf.columns=vectorizer.get_feature_names()

#intersection with features trained on:

intersect_1=intersection(features_to_use.columns,df_tfidf.columns)
for i in intersect_1:
	try:
		score=tf_idf_scores[i]
		score_2=float(df_tfidf[i])
		final_score=score*score_2
		df_features[i]=final_score
	except:
		pass


predicted=loaded_model.predict_proba(df_features)
#predicted=loaded_model.predict_proba(df_features.iloc[-1].values.reshape(-1,len(df_features.columns)))
#all_positives=[i[1] for i in predicted]

base_line_probability=0.027835888533322816
#base_line_probability=statistics.mean(all_positives)*100
query_probability=predicted[0][1]
increased_probabiluity=query_probability/base_line_probability
print(query_probability)
