# Overview
A machine learning model to classify scientific documents (articles and thesis) by field of study.
#
Available languages : Arabic, French, English.
#
Training set : 117976, Test set : 50558, Accuracy : 87%.
#
Available labels : 'Sciences and technology', 'Matter sciences', 'Mathematics and computer science', 'Natural and life sciences', 'Earth and universe sciences', 'Economics, marketing and management', 'Law and political sciences', 'Literature and foreign languages', 'social and human sciences', 'Sport and physical activities', 'Health sciences', 'Architecture and urban planning'.
# Use
from doc_classifier import classify
# 
summary = 'This article analyzes the basic classification of machine learning, including supervised learning, unsupervised learning, and reinforcement learning. It combines analysis on common algorithms in machine learning, such as decision tree algorithm, random forest algorithm, artificial neural network algorithm, SVM algorithm, Boosting and Bagging algorithm, BP algorithm. Through the development of theoretical systems, further improvement of autonomous learning capabilities, the integration of multiple digital technologies, and the promotion of personalized custom services, the purpose is to improve people's awareness of machine learning and accelerate the speed of popularization of machine learning.'
#
label = classify(summary)
#
print(label)
