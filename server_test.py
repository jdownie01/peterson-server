import subprocess

def subprocess_test():
    p = subprocess.Popen(
        "youtube-dl https://www.youtube.com/results?search_query=" + "run_through_the_jungle" + "&page=1",
        stdout=subprocess.PIPE, shell=True)
    output,_ = p.communicate()
    print(output)

subprocess_test()