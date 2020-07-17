from flask import Flask, jsonify, request, render_template, make_response
from Model import Model
import os

model_language = 'fr'
print("app.py ok01")
model = Model(model_language)
print("app.py ok02")
app = Flask(__name__)
print("app.py ok03")

@app.route('/health_status', methods=['GET'])
def get_health_status():
    return make_response(f"Leo-date API is online! Current version.", 200)


@app.route('/', methods=['POST'])
def parse_sentence():
    print("app.py ok1")
    sentence = request.get_json().get("sentence")
    print("app.py ok2")
    output_data = model.get_date_from_sentence(sentence)
    print("app.py ok3")
    return jsonify(data=output_data)

if __name__ == "__main__":
    app.run()
