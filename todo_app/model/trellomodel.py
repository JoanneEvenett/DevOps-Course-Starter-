from datetime import datetime
import locale

class BoardListClass:
    def __init__(self, listItem, cardList, idpreviousList, idnextList):
        self._listItem = listItem
        self._cardList = cardList
        self._idpreviousList = idpreviousList
        self._idnextList = idnextList
    @property
    def listItem(self):
        return self._listItem
        
    @property
    def cardList(self):
        return self._cardList
        
    @property
    def idpreviousList(self):
        return self._idpreviousList
        
    @property
    def idnextList(self):
        return self._idnextList

class CardListItem:
    def __init__(self, cardItem):
        self._CardItem = cardItem

    @property
    def CardItem(self):
        return self._CardItem

#Module3
class NewBoardListClass:
    locale.setlocale(locale.LC_ALL, 'en_GB')
    format = "%Y-%m-%dT%H:%M:%S.%fZ"
    def __init__(self, todoList, doingList, doneList):
        self._todoList = todoList
        self._doingList = doingList
        self._show_all_done_items = doneList
        self._recent_done_items =  filter(lambda item: True if datetime.strptime(item["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ").date() == datetime.now().date() else False, doneList)             
        self._older_done_items =  filter(lambda item: False if datetime.strptime(item["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ").date() == datetime.now().date() else True, doneList)              
        if sum(1 for i in self._show_all_done_items) > 5:
           self._show_hide_all_done = False        
        else:
            self._show_hide_all_done = True
        self._toggle_all_done = False

    @property
    def todoList(self):
        return self._todoList        
    @property
    def doingList(self):
        return self._doingList
    @property
    def show_all_done_items(self):
        return self._show_all_done_items        

    @property
    def recent_done_item(self):
        #i = sum(1 for i in unordered_list if i % 2 == 0)
       # return filter(lambda item: True if datetime.strptime(item["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ").date() == datetime.now().date() else False, self._doneList)     
        return self._recent_done_items     
    @property
    def older_done_items(self): 
       # return filter(lambda item: False if datetime.strptime(item["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ").date() ==  datetime.now().date()  else True, self._doneList)     
        return self._older_done_items  

    @property
    def show_hide_all_done(self):         
        return self._show_hide_all_done
    
    @show_hide_all_done.setter
    def show_hide_all_done(self, value):
        self._show_hide_all_done = value

    @property
    def toggle_all_done(self):           
        return self._toggle_all_done

        
    @toggle_all_done.setter
    def toggle_all_done(self, value):
        self._toggle_all_done = value

