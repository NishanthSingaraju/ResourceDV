from flask import Flask, request
from flask_cors import CORS

import map

app = Flask(__name__)
CORS(app)


@app.route('/map', methods=["GET"])
def get_map_url():
  image, county_outline, state_outline = map.get_map()
  return {"image": image, "county": county_outline, "state": state_outline}
