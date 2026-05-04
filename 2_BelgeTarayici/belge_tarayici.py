import cv2 
import numpy as np
import time

def kagit_kenarlarini_bul(resim):
    
    gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gri,(5,5),0)
    kenarlar = cv2.Canny(blur,75,200)
    
    konturlar, _ = cv2.findContours(kenarlar, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # En büyük alanlı konturları sıralıyoruz
    konturlar = sorted(konturlar, key=cv2.contourArea, reverse=True)[:5]
    
    for kontur in konturlar:
        cevre = cv2.arcLength(kontur, True)
        yaklasik_kose = cv2.approxPolyDP(kontur, 0.02*cevre,True)
        
        if len(yaklasik_kose) == 4:
            return yaklasik_kose
    
    return None

def kagit_koseleri_sırala(koseler):
    koseler = koseler.reshape((4,2))
    yeni_koseler = np.zeros((4,2),dtype=np.float32)
    
    # Toplamları en küçük olan Sol-Üst, en büyük olan Sağ-Alt'tır.
    toplamlar = koseler.sum(axis=1)
    yeni_koseler[0] = koseler[np.argmin(toplamlar)]
    yeni_koseler[2] = koseler[np.argmax(toplamlar)]
    
    # Farkları en küçük olan Sağ-Üst, en büyük olan Sol-Alt'tır.
    farklar = np.diff(koseler, axis=1)
    yeni_koseler[1]=koseler[np.argmin(farklar)]
    yeni_koseler[3]=koseler[np.argmax(farklar)]
    
    return yeni_koseler

def perspektif_duzelt(resim,koseler):
    
    sirali_koseler = kagit_koseleri_sırala(koseler)
    (sol_ust, sag_ust,sag_alt, sol_alt ) = sirali_koseler
    
    # yeni resmin genisliği
    
    genislik_a = np.sqrt(((sag_alt[0] - sol_alt[0])**2) + ((sag_alt[1]-sol_alt[1])**2))
    genislik_b = np.sqrt(((sag_ust[0] - sol_ust[0])**2) + ((sag_ust[1]-sol_ust[1])**2))
    max_genislik = max(int(genislik_a), int(genislik_b))
    
    # yeni resmin yüksekliği
    yukseklik_a = np.sqrt(((sag_ust[0]-sag_alt[0])**2)+ (sag_ust[1]-sag_alt[1])**2)
    yukseklik_b = np.sqrt(((sol_ust[0]-sol_alt[0])**2)+ (sol_ust[1]- sol_alt[1])**2)
    max_yukseklik= max(int(yukseklik_a), int(yukseklik_b))
    
    # hedef düz bir dikdörtgen ölçüleri:
    
    hedef_olculer = np.array([
       [0,0],
       [max_genislik -1 , 0], #pikseller 0dan başladığı için çıkardık
       [max_genislik-1,max_yukseklik-1],
       [0,max_yukseklik-1]
       
    ], dtype=np.float32)   
    
    matris = cv2.getPerspectiveTransform(sirali_koseler,hedef_olculer) #koseleri eslestirir
    return cv2.warpPerspective(resim, matris,(max_genislik, max_yukseklik)) #tüm resme uygular



def okunabilirlik_artir(resim):
    # kontrast yukseltip siyah beyaz belge dönüşümü
    
    # gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    
    # # yazıları netleştirmek içn: 
    
    # tarama_efekti = cv2.adaptiveThreshold(gri,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,25,10)
    
    # return cv2.cvtColor(tarama_efekti,cv2.COLOR_GRAY2BGR)
    
    # clahe yöntemi ile bölgesel parlaklık dengelenir
    gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    vurgulanmis_gri = clahe.apply(gri)
    
    return cv2.cvtColor(vurgulanmis_gri, cv2.COLOR_GRAY2BGR)

def kameradan_foto_cek():
    kamera = cv2.VideoCapture(0)
    if not kamera.isOpened():
        print("\n hata, kamera acilamadi")
        return None
    
    pencere_adi = "BELGE TARAYİCİ"
    cv2.namedWindow(pencere_adi, cv2.WINDOW_AUTOSIZE)
    
    print("\n" + "= "*35)
    print("       BELGE TARAYİCİ ACİLDİ")
    print("="*35)
    print("belgeyi cekmek icin 's' tusuna basin")
    print("cikis icin 'q' tusuna basin")
    
    yakalanan_kare = None
    
    while True:
        ret, kare = kamera.read()
        if not ret:
            print("goruntu alinamiyor")
            break
        
        # kagit kenarlarini yesille göstermek icin
        
        onizleme = kare.copy()
        koseler = kagit_kenarlarini_bul(kare)
        
        if koseler is not None:
            cv2.drawContours(onizleme,[koseler],-1,(0,255,0),2)
            
        cv2.imshow(pencere_adi,onizleme)
        
        tus = cv2.waitKey(1) & 0xFF
        if tus == ord('s'):
            print("\n belge yakalandi")
            yakalanan_kare = kare.copy()
            break
        elif tus == ord('q'):
            print("\n islem iptal edildi")
            break
        
        time.sleep(0.02)
        
    kamera.release()
    cv2.destroyWindow(pencere_adi)
    cv2.waitKey(1)
    return yakalanan_kare


def main():
    orijinal_resim = kameradan_foto_cek()
    
    if orijinal_resim is not None:
        koseler =kagit_kenarlarini_bul(orijinal_resim)
        
        if koseler is not None:
            duzeltilmis = perspektif_duzelt(orijinal_resim,koseler)
            tarama_sonucu = okunabilirlik_artir(duzeltilmis)
        else:
            print("\n kenarlar tespit edilemedi. orijinal resim kullanılacak")
            tarama_sonucu = orijinal_resim.copy()
        
        tarayici_penceresi = "TARAMA SONUCU"
        cv2.namedWindow(tarayici_penceresi, cv2.WINDOW_AUTOSIZE)
        
        print("\n" + "="*35)
        print("    TARAMA TAMAMLANDI")
        print("="*35)
        print("-> 's' : Taranmış belgeyi bilgisayara kaydet.")
        print("-> 'q' veya '0' : cikis yap.")
        
        while True:
            cv2.imshow(tarayici_penceresi,tarama_sonucu)
            
            tus=cv2.waitKey(1) & 0xFF
            secim = chr(tus).lower()
            
            if secim=='s':
                dosya_adi = "/home/zeynep/Desktop/taranmis_belge.jpg"
                cv2.imwrite(dosya_adi,tarama_sonucu)
                print(f"\nbelge {dosya_adi} olarak kaydedildi")
                break
            elif secim == '0' or tus==ord('q'):
                print("cikis yapiliyor")
                break
            
            time.sleep(0.02)
            
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    
    print("uygulama sonlandirildi")
    
    
if __name__=="__main__":
    main()
        