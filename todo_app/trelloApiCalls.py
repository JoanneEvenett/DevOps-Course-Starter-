
#TODO create global static variables such as Trello base url  

import requests, logging

log = logging.getLogger(__name__)

def GetListsOnBoard():
    secrets = file_read("todo_app\secrets.txt")
    boardId = secrets[0]
    key =  secrets[1] 
    token = secrets[2]

    log.info(boardId)
    log.info(key)
    log.info(token)

    url = "https://api.trello.com/1/boards/{0}/lists" 

    query = {
        'key': key,
        'token': token
    }

    response = requests.request(
        "GET",
        url.format(boardId),
        params=query
    )

    return response.json()

def GetCardsonBoard(idList):
    secrets = file_read("todo_app\secrets.txt")
    boardId = secrets[0]
    key =  secrets[1] 
    token = secrets[2]

    log.info(boardId)
    log.info(key)
    log.info(token)#
    urlCards = "https://api.trello.com/1/boards/{0}/cards" # root url could be stored and configured globally fpr re-use 

    queryCards = {
        'key': key,
        'token': token,
        'idList': idList ##doesnt seem to filter :-(
    }

    responseCards = requests.request(
        "GET",
        urlCards.format(boardId),
        params=queryCards
    )

    return responseCards.json()

def AddCardtoFirstList(newCard):
    secrets = file_read("todo_app\secrets.txt")
    boardId = secrets[0]
    key =  secrets[1] 
    token = secrets[2]   

    listsonBoard = GetListsOnBoard()

    idList = listsonBoard[0]["id"]

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

#TODO be good to change position so appear moved to bottom of list
def MoveCard(idCard, idList):
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
        'idList' : idList
    } 
    
    response = requests.request(
        "PUT",
        url.format(idCard),
        headers=headers,
        params=query,
    )


#TODO be good to update entire object as per on page
def UpdateCard(idCard, description, duedate):
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
        'desc' : description,
        'due' : duedate
    } 
    
    response = requests.request(
        "PUT",
        url.format(idCard),
        headers=headers,
        params=query,
    )
def file_read(fname):
        content_array = []
        with open(fname) as f:
                #Content_list is the list that contains the read lines.     
                for line in f:
                        content_array.append(line.rstrip())
        
        return content_array
