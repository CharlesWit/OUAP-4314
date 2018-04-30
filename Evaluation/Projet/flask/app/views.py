from flask import render_template, request, redirect, flash

from .forms import POIForm, Search

from app import app
from pymongo import MongoClient


client = MongoClient()
db = client.OUAP
db.musees.ensure_index([("appellation", "text"), ("adresse", "text"), ("bus", "text"), ("velib", "text")],
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


# def kardesh(query):
#     """
#     This function deals with queries across multiple collections. For example, for a comic with a specific author and/or series name.
#     If the query has the keys author_name and/or series_name, an additional query parses the authors and/or series collections in order
#     to retrieve the list of ids matching the authors and/or series name. This retrieve list is used as a condition for the initial query:
#     the authors/series id must belong to the list of ids previously retrieved.
#
#     Args:
#         query: a mongo formatted query string
#
#     Returns:
#         query: the updated query with matching author and/or series ids
#     """
#     if query.get("author_name"):
#         list_author_id = []
#         fetch_name = query["author_name"]
#
#         query_match = {}
#         query_match.update({'$or': [{'last_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
#                                 {'first_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
#                                 {'nickname': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
#                                 ]})
#         for document in db["authors"].find(query_match):
#             list_author_id.append(document["_id"])
#         # author_name is removed from the keys because it does not appear in the series and comics collections
#         query.pop("author_name")
#         query.update({"author_id": {"$in": list_author_id}})
#
#     if query.get("series_name"):
#         list_series_id = []
#         fetch_name = query["series_name"]
#
#         query_match = {}
#         query_match.update({"name": {'$regex': "\\b" + fetch_name.strip(), '$options': 'i'}})
#
#         for document in db["series"].find(query_match):
#             list_series_id.append(document["_id"])
#
#         # series_name is removed because it does not exist in the comics collection
#         query.pop("series_name")
#         query.update({"series_id": {"$in": list_series_id}})
#
#     return query

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


@app.route('/results')
def search_results(query):

    # query = request.form['q']
    text_results = db.Runcommand('text', search=str(query), limit=None)
    doc_matches = (res['obj'] for res in text_results['results'])

    if not doc_matches:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=doc_matches)


# @app.route('/museum', methods=['POST'])
# def museum():
#     """
#     The route for the author result page when the user submits a form for a query of the authors collection.
#     A redirection to an author's specific page is proposed.
#
#     Returns:
#         render_template: the template page is author.html and the output contains first_name, last_name, nickname, birth_date and death_date.
#         Birth_date and death_date are datetime variables which are formatted into day-month-year format.
#         The page also includes a redirection to a specific author's page thanks to the redirect_author added to the returned document.
#         This redirect_author is processed differently from the rest. It is further explained in the jinja template macros.html.
#     """
#     output = {}
#     author_form = AuthorForm()
#     if author_form.validate_on_submit():
#         list_document = []
#
#         fetch_name = request.form.get('name', None).strip()
#         fetch_country = request.form.get('country', None).strip()
#
#         mongo_formatted_string = {}
#
#         if fetch_name:
#             mongo_formatted_string.update({'$or': [{'last_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
#                                         {'first_name': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
#                                         {'nickname': {'$regex': "\\b" + fetch_name, '$options': 'i'}},
#                                         ]})
#         if fetch_country:
#             mongo_formatted_string.update({'country': {'$regex': "\\b" + fetch_country, '$options': 'i'}})
#
#         if mongo_formatted_string:
#             for document in db["authors"].find(mongo_formatted_string):
#                 document_updated = {"redirect_author": ["/author/{0}".format(document["_id"]), "Go."]}
#                 document_updated.update({key: (document[key] if document.get(key) else "") for key in ("first_name", "last_name", "nickname", "birth_date", "death_date")})
#                 if document_updated.get("death_date"): document_updated.update({"death_date": "{:%d-%m-%Y}".format(document["death_date"])})
#                 if document_updated.get("birth_date"): document_updated.update({"birth_date": "{:%d-%m-%Y}".format(document["birth_date"])})
#                 list_document.append(document_updated)
#             output["list_document"] = list_document
#
#     return render_template('author.html', output=output)

