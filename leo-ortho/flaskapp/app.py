from flask import Flask, jsonify, request, render_template, make_response
from Model import Model
import os

model_language = 'fr'
model = Model(model_language)

app = Flask(__name__)


@app.route('/health_status', methods=['GET'])
def get_health_status():
    return make_response(f"Leo-ortho API is online! Current version.", 200)


@app.route('/', methods=['POST'])
def parse_sentence():
    sentence = request.get_json().get("sentence")
    output_data = model.get_spellchecker_from_sentence(sentence)

    return jsonify(data=output_data)

if __name__ == "__main__":
    app.run()
