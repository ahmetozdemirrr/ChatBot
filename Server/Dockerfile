# Python resmi imajını temel alıyoruz
FROM python:3.10

# Çalışma dizinini ayarlıyoruz
WORKDIR /app

# Gerekli dosyaları kopyalıyoruz requirements dosyası genelde 
# her Dockerfile için yazılır içinde hangi bağımlılıkların olduğu yazılı olur
# mesela flask örneğinde içerik şu şekildedir: 
# Flask
# requests
COPY Server/requirements.txt requirements.txt
COPY Server/flaskServer.py flaskServer.py
COPY Server/templates templates

# Gerekli bağımlılıkları yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
# ARG FLASK_PORT
ENV FLASK_PORT=${FLASK_PORT}
EXPOSE ${FLASK_PORT}

# Flask sunucusunu çalıştırma komutu
CMD ["python3", "flaskServer.py"]
