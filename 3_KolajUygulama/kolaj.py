import cv2
import pandas as pd 
import numpy as np


def kolaj_olustur(csv_dosyasi):
    df = pd.read_csv(csv_dosyasi)
    kesilmis_resimler = []
    
    
    for index, satir in df.iterrows():
        # satırdaki veriler değişkenlere atanır
        
        yol = satir['resim_yolu']
        x1,y1 = satir['x1'], satir['y1']
        x2,y2 = satir['x2'], satir['y2']
        
        resim = cv2.imread(yol)
        
        if resim is None:
            print(f"hata: {yol} bulunamadi ")
            continue
        
        # numpy ile kırpma
        kirpilmis = resim[y1:y2, x1:x2]
        
        # standart boyuta getir
        
        std_resim = cv2.resize(kirpilmis, (200,200))
        
        kesilmis_resimler.append(std_resim)
        
    if len(kesilmis_resimler) > 0:
        
        kolaj = np.hstack(kesilmis_resimler) #horizontal stack -> yatayda yan yana yapıştırır
        
        cv2.imshow("otomatik kolaj", kolaj)
        cv2.imwrite("sonuc_kolaj.jpg", kolaj)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("birleştirecek resim yok ")
        
kolaj_olustur('kolajverileri.csv')