# 📸 Kamera ve Görüntü Filtreleme Uygulaması

Bu proje, bilgisayarınızın kamerasını kullanarak anlık fotoğraf çeken ve bu fotoğraf üzerinde sadece klavye tuşlarıyla çeşitli görüntü işleme filtreleri uygulayan bir Python uygulamasıdır.

## 🚀 Özellikler

* **Canlı Önizleme & Çekim:** Kameradan anlık görüntü alarak tek tuşla (`s`) fotoğraf çekebilirsiniz.
* **Canlı Filtre Değişimi:** Çektiğiniz fotoğraf üzerinde görsel pencere seçiliyken klavyedeki tuşlarla anlık filtre değiştirebilirsiniz.
* **Dinamik Kenar Tespiti:** Ortamdaki ışık ve kontrast durumuna göre kenarları net bir şekilde yakalar.
* **Görsel Kayıt:** Filtreli sonucu klavyeden `s` tuşuna basarak doğrudan bilgisayarınıza kaydedebilirsiniz.

---

## 🛠️ Nasıl Çalışır? (Klavye Kısayolları)

Uygulama tamamen klavye tuşları ile kontrol edilir. Terminalde girdi bekleme donmaları yaşanmaz.

### 1. Kamera Ekranındayken:
* **`s`** : Fotoğrafı çeker ve filtreleme ekranına aktarır.
* **`q`** : Kamerayı kapatır ve programdan çıkar.

### 2. Filtreleme Ekranındayken (Orijinal | Filtreli Yan Yana):
* **`1`** : Siyah-Beyaz (Grayscale) Filtresi uygular.
* **`2`** : Sepya (Retro) Filtresi uygular.
* **`3`** : Bulanıklaştırma (Blur) Filtresi uygular.
* **`4`** : Kenar Tespiti (Canny Edge Detection) uygular.
* **`s`** : Filtrelenmiş resmi bilgisayarınıza kaydeder.
* **`0` veya `q`** : Uygulamadan tamamen çıkar.
