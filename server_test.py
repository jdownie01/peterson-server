import subprocess
import server


def execute_search_test(term):
	search_term = "Never Going To Give You Up"
	
	result = server.execute_search(search_term)
	
	assert result == "youtube"
	
def parse_sanatize_test(http_input):
	pass
	
def subprocess_test():
    p = subprocess.Popen(
        "youtube-dl https://www.youtube.com/results?search_query=" + "run_through_the_jungle" + "&page=1",
        stdout=subprocess.PIPE, shell=True)
    output,_ = p.communicate()
    print(output)

subprocess_test()
