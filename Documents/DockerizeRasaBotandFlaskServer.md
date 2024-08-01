<div style="text-align: center;">
    <h2>Flask Server Üzerinden İstek Alan ve Docker Konteynerda Çalışan RASA Bot</h2>
</div>




Bu raporun içeriği şu şekildedir; şu ana kadar geliştirdiğim RASA botunu bir Dockerfile ile Dockerize edip bir konteyner üzerinde çalıştırmaya çalıştım. Ardından flask ile yerel bir sunucu yazdım ve yerel bir port üzerinden API olarak botu çalıştıran bu sayede flask server üzerinden iletişime geçebilen bir sistem tasarladım. Rapor bu adımları nasıl gerçekleştirdiğimi, takıldığım noktaları ve bazı önemli noktaları içerir.



Öncelikle daha anlaşılır olması açısından projemin dosya yapısını şu şekilde buraya koyayım ki bazı noktalarda neyi nerede yaptğımızı anlayabilelim.



Project tree:

```text
frstRasa/
├── actions
├── app
├── config.yml
├── credentials.yml
├── data
├── docker-compose.yml
├── Dockerfile
├── domain.yml
├── endpoints.yml
├── models
├── requirements.txt
├── Server
│   └── flaskServer.py
└── tests
```



**frstRasa** yazdığım ilk botun bulunduğu dizinin adıdır. `docker-compose.yml`, `Dockerfile` , `requirements.txt` ve diziniyler beraber (Server) `flaskServer.py` dosyaları sonradan eklendi. Onun dışındaki dosya ve dizinler zaten her RASA projesinde bulunan dizinlerdir.



***actions:*** Rasa botu için özel eylemleri (actions) tanımlayan dosyaların bulunduğu dizin.

***app:*** Docker konteynerında botun kodlarının kopyalandığı dizin. (Dockerfile'da belirtilen COPY . /app komutu ile bu dizine kopyalanıyor.)

***config.yml:*** Rasa'nın yapılandırma ayarlarını içeren dosya.

***data:*** Eğitim verilerini içeren dizin (NLU ve dialog verileri).

***docker-compose.yml:*** Docker Compose yapılandırma dosyası.

***Dockerfile:*** Docker imajını oluşturmak için kullanılan yapılandırma dosyası.

***domain.yml:*** Rasa botunun domain ayarlarını (intents, entities, actions vb.) içeren dosya.

***endpoints.yml:*** Rasa'nın HTTP sunucusuna ait endpoint yapılandırmalarını içeren dosya.

***models:*** Eğitim sonucunda oluşturulan modellerin bulunduğu dizin.

***requirements.txt:*** Python bağımlılıklarını içeren dosya.

***Server:*** Flask sunucusunun bulunduğu dizin.
	***flaskServer.py:*** Flask sunucusunun ana Python dosyası.








### 1 - Docker Sistemi Üzerinde RASA Tabanlı Bot Çalıştırılması: Dockerfile



Dockerfile, Docker konteynerları oluşturmak için kullanılan bir dosyadır. İçerisinde, bir konteynerın nasıl yapılandırılacağını ve hangi adımların izleneceğini tanımlayan talimatlar bulunur. Öncelikle bir docker build almak için şu şekilde geliştirdiğim Dockerfile'ı açıklayayım:



```Dockerfile

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

```



**Line 1:** 

Bu satır Docker imajının Rasa'nın en son sürümünü temel alarak oluşturulacağını belirtir. `rasa/rasa:latest` ifadesi, Rasa'nın Docker Hub üzerindeki en güncel sürümünü kullanmamızı sağlar. Bu, Rasa'nın tüm temel bağımlılıkları ve çalışma ortamı ile birlikte indirilmesini sağlar (Yaklaşık 1 GB dosya indirilecektir bu stepte).



**Line 2:**

Bu komut, bulunduğunuz proje dizinindeki tüm dosyaları (RASA kodları ve yapılandırma dosyaları da dahil) Docker konteynerının içindeki `/app` dizinine kopyalar. Bu komut sayesinde, geliştirdiğim botun tüm kodları konteyner içinde bulunur ve çalıştırılabilir.



**Line 3:**

Bu komut, Docker konteynerında çalışacak tüm komutların /app dizini içinde çalıştırılacağını belirtir. Böylece, sonradan çalıştırılacak komutlar bu dizin içinde işlem yapar (Mesela 9. stepteki komut bu dizinde çlaışacaktır).



**Line 4:**

Bu komut, konteyner içinde root kullanıcısı olarak işlem yapmamızı sağlar. Root kullanıcısı, sistem üzerinde tam yetkiye sahip olduğu için dosya izinlerini değiştirme ve paket yükleme gibi işlemler yapılabilir. (Normalde bazı işlemler için bu yetki isteniyor, her adımda root şifresi istenmesinin önüne geçmek için Dockerfile içine koydum bunu da)



**Line 5:**

Dockerfile'ı ilk yazdığımda bu kütüphane ve yapılandırma dosyalarını kullanamıyordum ve `permission denied` hatası alıyordum. Ardından root yetkisi verdiğimde de dosyaların çalıştırılabilir formatta olmadığı hatası almaya başladım. Çözüm olarak (chmod +x) ile tüm kütüphane dosyalarına çalıştırılabilme yetkisi verdim. Bu komut, Rasa'nın sanal ortamındaki dosyalara tam erişim izni verir. `chmod -R 777` komutu, belirtilen dizindeki tüm dosya ve klasörlere okuma, yazma ve çalıştırma izinleri verir. 

Bu, Rasa'nın bağımlılıklarını düzgün bir şekilde çalıştırabilmesi için gereklidir çünkü bazı arka planda çalışan bağımlılıklar kütüphaneler aracılığıyla bu dosyaları kullanır dosyalar da çalıştırabilme (+x) yetkisine sahip olmadığı için hata alıyordum. Bu durumu bu şekilde düzelttim ancak normalde `venv` ile derleyebildiğim bot; bu şekilde çalıştırınca neden bu yetkiyi kaybetti, net bir fikrim yok ancak tahminimce `venv`'lerde ve Docker sistemlerinin çalışma farkından dolayı kaynaklanıyor. Docker sistemden bağımsız çalışır bu yüzden olabilir.



**Line 6:**

Bu komut, `requirements.txt` dosyasındaki bağımlılıkları yükler. `--no-cache-dir` bayrağı, pip'in önbellek kullanmamasını sağlar, bu da daha temiz bir kurulum sağlar.


requirements.txt:
```text
rasa
```



**Line 7:**

Bu komut, Pandas kütüphanesini yükler. Normalde çok şart değil aslında ancak yazdığım botta bu kütüphaneyi kullanmıştım bu yüzden çalışabilmesi için bunu da indirdim. Aynı şekilde sistemde yüklü olmayıp kullanmamız gerekn kütüphaneler vs. varsa bu şekilde indirmeliyiz Dockerfile ile.



**Line 8:**

Bu komut, Docker konteynerının 5005 portunu açar. Bu, Rasa sunucusunun bu port üzerinden erişilebilir olmasını sağlar. Bu port default olarak RASA için çalışmış olacak artık.



**Line 9:**

Bu komut, Docker konteynerı başlatıldığında çalıştırılacak varsayılan komutu belirler. Burada, Rasa sunucusu `--enable-api` ve `--cors "*"`, `--port "5005"` seçenekleri ile başlatılır. `--enable-api` Rasa'nın API modunu etkinleştirir, `--cors "*"` tüm kaynaklardan gelen isteklere izin verir ve `--port "5005"` port 5005'te sunucuyu dinlemeye başlar. 

Yani bu komut kısaca RASA botunu bir api olarak başlatır. Normalde çalıştığımız gibi terminalden açmaz arayüzü. Botu API olarak kullanabilmek için daha önce yazdığımız mobil program için de bu komutu kullanıyordum .




```text
Not: Bu Dockerfile `rasa train` adımını içermez çünkü hali hazırda zaten derleyip oluşturduğum bir model vardı. Bunu istemiyorsak Dockerfile'a 9. stepten hemen önce bu komut eklenebilir.
```





### 2 - Docker Sistemi Üzerinde RASA Tabanlı Bot Çalıştırılması: docker-compose.yml




Docker Compose, Docker konteynerlerini tanımlamak ve çalıştırmak için kullanılan bir araçtır. Birden fazla konteynerin birlikte çalışmasını kolaylaştırır ve bu konteynerlerin konfigürasyonlarını tek bir dosya (genellikle docker-compose.yml dosyası) ile yönetmemizi sağlar. Bu sayede, karmaşık uygulamaları tek bir komutla başlatabilir, durdurabilir ve yönetebilirsiniz. Aurıca kullanıcı oturumlarını yöneteceğimiz Redis yapısını da bu dosyada yapılandıracağız.



* `services` anahtarı, tanımlanan tüm konteyner hizmetlerini içerir. Burada rasa adında bir hizmet tanımlanmıştır.

* `build`: Bu satır, Dockerfile'ın bulunduğu dizini belirtir ve Dockerfile kullanılarak imajın oluşturulacağını söyler. Nokta (.) mevcut dizini ifade eder.

* `ports`: Bu bölüm, konteynerin hangi portları kullanacağını tanımlar. 5005:5005 ifadesi, host makinedeki 5005 portunun konteyner içindeki 5005 portuna yönlendirileceğini belirtir. Bu sayede, Rasa botuna yerel makineden 5005 portu üzerinden erişilebilir.

* `volumes`: Bu bölüm, dosya sistemini bağlamayı tanımlar. .:/app ifadesi, yerel dizini (.) konteyner içindeki /app dizinine bağlar. Bu, konteynerin yerel dosyalara erişebilmesini sağlar ve yapılan değişikliklerin anında konteyner içinde yansıtılmasını sağlar.

* `command`:Bu bölüm, konteyner başlatıldığında çalıştırılacak komutu belirtir. Burada, rasa run --enable-api --cors "*" --port "5005" komutu çalıştırılır. Bu komut, Rasa sunucusunu API modunda başlatır, CORS ayarlarını yapar ve 5005 portundan dinlemeye başlar.





### 3 - Docker Sistemi Üzerinde RASA Tabanlı Bot Çalıştırılması: Docker Build




Tüm bu adımlardan sonra şimdi Docker build'i şu şekilde alacağız:


```bash
~/frstRasa$ sudo docker-compose up --build
```

Bu komut, docker-compose.yml dosyasında tanımlanan tüm hizmetleri başlatır ve gerekli imajları oluşturur.



**sudo:** Yüksek ayrıcalıklarla (root yetkileri) komutu çalıştırır. Bu, Docker komutlarının çalıştırılması için gereklidir.

**docker-compose:** Docker Compose aracı kullanılarak hizmetlerin yönetilmesini sağlar.

**up:**Tanımlanan tüm hizmetleri başlatır. Eğer imajlar mevcut değilse, önce bu imajları oluşturur.

**--build:** Tüm hizmetler için imajları yeniden oluşturur. Bu, Dockerfile'da yapılan herhangi bir değişikliğin uygulanmasını sağlar.



Komut, proje dizininde bulunan docker-compose.yml dosyasını ve Dockerfile'ı okuyarak gerekli yapılandırmaları alır. Komut çalışırken, başlatılan konteynerların logları terminalde görüntülenir. Bu loglar, hizmetlerin doğru bir şekilde başlatıldığını ve çalıştığını doğrulamak için kullanılabilir. Aşağıda bunların bazı kısımlarını ekran görüntüsü olarak koyacağım.



**Çıktı:**



![](/home/ahmete/Screenshots/Screenshot from 2024-08-01 16-03-34.png)

![](/home/ahmete/Screenshots/Screenshot from 2024-08-01 16-03-50.png)

![](/home/ahmete/Screenshots/Screenshot from 2024-08-01 16-04-20.png)

![](/home/ahmete/Screenshots/Screenshot from 2024-08-01 16-04-39.png)





Bu adımlardan sonra build alınmış olunuyor. Süreç içinde birtakım büyük boyutlu indirme ve büyük dosyaların konteyner içerisine kopyalanma işlemleri olduğu için işlem ilk kez yapıldığında biraz uzun sürebiliyor.




Tüm bu adımlardan sonra RASA botumuz API olarak çalışır ve hazır durumda olmuş oluyor. Bu API yerel ağda 5005 portundan komut dinlemeye hazırdır. Şimdi bu adımda da yazdığım flask tabanlı sunucuyu açıklayacağım.






### 4 - Flask - Server Üzerinden Dockerla Çalıştırılmış Bot ile İletişime Geçme



Öncelikle bu adım için basit bir flask sunucu-istemci kodu yazdım. Kod şu şekildedir:




```Python

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

```



ardından şu şekilde çalıştırılır:



```bash
~/frstRasa/Server$ python3 flaskServer.py
```





#### Kodun Açıklaması:

##### 1 - Gerekli kütüphanelerin import edilmesi:

* **Flask:** Flask web framework'ünü kullanmak için içe aktarılır.
* **request:** HTTP isteklerini işlemek için kullanılır.
* **jsonify:** JSON formatında veri döndürmek için kullanılır.
* **render_template_string:** HTML şablonlarını işlemek için kullanılır.
* **requests:** Diğer web hizmetlerine HTTP istekleri göndermek için kullanılır.



##### 2 - Flask uygulaması oluşturulması:


```Python
app = Flask(__name__)
```

* Flask uygulaması oluşturulur ve app değişkenine atanır. Bu, web uygulamamızı başlatmak ve yapılandırmak için kullanılır.



##### 3 - Ana Sayfa Rota Tanımlaması:


```Python
@app.route('/')
def index():
    return render_template_string('''
        <form action="/bot" method="post">
            <input type="text" name="message">
            <input type="submit">
        </form>
    ''')
```

* / rotası tanımlanır. Bu rota, form içeren basit bir HTML sayfası döndürür. (Aşağıya yerelde oluşturulan bu HTML sayfasının görüntüsünü ekleyeceğim)
* render_template_string: HTML formunu doğrudan bir string olarak döndürmek için kullanılır.



##### 4 - Bot İle İletişime Geçme Rota Tanımlaması:

```Python
@app.route('/bot', methods=['POST'])
def get_bot_response():
    user_message = request.form.get('message')
    
    response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={"sender": "test_user", "message": user_message}
    )
    
    return jsonify(response.json())
```

* /bot rotası tanımlanır ve POST yöntemi ile çalışır.
* request.form.get('message'): Formdan gelen kullanıcı mesajını alır. (Sayfada kutucuk içine bir şey yazılır ve submit edilir)
* requests.post: Rasa botuna HTTP POST isteği gönderir.
* URL: http://localhost:5005/webhooks/rest/webhook (Rasa'nın varsayılan webhook URL'si)
	* Bu kısımı `endpoints.yml` dosyasında zaten önce de şu şekilde tanımlamıştık:
		```YAML
		action_endpoint:
  		url: "http://localhost:5055/webhook"
		```

* JSON payload: {"sender": "test_user", "message": user_message} (Kullanıcı mesajı ve gönderen bilgileri)
* response.json(): Rasa botundan gelen yanıt JSON formatında alınır.
* jsonify: Yanıtı JSON formatında döndürür.



##### 5 - Uygulamanın Başlatılması:

```Python
if __name__ == '__main__':
    app.run(port=5000)
```

* Flask uygulamasını 5000 portunda başlatır.
* Bu bölüm, komut dosyası doğrudan çalıştırıldığında çalıştırılmasını sağlar.





**Çıktı:**



![image-20240801163333666](/home/ahmete/.config/Typora/typora-user-images/image-20240801163333666.png)



Kodu çalıştırdıktan sonra (https://127.0.0.1:5000) adresi ya da diğer bir deyimle (http://localhost:5000/) adresi tarayıcıda açılır.



![](/home/ahmete/Screenshots/Screenshot from 2024-08-01 15-00-44.png)

Girilen mesaj submit edildikten sonra cevabın verileceği yeni sayfa açılır.



![](/home/ahmete/Screenshots/Screenshot from 2024-08-01 15-00-56.png)



Pretty print ile daha okunabilir bir şekilde görüntülenebilir (bu kısım daha sonra flask-server dosyasında daha güzel bir görüntü olacak şekilde ele alınabilir);

![](/home/ahmete/Screenshots/Screenshot from 2024-08-01 15-02-07.png)





Bu raporda, Docker ve Flask kullanarak bir Rasa botunun nasıl konteynerize edildiğini ve API olarak çalıştırıldığını adım adım inceledim. Öncelikle, Dockerfile kullanarak botu bir Docker imajına dönüştürdüm ve ardından docker-compose.yml dosyası ile bu imajı konteynerda çalıştırdım. Son olarak, Flask ile yazdığımız basit bir sunucu aracılığıyla Rasa botuna nasıl istek gönderileceğini gösterdim. Bu süreçte karşılaşılan sorunları ve bunların nasıl çözüldüğünü açıkladım.

Bu çalışmanın sonucunda, Rasa botunu Docker kullanarak izole bir ortamda çalıştırmanın ve Flask sunucusu üzerinden API istekleri alarak botla etkileşime geçmenin mümkün olduğunu gördüm.

Bu rapor, Docker ve Flask kullanarak Rasa botunun nasıl konteynerize edileceği ve API olarak çalıştırılacağı konusunda rehber niteliğindedir. 
