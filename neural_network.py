import pandas as pd
from sklearn.model_selection import train_test_split  
from sklearn.neural_network import MLPClassifier 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

df_input = pd.read_csv("input.csv",sep='\t')
df_input1 = df_input.drop('Unnamed: 0', axis=1)

x = df_input1.iloc[:, 0:-1]
y = df_input1.iloc[:,-1]

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3,stratify=y, random_state=21)
mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=822,random_state=21 ,verbose=10)

mlp.fit(X_train, y_train)

##To store our model :
import pickle
filename = 'machinel.sav'
pickle.dump(mlp, open(filename, 'wb'))

##To restore :
model=pickle.load(open(filename, 'rb'))
