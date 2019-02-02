import os
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
from operator import itemgetter
from sklearn.feature_extraction.text import CountVectorizer

####################Creation of our BOW ( bag_of_words)#######################
## Transform a file to a list of paragraphs
def parag_file(direc, file):
    os.chdir(direc)
   	all_paragraphs = []
    with open(file , 'r') as f:
        for line in f:
            try:
                myliste = sent_tokenize(line)
                if myliste != []:
                   	all_paragraphs.append(myliste)
            except UnicodeDecodeError:
                continue
    return	all_paragraphs
	all_paragraphs = parag_file(direc, file)

## Transform the list of all paragphaes to n_grams: the varibale n to determine the number of n_grams
def file_to_ngrams(all_paragraphs, n):
    lista = []
    for line in	all_paragraphs:
        ngram = list(ngrams(line[0], n, pad_left=True, pad_right=True ,left_pad_symbol=' ', right_pad_symbol=' '))
        for tupl in ngram:
            lista.append(tupl)
    return lista

##join ngrams to 1 char
def ngram_join(lista):
    ngram_list = []
    for tupl in lista:
        ngram_list.append(''.join(tupl))
    return ngram_list

##Create a dictionary to contain : n_grams and their frequencies
def ngram_freq_file(ngram_list):
    ngrams_statistics = {}

    for ngram in ngram_list:
        if ngram in ngrams_statistics.keys():
            ngram_occurrences = ngrams_statistics[ngram]
            ngrams_statistics.update({ngram:ngram_occurrences+1})
        else:
            ngrams_statistics.update({ngram:1})
    return ngrams_statistics

##Sort this dictionary to choose the first tops
def sorting_storing(ngrams_statistics, direc, file):
    os.chdir(direc)
    ngrams_statistics_sorted = sorted(ngrams_statistics.items(),key=itemgetter(1),reverse=True)
    with open(file, 'w') as f:
        for key, value in ngrams_statistics_sorted:
            f.write(key + ":" + str(value) + '\n')

##Apply this function for all files to a specific language 
def parcours_dir(direc,direc_dest):
    os.chdir(direc)
    list_files = os.listdir(direc)
    for file in list_files:
        try : 
           	all_paragraphs = paragraph_file(direc, file)
        except UnicodeDecodeError:
            continue
        lista = file_to_ngrams(all_paragraphs, 3)
        ngram_list = ngram_join(lista)
        ngrams_statistics = ngram_freq_file(ngram_list)
        sorting_storing(ngrams_statistics,direc_dest, file)
        #sorting(ngrams_statistics,ngrams_statistics_sorted_all)


##sort ngrams_staictcs and add them to a new dictionary ( a global variable) for each language 
ngrams_statistics_sorted_all_fran=[]
ngrams_statistics_sorted_all_espa=[]
ngrams_statistics_sorted_all_ital=[]
ngrams_statistics_sorted_all_port=[]

def sorting(ngrams_statistics , ngrams_statistics_sorted_all):
    ngrams_statistics_sorted_all.extend(sorted(ngrams_statistics.items(),key=itemgetter(1),reverse=True)[:10])

##Apply all that to a directory ( language)
def parcours_dir(direc , ngrams_statistics_sorted_all):
    os.chdir(direc)
    list_files = os.listdir(direc)
    for file in list_files:
        try : 
            l_paragraphs = paragraph_file(direc, file)
        except UnicodeDecodeError:
            continue
        lista = ngrams_file(l_paragraphs, 3)
        ngram_list = ngram_join(lista)
        ngrams_statistics = ngram_freq_file(ngram_list)
        #sorting_storing(ngrams_statistics, "/Users/macbook/portugais", file)
        sorting(ngrams_statistics, ngrams_statistics_sorted_all)


## Sort list of n_grams
def tri_liste(liste,n):
    ll=[]
    liste=sorted(liste,key=itemgetter(1),reverse=True)
    ll.append(liste[0][0])
    for i in range(len(liste)):
        if liste[i][0] not in ll:
            ll.append(liste[i][0])
    return ll[:n]
#l=tri_liste(ngrams_statistics_sorted_all_fran,500)
#lspa=tri_liste(ngrams_statistics_sorted_all_espa,500)
#lita=tri_liste(ngrams_statistics_sorted_all_ital,500)
#lpor=tri_liste(ngrams_statistics_sorted_all_port,500)

##store it ( just keys)
def stock(l,file):
    with open(file, 'w') as f:
        for elt in l:
            f.write(elt+'\n')


##Convert file to list
def convert(file):
    dict_in = {}
    N=0
    with open(file,'r') as df:
        lines = [line.replace('\n','').split(":") for line in df]
        for line in lines:
            dict_in[line[0]] = int(line[1])
            N+=int(line[1])
    return dict_in

 ## to count frequencies
 def count_freq(d):
    n=0
    for val in d.values():
        n+=val
    return n


##convert our files to one bow 
def bag_of_words(list_of_ngrams):
	bow=[]
	for file in list_of_ngrams:
	    with open (file,'r') as f:
	        for line in f :
	            bow+=sent_tokenize(line)
	return bow


# convert bow to bow _final
def bow_final(bow):
	dic_bow={}
	bow_sorted=[]
	bow_sorted_best=[]
	dic_bow = ngram_freq_file(bow)
	bow_sorted=sorted(dic_bow.items(),key=itemgetter(1))
	bow_sorted_best =[k for k in bow_sorted if  k[1] < 3]
	bow_final = []
	for elt in bow_sorted_best:
	    bow_final.append(elt[0])
	return bow_final



######################Feature Vectors##########################
df_columns = []
df_columns.extend(bow_final)
df_columns.extend(["langue"])
zeros = zeros(shape=(9450,len(df_columns)))
df_fr = pd.DataFrame(zeros, columns=df_columns)
zeros = zeros(shape=(9433,len(df_columns)))
df_es = pd.DataFrame(zeros, columns=df_columns)
zeros = zeros(shape=(9434,len(df_columns)))
df_pt = pd.DataFrame(zeros, columns=df_columns)
zeros = zeros(shape=(9486,len(df_columns)))
df_it = pd.DataFrame(zeros, columns=df_columns)

##insert_into_df_frequencies
def insert_into_df(direc,liste,df,k):
    os.chdir(direc)
    list_files = os.listdir(direc)
    for i in range(len(list_files)):
        try :
            d={}
            d=convert(list_files[i])
            n=count_freq(d)
            for elt in liste:
                for key,val in d.items():
                    if elt==key:
                        df[elt][i]=val/n
                        df.iloc[i,-1]=k
        except UnicodeDecodeError:
            continue

df_fr_clean = df_fr[df_fr.langue!=0]
df_es_clean = df_es[df_es.langue!=0]
df_pt_clean = df_pt[df_pt.langue!=0]
df_it_clean = df_it[df_it.langue!=0]
df_final = pd.concat([df_fr_clean[:9392],df_es_clean[:9392],df_pt_clean[:9392],df_it_clean[:9392]])
#Transform data frame to csv
df_final.to_csv("input.csv",sep='\t', encoding='utf-8')
