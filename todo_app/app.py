from flask import Flask, request, render_template, redirect # needed to specify explicitly to use this
from todo_app.flask_config import Config
from todo_app.model.trellomodel import *
from todo_app.trelloApiCalls import *

import requests, logging
from datetime import datetime


def create_app():    
    app = Flask(__name__)
    app.config.from_object(Config)
    log = logging.getLogger(__name__)

    #module 3 
    @app.route('/')
    def get_trello_lists():
        
        #get list id by name, ideally would like to retrieve Id by name fro, response but no time so hard=coded below
        #boardLists = []
        #results = GetListsOnBoard()

        todoList = get_cards_on_lists("6050cee9111302705ff69917")
        doingList = get_cards_on_lists("6050cee9111302705ff69918")
        doneList = get_cards_on_lists("6050cee9111302705ff69919")
    
        item_view_model = NewBoardListClass(todoList, doingList, doneList)
        return render_template('lists.html', item_view_model = item_view_model)


    @app.route('/showMore', methods=['POST'])
    def show_more():

        todoList = get_cards_on_lists("6050cee9111302705ff69917")
        doingList = get_cards_on_lists("6050cee9111302705ff69918")
        doneList = get_cards_on_lists("6050cee9111302705ff69919")

        item_view_model = NewBoardListClass(todoList, doingList, doneList)
        item_view_model.show_hide_all_done = False
        item_view_model.toggle_all_done = True
        return render_template('lists.html', item_view_model = item_view_model)

    @app.route('/showLess', methods=['POST'])
    def show_less():

        todoList = get_cards_on_lists("6050cee9111302705ff69917")
        doingList = get_cards_on_lists("6050cee9111302705ff69918")
        doneList = get_cards_on_lists("6050cee9111302705ff69919")

        item_view_model = NewBoardListClass(todoList, doingList, doneList)
        item_view_model.show_all_done = False
        item_view_model.toggle_all_done = False
        return render_template('lists.html', item_view_model = item_view_model)

    @app.route('/module2')
    def cards():

        boardLists = []
        results = get_lists_on_board()

        for index, boardListItem in enumerate(results): 
        
            cardsLists = []
            responseCards = get_cards_on_board(boardListItem["id"])

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
        add_card_to_first_list(newCard)

        return redirect('/')

    @app.route('/cards/moveCardUp/<idCard>/<idNextList>') 
    def completeTask( idCard, idNextList):   

        move_card(idCard, idNextList)

        return redirect('/')


    @app.route('/cards/moveCardUp/<idCard>/<idPreviousList>') 
    def redoTask( idCard, idPreviousList):   

        move_card(idCard, idPreviousList)

        return redirect('/')


    @app.route('/cards/<idCard>/<descriptionCard>/<duedate>') # TODO could be feasible to post entire card object back?
    def updateTask( idCard, descriptionCard, duedate):  

        log.info(descriptionCard)
        update_card(idCard, descriptionCard, duedate)

        return redirect('/')


    return app

app = create_app()