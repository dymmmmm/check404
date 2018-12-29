import urllib.request
from multiprocessing.pool import ThreadPool
from requests_html import HTMLSession

class check_404(object):
    def __init__(self, urls):
        self.urls = urls

    def check_url(self, url):
        result = {}
        result['url'] = url
        try:
            result['code'] = urllib.request.urlopen(url).getcode()

        except urllib.request.URLError as e:
            if hasattr(e, 'code'):
                result['code'] = e.code
            else:
                result['code'] = e

        return result

    def get_results(self):
        pool = ThreadPool(processes=len(self.urls))
        results = [pool.apply_async(self.check_url, (url,)) for url in self.urls]
        data = []

        for res in results:
            data.append(res.get())

        return data

if __name__ == "__main__":
    url = ['http://facebook.com', 'http://google.com', 'http://facc.io', 'http://www.google.com/dsa','http://www.baidu.com']
    #url =[ 'http://www.baidu.com','http://www.qq.com']
    #url = ['http://facc.io']

    checker = check_404(url)
    results = checker.get_results()
    for result in results:
        if result['code']!= 200:
            print("URL: {0} \nSTATUS: {1}\n".format(result['url'], result['code']))
            url.remove(result['url'])
        else:
            print("URL: {0} \nSTATUS: {1}\n".format(result['url'], result['code']))
    #print(url)

    urls = []
    session = HTMLSession()
    for x in url:
         r = session.get(x)
         for y in r.html.links:
            urls.append(y)
    #print(urls)

    urls_new = []
    for x in urls:
       if x.startswith( 'http://' ) or x.startswith( 'https://' ) or x.startswith( 'www.' ):
           urls_new.append(x)
    #print(urls_new)
    #print(len(urls_new))

    if len(urls_new)!= 0:
       checker = check_404(urls_new)
       results = checker.get_results()
       for result in results:
         #print(result['code'])
         print("URL: {0} \nSTATUS: {1}\n".format(result['url'], result['code']))
         with open('200.txt', 'a') as f:
             f.write(result['url'] + '\n')