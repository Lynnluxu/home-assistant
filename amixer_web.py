from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import run
from urllib.parse import urlsplit, parse_qs


html_code = """<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Change volume</title>
    <style>
body { background-color: black; }

.container {
  display: flex;
  align-items: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: .5rem 1rem;
  background-color: white;
  border-radius: .25rem;
  font-size: 2rem;
}

.volume { margin-left: 1rem; }
    </style>
  </head>
  <body>
    <script type="text/javascript">
function setNewVolume(newVolume) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/?new_volume=' + newVolume);
    xhr.send();
}
    </script>

    <div class="container">
      <span>🔊</span>
      <input class="volume" type="range" min="0" max="100" onchange="setNewVolume(this.value)">
    </div>
  </body>
</html>
""".encode()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        params = parse_qs(urlsplit(self.path).query)
        try:
            new_volume = params["new_volume"][0]
        except KeyError:
            self.wfile.write(html_code)
        else:
            # Sanitize user input
            new_volume = max(0, min(int(new_volume), 100))

            run(f"amixer -M set 'PCM' {new_volume}%".split(' '))


HTTPServer(("0.0.0.0", 15000), RequestHandler).serve_forever()
