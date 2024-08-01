# RASA'nın çalışması için son sürüm imajı temel alıyoruz
# 1
FROM rasa/rasa:latest

# Botun kodlarını kopyalıyoruz konteyner içine (bunu yapabilmek için proje dizininde bu işlemlerin yapılması gerekiyor)
# 2
COPY . /app

# Çalışması dizini olarak /app'i seçiyoruz, ki sonraki komutlarımız bunun üzerinde çalışsın
# 3
WORKDIR /app

# ROOT yetkisi ver ve daha sonra sanal ortamdaki dosyaları kullanabilmek için çalıştırma izni ver
# 4
USER root
# 5
RUN chmod -R 777 /opt/venv/lib/python3.10/site-packages/

# Gerekli bazı bağımlılıkları indiriyoruz
# 6
RUN pip install --no-cache-dir -r requirements.txt
# 7
RUN pip install pandas

# Expose port (RASA için 5005 portunu default olarak ayarlıyoruz)
# 8
EXPOSE 5005

# RASA çalıştırma komutu
# 9
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]

