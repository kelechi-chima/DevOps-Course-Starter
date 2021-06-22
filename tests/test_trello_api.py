"""Integration tests for trello_api module"""

import json
import pytest
import re
from dotenv import find_dotenv, load_dotenv
from todo_app.app import create_app
from todo_app.trello_api import board_name, doing_list_name, done_list_name, todo_list_name
from unittest.mock import Mock, patch

TEST_BOARD_ID = '1'
TEST_TODO_LIST_ID = '1'
TEST_DOING_LIST_ID = '2'
TEST_DONE_LIST_ID = '3'

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = create_app()
    with test_app.test_client() as client:
        yield client

@patch('todo_app.trello_api.requests.get')
@patch('todo_app.trello_api.requests.post')
def test_index_page(mock_post, mock_get, client):
    mock_get.side_effect = mock_get_calls
    mock_post.side_effect = mock_post_calls

    response = client.get('/')
    assert response.status_code == 200

def mock_get_calls(url, params):
    if url == 'https://api.trello.com/1/members/me/boards' and params is not None:
        response = Mock()
        response.status_code = 200
        json_string = f'[{{"id": "{TEST_BOARD_ID}", "name": "{board_name}"}}]'
        response.json.return_value = json.loads(json_string)
        return response
    elif url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        response.status_code = 200
        response.json.return_value = [
            {'id': TEST_TODO_LIST_ID, 'name': todo_list_name}, 
            {'id': TEST_DOING_LIST_ID, 'name': doing_list_name}, 
            {'id': TEST_DONE_LIST_ID, 'name': done_list_name}
        ]
        return response
    elif re.search('https://api.trello.com/1/lists/.*/cards', url) is not None:
        response = Mock()
        response.status_code = 200
        response.json.return_value = []
        return response
    return None

def mock_post_calls(url, params):
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists' and params['name'] == todo_list_name:
        response = Mock()
        response.status_code = 200
        response.json.return_value = {'id': TEST_TODO_LIST_ID}
        return response
    elif url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists' and params['name'] == doing_list_name:
        response = Mock()
        response.status_code = 200
        response.json.return_value = {'id': TEST_DOING_LIST_ID}
        return response
    elif url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists' and params['name'] == done_list_name:
        response = Mock()
        response.status_code = 200
        response.json.return_value = {'id': TEST_DONE_LIST_ID}
        return response
    return None