# RASA SDK'nın en son sürümünü kullanarak bir temel imaj oluşturuyoruz
FROM rasa/rasa-sdk:latest

# Çalışma dizinini ayarlıyoruz
WORKDIR /app

# Gerekli dosyaları kopyalıyoruz
COPY actions /app/actions
COPY actions/requirements.txt /app/requirements.txt

# Gerekli bağımlılıkları root yetkileri ile yüklüyoruz
USER root
RUN pip install --no-cache-dir -r /app/requirements.txt

# Uygulama kullanıcıya geri dönüyoruz
USER 1001

ARG ACTION_SERVER_PORT
ENV ACTION_SERVER_PORT=$ACTION_SERVER_PORT
EXPOSE $ACTION_SERVER_PORT

# Action server'ı başlatıyoruz
CMD ["start", "--actions", "actions"]
