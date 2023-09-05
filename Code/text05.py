#V_CAR為加速度

import random
import time
V_CAR = [4,0] #車輛速度
V_UAV = [6,0] #無人機速度(x)

delaytTime = 2.5 #(s)
target=(10,0) #目標位置
location_UAV=[(0,0)]  #無人機及車輛初始位置
location_CAR=[(target)]

#Time[0]=0  沒+delaytime
print("Time0:",0,"location_UAV:",location_UAV[0],"location_car:",location_CAR[0])


a=1
while a<100:
   
    location_UAV.append((location_CAR[a-1])) 
    if a==1: 
        time=delaytTime
    else:
        time=time+(((location_UAV[a][0]-location_UAV[a-1][0])**2+(location_UAV[a][1]-location_UAV[a-1][1])**2)**0.5)/(V_UAV[0]**2+V_UAV[1]**2)**0.5#(Lu[1]-Lu[0])/V_uav
    k=round(random.uniform(0,1),2)
    if k>0.2:
        x=round(random.uniform(-1,1),2)
        V_CAR[0]=V_CAR[0]*(1+x)
        V_CAR[1]=V_CAR[1]*(1+x)
    location_CAR.append((location_CAR[0][0]+time*V_CAR[0],location_CAR[0][1]+time*V_CAR[1])) 
    d=abs(((location_UAV[a][0]-location_CAR[a][0])**2+(location_UAV[a][1]-location_CAR[a][1])**2)**0.5)
    print("Time",a,":",round(time,3),"location_UAV",a,":",location_UAV[a],"location_car",a,":",location_CAR[a],"d=",d)
    
   
    if d <0.5:
        print(a,"is answer")
        #閥值 = 0.5
        break
    
    a+=1

print()
    

#S.T. d[k] / UAV_V <= k
