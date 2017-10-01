#SupremeReview Overview
Each year, thousands of litigants petition The Supreme Court of the United States (SCOTUS) to hear their cases and overturn a lower court's ruling. However, only a few percentage of these cases are actually heard by the court; most petitions are denied. SupremeReview is a computational approach for predicting which cases SCOTUS will hear, given the text of a lower court's decision.
**Supreme Review predicts which cases will be heard by SCOTUS and which will not.** 
SupremeReview predictions be generated using the code in this repository or at the following website:http://www.supremereview.online/.

#SupremeReview Methodology
SupremeReview uses logistic regression on features derived from Court of Appeal (CoA) decisions. I retrieved from the 11 court of appeals circuits 9,451 decisions (from the years 2010-2015) were one of the litigants appealed to SCOTUS to review (and thus possibly overturn) the ruling. Note that the decision of SCOTUS to review the cases does **not** mean that the repeal the ruling. It simply means that SCOTUS agrees to take the case.

The workflow of SupremeReview is shown below:

