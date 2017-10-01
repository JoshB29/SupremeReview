# SupremeReview--Will SCOTUS Take Your Case?
Analysis of Court of Appeals Decisions to predict which cases the Supreme Court will grant hearings to.

# Overview
Each year, thousands of litigants petition The Supreme Court of the United States (SCOTUS) to hear their cases and overturn a lower court's ruling. However, only a few percentage of these cases are actually heard by the court; most petitions are denied. SupremeReview is a computational approach for predicting which cases SCOTUS will hear, given the text of a lower court's decision. While there are geneneral established for manually judging which cases SCOTUS will take (in technical legal terms, this called granting *writ of certiorari*), SupremeReview assigns a quantitative probability (using logistic regression) for any case for whether it will be heard.

See the "Methodology" section for more information regarding how SupremeReview was trained, and its performance.

# Use
SupremeReview relies on analyzing Court of Appeal Decisions, after extracting features from the decisions (a percentage of which were heard by SCOTUS), a logistic classifier is trained to predict which cases will be heard and which not. The final score is scalar between 0 and 1, where 1 represents the highest possible score of the case being heard by SCOTUS, and 0 represents the lowest possible score.

## SCOTUS_analysis_Final.ipynb
There are two python scripts provided. The first, SCOTUS_analysis_Final.ipynb, is an iPython notebook that trains the SupremeReview classifier using logistic regression. This script reads  a list of files that represent IDs of cases that take the following form:

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



Methodology
