# -*- coding: utf-8 -*-

import requests
import pymongo
from bs4 import BeautifulSoup
import re

headers_musees = {
    'Origin': 'https://meslieux.paris.fr',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'application/json, text/plain, /',
    'Referer': 'https://meslieux.paris.fr/musees-municipaux',
    'Connection': 'keep-alive',
    'Content-Length': '0',
}

params = (
    ('m_tid', '67'),
    ('limit', '500'),
    ('order', 'name ASC'),
    ('lat', '48.8742'),
    ('lon', '2.38'),
)

headers_jardins = {
    'Origin': 'https://meslieux.paris.fr',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'application/json, text/plain, /',
    'Referer': 'https://meslieux.paris.fr/principaux-parcs-et-jardins',
    'Connection': 'keep-alive',
    'Content-Length': '0',
}


t = str.maketrans("äâàéèëêïîöôüûù'", "aaaeeeeiioouuu ")

client = pymongo.MongoClient('localhost', 27017)
client.drop_database('OUAP')
database = client.OUAP
musees = database.musees
jardins = database.jardins

REGFUL = r"(\d{1,3})?(\s|,)*(b[is]*|t[er]*)?\s*(avenue|arcade|boulevard|cite|cours|chemin|carrefour|rue|ruelle|" \
         r"route|square|parc|parvis|pont|promenade|port|faubourg|passage|hameau|gal|galerie|voie|chaussee|peristyle|" \
         r"esplanade|allee|impasse|place|villa|quai)\s((d.{1,2}\s|d')?\s?(l.{1,2}\s|l')?\s?(\b\w+\s?|\.?){1,5})"


def ajoute_adresse(elem_json):
    """
    Fonction renvoyant un dictionnaire contenant les elements d'une adresse
    Args:
        elem_json (dict): un element du json de la page scrapée
    Returns:
        dict: un dictionnaire contenant les elements de l'adresse contenue dans le json
    """
    adresse = elem_json['address']
    adresse = adresse.translate(t).replace("-", " ").replace("\ ", "'")
    reg = re.findall(REGFUL, adresse, re.IGNORECASE)
    ad_dict = {}
    for i in reg:
        if i[0]:
            ad_dict["numero"] = i[0]
        elif not i[0]:
            ad_dict["numero"] = ""
        if i[3]:
            ad_dict["voie"] = i[3]
        if i[4]:
            ad_dict["nom_voie"] = i[4]
    
    ad_dict['ville'] = elem_json['city']
    ad_dict["code_postal"] = elem_json['zip_code']

    return ad_dict


def ajoute_horaires(elem_json):
    """
    Fonction renvoyant un dictionnaire contenant les elements d'une adresse
    Args:
        elem_json (dict): un element du json de la page scrapée
    Returns:
        dict: un dictionnaire contenant les elements de l'adresse contenue dans le json
    """
    horaires = elem_json['calendars']
    h_dict = {}
    for key, value in horaires.items():
        open_close = value[:2][0][:2]
        if open_close[0] == 'closed':
            h_dict[key] = ['closed']
            continue
        
        h_dict[key] = open_close

    return h_dict


def ajoute_infos(elem_soup):
    """
    Fonction qui renvoi les informations du lieu
    """
    info_html = elem_soup.find("div", attrs={"itemprop": "description"})
    return info_html.text.strip()


def ajoute_velib(elem_soup):
    """
    Args:
        elem_soup: un élement de type BeautifulSoup
    Returns:
        dict: un dictionnaire avec numéro de station et adresse
    """
    v_dict = {}
    for elem in elem_soup.find_all(class_="information"):
        if re.search("Velib", elem.text):
            liste_station = elem.text.split('\n')[3:-3]
            for station in liste_station:
                elem = station.split(',')
                v_dict[elem[0]] = elem[1]
    
    return v_dict


def ajoute_bus(elem_soup):
    """
    Args:
        elem_soup: un élement de type BeautifulSoup
    Returns:
        list: une liste des numéros de ligne de bus
    """
    list_ = []
    for elem in elem_soup.find_all(class_="information"):
        reg = re.search(r"Bus\s?(:|n°)?\s?((\d*,?\s?)*)", elem.text)
        if reg:
            liste_bus = reg.group(2).split(",")
            for ligne in liste_bus:
                list_.append(re.search(r"(\d+)", ligne).group(1))
    
    return list_


def scrap(response_json):
    """
    Fonction qui ajoute les informations contenues dans response_json dans collection
    Args:
        response_json: le json de la page scrappée
    Returns:
        list: une liste des documents à insérer
    """
    list_ = []
    for elem in response_json:
        loc_dict = {"lat": elem['lat'], "lon": elem['lon']}
        ad_dict = ajoute_adresse(elem)
        h_dict = ajoute_horaires(elem)
        
        url = "http://equipement.paris.fr/" + elem['name'].lower().translate(t).replace(" ", "-") + "-" + elem['idequipement']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        infos = ajoute_infos(soup)
        velib = ajoute_velib(soup)
        bus = ajoute_bus(soup)

        list_.append({"appellation": elem['name'],
                      "adresses": ad_dict,
                      "locs": loc_dict,
                      "buss": bus,
                      "velibs": velib,
                      "infos": infos,
                      "horaires": h_dict})

    return list_


def add_database(mus, jar):
    """
    Fonction qui ajoute tous les elements à la database (jardins et musees municipaux)
    """
    response_musees = requests.post('https://meslieux.paris.fr/proxy/data/get/equipements/get_equipements', headers=headers_musees, params=params)
    response_jardins = requests.post('https://meslieux.paris.fr/proxy/data/get/equipements/get_equipements', headers=headers_jardins, params=params)

    mus.insert_many(scrap(response_musees.json()))
    jar.insert_many(scrap(response_jardins.json()))


add_database(musees, jardins)

