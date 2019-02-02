import re
import string


def cleaning(file):
    with open(file, 'r') as f1:
        text = f1.read()
        #removing tags , using regex
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr, '', text)
        text = text.lower()
 		    # punctuation + digits
        for e in string.punctuation + string.digits :
            text = text.replace(e ," ")
            
    with open(file, 'w') as f2:
        f2.write(text)

#directory=language
def all_directory(direc):
    os.chdir(direc)
    list_files = os.listdir(direc)
    for file in list_files:
        cleaning(file)
