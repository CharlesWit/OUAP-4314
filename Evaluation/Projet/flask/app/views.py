# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash, jsonify, Response, json
from app import app
from bson.json_util import dumps as dp
from pymongo import MongoClient


client = MongoClient()
db = client.OUAP
# db.musees.create_index([("appellation", "text"), ("adresse", "text"), ("bus", "text"), ("velib", "text")],
#     )
# db.jardins.ensure_index([("appellation", "text"), ("adresse", "text"), ("bus", "text"), ("velib", "text")],
#                         name="search_index")


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


@app.route('/jardins', methods=['GET', 'POST'])
def jardins():
    """
    La route pour la page d'accueil.

    Returns:
        render_template: le template musées.html qui définit la page d'accueil musées
    """

    results = db.jardins.find()
    res = dp(results)
    res = jsonify(res)
    # response = Response(
    #     response=json.dumps(results),
    #     status=200,
    #     mimetype='application/json'
    # )
    # results = json.dumps([e.toJSON() for e in results])
    return res


@app.route('/musees', methods=['GET', 'POST'])
def musees():
    """
    La route pour la page d'accueil.

    Returns:
        render_template: le template musees.html qui définit la page d'accueil musées
    """

    data_m = db.musees.find()
    a1 = "active"
    return render_template('musees.html', a1=a1, musees=data_m, t='Musées', h='Base des musées et lieux culturels')


    # results = db.musees.find()
    # res = dp(results)
    # res = jsonify(res)
    # # response = Response(
    # #     response=json.dumps(results),
    # #     status=200,
    # #     mimetype='application/json'
    # # )
    # return res


# @app.route("/search", methods=['GET'])
# def search():
#
#     # Rechercher une annonce : redirige vers la page de recherche
#
#     key = request.values.get("key")
#     refer = request.values.get("refer")
#     if key == "_id":
#         posts_l = musees.find({refer:ObjectId(key)})
#     else:
#         posts_l = musees.find({refer:key})
#     return render_template('search.html', posts=posts_l, t=title, h=heading)


#
# @app.route('/results', methods =['GET', 'POST'])
# def search_results(query):
#
#     if query is None :
#         query = ''
#     # query = request.form['q']
#     text_results = db.musees.find_one({'$text': {'$search': str(query)}})
#     doc_matches = (res['obj'] for res in text_results['results'])
#
#     if not doc_matches:
#         flash('No results found!')
#         return redirect('/')
#     else:
#         # display results
#         return render_template('results.html', results=doc_matches)
#
