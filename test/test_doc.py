def test_example():
    import basc_py4chan
    b = basc_py4chan.Board('b')
    b_vars = vars(b).copy()
    b_vars.pop('_url')
    b_vars.pop('_requests_session')
    assert b_vars == {
        '_board_name': 'b',
        '_https': False,
        '_protocol': 'http://',
        '_thread_cache': {}
    }
    threads = b.get_threads()
    assert threads
    thread = b.get_thread(threads[0].id)
    assert thread
    thread_files = list(thread.files())
    if thread_files:
        assert thread_files[0]
    thread.update()
