#car location 

import random
import matplotlib.pyplot as plt
import keyboard
import time

# # 按按鈕
# while True:
#     print("1")
#     time.sleep(2)  
#     if keyboard.read_key() == "p":
#         print("You pressed p")
#         break

#車輛數X
car_num=5
car=[]

#車輛初始位置(x,y,v)
for i  in range(1,car_num+1):
    x = random.randint(0,100)
    y = random.choice([0,3])
    v = random.randint(20,100)
    car.append([x,y,v])  # 將新的 [x, y, v] 值添加到 car 列表
print(car_num,"台車" , "座標為" , car)
t=1
while True:
    
    for j  in range(0,car_num):    
        car[j][0] = round((car[j][0] + car[j][2]),3)  #車輛X座標改變

        k = random.random()
        if k > 0.2 :  #更改Y(車道) 
            if car[j][1] == 0:
                car[j][1] = 3
            else: car[j][1] = 0        
        a = random.uniform(0.1,-0.1) 
        New_v = car[j][2] * (1+a)
        car[j][2] = round(New_v,3) #更改車輛速度
    print(car_num,"台車Time", t , "座標為" , car)
    if keyboard.read_key() == "p":
        print("You pressed p")
        break
    time.sleep(1)
    t+=1
    
print("A")       


while True:

    print("A")
    time.sleep(1)

        

''' 
V_UAV = (0,6) #無人機速度(y)
V_CAR = (0,4) #車輛速度
target=(0 ,10) #目標位置
totalTime = 5 #花費時間(s)  
location_UAV=[]
location_CAR=[] 
location_UAV.append((1,2)) 
location_CAR.append((3,4)) 
location_UAV.append((5,6)) 
location_UAV[0]=(7,8)
print(location_CAR)
print(location_UAV)
#S.T. d[k] / UAV_V <= k

'''