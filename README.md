# SupremeReview-Will SCOTUS Take Your Case?
Analysis of Court of Appeals Decisions to predict which cases the Supreme Court will grant hearings to.

# Overview
Each year, thousands of litigants petition The Supreme Court of the United States (SCOTUS) to hear their cases and overturn a lower court's ruling. However, only a few percentage of these cases are actually heard by the court; most petitions are denied. SupremeReview is a computational approach for predicting which cases SCOTUS will hear, given the text of a lower court's decision. While there are geneneral established for manually judging which cases SCOTUS will take (in technical legal terms, this called granting *writ of certiorari*), SupremeReview assigns a quantitative probability (using logistic regression) for any case for whether it will be heard.
SupremeReview predictions be generated using the code in this repository or at the following website:http://www.supremereview.online/.

See the "Methodology" document for more information regarding how SupremeReview was trained its performance.

# Use
SupremeReview relies on analyzing Court of Appeal Decisions, after extracting features from the decisions (a percentage of which were heard by SCOTUS), a logistic classifier is trained to predict which cases will be heard and which not. The final score is scalar between 0 and 1, where 1 represents the highest possible score of the case being heard by SCOTUS, and 0 represents the lowest possible score.

There are two python scripts provided:
## SCOTUS_analysis_Final.ipynb
This is an iPython notebook that trains the SupremeReview classifier using logistic regression. This script reads  a list of files that represent IDs of cases that take the following form:

    ID   label    file_location

Where ID is a number identifier for the case, the label is whether it was heard by the court, and  file_locationis the path to a plain text file of the court of appeals decision. For example:

    ID      label   file_location
    0810835 1       /Users/joshuabroyde/Projects/Supreme_Court_Data/All_Decisions/text/0810835.txt
    081423  1       /Users/joshuabroyde/Projects/Supreme_Court_Data/All_Decisions/text/081423.txt
    081438  1       /Users/joshuabroyde/Projects/Supreme_Court_Data/All_Decisions/text/081438.txt

This script will produce a number of files in the directory it is run in:
    
    finalized_model.sav: The final logistic regression model
    features_to_use.txt: Features used by the model
    output_predictions.csv: Output predictions for the files that were analyzed.
    
As well as a ROC curve showing the model performance, and an bargraph showing feature importance.

## SCOTUS_new_document.py

This script will take a new document and run it through the logistic classifier to predict whether it will be heard by SCOTUS. The path to the classifier must be provided, as well as a path to the original decisions trained on. Note that this script takes a PDF of the new decision. This script can be run from the command line:

   python ~/Scripts/SCOTUS_new_document.py New_Decision.pdf
   
**Supreme Review predicts which cases will be heard by SCOTUS and which will not.** 
SupremeReview predictions be generated using the code in this repository or at the following website:http://www.supremereview.online/.

# SupremeReview Methodology
SupremeReview uses logistic regression on features derived from Court of Appeal (CoA) decisions. I retrieved from the 11 court of appeals circuits 9,451 decisions (from the years 2010-2015) where one of the litigants appealed to SCOTUS to review (and thus possibly overturn) the ruling. Note that the decision of SCOTUS to review the cases does **not** mean that the repeal the ruling; it simply means that SCOTUS agrees to take the case. Of these 9,451 cases 148 were actually reviewed by SCOTUS.

The workflow of SupremeReview is shown below:
![pj_0004](https://user-images.githubusercontent.com/29230946/31057895-51282d48-a6b8-11e7-9e00-d370d316c58d.jpg)

Specifically, after the PDF of each decision was converted into text, features (in the form of unigrams) were extracted. There were a total of 34 features: a bag of words approach was used to detect the presence of the words "dissent" and "disagree" in each decision. Similarily, the length of each decision (in the form of a word count) was calculated. Finally, the Term-Frequency Inverse Document Frequency algorithm was used to calculate the relevence scores for all words with at least 10 characters that were present in at least 2000 of the documents (i.e. 20% of the entire corpus).

I then appliedLogistic regression  to this entire feature matrix, treating it as classification problem; decisions that were not heard by SCOTUS were assigned a label of 0, and decisions that were heard by SCOTUS were given a label of 1.  L2 regularization and 10 by 10 fold Kfold repeated cross-validation. The ROC curve for these results are shown below:

![pj_0005](https://user-images.githubusercontent.com/29230946/31057943-631a5eb2-a6b9-11e7-806c-7afbaab63c32.jpg)

In the ROC curve, the yellow line shows the clasifier performance. At a flase positive rate of 7%, a true positive rate of 50% was achieved. This is a true positive rate 7 times greater than random.

#Feature Importance

A subset of feature importances are shown below. In the Y axis, the features are displayed, while the actual feature importance is shown on the X axis (calculated by taking the regression coefficient normalized by the standard deviation of the feature values). Note that in this plot all of the features are unigram TF-IDF scores, except for word-count, which is the word count of the document, and the dissent feature, which is given a 1 if the word dissent is the document and 0 if not.

![pj_0007](https://user-images.githubusercontent.com/29230946/31057965-c709d56a-a6b9-11e7-87de-ed448b2c931a.jpg)

#Miscellaneous Issues

A common issue with unbalanced classification problems (such as the one faced in this project) is overfitting. Thus, I compared the logistic classifier described above to a similair approach, except artifically creating a balanced classifier. In this alternate approach, I sampled half of the granted decisions, and a sample *of the same size* from the not granted the decisions. After training a logistic classifier, I then evaluated the performance on the rest of the decisions. A plot of the scores is shown below:


![pj_0010](https://user-images.githubusercontent.com/29230946/31058065-64cb6b32-a6bb-11e7-935f-be4d3a15b2ad.jpg)

Note that the balanced classifer has an average score of 19%, while the balanced classifier has an average has an average score of on 2.5%. Since, in reality, only about 1.6% of cases petitioned to SCOTUS are actually heard, the unbalanced classifier in this case provides a more realistic score, and is thus the final model used in the analysis and on the corresponding website.




