# series: bildiğimiz diziler
# dataFrame: ik boyutlu matrisler

import pandas as pd
import numpy as np

from numpy.random import randn

print("######################################## PANDAS ########################################")
print("######################################## 1 - Series ########################################")

label_list = ["Ahmet", "Esma", "Leyla", "Yusuf", "Ali"]
data_list = [10, 20, 30, 40, 50]

# pandas series init signature:
# pandas.Series(data=None, index=None, dtype=None, name=None, copy=None, fastpath=_NoDefault.no_default) 

print(pd.Series(data = data_list, index = label_list))

# pd.Series(data_list, label_list, ) -> yukarıdaki ile aynı: sıralı verilecekse isimlere gerek yok
 
print(pd.Series(label_list)) # -> default olarak 0'dan başlayarak index ataması yapar

# en aşağıda basılan (dtype:) data type'ını belirtir

# Series'lar numpy arraylarini de parametre olarak alabilir

npArray = np.array([10, 20, 30, 40, 50])
print(pd.Series(npArray))

# python'da dictionaryler aşağıdaki gibi tanımlanır

dataDictionary = {"Ahmet":10, "Esma":100, "Zehra":50, "Ali":5}

# bu tarz dictionary verileri de Series'lere parametre olarak verilebilir

print(pd.Series(dataDictionary))

ser2017 = pd.Series([5, 10, 14, 20], ["Buğday", "Mısır", "Kiraz", "Erik"])
ser2018 = pd.Series([2, 12, 12, 21], ["Buğday", "Mısır", "Çilek", "Erik"])

print(ser2017 + ser2018)
# output: 
# Buğday     7.0
# Erik      41.0
# Kiraz      NaN
# Mısır     22.0
# Çilek      NaN
# dtype: float64

total = ser2017 + ser2018
print(total["Erik"]) # out -> 41


print("######################################## 2 - DATAFRAMES ########################################")

# pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)

dataFr = pd.DataFrame(data = randn(3, 3), index = ["A", "B", "C"], columns = ["Column1", "Column2", "Column3"])

print(dataFr)

# output:

#     Column1   Column2   Column3
# A  0.047323  1.425566 -0.207072
# B -2.047696  1.585823  0.769235
# C  0.481411 -0.759360 -1.922188

print(dataFr["Column3"]) 

# output:

# A    0.914232
# B   -2.416813
# C   -0.312112
# Name: Column3, dtype: float64

print(type(dataFr["Column2"]))

# output: <class 'pandas.core.series.Series'>

print(dataFr.loc["A"]) # A locationundaki satırı basar

# output:

# Column1    0.450151
# Column2    0.750531
# Column3    0.737958
# Name: A, dtype: float64

print(dataFr[["Column3", "Column2"]]) # -> sadece belirtilen columnları getirir, bunları birleştirir aynı zamanda

# column ekleme:

dataFr["Column4"] = pd.Series(data = randn(3), index = ["A", "B", "C"]) # -> boyutlar aynı olmalı

print(dataFr)

dataFr["Total Sum"] = dataFr["Column1"] + dataFr["Column2"] + dataFr["Column3"] + dataFr["Column4"]

print(dataFr)

# column silme:

print(dataFr.drop("Column4", axis = 1))
# ya da
# dataFr.drop("Column4", axis = 1, inplace = True) dersek buradaki True değişikliği kalıcı tutu anlamına gelir

print(dataFr.drop("A", axis = 0))

# axis 1 column ifade ederken axis 0 ise row ifade eder


# index erişimleri
# dataFr.loc["A"] ile dataFr.iloc[0] aynı şeydir

print("loc ile:\n", dataFr.loc["A"])
print("iloc ile:\n", dataFr.iloc[0])

print("ikili indeks sorgusu: ", dataFr["Column2"].loc["B"])
print("İkili indeks sorgusu farklı şekilde: ", dataFr.loc["B", "Column2"]);

# output:

# ikili indeks sorgusu:  1.2761227461899818
# İkili indeks sorgusu farklı şekilde:  1.2761227461899818

print(dataFr.loc[["A", "B"], ["Column1", "Column2"]])

# output:

#     Column1   Column2
# A  0.899352  1.654399
# B -0.233148 -0.426880


print("#################################### 3 - DATAFRAME Filtreleme ###################################")


df = pd.DataFrame(data = randn(4, 3), index = ["A", "B", "C", "D"], columns = ["Col1", "Col2", "Col3"])

# FİLTRELEME #

print(df > -1)

# output:

#     Col1   Col2  Col3
# A  False  False  True
# B   True   True  True
# C   True   True  True
# D   True   True  True

booleanDf = df > 0

print("\nBoolean DataFrame:") 
print(booleanDf) 

# sadece istenen değerlerin filtrelenmesi:

print(df[booleanDf])

# output:

#        Col1      Col2  Col3
# A       NaN  0.213081   NaN
# B  0.766856       NaN   NaN
# C  1.508057  0.487035   NaN
# D  0.215560  0.552642   NaN

print(df["Col1"] > 0)

# output:

# A    False
# B     True
# C    False
# D    False
# Name: Col1, dtype: bool

# daha derin filtreleme (iki serinin bazı koşullar altındaki döndürdüğü değerlere göre)

print("ilk şart:")
print(df["Col1"] > 0)
print("ikinci şart:")
print(df["Col2"] > 0)
print("sonuç:")
print(df[(df["Col1"] > 0) & (df["Col2"] > 0)])

# output:

# ilk şart:
# A    False
# B    False
# C    False
# D     True
# Name: Col1, dtype: bool
# ikinci şart:
# A    True
# B    True
# C    True
# D    True
# Name: Col2, dtype: bool
# sonuç:
#        Col1      Col2      Col3
# D  1.125793  1.187691  0.352435

df["Col4"] = pd.Series(randn(4), ["A", "B", "C", "D"])
print(df)

# ya da

df["Col5"] = randn(4)
print(df)

# farklı tipte veri ekleme #

df["Col6"] = ["Ahmet", "Özdemir", "Esma", "Sönmez"]
print(df)

# columnları indeksleme (yani belirtilen column satırları belirler artık)

print(df.set_index("Col6"))

# output:

#              Col1      Col2      Col3      Col4      Col5
# Col6                                                     
# Ahmet   -2.080141 -1.134638 -0.078875  1.735651  0.170268
# Özdemir -0.202768  0.316096  0.581131 -0.210310 -1.196482
# Esma     1.645396  0.513070  2.353031  1.977928 -0.215412
# Sönmez  -0.346106 -0.246540  0.885348 -1.429260  0.533961

print(df.index.names) # index durumundaki column hangisiyse ismini basar


print("#################################### 4 - DATAFRAME Multi Index Tanımlama ###################################")

outerIndex = ["Group1", "Group1", "Group1", "Group2", "Group2", "Group2", "Group3", "Group3", "Group3"]
innerIndex = ["Index1", "Index2", "Index3", "Index1", "Index2", "Index3", "Index1", "Index2", "Index3"]

# zip fonksiyonu verilen iki objeyi birleştirerek bir obje döner
# list ile binevi type casting yapıyoruz

hierarchy = list(zip(outerIndex, innerIndex))

print(hierarchy)

hierarchy = pd.MultiIndex.from_tuples(hierarchy)

print(hierarchy)

df = pd.DataFrame(randn(9, 3), hierarchy, columns = ["Col1", "Col2", "Col3"])

print(df)

# output:

#                    Col1      Col2      Col3
# Group1 Index1 -1.475124 -1.064166  1.910591
#        Index2 -0.526529 -0.216134  1.252296
#        Index3 -1.011280 -1.769066  0.144857
# Group2 Index1  0.257369 -1.339181 -0.114158
#        Index2 -1.496174  0.612008 -0.919449
#        Index3 -0.424254 -0.905631 -2.116279
# Group3 Index1 -0.576492 -1.404038 -0.837897
#        Index2  0.241172 -0.107884 -0.094303
#        Index3  0.712200  0.093562  0.562492

print(df["Col1"])

# output:

# Group1  Index1    0.766186
#         Index2    1.062283
#         Index3    1.122859
# Group2  Index1    0.553025
#         Index2   -0.637958
#         Index3    1.009869
# Group3  Index1    2.005988
#         Index2    0.725094
#         Index3    0.284732
# Name: Col1, dtype: float64

print(df.loc["Group1"])

# output:

#             Col1      Col2      Col3
# Index1  1.318751  0.806243 -0.928294
# Index2 -0.016556  0.122044  0.745012
# Index3  0.905029 -1.276124  1.111509

print(df.loc["Group1"].loc["Index1"])

# output:

# Col1    0.815107
# Col2    0.845578
# Col3   -1.005505
# Name: Index1, dtype: float64

print(df.loc["Group1"].loc["Index1"]["Col1"])

# output: -0.18852815618808133

# Group ve Indexlere isim verme #

print(df.index.names)

# output: [None, None] -> default değeri

df.index.names = ["Groups", "Indexes"]

print(df)

# output:

#                     Col1      Col2      Col3
# Groups Indexes                              
# Group1 Index1  -0.555065  0.500110 -1.461022
#        Index2  -0.555506  1.155216 -0.107709
#        Index3   1.059743  0.313923  2.235770
# Group2 Index1  -2.800736  0.136558  0.894940
#        Index2  -1.973526  0.410690 -0.624872
#        Index3   1.323244 -0.116940 -0.540488
# Group3 Index1  -2.263141  0.592998 -1.176423
#        Index2   0.790158 -1.899637  1.307821
#        Index3   0.205755  0.918940 -0.821070


# diğer get yöntemleri #

print(df.xs("Group1"))

# output:

#              Col1      Col2      Col3
# Indexes                              
# Index1   0.889665  0.991369 -0.027456
# Index2   1.015015  2.564109  1.297778
# Index3   0.316171 -1.956113  2.291862

print(df.xs("Group1").xs("Index1"))

# output:

# Col1   -1.187516
# Col2    0.556377
# Col3    0.833436
# Name: Index1, dtype: float64

print(df.xs("Group1").xs("Index1").xs("Col1"))

# output : 0.8114516085692197

print(df.xs("Index1", level = "Indexes"))

# output:

#             Col1      Col2      Col3
# Groups                              
# Group1  0.839788  0.049407  1.081238
# Group2  0.776606  0.632674 -1.383541
# Group3  0.699700  0.046329  0.012878


print("#################################### 5 - Data Preproceessing ###################################")


arr = np.array([[10, 20, np.nan], [5, np.nan, np.nan], [21, np.nan, 12]])

df = pd.DataFrame(data = arr, index = ["index1", "index2", "index3"], columns = ["Col1", "Col2", "Col3"])

print(df)

# nan olan öğeleri silme
# dikkat!: axis default olarak 0'dır aksi belirtilmediği sürece

print("\nfor axis 0:\n")
print(df.dropna(axis = 0)) # -> bu satır tablodaki tüm satırları siler, çünkü na olan satırları siler
print("\nfor axis 1:\n")
print(df.dropna(axis = 1)) # -> sütun olarak NaN barındıranlar kontrol edilir, NaN varsa o sütun silinir

# output:

# for axis 0:

# Empty DataFrame
# Columns: [Col1, Col2, Col3]
# Index: []

# for axis 1:

#         Col1
# index1  10.0
# index2   5.0
# index3  21.0

# şartlı silme durumları:

print("\nŞartlı silinmeden önce:\n")
print(df)
print("\nŞartlı silinmeden sonra:\n")
print(df.dropna(thresh = 2)) # -> yani minimum 2 tane sayı varsa o satırı silme anlamına gelir

# output:

# Şartlı silinmeden önce:

#         Col1  Col2  Col3
# index1  10.0  20.0   NaN
# index2   5.0   NaN   NaN
# index3  21.0   NaN  12.0

# Şartlı silinmeden sonra:

#         Col1  Col2  Col3
# index1  10.0  20.0   NaN
# index3  21.0   NaN  12.0


# NaN'ları silmek yerine manipüle etmek (.fillna() ile) #

print(df.fillna(value = 1))

# output:

#         Col1  Col2  Col3
# index1  10.0  20.0   1.0
# index2   5.0   1.0   1.0
# index3  21.0   1.0  12.0

# Dolu olan hücrelerdeki verilerin ortalamasını NaN'lara yazmak #

print(df.sum())

# output:

# Col1    36.0
# Col2    20.0
# Col3    12.0
# dtype: float64

print(df.sum().sum())

# output: 68.0

df.size    # -> toplam veri sayısını döner
df.isnull() # -> NaN olan verilerin sayısını bulmak için

def calculateMean(df):
	
	totalSum = df.sum().sum()
	totalFilled = df.size - df.isnull().sum().sum();

	return totalSum / totalFilled

print(df.fillna(value = calculateMean(df)))

# output:

#         Col1  Col2  Col3
# index1  10.0  20.0  13.6
# index2   5.0  13.6  13.6
# index3  21.0  13.6  12.0


print("#################################### 6 - GROUPBY METODU ###################################")


dataset = {"Departman" : ["Bilişim", "İnsan kaynakları", "Üretim", "Üretim", "Bilişim", "İnsan kaynakları"],
		   "Çalışan" : ["Mustafa", "Jale", "Kadir", "Zeynep", "Murat", "Ahmet"],	
		   "Maaş" : [3000, 3500, 2500, 4500, 4000, 2000]}

df = pd.DataFrame(dataset)

print(df)

# output:

#           Departman  Çalışan  Maaş
# 0           Bilişim  Mustafa  3000
# 1  İnsan kaynakları     Jale  3500
# 2            Üretim    Kadir  2500
# 3            Üretim   Zeynep  4500
# 4           Bilişim    Murat  4000
# 5  İnsan kaynakları    Ahmet  2000


DepGroup = df.groupby("Departman")

print(DepGroup)

# output: <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7572dc977f70>
# burada bir objenin oluşturulduğu belirtiliyor

print(DepGroup.sum())

# output:

#                        Çalışan  Maaş
# Departman                           
# Bilişim           MustafaMurat  7000
# Üretim             KadirZeynep  7000
# İnsan kaynakları     JaleAhmet  5500

# !!!!!!!!!! satırlardaki değerleri okumaya çalışacağın zaman loc özelliğini kullan !!!!!!!!!!

print(df.groupby("Departman").sum().loc["Bilişim"]) 

# output:

# Çalışan    MustafaMurat
# Maaş               7000
# Name: Bilişim, dtype: object

print("Sadece sayıyı elde etmek istiyorsan obje yerine, şu şekilde tür dönüşümü yapman gerek:")
print("int(df.groupby(\"Departman\").sum().loc[\"Bilişim\"])")

print(df.groupby("Departman").count())

# output:

#                   Çalışan  Maaş
# Departman                      
# Bilişim                 2     2
# Üretim                  2     2
# İnsan kaynakları        2     2

print(df.groupby("Departman").max())

# output:

#                   Çalışan  Maaş
# Departman                      
# Bilişim           Mustafa  4000
# Üretim             Zeynep  4500
# İnsan kaynakları     Jale  3500

# şuna dikkat et; bu tablo şunu ifade eder, departmanları küçükten büyüğe sıralar alfabetik olarak
# ardından her departmandaki en büyük maaşı ve alfabetik olarak en büyük ismi listeler
# .min() de aynı mantıkta çalışır!

print(df.groupby("Departman").min()["Maaş"])

# output:

# Departman
# Bilişim             3000
# Üretim              2500
# İnsan kaynakları    2000
# Name: Maaş, dtype: int64

# print(df.groupby("Departman").min()["Maaş"]["Bilişim"]) şeklinde yazıldığında;
# sadece bilişim departmanı için sonuç basılır.

# print(df.groupby("Departman").mean()) şeklinde kullanıldığı zaman sayısal olmayan sütunlar da
# olacağı için type error hatası alınır

print(df.groupby("Departman").mean(numeric_only = True))

# ya da

print(df.groupby("Departman")[["Maaş"]].mean())

# şeklinde kullanılabilir nasıl ihtiyaç duyuluyorsa artık

# output:

#                     Maaş
# Departman               
# Bilişim           3500.0
# Üretim            3500.0
# İnsan kaynakları  2750.0


print("#################################### 6 - MERGE, JOIN and CONCATENATE Metodları ###################################")


dataset1 = {"A" : ["A1", "A2", "A3", "A4"],
			"B" : ["B1", "B2", "B3", "B4"],
			"C" : ["C1", "C2", "C3", "C4"],}

dataset2 = {"A" : ["A5", "A6", "A7", "A8"],
			"B" : ["B5", "B6", "B7", "B8"],
			"C" : ["C5", "C6", "C7", "C8"],}

df1 = pd.DataFrame(dataset1, index = [1, 2, 3, 4])
df2 = pd.DataFrame(dataset2, index = [5, 6, 7, 8])

# CONCATENATE:

print(pd.concat([df1, df2]))

# output:

#     A   B   C
# 1  A1  B1  C1
# 2  A2  B2  C2
# 3  A3  B3  C3
# 4  A4  B4  C4
# 5  A5  B5  C5
# 6  A6  B6  C6
# 7  A7  B7  C7
# 8  A8  B8  C8

# indekslere göre birleştirilmiş hali budur

print(pd.concat([df1, df2], axis = 1))

# output:

#      A    B    C    A    B    C
# 1   A1   B1   C1  NaN  NaN  NaN
# 2   A2   B2   C2  NaN  NaN  NaN
# 3   A3   B3   C3  NaN  NaN  NaN
# 4   A4   B4   C4  NaN  NaN  NaN
# 5  NaN  NaN  NaN   A5   B5   C5
# 6  NaN  NaN  NaN   A6   B6   C6
# 7  NaN  NaN  NaN   A7   B7   C7
# 8  NaN  NaN  NaN   A8   B8   C8

# satır veya sütun sayılarında bu şekilde uyumsuzluk olduğu zaman kaşrılık alamayan hücreler NaN ile doldurulur

# JOIN:

dataset1 = {"A" : ["A1", "A2", "A3", "A4"],
			"B" : ["B1", "B2", "B3", "B4"]}

dataset2 = {"X" : ["X1", "X2", "X3"],
			"Y" : ["Y1", "Y2", "Y3"]}

df1 = pd.DataFrame(dataset1, index = [1, 2, 3, 4])
df2 = pd.DataFrame(dataset2, index = [1, 2, 3])

print(df1.join(df2)) # how='left' şeklinde bir parametre de alır; right, inner, outer falan da 
# olabiliyor ancak en çok genelde left kullanılıyor ve default olark left işaretlidir her zaman

# output:

#     A   B    X    Y
# 1  A1  B1   X1   Y1
# 2  A2  B2   X2   Y2
# 3  A3  B3   X3   Y3
# 4  A4  B4  NaN  NaN

# -> df1 üzerindeki tüm indeksler gelir sol tarafa, sağ tarafta da df2 yerleştirilir; eksiklik varsa
# NaN ile doldurulur, fazlalık varsa da fazla olan kısımlar tabloya dahil edilmez.


# MERGE:

dataset1 = {"A" : ["A1", "A2", "A3"],
			"B" : ["B1", "B2", "B3"],
			"anahtar" : ["K1", "K2", "K3"]}
 	
dataset2 = {"X" : ["X1", "X2", "X3", "X4"],
			"Y" : ["Y1", "Y2", "Y3", "Y4"],
			"anahtar" : ["K1", "K2", "K3", "K4"]}

df1 = pd.DataFrame(dataset1, index = [1, 2, 3])
df2 = pd.DataFrame(dataset2, index = [1, 2, 3, 4])

# anahtar parametresi ile iki tane dataFrame birleştirilmeye çalışılır
# join'in aksine daha çok sütunlar üzerinden birleştirme gerçekleştirilir

print(pd.merge(df1, df2, on = "anahtar"))

# output:

#     A   B anahtar   X   Y
# 0  A1  B1      K1  X1  Y1
# 1  A2  B2      K2  X2  Y2
# 2  A3  B3      K3  X3  Y3

# how='inner' şeklinde default olarak gelir, on parametresi yazılmasa da sanırım ortak olanı
# kendisi bulup yapıyor ancak işimizi garantiye almak için, biz hangi sütun üzerinden merge
# işlemi yapacaksak o sütunu on'a argüman olarak atamalıyız




























































































