import numpy as np
import cv2 

drawing = False
point = (0,0)

def mouse_drawing(event, x, y, flags, params):
    global point, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            cv2.rectangle(frame,point,(x,y),(0,0,255),0)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame,point,(x,y),(0,0,255),0)

cap = cv2.VideoCapture(0)
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

while True:
   _, frame = cap.read()
   cv2.imshow("Frame", frame)
   key = cv2.waitKey(25)
   if key== 13:    
     print('done')
   elif key == 27:
     break

cap.release()
cv2.destroyAllWindows()