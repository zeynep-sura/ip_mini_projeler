# 📄 Belge Tarayıcı (Document Scanner)

Bu proje, Python ve OpenCV kullanarak kameradan alınan görüntüdeki kağıdı otomatik olarak algılayan, perspektifini düzelten (yamukluğu gideren) ve okunabilirliğini artıran bir çalışmadır.

---

## 🚀 Özellikler

* **Canlı Kenar Algılama:** Kamera görüntüsündeki en büyük 4 köşeli şekli (kağıdı) tespit eder ve yeşil bir çerçeveyle gösterir.
* **Perspektif Düzeltme:** Yamuk duran kağıdı tam üstten çekilmiş gibi dümdüz bir dikdörtgen haline getirir.
* **Görüntü İyileştirme:** Belge üzerindeki gölgeleri ve loş ışığı kırarak yazıları daha belirgin hale getirir.
* **Kaydetme Seçeneği:** Taranan belgeyi klavyeden `s` tuşuna basarak doğrudan bilgisayara kaydeder.

---

## 🛠️ Nasıl Çalışır?

Algoritma arka planda 4 ana adımdan oluşur:

1. **Ön İşleme:** Görüntü gri tona çevrilir, `GaussianBlur` ile pürüzler silinir ve `Canny` ile kenarlar bulunur.
2. **Köşe Sıralama:** Bulunan 4 köşe; Sol-Üst, Sağ-Üst, Sağ-Alt ve Sol-Alt olarak matematiksel olarak hizalanır.
3. **Dönüşüm Matrisi:** `cv2.getPerspectiveTransform` ve `cv2.warpPerspective` fonksiyonları kullanılarak resim kırpılır ve düzleştirilir.
4. **Kontrast Ayarı:** `CLAHE` (Bölgesel Kontrast Sınırlı Adaptif Histogram Eşitleme) yöntemiyle yazılar netleştirilir.

---
