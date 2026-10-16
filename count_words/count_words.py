#Count Words in a String
#Counts the number of individual words in a string. For added complexity read these strings in from a text file and generate a summary.

f = open('testfile.txt','r')
content = f.read()

def count_words(textvalue):
    a = len(textvalue.split())
    return a  


count_words(content)

content
