from todo_app.model.trellomodel import NewBoardListClass, ItemClass
from todo_app.trelloApiCalls import move_card, get_cards_on_lists, add_card_to_first_list

from datetime import datetime
import locale
import json

def test_todoLists_unit_test():
    
    # Arrange
    jsonStr = '[{ "id": "1", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
    todoList = json.loads(jsonStr)
    jsonStr = '[{ "id": "2", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
    doingList = json.loads(jsonStr)
    jsonStr = '[{ "id": "3", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
    doneList = json.loads(jsonStr)
    
    # Act
    boardList = NewBoardListClass(todoList, doingList, doneList)

    # Assert
    assert boardList.todoList == todoList
    assert boardList.doingList == doingList
    assert boardList.all_done_items == doneList

def test_doneLists_unit_test():
    # Arrange
    jsonStr = '[{ "id": "4", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
    todoList = json.loads(jsonStr)
    jsonStr = '[{ "id": "5", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
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
    assert todaysCount == 1
    assert beforeTodayCount == 2
    assert allDoneCount == 3



def test_todoLists():#unit or integration test?

    # Arrange 
    #TODO if more time getting the lists dynamics rather than hard coding id
    todoList = get_cards_on_lists("6050cee9111302705ff69917")
    doingList = get_cards_on_lists("6050cee9111302705ff69918")
    doneList = get_cards_on_lists("6050cee9111302705ff69919")

    # Act
    boardList = NewBoardListClass(todoList, doingList, doneList)

    # Assert
    assert boardList.todoList == todoList
    assert boardList.doingList == doingList
    assert boardList.all_done_items == doneList

def todoLists_count():# candidate to mock, TODO move to integration tests area

    # Arrange  
    beforetodoList = get_cards_on_lists("6050cee9111302705ff69917") 
    add_card_to_first_list("newCard")

    todoList = get_cards_on_lists("6050cee9111302705ff69917")
    doingList = get_cards_on_lists("6050cee9111302705ff69918")
    doneList = get_cards_on_lists("6050cee9111302705ff69919")

    # Act
    boardList = NewBoardListClass(todoList, doingList, doneList)
    
    beforeCount = sum(1 for i in beforetodoList)
    afterCount = sum(1 for i in boardList.todoList)

    # Assert
    assert boardList.todoList == todoList
    assert afterCount == (beforeCount + 1)
    
    #Mock this or run a tidy up to remove above created card
def test_doneLists():#unit or integration test?

    # Arrange
    todoList = get_cards_on_lists("6050cee9111302705ff69917")
    doingList = get_cards_on_lists("6050cee9111302705ff69918")
    doneList = get_cards_on_lists("6050cee9111302705ff69919")

    # Act
    boardList = NewBoardListClass(todoList, doingList, doneList)
 
    allDoneCount = sum(1 for i in boardList.all_done_items)
    todaysCount = sum(1 for i in boardList.recent_done_items)
    beforeTodayCount = sum(1 for i in boardList.older_done_items)

    # Assert
    assert allDoneCount == todaysCount + beforeTodayCount