import os
import pytest
import requests
import time
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from threading import Thread
from todo_app.app import create_app
from todo_app.trello_api import create_board

board_id = ''

def create_trello_board():
    url = 'https://api.trello.com/1/boards/'
    query = { 'key': os.environ.get('TRELLO_API_KEY'), 'token': os.environ.get('TRELLO_API_TOKEN'), 'name': os.environ.get('BOARD_NAME') }
    response = requests.post(url, params=query)
    result = response.json()
    return result['id']

def delete_trello_board():
    url = f'https://api.trello.com/1/boards/{board_id}'
    query = { 'key': os.environ.get('TRELLO_API_KEY'), 'token': os.environ.get('TRELLO_API_TOKEN') }
    requests.delete(url, params=query)

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=False)
    os.environ['BOARD_NAME'] = 'Test Board'
    global board_id
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    application = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    delete_trello_board()

@pytest.fixture(scope='module')
def driver():
    current_dir = os.getcwd()
    chromedriver_executable = f'{current_dir}/chromedriver'
    with webdriver.Chrome(chromedriver_executable) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
    time.sleep(2)
    new_item_box = driver.find_element_by_name('new_item_title')
    new_item_box.send_keys('Buy bread')
    new_item_box.submit()
    time.sleep(2)
    assert 'Buy bread' in driver.page_source