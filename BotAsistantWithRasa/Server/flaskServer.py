from flask import Flask, request, jsonify, render_template_string
import requests


# Flask uygulaması oluşturma
app = Flask(__name__)



@app.route('/') # Ana sayfa rotası, HTML formu döndürür
def index():

    return render_template_string('''
        <form action="/bot" method="post">
            <input type="text" name="message">
            <input type="submit">
        </form>
    ''')



@app.route('/bot', methods=['POST']) # Bot ile iletişime geçme rotası
def get_bot_response():

    # Kullanıcı mesajını formdan al
    user_message = request.form.get('message')
    
    # Rasa botuna HTTP POST isteği gönder
    response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={"sender": "test_user", "message": user_message}
    )
    
    # Rasa botundan gelen yanıtı JSON formatında döndür
    return jsonify(response.json())



# Flask uygulamasını başlatma
if __name__ == '__main__':

    app.run(port=5000)
