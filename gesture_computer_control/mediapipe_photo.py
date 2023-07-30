import cv2
import numpy as np
import mediapipe as mp
import time
import os
import csv
import pandas as pd
import time

import gb_model
import windows

import subprocess
import signal

# Подключаем камеру
cap = cv2.VideoCapture(0)
cap.set(3, 640) # Width
cap.set(4, 480) # Lenght
cap.set(10, 100) # Brightness

mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
npDraw = mp.solutions.drawing_utils


pTime = 0
cTime = 0

dict = {"1_x": [],
"1_y": [],
"1_z": [],
"2_x": [],
"2_y": [],
"2_z": [],
"3_x": [],
"3_y": [],
"3_z": [],
"4_x": [],
"4_y": [],
"4_z": [],
"5_x": [],
"5_y": [],
"5_z": [],
"6_x": [],
"6_y": [],
"6_z": [],
"7_x": [],
"7_y": [],
"7_z": [],
"8_x": [],
"8_y": [],
"8_z": [],
"9_x": [],
"9_y": [],
"9_z": [],
"10_x": [],
"10_y": [],
"10_z": [],
"11_x": [],
"11_y": [],
"11_z": [],
"12_x": [],
"12_y": [],
"12_z": [],
"13_x": [],
"13_y": [],
"13_z": [],
"14_x": [],
"14_y": [],
"14_z": [],
"15_x": [],
"15_y": [],
"15_z": [],
"16_x": [],
"16_y": [],
"16_z": [],
"17_x": [],
"17_y": [],
"17_z": [],
"18_x": [],
"18_y": [],
"18_z": [],
"19_x": [],
"19_y": [],
"19_z": [],
"20_x": [],
"20_y": [],
"20_z": [],
"21_x": [],
"21_y": [],
"21_z": [],
"target": []}

df = pd.DataFrame(dict)

label = 2

num_comands = 10
label_count = [0] * num_comands

start_time = time.time()

browser_proc = windows.Window(path = '/bin/firefox')
telegram_proc = windows.Window(path = '/bin/Telegram')
current_proc = browser_proc

	#Зацикливаем получение кадров от камеры
while True:

    if (time.time() - start_time > 0.1):
        start_time = time.time()
    else:
        continue
    success, img = cap.read()
    img = cv2.flip(img,1) # Mirror flip

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            points_hand = []
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                points_hand = points_hand + [lm.x * w, lm.y * w, lm.z * w]
               # print(id, lm)
                if  id == 8 or id == 12:
                    cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)

            npDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)



            # with open('eggs.csv', "a", newline="") as file:
            #     user = points_hand
            #     writer = csv.writer(file)
            #     writer.writerow(user)

            # with open('readme.txt', 'a') as f:
            #     s = ''
            #     i = 0
            #     for x in points_hand:
            #         s += (str(x) + ' ')
            #         i += 1
            #
            #     f.write(s)
            #     f.write('\n')
            #     f.write('new')
            #     f.write(str(len(points_hand)))
            #     f.write(str(i))

            label = gb_model.pred([points_hand])
            l = int(label)
            print (l)
            label_count[l] += 1;
            for i in range(1, num_comands):
                label_count[(l + i) % num_comands] = 0


            match label:
                case 1:
                    print (label_count)
                    if label_count[1] > 10:
                            # example.play_cikle(num_comands, cap)
                            browser_proc.open()
                            current_proc = browser_proc

                case 0:
                    print (label_count)
                    if label_count[0] > 10:
                        #if current_proc is not None:
                        current_proc.close()
                    # except:
                    #     browser_proc.kill()
                    #     print ("cant end the process")
                    # if browser_driver is not None and browser_driver.poll() is None:
                    #     browser_driver.terminate()
                    #     browser_driver.wait(1)
                    #     browser_driver = None

                # case _:
                #     break

                case 3:
                    if label_count[3] > 10:
                        telegram_proc.open()
                        #time.sleep(1)
                        current_proc = telegram_proc

            # points_hand = points_hand + [label]
            # new_row = points_hand
            # df.loc[len(df)] = new_row
            break

    else:
        label = 2



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(label)),(10,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2) # ФреймРейт

    cv2.imshow('python', img)
    if cv2.waitKey(20) == 27: # exit on ESC
        break

df.to_csv('out_2.csv')

cv2.destroyWindow("python")
cap.release()
cv2.waitKey(1)
