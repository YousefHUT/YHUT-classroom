Pyhon-tkinter ile çalışan basit bir sınıf yoklama sistemi uygulaması.
## Uygulama ne yapıyor:
- Sınıflar oluşturabilir
- Sınıflara öğrenci ekleyebilir, düzenleyebilir, silinebilir
- Sınıftaki öğrencilere artı puan eklenebilir, silinebilir
- İstediğiniz tarihe göre yoklama alınabilir

## Ne kullanarak çalışıyor:
- Sınıfları classes klasöründeki sınıfların adlarında olan klasörlerin içindeki json dosyalarında kaydediyor.
- Tkinter arayüzünü [Pygubu](https://github.com/alejandroautalan/pygubu) kütüphanesi ile tasarladığım app.ui adındaki xml dosyasında bulunuyor.
- Dosya yolları [Pathlib](https://pypi.org/project/pathlib/) ile tanımlandığından python olan bütün işletim sistemlerinde hatasız çalışıyor.

## Derekli kütüphaneler:
```
pip install pygubu pathlib
```
## Kurulum:
Projeyi zip olarak indirip yada klonlayıp kullanabilirsiniz.

## Kullanım:
- "__init__.py" dosyasını python ile açın

![resim](https://github.com/user-attachments/assets/13c52e75-e7d4-4c80-bf45-e8ea14576bdb)
- Kırmızı bölge içinde olan yerden sınıf seçin yada sınıf ekleyin
- Sınıf eklemek için sınıf adını ordaki kutucuğa yazın ve yanındaki artı butonuna basın.
- Sınıf seçmek için kutucuğun yanındaki oka basıp sınıfınızı seçin.

![resim](https://github.com/user-attachments/assets/856ac495-aa9a-41ee-81f7-ce73cc2fd553)
- Öğrenci eklemek için tablonun üstündeki öğrenci ekleme tuşuna basın.

![resim](https://github.com/user-attachments/assets/3a3c757b-cf84-415e-b7c4-b614acd30a75)
- Açılan pencereye öğrencinizin numarasını ve ad soyadını yazıp kaydetme butonuna basın.

![resim](https://github.com/user-attachments/assets/34838241-0a9a-45c8-a544-60de544060b8)
- Öğreniyi seçmek için öğrencinin adına tıklayın

![resim](https://github.com/user-attachments/assets/ace1775a-22a8-48bb-9ec7-3da5dbf0e96d)
- Buradan öğrenciye puan verebilir, yoklamasını alabilir, düzenleyebilir ve silebilirsiniz.

- Yoklama almak için tarih seçebilir yada yoklama tarihi ekleyebilirsiniz.
- Tarih eklemek için tarih ekleme butonuna basın.
![resim](https://github.com/user-attachments/assets/6c030a8e-4f61-497f-a8f1-6f5f65e544eb)
- Bugünün tarihini otomatik seçmek için takvim tuşuna basınız (Bilgisayarda kayıtlı olan tarih ve saate göre işler)
- Kaydetmek için kayıt tuşuna basın.

- Tarih seçmek için tarih çerçevesi içindeki kutucuğun yanındaki oka basıp tarihi seçin.

![resim](https://github.com/user-attachments/assets/9ea537f4-d213-4255-967f-4f782e964b63)
- Listedeki öğrenciye faredeki şekilde tıklayarak örenciyi var yada yok olarak değiştirebilirsiniz.

![resim](https://github.com/user-attachments/assets/d5c96ff9-98ad-4906-9723-13d95774672a)
- Bütün öğrencilerin yoklamasını hızlı bir şekilde almak için kırmızı kutu içindeki yere tıklayın

![resim](https://github.com/user-attachments/assets/fbd54635-4bfb-483d-9af9-d57fe109e693)
- Ekranda adı gözüken kişi yoklamada varsa yeşil butona, yoksa kırmızı butona basabilirsiniz.
- Eğer hatalı işaretleme yaptıysanız geri/ileri gidebilirsiniz.
