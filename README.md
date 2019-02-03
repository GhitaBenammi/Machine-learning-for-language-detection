# Machine-learning-for-language-detection: Text Classification using python, scikit-learn and NLTK  , Neural Network(MLP)

Introduction:
In natural language processing, language identification or language guessing is the problem of determining which
natural language given content is in . We will focus just on Frensh , Spanish , Portuguese and Italian.

Abstract:
1-download the data set from http://www.statmt.org/europarl/ ( download==>"source release"==>choose: Fr , es , pt , it)
2-Extract features from text files ( cleaning.py + feature_preparation.py)
3-Running ML algorithms , we will use MLP ( libraries =>scikit-learn and NLTK )

More details:
##First , don't forget to install nltk :)
1-Text files are actually series of words (ordered). In order to run machine learning algorithms we need to convert the text
files into numerical feature vectors. 
We will be using bag of words model for our example.
Our bag-of-words will contain n-grams 
Then, we need to get the frequency distribution of the words in all files (TF), We need to covert the text corpus into the feature vectors
2-Building a Classifier:
After cleanup, it is time to build the classifier to identify language of each file
There are many algorithms to choose from, we will use a neural network (espacially MLP) Classifier and train the model on the training set.




###########################If there are any omissions or mistakes, please do not hesitate to let me know.
###########################Email : ghitabenammi@gmail.com





<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3 MAKE CODE NOT WAR <3<3<3<3<3<3<3<3<3<3<3<3<3<3<3
