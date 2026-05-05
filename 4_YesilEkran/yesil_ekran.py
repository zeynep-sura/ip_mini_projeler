import cv2
import numpy as np

#  resimleri oku

on_plan= cv2.imread('yesil.jpg')
arka_plan = cv2.imread('manzara.jpg')

if on_plan is None or arka_plan is None:
    print("hata: resimlere ulasilamadi")
    exit()
    
# arka plan ön planla aynı boyutta olmalı 
yukseklik, genislik, _ = on_plan.shape
arka_plan = cv2.resize(arka_plan,(genislik,yukseklik))

# bgr -> hsv gecisi: yesili daha kolay tespit etmek icin

hsv = cv2.cvtColor(on_plan, cv2.COLOR_BGR2HSV)

#  hsv formatında yeşilin alt ve üst sınırlarını belirliyoruz

alt_yesil = np.array([35,40,40])
ust_yesil = np.array([85,255,255])

#  inrange: yeşil yerleri beyaz diğer yerleri siyah yapar

yesil_maske = cv2.inRange(hsv, alt_yesil,ust_yesil)

#  yesil olmayan alanlar için
# bitwise_not : siyaı beyaza, beyazı siyaha çevirir
diger_maske = cv2.bitwise_not(yesil_maske)

# ön plandan yeşil olmayanları alıyoruz

diger = cv2.bitwise_and(on_plan,on_plan, mask=diger_maske)
sadece_arka_plan = cv2.bitwise_and(arka_plan, arka_plan, mask=yesil_maske)

son_goruntu = cv2.add(diger,sadece_arka_plan)
cv2.imshow('orijinal resim', on_plan)
cv2.imshow('yesil alanlar', yesil_maske)
cv2.imshow('sadece nesne', diger)
cv2.imshow('sonuc',son_goruntu)

cv2.waitKey(0)
cv2.destroyAllWindows()