import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])

print("tek boyutlunun 4. elemanı :", arr1[4])

arr2 = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])

print("üç boyutlunun 2ye 2si :", arr2[2][2])

# ikisinde de son eleman dahil edilmez (arange)

print(np.arange(10, 20)) # -> 10 ile 20 arasında değerler sıralar
print(np.arange(10, 20, 3)) # -> 10 ile 20 arasında 3'er 3'er atlayarak değerler sıralar

print(np.zeros(10)) # -> 10 tane 0 elemanı barındıran bir array (default olarak double sayı atanır)
print(np.zeros((2, 2))) # -> 2x2'lik arrayi yine 0 ile dolduruyor

print(np.ones(10)) # -> 10 tane 1 elemanı barındıran bir array (default olarak double sayı atanır)
print(np.ones((2, 2))) # -> 2x2'lik arrayi yine 1 ile dolduruyor

print(np.linspace(0, 100, 5)) # 0 ile 100 arasını 5 eşit parçaya bölerek double array oluşturur

print(np.eye(4)) # 4x4'lük birim matris oluşturur

print(np.random.randint(0, 10)) # 0 ile 10 arası random bir integer, başlangıcın default değeri 0'dır
print(np.random.randint(0, 10, 5)) # 5'lik random int array

print(np.random.rand(5)) # 0 ile 1 arasında 5 elemanlı bir array

print(np.random.randn(5)) # 0'ın etrafında gaussioan distribution yaparak 5 elemanlı bir array döner


##########

arrayim = np.arange(30)
print(arrayim.reshape(6, 5)) # verilen arraye ait elemanları 5x5'lik bir matrise yerleştirir
# burada verilen 2 parametre array için fix olmalı mesela 6x5 = 30 şeklinde...

newArray = np.random.randint(1, 100, 10)
print(newArray)
print(newArray.max()) # arrayin en büyük değerini döner
print(newArray.min()) # arrayin en küçük değerini döner
print(newArray.sum()) # tüm değerlerin toplamını döner
print(newArray.mean()) # tüm değerlerin ortalamasını döner
print(newArray.argmax()) # en büyük değerin indeksini döner
print(newArray.argmin()) # en küçük değerin indeksini döner


detArray = np.random.randint(1, 100, 25)
print(detArray)
detArray = detArray.reshape(5, 5)
print(detArray)

x = np.linalg.det(detArray) # -> detArray arrayinin determinantını bulur
print("detArray'in determinantı: ", x)

################################################################################

arr = np.arange(1, 10)

print(arr)
print(arr[1:5]) # -> 1 ile 5. indeks arasındaki sayılar
print(arr[::2]) # -> tüm değerleri bas ama 2 atlaya atlaya bas

arr[0:3] = 25
print(arr)

arr = np.arange(1, 10)
arr2 = arr

arr2[:3] = 100
print(arr2)
print(arr)

# eşitlemeden sonra arr2'yi değiştirsek arr de aynı şekilde değişir (pointer meselesi yüzünden)

# bu durumun yaşanmaması için:
arr = np.arange(1, 10)
arr2 = arr.copy()

newArray = np.arange(1, 21)
newArray = newArray.reshape(5, 4)

print(newArray[:, :2]) # -> çift boyutlu matrisde tüm satırları alırken sütunların sadece ilk ikisini alıp döner

arr = np.arange(1, 11)
print(arr > 3) # her indeksteki değeri 3 ile karşılaştırıp true ya da false ataması yapar

booleanArray = arr > 3

print(arr[booleanArray]) # sadece true olan değerleri tutar

################################################################################

arr1 = np.array([10, 20, 30, 40, 50, 60])
arr2 = np.array([1, 2, 3, 4, 5, 6])

print("arr1: ", arr1)
print("arr2: ", arr2)
print("arr1 + arr2: ", arr1 + arr2)
print("arr1 + 10: ", arr1 + 10)

# !Böyle işlemler için iki arrayin de boyutu aynı olmalıdır!

np.sqrt(arr1) # -> her bir elemanın karekökünü alır 

