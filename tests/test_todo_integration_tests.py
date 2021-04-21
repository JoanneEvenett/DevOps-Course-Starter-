from todo_app.model.trellomodel import NewBoardListClass, ItemClass
from todo_app.trelloApiCalls import move_card, get_cards_on_lists, add_card_to_first_list

from datetime import datetime
import locale

def test_todoLists_integration_test():

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

def test_todoLists():

    # Arrange  
    beforetodoList = get_cards_on_lists("6050cee9111302705ff69917") 

    newCard = add_card_to_first_list("newCard")

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
def test_doneLists():

    # Arrange
    todoList = get_cards_on_lists("6050cee9111302705ff69917")
    doingList = get_cards_on_lists("6050cee9111302705ff69918")
    doneList = get_cards_on_lists("6050cee9111302705ff69919")

    # Act
    boardList = NewBoardListClass(todoList, doingList, doneList)
 
    allDoneCount = sum(1 for i in boardList.all_done_items)
    todaysCount = sum(1 for i in boardList.recent_done_items)
    befoeTodayCount = sum(1 for i in boardList.older_done_items)

    # Assert
    assert allDoneCount == todaysCount + befoeTodayCount