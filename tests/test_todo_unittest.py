from todo_app.model.trellomodel import NewBoardListClass, ItemClass
from todo_app.trelloApiCalls import move_card, get_cards_on_lists, add_card_to_first_list

from datetime import datetime
import locale
import json

def test_todoLists_unit_test():
    
    # Arrange
    jsonStr = '[{ "id": "1", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
    todoList = json.loads(jsonStr)
    doingList = json.loads(jsonStr)
    doneList = json.loads(jsonStr)
    
    # Act
    boardList = NewBoardListClass(todoList, doingList, doneList)

    # Assert
    assert boardList.todoList == todoList
    assert boardList.doingList == doingList
    assert boardList.all_done_items == doneList

def test_doneLists_unit_test():
    # Arrange
    jsonStr = '[{ "id": "1", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
    todoList = json.loads(jsonStr)
    doingList = json.loads(jsonStr)
 
    dateNow = datetime.now()
    dateNowStr = ""+str(dateNow.year)+"-"+str(dateNow.month)+"-"+str(dateNow.day)+"T12:49:00.329Z"
    jsonStrDone = '[{ "id": "1", "dateLastActivity": "'+dateNowStr+'", "name": "test"}, '
    jsonStrDone +=  '{ "id": "2", "dateLastActivity": "2020-04-20T12:49:00.329Z", "name": "test"},'
    jsonStrDone +=  ' { "id": "3", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
    doneList = json.loads(jsonStrDone)

    # Act
    boardList = NewBoardListClass(todoList, doingList, doneList)
 
    allDoneCount = sum(1 for i in boardList.all_done_items)
    todaysCount = sum(1 for i in boardList.recent_done_items)
    beforeTodayCount = sum(1 for i in boardList.older_done_items)

    # Assert
    assert allDoneCount == todaysCount + beforeTodayCount
