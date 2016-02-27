
from bs4 import BeautifulSoup
import time

'''Note: these functions aren't fully generalized to all ebook formats yet'''


def get_soups_from_ebook(fname):
    '''Break apart an ebook by open-close xml tags into a list of BeautifulSouop objects'''
    raw = get_epub_content(fname, True)
    subsections = []
    idx = raw.find('<?xml')
    while idx != -1:
        end_idx = raw[idx:].find('</html>')+7 + idx
        subsections.append(raw[idx:end_idx])
        #print(subsections[-1][305:360])
        idx = raw[end_idx:].find('<?xml')
        if idx == -1:
            break
        idx += end_idx
    soups = []
    for subsec in subsections:
        soups.append(BeautifulSoup(subsec, 'lxml'))
    return soups

def get_epub_content(path, keep_html=False):
    '''Get the plain text from an ebook'''
    import epub
    book = epub.open_epub(path)
    data = ""
    for item in book.opf.manifest.values():
        content = book.read_item(item)
        if str(content)[:3] == "b'<":
            data += content.decode("utf-8")
    if not keep_html:
        data = strip_html(data)
    return data

def strip_html(s):
    '''Remove html tags to return formatted text'''
    from html.parser import HTMLParser
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = ""
            self.body = False
        def handle_starttag(self, tag, attrs):
            if tag == 'body':
                self.body = True
        def handle_endtag(self, tag):
            if tag == 'p':
                self.result += '\n'
            if tag == 'body':
                self.body = False
        def handle_data(self, data):
            if self.body:
                self.result += data
    parser = MyHTMLParser()
    parser.feed(s)
    return parser.result
