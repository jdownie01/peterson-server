# Python 3 peterson HTTPS server
import glob
import os
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "0.0.0.0"
serverPort = 8000
my_queue = []


class ThreadingQueue(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            # More statements comes here
            # print(my_queue)
            for i in my_queue:
                play_music(i)
                my_queue.remove(i)
                # TODO: Delete file from server.

            time.sleep(self.interval)


tr = ThreadingQueue()


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # TODO: Change request term to include password.
        term = parse_sanitize(self.path.split("/")[1])
        self.wfile.write(bytes("<html><head><title>Peterson Server</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % term, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<b> QUEUE </b>", "utf-8"))
        for i in my_queue:
            self.wfile.write(bytes("<p>" + i + "</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        if term != "skip":
            music_file = execute_search(term)
            my_queue.append(music_file)
        else:
            subprocess.run(['killall', '-9', 'aplay'])
        # play_music(music_file)
        #


def execute_search(term):
    """
    Executes a search via youtube-dl

    :param term: the search term
    :return: the latest edited file, currently the best way to determine the newly created file
    """
    p = subprocess.Popen(
        "youtube-dl -x --audio-format wav --verbose \"ytsearch1:" + term + "\"",
        stdout=subprocess.PIPE, shell=True)
    p.communicate()  # has output for debugging
    try:
        # FIXME: If term isn't properly sanitized then this can be used to execute malicious files
        list_of_files = glob.glob('*.wav')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    except ValueError:
        # No MP3 files exist
        print("youtube-dl failed!")
        return "ERROR"


def parse_sanitize(http_input):
    """
    Sanitizes input strings

    :param http_input: the input to be sanitized
    :return: the now sanitized input
    """
    parsed = http_input.replace("_", " ")
    return parsed


def play_music(file):
    """
    Plays the requested music file using aplay

    :param file: the file to be played
    """
    if file.split(".")[1] == "wav":
        if os.path.exists(file):
            subprocess.run(["aplay", file])
        else:
            # TODO: Implement Logger
            raise FileNotFoundError
    else:
        raise TypeError


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    while 1 == 1:
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass
            x = input("Please enter a command: ")
            if x == "p":
                subprocess.run(['killall', '-9', 'aplay'])
            else:
                break

    webServer.server_close()
    print("Server stopped.")
