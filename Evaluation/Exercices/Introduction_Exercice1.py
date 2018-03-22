# Introduction - Exercice 1

import requests


class HTTPReq:

    def __init__(self, timeOut = 10):
        self.UserAg = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        self.TimeOut = timeOut
        print(self.TimeOut)

    def httprq(self, url):
        rp = requests.get(url, headers={'User-Agent': self.UserAg}, timeout=self.TimeOut)
        if rp.status_code != 200:
            rp = HTTPReq(self.TimeOut).httprq(url)
        return rp


# req = HTTPReq()
# rep = req.httprq("http://www.apple.com")
# print(rep)
