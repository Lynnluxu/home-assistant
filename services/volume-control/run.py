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
    xhr.open('POST', '/api/volume', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    xhr.send('value=' + newVolume);
}
    </script>

    <div class="container">
      <span>🔊</span>
      <input class="volume" type="range" min="0" max="100" onchange="setNewVolume(this.value)">
    </div>
  </body>
</html>
"""


@app.route("/")
def index():
    return html_code


class Volume(Resource):
    def _get_volume(self):
        return int(check_output(
            "amixer -M get 'PCM' | awk 'NR==5 {print $4}' | sed 's|[^0-9]||g'",
            shell=True))

    def get(self):
        return {"message": "Success", "data": {"volume": self._get_volume()}}

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


api.add_resource(Volume, '/api/volume')


def main():
    app.run(host='0.0.0.0', port=15000, debug=True)


if __name__ == '__main__':
    main()
