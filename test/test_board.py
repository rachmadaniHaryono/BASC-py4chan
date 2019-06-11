def test_get_threads():
    import basc_py4chan
    b = basc_py4chan.Board('b')
    assert b.get_threads()
