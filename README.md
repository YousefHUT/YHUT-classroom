Pyhon-tkinter ile çalışan basit bir sınıf yoklama sistemi uygulaması.

![resim](https://github.com/user-attachments/assets/9f17bf02-e265-4413-97b0-01ace53d6896)


## Uygulama ne yapıyor:
- Sınıflar oluşturabilir
- Sınıflara öğrenci ekleyebilir, düzenleyebilir, silinebilir
- Sınıftaki öğrencilere artı puan eklenebilir, silinebilir
- İstediğiniz tarihe göre yoklama alınabilir
- Sınıfı exel tablosuna aktarabilir yada aktarılanı içe aktarbilrisiniz.
- Kullanıcı ve parola girişi ile koruma bulunmaktadır.
- İki aşamalı doğrulama ile parola sıfırlama seçeneğine sahip.
- Öğrecilerin hızlı yoklama alınması için özel bir menü bulunmakta.
- Öğrencileri numarasına, ad/soyadına ve etiketine göre filtreleyip arayabilirsiniz.
- Rastgele öğrenci seçme.
- Öğrenci istatistikleri gösterme ekranı ile devamsızlıkları takip edebilirsiniz.

## Ne kullanarak çalışıyor:
- Sınıfları classes klasöründeki sınıfların adlarında olan klasörlerin içindeki json dosyalarında kaydediyor.
- Tkinter arayüzünü [Pygubu](https://github.com/alejandroautalan/pygubu) kütüphanesi ile tasarladığım app.ui adındaki xml dosyasında bulunuyor.
- Dosya yolları [Pathlib](https://pypi.org/project/pathlib/) ile tanımlandığından python olan bütün işletim sistemlerinde hatasız çalışıyor.
- Pandas kütüphanesi ile sınıfları exel tablosuna yada aktarılmış tabloyu içe aktarıyor.
- pyotp ile 2 aşamalı doğrulama kodu oluşturup giriş için kullanıyor.
- qrcode kütüphanesiyle 2 aşamalı doğrulama kodunun qr kodunu çıkartabiliyor.
- hashlib ile kullanıcı adı ve parolayı tek yönlü şifreleyip kaydediyor.

## Gerekli kütüphaneler:
```
pip install pygubu pathlib pandas pyotp qrcode hashlib
```
## Kurulum:
Projeyi zip olarak indirip yada klonlayıp kullanabilirsiniz. [Releases](https://github.com/YousefHUT/YHUT-classroom/releases) sayfasından windows veya linux için olan hazır build edilmiş sürümleri kullanabilirsiniz.

## Kullanım:
- "__main__.py" dosyasını python ile açın

![resim](https://github.com/user-attachments/assets/669b1ddb-35e0-4f84-9c58-7d94a99f2136)
- İlk defa giriş yaptıysanız kullanıcı adı ve şifreyi girin.

![resim](https://github.com/user-attachments/assets/09bded4c-db2d-47c7-9861-ec4b0e2fe3fc)
- Çıkan qr kodu microsoft authenticator yada google authenticator gibi bir iki aşamalı doğrula uygulamasına okutun yada koda tıklayıp kodu kopyalayıp yapıştırın.
- Pencereyi kapatıp giriş yapın.

![resim](https://github.com/user-attachments/assets/0ef33d7c-33a5-46bc-9447-9cafbce15373)
- Kırmızı bölge içinde olan yerden sınıf seçin yada sınıf ekleyin.
- Sınıf eklemek için sınıf adını ordaki kutucuğa yazın ve yanındaki artı butonuna basın.
- Sınıf seçmek için kutucuğun yanındaki oka basıp sınıfınızı seçin.

![resim](https://github.com/user-attachments/assets/8403a11d-8b9f-409f-9d54-22848960d8c5)
- Öğrenci eklemek için öğrenci sekmesindeki öğrenci ekleme tuşuna basın.

![resim](https://github.com/user-attachments/assets/defe1a01-c2f2-4d78-bcc2-ed060aa79edf)
- Açılan pencereye öğrencinizin numarasını ve ad soyadını yazıp kaydetme butonuna basın (Arama yerinde filtrelemek istediğiniz bir özellik varsa "Durumu" yerine yazabilirsiniz).
- Öğreniyi seçmek için öğrencinin adına tıklayın

![resim](https://github.com/user-attachments/assets/550685fd-2366-4c5c-a060-fa8c33a02e8d)
- Buradan öğrenciye puan verebilir, yoklamasını alabilir, düzenleyebilir ve silebilirsiniz.
- Öğrenci hakkında daha fazla bilgi almak için kırmızı alanın sağ altındaki öğrenci hakkında butonuna basın.

![resim](https://github.com/user-attachments/assets/71192dc4-2a9d-4989-8ee5-a39917e805fc)
- Buradan öğrencinin devamsızlık bilgisi gibi bilgilere ulaşabilirsiniz.


![resim](https://github.com/user-attachments/assets/ca104404-ba75-4833-969a-64fd05783066)
- Yoklama almak için kırmızı alandan tarih seçebilir yada yoklama tarihi ekleyebilirsiniz.
- Tarih eklemek için tarih ekleme butonuna basın.

![resim](https://github.com/user-attachments/assets/6c030a8e-4f61-497f-a8f1-6f5f65e544eb)
- Bugünün tarihini otomatik seçmek için takvim tuşuna basınız (Bilgisayarda kayıtlı olan tarih ve saate göre çalışır)
- Kaydetmek için kayıt tuşuna basın.

![resim](https://github.com/user-attachments/assets/bcd80482-3300-4191-8538-8ffa7fdd9302)
- Kırmızı olan alandan öğrencileri numarası yada adına göre arayabilir, durumunu ve gelip gelmeyeni filtreleyebilirsiniz.
- Listeden rastgele öğrenci seçmek için zar tuşuna basın (NOT! rastgele öğrenci, hızlı yoklama özellikleri filtrelenmiş listeden öğrenci seçer).
- Sol üstteki menüden sınıfı içe yada dışa aktarabilirsiniz.
- .txt olarak kaydederseniz yoklama verilerini kaydetmez. En iyi sonuç için .xlsx seçeneğini seçin.

![resim](https://github.com/user-attachments/assets/22387630-782f-4078-9ace-98a4afbbc965)
- Kırmızı alanın içinde tüm öğrencilerin yoklamasını almak için butonlar bulunmaktadır.
- Bütün öğrencilerin yoklamasını hızlı bir şekilde almak için şimşekli öğrenci resmi olan (Hızlı yoklama) butonuna basın.

![resim](https://github.com/user-attachments/assets/fbd54635-4bfb-483d-9af9-d57fe109e693)
- Ekranda adı gözüken kişi yoklamada varsa yeşil butona, yoksa kırmızı butona basabilirsiniz.
- Eğer hatalı işaretleme yaptıysanız geri/ileri gidebilirsiniz.
