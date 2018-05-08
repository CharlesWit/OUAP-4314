from flask import render_template, request, redirect, flash

from .forms import Search

from app import app
from pymongo import MongoClient


client = MongoClient()
db = client.OUAP
db.musees.create_index([("appellation", "text"), ("adresse", "text"), ("bus", "text"), ("velib", "text")],
                       name="search_index")
db.jardins.ensure_index([("appellation", "text"), ("adresse", "text"), ("bus", "text"), ("velib", "text")],
                        name="search_index")


def poi_by_name(appellation):
    """
    Retourne une liste d'adresses d'un POI selon son appellation

    Args:
        appellation: le nom d'un POI (musée ou jardin)

    Returns:
        document["adresse"]: l'adresse complète d'un musée
    """
    document = db.musees.find_one({'appellation': appellation})
    adresse = document["adresses"]
    return adresse


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    La route pour la page d'accueil.

    Returns:
        render_template: le template index.html qui contient le formulaire de recherche
    """

    search = Search()
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)


@app.route('/results', methods =['GET', 'POST'])
def search_results(query):

    if query is None :
        query = ''
    # query = request.form['q']
    text_results = db.musees.find_one({'$text': {'$search': str(query)}})
    doc_matches = (res['obj'] for res in text_results['results'])

    if not doc_matches:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=doc_matches)

