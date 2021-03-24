from flask import Flask, request, render_template, redirect # needed to specify explicitly to use this
from todo_app.flask_config import Config
from todo_app.model.trellomodel import *
from todo_app.trelloApiCalls import *

import requests

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def cards():
    # get secrets
    secrets = file_read("todo_app\secrets.txt")
    boardId = secrets[0]
    key =  secrets[1] 
    token = secrets[2]

    url = "https://api.trello.com/1/boards/{0}/lists" # root url could be stored and configured globally fpr re-use 

    query = {
        'key': key,
        'token': token
    }

    response = requests.request(
        "GET",
        url.format(boardId),
        params=query
    )

    boardLists = []

    results = response.json()

    for index, boardListItem in enumerate(results): 
        urlCards = "https://api.trello.com/1/boards/{0}/cards" # root url could be stored and configured globally fpr re-use 

        queryCards = {
            'key': key,
            'token': token,
            'idList': boardListItem["id"] ##doesnt seem to filter :-(
        }

        responseCards = requests.request(
            "GET",
            urlCards.format(boardId),
            params=queryCards
        )

        cardsLists = []

        #assumes ordered by position
        for cardItem in responseCards.json(): 
            if cardItem["idList"] == boardListItem["id"]:
                cardsLists.append(CardListItem(cardItem))

        idpreviousList = ""
        idnextList = ""

        if index == 0:
           idnextList = results[index+1]["id"]
        elif index == len(results) - 1:
           idpreviousList = results[index-1]["id"]
        else:    
           idnextList = results[index+1]["id"]
           idpreviousList = results[index-1]["id"]

        boardLists.append(BoardListClass(boardListItem, cardsLists, idpreviousList, idnextList ))
    
    return render_template("cards.html", cards = boardLists)

@app.route('/cards', methods=['POST']) # could be feasible to post entire card object back
def addCard():
    #read form data - newItem - submitted in the POST request
    newCard = request.form['newCard']
    secrets = file_read("todo_app\secrets.txt")
    boardId = secrets[0]
    key =  secrets[1] 
    token = secrets[2]   
    idList = secrets[3]   # first list

    url = 'https://api.trello.com/1/lists/{0}/cards'

    query = {
        'key': key,
        'token': token,
        'name' : newCard
    } 
    
    response = requests.request(
        "POST",
        url.format(idList),
        params=query
    )

    return redirect('/')

@app.route('/cards/moveCardUp/<idCard>/<idNextList>') #Put
def moveCardUp( idCard, idNextList):   

    secrets = file_read("todo_app\secrets.txt")
    boardId = secrets[0]
    key =  secrets[1] 
    token = secrets[2]   

    url = 'https://api.trello.com/1/cards/{0}'

    headers = {
    "Accept": "application/json"
    }

    query = {
        'key': key,
        'token': token,
        'idList' : idNextList
    } 
    
    response = requests.request(
        "PUT",
        url.format(idCard),
        headers=headers,
        params=query,
    )

    return redirect('/')


@app.route('/cards/moveCardUp/<idCard>/<idPreviousList>') #Put
def moveCardDown( idCard, idPreviousList):   

    secrets = file_read("todo_app\secrets.txt")
    boardId = secrets[0]
    key =  secrets[1] 
    token = secrets[2]   

    url = 'https://api.trello.com/1/cards/{0}'

    headers = {
    "Accept": "application/json"
    }

    query = {
        'key': key,
        'token': token,
        'idList' : idPreviousList
    } 
    
    response = requests.request(
        "PUT",
        url.format(idCard),
        headers=headers,
        params=query,
    )

    return redirect('/')


def file_read(fname):
        content_array = []
        with open(fname) as f:
                #Content_list is the list that contains the read lines.     
                for line in f:
                        content_array.append(line.rstrip())
        
        return content_array


if __name__ == '__main__':
    app.run()
