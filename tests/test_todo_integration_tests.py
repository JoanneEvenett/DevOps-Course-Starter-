
import pytest
import dotenv
from requests.api import patch
from todo_app.app import create_app as create_app
from unittest.mock import *

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_loading_page(client):
    res = client.get('/')
    assert res.status_code == 200


#Haven't check if the next ones actually work - no time
@patch('requests.get')
def test_get_list(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists("https://api.trello.com/1/boards/6050cee9111302705ff69916/lists")#ideally would read Id from the secrets file
    response = client.get('/')           
    assert response.status_code == 200
      
def mock_get_lists(url):
    if url == f'https://api.trello.com/1/boards/6050cee9111302705ff69916/lists':
        response = Mock()
    # sample_trello_lists_response should point to some test response data
        response.json.return_value = '[{ "id": "4", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
        return response
    elif url == f'https://api.trello.com/1/boards/6050cee9111302705ff69916/lists':
        response = Mock()
    # sample_trello_lists_response should point to some test response data
        response.json.return_value = '[{ "id": "4", "dateLastActivity": "2021-04-20T12:49:00.329Z", "name": "test"}]'
        return response
    return None

@patch('requests.get')
def test_get_list_done(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists("https://api.trello.com/1/boards/6050cee9111302705ff69916/lists")
    response = client.get('/')           
    assert response.status_code == 200  
