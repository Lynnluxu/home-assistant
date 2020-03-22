import os
from subprocess import check_output, run

from flask import Flask
from flask_restful import Api, reqparse, Resource


app = Flask(__name__)
api = Api(app)


html_code = """<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Change volume</title>
    <style>
html, body {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
}

body {
  /* https://leaverou.github.io/css3patterns/#madras */
  background-color: hsl(34, 53%, 82%);
  background-image:
    repeating-linear-gradient(45deg, transparent 5px, hsla(197, 62%, 11%, 0.5) 5px, hsla(197, 62%, 11%, 0.5) 10px,
      hsla(5, 53%, 63%, 0) 10px, hsla(5, 53%, 63%, 0) 35px, hsla(5, 53%, 63%, 0.5) 35px, hsla(5, 53%, 63%, 0.5) 40px,
      hsla(197, 62%, 11%, 0.5) 40px, hsla(197, 62%, 11%, 0.5) 50px, hsla(197, 62%, 11%, 0) 50px, hsla(197, 62%, 11%, 0) 60px,
      hsla(5, 53%, 63%, 0.5) 60px, hsla(5, 53%, 63%, 0.5) 70px, hsla(35, 91%, 65%, 0.5) 70px, hsla(35, 91%, 65%, 0.5) 80px,
      hsla(35, 91%, 65%, 0) 80px, hsla(35, 91%, 65%, 0) 90px, hsla(5, 53%, 63%, 0.5) 90px, hsla(5, 53%, 63%, 0.5) 110px,
      hsla(5, 53%, 63%, 0) 110px, hsla(5, 53%, 63%, 0) 120px, hsla(197, 62%, 11%, 0.5) 120px, hsla(197, 62%, 11%, 0.5) 140px
    ),
    repeating-linear-gradient(135deg, transparent 5px, hsla(197, 62%, 11%, 0.5) 5px, hsla(197, 62%, 11%, 0.5) 10px,
      hsla(5, 53%, 63%, 0) 10px, hsla(5, 53%, 63%, 0) 35px, hsla(5, 53%, 63%, 0.5) 35px, hsla(5, 53%, 63%, 0.5) 40px,
      hsla(197, 62%, 11%, 0.5) 40px, hsla(197, 62%, 11%, 0.5) 50px, hsla(197, 62%, 11%, 0) 50px, hsla(197, 62%, 11%, 0) 60px,
      hsla(5, 53%, 63%, 0.5) 60px, hsla(5, 53%, 63%, 0.5) 70px, hsla(35, 91%, 65%, 0.5) 70px, hsla(35, 91%, 65%, 0.5) 80px,
      hsla(35, 91%, 65%, 0) 80px, hsla(35, 91%, 65%, 0) 90px, hsla(5, 53%, 63%, 0.5) 90px, hsla(5, 53%, 63%, 0.5) 110px,
      hsla(5, 53%, 63%, 0) 110px, hsla(5, 53%, 63%, 0) 140px, hsla(197, 62%, 11%, 0.5) 140px, hsla(197, 62%, 11%, 0.5) 160px
    );
}

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
  box-shadow: 0 .25rem 1rem rgba(0, 0, 0, .4);
}

.volume { margin-left: 1rem; }
    </style>
  </head>
  <body>
    <script type="text/javascript">
function setNewVolume(newVolume) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/volume', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    xhr.send('value=' + newVolume);
}
    </script>

    <div class="container">
      <span>🔊</span>
      <input class="volume" type="range" min="0" max="100" value="%volume" onchange="setNewVolume(this.value)">
    </div>
  </body>
</html>
"""


def get_volume():
    return int(check_output(
        "amixer -M get 'PCM' | awk 'NR==5 {print $4}' | sed 's|[^0-9]||g'",
        shell=True))


@app.route("/")
def index():
    # XXX: The string is too "complex" to use standard string formatting.
    # Instead, an ugly workaround is used.
    return html_code.replace("%volume", str(get_volume()))


class Volume(Resource):
    def get(self):
        return {"message": "Success", "data": {"volume": get_volume()}}

    def post(self):
        actions = {"set": '', "increase": '+', "decrease": '-'}

        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, default="set",
                            choices=actions.keys())
        parser.add_argument('value', required=True, type=int, choices=range(101))
        args = parser.parse_args()

        action_chr = actions[args['action']]
        run(f"amixer -M set 'PCM' {args['value']}%{action_chr}".split(' '))

        return self.get(), 201


class PlayBeep(Resource):
    def get(self):
        here = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(here, "beep.wav")
        run(f"aplay {filepath}".split(' '))
        return {"message": "Success", "data": {}}


api.add_resource(Volume, '/api/volume')
api.add_resource(PlayBeep, '/api/play-beep')


def main():
    app.run(host='0.0.0.0', port=15000, debug=True)


if __name__ == '__main__':
    main()
