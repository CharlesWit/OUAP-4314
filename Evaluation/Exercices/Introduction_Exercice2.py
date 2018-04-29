# Introduction - Exercice 2

import requests
from Introduction_Exercice1 import HTTPReq


def remove_spaces(string):
    return ' '.join(string.split())


def toReadableHTML(string):
    tmp = string.split()
    return ' '.join()   # Faux


print(remove_spaces("You        know   those  days when       you get   the  mean    reds?"))

# rep = HTTPReq(5).httprq("http://www.apple.com")
# print(rep)
