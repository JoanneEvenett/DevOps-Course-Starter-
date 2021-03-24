from flask import Flask, request, render_template, redirect # needed to specify explicitly to use this
from todo_app.flask_config import Config
from todo_app.model.trellomodel import *
from todo_app.trelloApiCalls import *

import requests, logging

app = Flask(__name__)
app.config.from_object(Config)
log = logging.getLogger(__name__)


@app.route('/')
def cards():

    boardLists = []
    results = GetListsOnBoard()

    for index, boardListItem in enumerate(results): 
       
        cardsLists = []
        responseCards = GetCardsonBoard(boardListItem["id"])

        #default ordering by position (as per created sequence)
        for cardItem in responseCards: 
            if cardItem["idList"] == boardListItem["id"]:
                cardsLists.append(CardListItem(cardItem))

        idpreviousList = ""
        idnextList = ""

        #crude, but retrieving the previous and next list, required for page to move
        if index == 0:
           idnextList = results[index+1]["id"]
        elif index == len(results) - 1:
           idpreviousList = results[index-1]["id"]
        else:    
           idnextList = results[index+1]["id"]
           idpreviousList = results[index-1]["id"]

        boardLists.append(BoardListClass(boardListItem, cardsLists, idpreviousList, idnextList))
    
    return render_template("cards.html", cards = boardLists)

@app.route('/cards', methods=['POST'])
def addCard():
    newCard = request.form['newCard']
    AddCardtoFirstList(newCard)

    return redirect('/')

@app.route('/cards/moveCardUp/<idCard>/<idNextList>') 
def completeTask( idCard, idNextList):   

    MoveCard(idCard, idNextList)

    return redirect('/')


@app.route('/cards/moveCardUp/<idCard>/<idPreviousList>') 
def redoTask( idCard, idPreviousList):   

    MoveCard(idCard, idPreviousList)

    return redirect('/')


@app.route('/cards/<idCard>/<descriptionCard>/<duedate>') # TODO could be feasible to post entire card object back?
def updateTask( idCard, descriptionCard, duedate):  

    log.info(descriptionCard)
    UpdateCard(idCard, descriptionCard, duedate)

    return redirect('/')

if __name__ == '__main__':
    app.run()
