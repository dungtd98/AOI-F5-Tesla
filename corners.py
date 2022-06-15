import cv2
import numpy as np
drawing = False
points=[]
def nothing(evt):
    pass

def zoom_roi(roi, scale):
    return cv2.resize(roi, None, fx=scale, fy=scale)

def draw_roi(evt, x, y, flags, param):
    global drawing
    if evt == cv2.EVENT_LBUTTONDOWN:
        
        drawing=True
        points.append((x, y))
    elif evt == cv2.EVENT_MOUSEMOVE:
        if len(points)>2:
            del points[1:]
        if drawing == True:
            points.append((x,y))          
    elif evt == cv2.EVENT_LBUTTONUP:
        drawing = False
        points.append((x,y))

def get_limit_color_space(win_name, trackBars=['H','S', 'V']):
    limit_surface = []
    for trackBar in trackBars:
        value = cv2.getTrackbarPos(trackBar, win_name)
        limit_surface.append(value)
    
    return np.array(limit_surface, dtype=np.uint8)

set_win = "setting"
frame_win = 'frame'
cv2.namedWindow(set_win)
cv2.namedWindow(frame_win)
cv2.createTrackbar('maxH', set_win, 255, 255, nothing)
cv2.createTrackbar('maxS', set_win, 255, 255, nothing)
cv2.createTrackbar('maxV', set_win, 255, 255, nothing)

cv2.createTrackbar('minH', set_win, 0, 255, nothing)
cv2.createTrackbar('minS', set_win, 0, 255, nothing)
cv2.createTrackbar('minV', set_win, 0, 255, nothing)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 4608)
cap.set(4, 3456)
cv2.setMouseCallback(frame_win, draw_roi)
while 1:
    key = cv2.waitKey(1)&0xff
    MIN = get_limit_color_space(set_win, 
        trackBars=['minH','minS','minV'])
    MAX = get_limit_color_space(set_win,
        trackBars=['maxH','maxS','maxV'])
    frame = cap.read()[1]
    frame = cv2.resize(frame, (576,432))
    if len(points)==2:
        cv2.rectangle(frame,points[0],
                        points[1],
                        (0,255,0),
                        thickness=1)
    print(points)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, MIN, MAX)

    cv2.imshow(frame_win, frame)

    if key == ord('n'):
        points.clear()
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()