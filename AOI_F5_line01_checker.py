import cv2
import numpy as np
import csv
import FINS_TCP
from FINS_TCP import *
import time
from datetime import datetime, date


ip='192.168.250.1'
cmd_NADS = MakeFrame().FINScmdHeader(length_cmd=4, cmd=0)
soc = TCPconnect(host=ip, port=9600)
soc.connectt()


def readDM(area):
    content = soc.ReadMemory(FINS_TCP.FinsCommandCode().MEMORY_AREA_READ,
                            FINS_TCP.FinsPLCMemoryAreas().DATA_MEMORY_WORD, area)
    return content

def writeDM(area, mess):
    soc.WriteMemory(FINS_TCP.FinsCommandCode().MEMORY_AREA_WRITE,
                    FINS_TCP.FinsPLCMemoryAreas().DATA_MEMORY_WORD, area, mess)

def saveImg(dir, frame):
    now = datetime.now()
    time = now.strftime("%H:%M:%S").replace(':', '-')
    today = str(date.today()).replace('-','')
    cv2.imwrite(r'./image/'+today+dir+ time +'.jpg', frame)

with open('setting.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    setting_data = []
    for row in reader_obj:
        row = [int(i) for i in row]
        setting_data.append(row)
print(setting_data)
MIN = np.array(setting_data[0], dtype = np.uint8)
MAX = np.array(setting_data[1], dtype = np.uint8)
pointA = setting_data[2]
pointA = (pointA[0], pointA[1])

pointB = setting_data[3]
pointB = (pointB[0], pointB[1])

with open('area.csv') as file_obj:
    reader = csv.reader(file_obj)
    for row in reader:
        area_lim = [int(i) for i in row]


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 2592)
cap.set(4, 1944)

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

def zoom_roi(roi, scale):
    return cv2.resize(roi, None, fx=scale, fy=scale)
kernel = np.ones((5,5), np.uint8)
while 1:
    area = 0
    key = cv2.waitKey(1)&0xff
    frame = cap.read()[1]
    frame = cv2.resize(frame, (648,486))
    frame = cv2.flip(frame, 0)
    roi = cropped_roi(pointA, pointB)
    roi = zoom_roi(roi, 5)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, MIN, MAX)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8))
    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts)>=1:
        max_contour = max(cnts, key=cv2.contourArea)
        area = cv2.contourArea(max_contour)
        x,y,w,h = cv2.boundingRect(max_contour)
    if key == ord('c'):
        print(area,w,h)
    if readDM(300)[-1] == 1:
        print(area)
        writeDM(300,0)
        if area_lim[1]>area>area_lim[0]:
            cv2.putText(roi, 'OK', (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
            saveImg('/OK/', roi)
            writeDM(301,1)
        else:
           
            cv2.putText(roi, 'NG', (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255), 2)
            saveImg('/NG/', roi)
            writeDM(302,1)
        cv2.imshow('roi', roi)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
