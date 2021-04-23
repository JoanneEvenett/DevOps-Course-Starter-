
import pytest
import dotenv
from requests.api import patch
from todo_app.app import *
from unittest.mock import *

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_loading_page(client):
     with client:
        res = client.get('/')
        assert res.status_code == 200


@patch('requests.get')
def test_loading_page_done_list(mock_get_requests, client):
     with client:
         mock_get_requests.side_effect = mock_get_lists
         response = client.get('/')           
         assert response.status_code == 200
      
def mock_get_lists(url):
    if url == f'https://api.trello.com/1/boards/6050cee9111302705ff69916/lists':
        response = Mock()
    # sample_trello_lists_response should point to some test response data
        response.json.return_value = ""
        return response
    return None
