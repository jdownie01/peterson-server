import server
import os


def test_execute_search():
    search_term = "Never Going To Give You Up"

    result = server.execute_search(server.parse_sanitize(search_term))

    assert result == "Rick Astley - Never Gonna Give You Up (Video)-dQw4w9WgXcQ.wav"

    # TODO: Clean up
    try:
        os.remove("Rick Astley - Never Gonna Give You Up (Video)-dQw4w9WgXcQ.wav")
    except FileNotFoundError:
        assert False


def test_parse_sanitize():
    term = "a_weird link_and_stuff"

    result = server.parse_sanitize(term)

    assert result == "a weird link and stuff"


def test_play_music_not_found():
    try:
        server.play_music("not_a_file.wav")
        assert False
    except FileNotFoundError:
        assert True


def test_play_music_not_wav():
    try:
        server.play_music("this_is_a_mp3.mp3")
        assert False
    except TypeError:
        assert True
