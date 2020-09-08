import requests
import xml.etree.ElementTree as ET

# Get a real consumer key & secret from: https://www.goodreads.com/api/keys
CONSUMER_KEY = 'YOUR_KEY_HERE'

# search the Sunnyvale Library for the book
# Since I don't work for a library, they won't give me access to the bibliocommons APIs.
# So I have to use a workaound to do the search with the public search URL and return an URL to the book if it exists. 
def search_book(booktitle, author):

    r =requests.get('https://gateway.bibliocommons.com/v2/libraries/sunnyvale/rss/search?custom_edit=false&query=%28title%3A%28'+ booktitle + '%29%20AND%20contributor%3A%28' + author + '%29%20%29&searchType=bl&suppress=true&view=grouped&initialSearch=true')

    root = ET.fromstring(r.content)
    for child in root.iter('*'):
        if child.tag == "guid":
           return(child.text)

r = requests.get('https://www.goodreads.com/review/list/65514011.xml?key=' + CONSUMER_KEY + '&v=2&shelf=to-read&per_page=200&page=1')

root = ET.fromstring(r.content)

for attribute in root:
    for books in attribute.iter('review'):  
        for book in books.iter('book'): 
            name = book.find('title')
            for authors in books.iter('authors'):
                for author in authors.iter('author'):
                    author = author.find('name')
            print(name.text, "--", author.text)
            print(search_book(name.text.replace('#', ''), author.text))
            print('-------')
