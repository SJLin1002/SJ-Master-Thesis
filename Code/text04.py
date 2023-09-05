#V_CAR等速情況

import random
import time
V_CAR = (4,2) #車輛速度
V_UAV = (6,3) #無人機速度(x)
delaytTime = 2.5 #(s)
target=(10,0) #目標位置
location_UAV=[(0,0)]  #無人機及車輛初始位置
location_CAR=[(target)] 

#Time[0]=0  沒+delaytime
print("Time0:",0,"location_UAV:",location_UAV,"location_car:",location_CAR[0])

#Time[1]=2.5 
time=delaytTime  #時間2.5 開始
location_UAV.append((location_UAV[0][0]+time*V_UAV[0],location_UAV[0][0]+time*V_UAV[1])) #無人機新位置
location_CAR.append((location_CAR[0][0]+time*V_CAR[0],location_CAR[0][1]+time*V_CAR[1])) #車輛新位置
print("Time1:",time,"location_UAV:",location_UAV[1],"location_car:",location_CAR[1])

a=2
while a<20:
    location_UAV.append((location_CAR[a-1]))   
    time=(((location_UAV[a][0]-location_UAV[0][0])**2+(location_UAV[a][1]-location_UAV[0][1])**2)**0.5)/V_UAV[0] #(Lu[1]-Lu[0])/V_uav
    location_CAR.append((location_CAR[0][0]+time*V_CAR[0],location_CAR[0][1]+time*V_CAR[1])) 
    d=abs(((location_UAV[a][0]-location_CAR[a][0])**2+(location_UAV[a][1]-location_CAR[a][1])**2)**0.5)
    print("Time",a,":",time,"location_UAV[",a,"]:",location_UAV[a],"location_car[",a,"]:",location_CAR[a],"d=",d)
    a+=1
   
    if d <0.5:
        print(a,"is answer")
        break
print()

#S.T. d[k] / UAV_V <= k
