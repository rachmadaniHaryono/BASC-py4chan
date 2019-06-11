import os
import tempfile
import json

import pytest
import vcr

from basc_py4chan_server.__main__ import create_app


@vcr.use_cassette('fixtures/vcr_cassettes/test_main.yaml', record_mode='new')
def test_main():
    from basc_py4chan import get_all_boards, Url
    boards = get_all_boards()
    assert len(boards) > 0
    board0 = boards[0]
    jsonable_obj = []
    non_jsonable_obj = []
    for key, value in vars(board0).items():
        try:
            json.dumps(value)
            jsonable_obj.append((key, value))
        except TypeError:
            non_jsonable_obj.append((key, value))
    assert jsonable_obj == \
        [('_board_name', '3'), ('_https', False), ('_protocol', 'http://'), ('_thread_cache', {})]
    assert list(zip(*non_jsonable_obj))[0] == ('_url', '_requests_session')
    assert isinstance(board0._url, Url)
    assert vars(board0._url) ==  \
        {
            'URL': {
                'api': {'board': 'http://a.4cdn.org/{board}/{page}.json', 'thread': 'http://a.4cdn.org/{board}/thread/{thread_id}.json'},
                'data': {'file': 'http://i.4cdn.org/{board}/{tim}{ext}', 'static': 'http://s.4cdn.org/image/{item}', 'thumbs': 'http://i.4cdn.org/{board}/{tim}s.jpg'},
                'domain': {
                    'api': 'http://a.4cdn.org',
                    'boards': 'http://boards.4chan.org',
                    'boards_4channel': 'http://boards.4channel.org',
                    'file': 'http://i.4cdn.org',
                    'static': 'http://s.4cdn.org',
                    'thumbs': 'http://i.4cdn.org'},
             'http': {'board': 'http://boards.4chan.org/{board}/{page}', 'thread': 'http://boards.4chan.org/{board}/thread/{thread_id}'},
             'listing': {
                 'archived_thread_list': 'http://a.4cdn.org/{board}/archive.json',
                 'board_list': 'http://a.4cdn.org/boards.json',
                 'catalog': 'http://a.4cdn.org/{board}/catalog.json',
                 'thread_list': 'http://a.4cdn.org/{board}/threads.json'}},
            '_board_name': '3',
            '_protocol': 'http://'}


@pytest.fixture
def client():
    app = create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'' in rv.data
    assert rv.status_code == 200
