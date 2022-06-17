import cv2
import numpy as np
import csv
drawing = False

point0 = None
point1 = None
def nothing(evt):
    pass

def zoom_roi(roi, scale):
    return cv2.resize(roi, None, fx=scale, fy=scale)

def draw_roi(evt, x, y, flags, param):
    global drawing , point0, point1
    if evt == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        point0 = (x,y)
        
    elif evt == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            point1 = (x,y)

    elif evt == cv2.EVENT_RBUTTONDOWN:
        drawing = False
        point1 =(x, y)

def get_limit_color_space(win_name, trackBars=['H', 'S', 'V']):
    limit_surface = []
    for trackBar in trackBars:
        value = cv2.getTrackbarPos(trackBar, win_name)
        limit_surface.append(value)
    return np.array(limit_surface, dtype=np.uint8)

def cropped_roi(point0, point1):
    (x1, y1) = point0
    (x2, y2) = point1
    if x1>x2 and y1>y2:
        roi = frame[y2:y1, x2:x1]
    if x1<x2 and y1>y2:
        roi = frame[y2:y1, x1:x2]
    if x1<x2 and y1<y2:
        roi = frame[y1:y2, x1:x2]
    if x1>x2 and y1<y2:
        roi = frame[y1:y2, x2:x1]
    if x1==x2 or y1==y2:
        roi = frame[y1:y1+1, x1:x1+1]
    return roi

def check_cnt(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, 
            cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key = cv2.contourArea)
    area = cv2.contourArea(max_contour)
    x,y,w,h = cv2.boundingRect(max_contour)
    print(area)
    
set_win = "setting"
frame_win = 'frame'
cv2.namedWindow(set_win, cv2.WINDOW_NORMAL)
cv2.resizeWindow(set_win, 500, 120)
cv2.namedWindow(frame_win)
cv2.createTrackbar('maxH', set_win, 255, 255, nothing)
cv2.createTrackbar('maxS', set_win, 255, 255, nothing)
cv2.createTrackbar('maxV', set_win, 255, 255, nothing)

cv2.createTrackbar('minH', set_win, 0, 255, nothing)
cv2.createTrackbar('minS', set_win, 0, 255, nothing)
cv2.createTrackbar('minV', set_win, 0, 255, nothing)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 2592)
cap.set(4, 1944)
cv2.setMouseCallback(frame_win, draw_roi)
kernel = np.ones((5,5), np.uint8)
while 1:
    key = cv2.waitKey(1)&0xff
    MIN = get_limit_color_space(set_win, 
        trackBars=['minH', 'minS', 'minV'])
    MAX = get_limit_color_space(set_win,
        trackBars=['maxH', 'maxS', 'maxV'])
    frame = cap.read()[1]
    frame = cv2.resize(frame, (648,486))
    frame = cv2.flip(frame, 0)
    if point0 is not None and point1 is not None:
        cv2.rectangle(frame, point0, point1, (0,255,0), thickness=1)
        roi_img = cropped_roi(point0, point1)
        roi_img = zoom_roi(roi_img, 5)
        hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, MIN, MAX)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8))
        check_cnt(mask)
        cv2.imshow('roi', roi_img)
        cv2.imshow('mask', mask)
    cv2.imshow(frame_win, frame)
    
    if key == ord('s'):
        with open('setting.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            rows = [
                MIN.tolist(),
                MAX.tolist(),
                [point0[0],point0[1],0],
                [point1[0],point1[1],0]
            ]
            writer.writerows(rows)
            print("Saved successfully")

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()