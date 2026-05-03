import cv2
import numpy as np 
import time

def siyah_beyaz_filtre(resim):
    
    gri_resim = cv2.cvtColor(resim,cv2.COLOR_BGR2GRAY)  #renk dönüşümü
   
    return cv2.cvtColor(gri_resim, cv2.COLOR_GRAY2BGR)

def bulanik_filtre(resim, cekirdek_boyutu=(15,15)):
    
    return cv2.GaussianBlur(resim, cekirdek_boyutu, 0) #blur uygular

def kenar_tespit(resim):
    #canny için gri resim şart
    gri= cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    
    #gürültüyü azaltmak için hafif blur kenrar tespitini iyileştirir
    
    blur=cv2.GaussianBlur(gri,(5,5), 0)
    
    # --- OTOMATİK EŞİK HESAPLAMA ---
    # Resmin medyanını alıyoruz
    medyan = np.median(blur)
    alt_esik = int(max(0, (1.0 - 0.33) * medyan))
    ust_esik = int(min(255, (1.0 + 0.33) * medyan))
    #canny sonucu tek kanallı (siyah beyaz kenarlar) resimdir
    
    kenarlar= cv2.Canny(blur,alt_esik,ust_esik)
    
    
    return cv2.cvtColor(kenarlar,cv2.COLOR_GRAY2BGR)

    
def sepya_filtre(resim):
    # Sepya dönüşüm matrisi
    sepya_matrisi = np.array([[0.272, 0.534, 0.131], 
                              [0.349, 0.686, 0.168], 
                              [0.393, 0.769, 0.189]])
    
    sepya_resim = cv2.transform(resim, sepya_matrisi)
    
    # Piksel değerlerini 0-255 arasında sınırla (np.clip) ve uint8 formatına geri dön.
    return np.clip(sepya_resim, 0, 255).astype(np.uint8)


def kameradan_foto_cek():
    kamera = cv2.VideoCapture(0)
    
    if not kamera.isOpened():
        print("\n hata: kamera açılamadı")
        return None
    
    pencere_adi = "Kamera Onizleme"
    cv2.namedWindow(pencere_adi, cv2.WINDOW_AUTOSIZE)
    
    print("\n" + "="*30)
    print("     kamera açıldı       ")
    print("="*30)
    print("foto çekmek için 's' tuşuna basın")
    print("iptal etmek için 'q' tuşuna basın")
    
    yakalanan_kare=None
    
    while True:
        # ret: Görüntü başarıyla okundu mu? (True/False)
        # kare: Okunan anlık görüntü (NumPy array)
        ret, kare= kamera.read()
        
        if not ret:
            print("kameradan görüntü alınamıyor")
            break
        
        cv2.imshow(pencere_adi, kare) 
        
        # Klavyeden girdi bekle (1 milisaniye boyunca). 
        # Bu satır olmadan cv2.imshow görüntüyü güncelleyemez.
        tus = cv2.waitKey(1) & 0xFF
        
        if tus==ord('s'):
            print("\n Fotoğraf cekildi")
            # copy() kullanmalıyız, yoksa değişken kamera kapanınca kaybolabilir.
            yakalanan_kare = kare.copy()
            break
        
        elif tus==ord('q'):
            print("iptal edildi")
            break
        
        time.sleep(0.03)
  
    kamera.release()  #kamera serbest
    cv2.destroyWindow(pencere_adi)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    
    return yakalanan_kare


def main():
    
    orijinal_resim = kameradan_foto_cek()
    
    if orijinal_resim is not None:
        # Başlangıçta sağ tarafta orijinal resmin kopyası dursun.
        # Bu sayede pencere terminaldeki `input`'u beklemeden hemen açılır.
        secili_filtre = orijinal_resim.copy()
        sonuc_penceresi = "Orijinal | Filtrelenmis"
        cv2.namedWindow(sonuc_penceresi, cv2.WINDOW_AUTOSIZE)

        
        secilen_filtre = "orijinal"
        
        while True:
            sonuc = np.hstack((orijinal_resim, secili_filtre)) #ikisi aynı anda geliyor
            cv2.imshow(sonuc_penceresi, sonuc)
            
            print("\n--- Filtre Uygulaması ---")
            print("1. Siyah-Beyaz (Grayscale)")
            print("2. Sepya (Retro)")
            print("3. Bulanıklaştırma (Blur)")
            print("4. Kenar Tespiti (Canny)")
            print("s. Filtreli Resmi Kaydet (Save)") 
            print("0. Çıkış") 

            print("\n[BİLGİ] Lütfen resim penceresi seçiliyken bir tuşa basın...")
            tus = cv2.waitKey(0) & 0xFF
            
            # ASCII karakterlerini algılamak için 'chr()' kullanıyoruz.
            secim = chr(tus)
            
            sonuc_resim = None
            
            if secim == '1':
                secili_filtre = siyah_beyaz_filtre(orijinal_resim)
                secilen_filtre="siyah beyaz"
                print("Siyah-Beyaz filtre uygulandı.")
                
            elif secim == '2':
                secili_filtre = sepya_filtre(orijinal_resim)
                secilen_filtre="sepya"
                print("Sepya filtre uygulandı.")
            
            elif secim == '3':
                secili_filtre = bulanik_filtre(orijinal_resim)
                secilen_filtre="bulanik"
                print("Bulanıklaştırma uygulandı.")
            
            elif secim == '4':
                secili_filtre = kenar_tespit(orijinal_resim)
                secilen_filtre="kenar tespit"
                print("Kenar tespiti uygulandı.")
                
            elif secim == 's': 
                dosya_adi = f"sonuc_{secilen_filtre}.jpg"
                basarili_mi = cv2.imwrite(dosya_adi, secili_filtre)

                if basarili_mi:
                    print(f"\n Görüntü '{dosya_adi}' olarak kaydedildi!")
                else:
                    print("\n[HATA] Görüntü kaydedilemedi!")
            
            elif secim == '0' or tus == ord('q'):
                print("Filtre ekranından çıkılıyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen tekrar deneyin.")
                continue 
                
            time.sleep(0.03)
            
        # Programdan çıkarken tüm pencereleri temizce kapatıyoruz.
        cv2.destroyWindow(sonuc_penceresi)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
                
    print("\n uygulama sonlandırıldı")
    
#program doğrudam çalıştıırlıyor mu diye kontrol 

if __name__ == "__main__":
    main()