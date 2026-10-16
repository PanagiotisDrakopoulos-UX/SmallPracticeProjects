f = open('testfile.txt','r')
content = f.read()

def count_words(textvalue):
    a = len(textvalue.split())
    return a  


count_words(content)

content