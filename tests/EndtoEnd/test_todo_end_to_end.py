
import threading
from todo_app.trelloApiCalls import create_trello_board, delete_trello_board
import pytest
import dotenv
from requests.api import patch
from todo_app.app import create_app as create_app
from unittest.mock import *
import os
from threading import Thread
from selenium import webdriver

@pytest.fixture(scope='module')
def app_with_temp_board():
 # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ[board_id]
    # construct the new application
    application = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: 
    
application.run(use_reloader=False))
    threading.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver
        yield driver

def test_task_journey(driver, app_with_temp_board):
 driver.get('http://localhost:5000/')
 assert driver.title == 'To-Do App'