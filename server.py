# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import operator
import glob
from stat import ST_CTIME
import os, sys, time

hostName = "0.0.0.0"
serverPort = 8000


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        term = parse_sanitize(self.path.split("/")[1])
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % term, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        music_file = execute_search(term)
        play_music(music_file)
        #


def execute_search(term):
    p = subprocess.Popen(
        "youtube-dl -x --audio-format mp3 \"ytsearch1:" + term + "\"",
        stdout=subprocess.PIPE, shell=True)
    p.communicate()  # has output for debugging
    try:
        list_of_files = glob.glob('*.mp3')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    except ValueError:
        #No MP3 files exist
        print("youtube-dl failed!")
        return "ERROR"


def parse_sanitize(http_input):
    parsed = http_input.swap(" ", "_")
    return parsed


def play_music(file):
    subprocess.run(["aplay", file])


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
                break;

    webServer.server_close()
    print("Server stopped.")
