from bs4 import BeautifulSoup
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from requests import get

def render(source_html):
    class Render(QWebEngineView):
        def __init__(self, html):
            self.html = None
            self.app = QApplication([])
            QWebEngineView.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.setHtml(html)
            while self.html is None:
                self.app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
            self.app.quit()

        def _callable(self, data):
            self.html = data

        def _loadFinished(self):
            self.page().toHtml(self._callable)

    return Render(source_html).html

def search(x):
    query=str(x)
    query = query.replace(" ", "+")
    url='https://www.google.com/search?q=' + query
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    sample_html = get(url, headers=headers).text
    soup = BeautifulSoup(render(sample_html), "html.parser")
    res = soup.find('span', attrs={'class': 'cwcot'})
    if res==None:
        res = soup.find('div', attrs={'class': 'kno-fb-ctx', 'aria-level':'3', 'role':'heading'})
        if res==None:
            res = soup.find('div', attrs={'class': 'kno-rdesc'})
            if res==None:
                res = soup.find('span', attrs={'class': 'st'})
                res = res.get_text()
                a= soup.find_all('a')
                a=a[15]
                link=a['href']
                res= res + "/n <a href=\"%s\">Більше читайте тут</a>" % link
    try:
        res = res.get_text()
        return (res)
    except:
        res=res
        return (res)

# print (search("україна"))