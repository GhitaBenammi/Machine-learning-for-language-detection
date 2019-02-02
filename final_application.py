import os
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
from operator import itemgetter
from sklearn.feature_extraction.text import CountVectorizer
import re
import string
import pandas as pd
from numpy import zeros
import pickle 

##we will use a file to store the text that we want to predict 
##then , we will clean this file 
##transform it to a bow 
##transform bow to data-frame

def remove_brack(file):
    with open(file, 'r' , encoding="utf-8") as f1:
        text = f1.read()
        #les balises
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr, '', text)
        text = text.lower()
         # punctuation + digits
        for e in string.punctuation + string.digits :
            text = text.replace(e ," ")
            
    with open(file, 'w' , encoding="utf-8") as f2:
        f2.write(text)

def paragraph_file(file):
    #os.chdir(direc)
    l_paragraphs = []
    with open(file , 'r' , encoding='utf-8') as f:
        for line in f:
            try:
                myliste = sent_tokenize(line)
                if myliste != []:
                    l_paragraphs.append(myliste)
            except UnicodeDecodeError:
                continue
    return l_paragraphs

def ngrams_file(l_paragraphs, n):
    lista = []
    for line in l_paragraphs:
        ngram = list(ngrams(line[0], n, pad_left=True, pad_right=True ,left_pad_symbol=' ', right_pad_symbol=' '))
        for tupl in ngram:
            lista.append(tupl)
    return lista

def ngram_join(lista):
    ngram_list = []
    for tupl in lista:
        ngram_list.append(''.join(tupl))
    return ngram_list

def ngram_freq_file(ngram_list):
    ngrams_statistics = {}

    for ngram in ngram_list:
        if ngram in ngrams_statistics.keys():
            ngram_occurrences = ngrams_statistics[ngram]
            ngrams_statistics.update({ngram:ngram_occurrences+1})
        else:
            ngrams_statistics.update({ngram:1})
    return ngrams_statistics

def count_freq(d):
    n=0
    for val in d.values():
        n+=val
    return n

def bag_of_words(file):
    bow=[]
    with open (file,'r' , encoding="utf-8") as f:
        for line in f :
            bow+=sent_tokenize(line)
    return bow

def insert_into_df(df , liste ,d):
    n=count_freq(d)
    #print(n)
    for elt in liste:
        for key,val in d.items():
            if elt==key:
                #print(elt)
                df[elt][0]=val/n
                #print(df[elt][0])

##In this function , we will bring together all the previous functions 
def main(file):
    d = {

        1 : "Français",
        2 : "Espagnol",
        3 : "Portugais",
        4 : "Italien"
    }

    remove_brack(file)
    l_paragraphs = paragraph_file(file)
    lista=ngrams_file(l_paragraphs, 3)
    ngram_list=ngram_join(lista)
    ngrams_statistics=ngram_freq_file(ngram_list)
    bow=bag_of_words("bow_final.txt")
    df_columns = []
    df_columns.extend(bow)                     
    yeros = zeros(shape=(1,len(df_columns)))
    df_test = pd.DataFrame(yeros, columns=df_columns)
    insert_into_df( df_test, bow, ngrams_statistics )
    filename = 'machinel.sav'
    model = pickle.load(open(filename, 'rb')
    y_pred = model.predict(df_test)
    return  d[y_pred[0]]


##pred=main("test.txt")
##pred

#######################################graphic interface#################################################
from tkinter import *
import sys
char="waiting...."
def mHello():
    mtext=ment.get()
    with open("test.txt", 'w' , encoding="utf-8") as f:
        f.write(mtext)
    print(mtext)
    pred=main("test.txt")
    mlabel2=Label(mGui,text=pred, font='Time 14 bold' ,fg= "#e64e4e").place(x=350,y=300)
    return


mGui= Tk()
ment= StringVar()



background_image=PhotoImage(file="IMGBG.gif")
background_label = Label(mGui, image=background_image)
background_label.photo=background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
mGui.title(" Language Detection")

window_x = 764
window_y = 546
screen_x = int (mGui.winfo_screenwidth())
screen_y = int (mGui.winfo_screenheight())
posX = (screen_x // 2) - (window_x // 2)
posY = (screen_y // 2) - (window_y // 2)
geo = "{}x{}+{}+{}".format(window_x,window_y,posX,posY)
mGui.geometry(geo)



mlabel=Label(mGui,text="Entrer votre text ci-dessous", font='Time 18 bold', fg= "#940d0d").place(x=245,y=120)

mbutton= Button(mGui, relief=GROOVE, text="VALIDER", command= mHello, fg= "white", bg="#940d0d", font='Time 10 bold', width=10).place(x=350,y=250)
#mbutton= Button(mGui, text="VALIDER", command= mHello, fg= "white", bg="#940d0d", font='Time 10 bold', width=10).pack()
mEntry = Entry(mGui, textvariable=ment, width=70).place(x=190,y=200)



mGui.mainloop()

