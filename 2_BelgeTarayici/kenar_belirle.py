import cv2
import numpy as np 

def kagıt_tespit_et():
    
    kamera = cv2.VideoCapture(0)
    
    if not kamera.isOpened():
        print("hata")
        return
    
    while True:
        ret, kare = kamera.read()
        if not ret:
            break
        
        gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gri, (5,5),0)
        
        kenarlar = cv2.Canny(blur,75,200)
        
        # Konturları (şekilleri) çıkar
        konturlar, _ = cv2.findContours(kenarlar, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # En büyük 5 konturu seçiyoruz (Kağıt genellikle en büyüğüdür)
        konturlar = sorted(konturlar, key=cv2.contourArea, reverse=True)[:5]
         
        kagit_koseleri = None
        
        for kontur in konturlar:
            
            cevre = cv2.arcLength(kontur, True)
            yaklasik_sekil = cv2.approxPolyDP(kontur, 0.02* cevre, True)
            
            if len(yaklasik_sekil) == 4:
                kagit_koseleri = yaklasik_sekil
                break
            
        
        onizleme = kare.copy()
        
        if kagit_koseleri is not None:
            cv2.drawContours(onizleme, [kagit_koseleri], -1,(0,255,0),3)
            
        cv2.imshow("kagit algilama testi", onizleme)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    kamera.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    kagıt_tespit_et()