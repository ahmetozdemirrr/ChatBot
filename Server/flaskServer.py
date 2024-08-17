from flask import Flask, request, jsonify, render_template
import requests
import os


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/bot', methods=['POST'])
def get_bot_response():

    user_message = request.json.get('message')

    response = requests.post(
        'http://rasa:5005/webhooks/rest/webhook',
        json={"sender": "test_user", "message": user_message}
    )

    bot_responses = response.json()

    return jsonify(bot_responses)



# print(f"FLASK_PORT environment variable: {os.environ.get('FLASK_PORT')}")

if __name__ == '__main__':

    port = os.environ.get("FLASK_PORT", 5000)
    # print(f"Using port: {port}")
    app.run(host="0.0.0.0", port=int(port))