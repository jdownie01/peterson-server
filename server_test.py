import server


def execute_search_test():
    search_term = "Never Going To Give You Up"

    result = server.execute_search(server.parse_sanitize(search_term))

    assert result == "Rick Astley - Never Gonna Give You Up (Video)-dQw4w9WgXcQ.mp3"


def parse_sanitize_test(http_input):
    pass


def subprocess_test():
    print(server.execute_search("Never Going To Give You Up"))


#subprocess_test()
execute_search_test()