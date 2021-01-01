import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import string

#BeautifulSoup is basically used to get content from the web and scrap it

path = '/Users/rajanrai/Documents/Books/pg2680.epub' #change for a particular book

#get path of the epub file, then turn it to a list of HTML, each HTML is a chapter 
#extract the HTML out of the epub file using the “item.get_content()"
def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

# Now first get the noise bracket out and choose the type
# of content I want, then I scrape it all, put it in a text variable
# apply it on every HTML of a chapter, and then I will have a list of texts of each chapter.

blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script']

# Define a function that turns a single HTML into a single text that is clean of the unwanted elements:
def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

# Utilise the previous function to create another one that turns a list of HTML into a list of clean text
def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

# The function that takes the path to our Epub file, and gives as an output Its text
def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

out = epub2text(path)

lst = list()
for line in out:    
    line = line.strip()
    lst.extend(line.split('\n'))
    
dictionary = {}
excluded_words = ['a' , 'about', 'after', 'all','also', 'an', 'and', 'another', 'any', 'are', 'as', 'at', 'be'
                  , 'because', 'been', 'before', 'being', 'both', 'but', 'by', 'came', 'come', 'can','could','did'
                  , 'do', 'for', 'from', 'get', 'got', 'had', 'has', 'he', 'her', 'have', 'him','his','he', 'himself',
                  'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'like', 'me', 'made', 'many',
                  'might', 'my', 'much', 'most', 'not', 'never', 'now', 'of', 'on', 'only', 'or', 'other', 'out',
                  'said', 'same', 'see', 'she', 'should', 'still', 'some','such', 'than', 'that', 'the', 'them',
                  'their', 'there', 'then', 'therefore', 'these', 'they', 'this', 'those', 'to', 'too', 'was',
                  'way', 'we', 'well', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'will','with',
                  'would', 'you', 'your', 'here', 'up', 'down', 'must', 'asked',
                 'it\'s', 'so', 'thou', 'things', 'unto', 'h2', 'thy', ' thee', 'doth', 'no', 'thyself', 'how', 'whatsoever',
                 'furthermore', 'more', 'may', 'shall','upon', 'hath', 'thing', 'let', 'nor', 'anything','itself', 'shalt',
                 'hast', 'though', 'dost','whom','why','either', 'unto', 'thee', 'one', 'yet', 'very', 'anchor']

# prints 1 dictionary with words and corresponding count whilst ignoring words in exclusion list
for line in lst:
    line = line.translate(line.maketrans('','',string.punctuation))
    line = line.lower()
    words = line.split()
    words = [item for item in words if item.isalpha()]
    for word in words:
        if word not in excluded_words:
            dictionary[word] = dictionary.get(word, 0) + 1

# 1 list for every pair is a tuple                  
empty_list = list()
for key, value in dictionary.items():
    new_tuple = (value, key)
    empty_list.append(new_tuple)
                  
sort = sorted(empty_list, reverse=True)  
for key, value in sort:
    print(value, key) 
