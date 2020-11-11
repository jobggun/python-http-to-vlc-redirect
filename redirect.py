import http.server
import vlc

instance = vlc.Instance('--input-repeat=-1')
player = instance.media_player_new()

options = "sout=#transcode{vcodec=none,acodec=mp3,ab=320,channels=2,samplerate=44100,scodec=none}:http{mux=mp3,dst=:30001} no-sout-all sout-keep"
player.stop()

class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version='HTTP/1.1'
        self.send_response(303, 'See Other')

        media=instance.media_new(self.path[1:], options)
        player.set_media(media)
        player.play()

        while not player.is_playing():
            pass

        self.send_header('Location', 'http://localhost:30001')
        self.end_headers()

if __name__ == "__main__":
    print("Ready to play musics")
    http.server.HTTPServer(('', 30000), Server).serve_forever()
