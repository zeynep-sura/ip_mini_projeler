import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    hsv= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    alt_mavi = np.array([100,150,0])
    ust_mavi = np.array([140,255,255])
    
    maske = cv2.inRange(hsv,alt_mavi,ust_mavi)
    
    konturlar, _ = cv2.findContours(maske, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for kontur in konturlar:
        x,y,w,h = cv2.boundingRect(kontur)
        
        # (x,y) : sol üst köşe 
        # x+w (widht-genişlik), y+h(height): sağ alt köşe 
        
        cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
        
        cv2.putText(frame,"mavi nesne",(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,255,0),2)
        
    cv2.imshow("takip",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()