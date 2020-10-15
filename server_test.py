import server


def execute_search_test():
    search_term = "Never Going To Give You Up"

    result = server.execute_search(search_term)

    assert result == "youtube"


def parse_sanitize_test(http_input):
    pass


def subprocess_test():
    print(server.execute_search("Never Going To Give You Up"))


subprocess_test()
