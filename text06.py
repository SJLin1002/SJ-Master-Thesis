#以時間為基準
import random
import time



V_CAR=40
V_UAV=50

delaytTime = 2.5 #(s)
target=(10,0) #目標位置
location_UAV=[(0,0,1)]  #無人機及車輛初始位置
location_CAR=[(0,0)]

#Time[0]=0  沒+delaytime
print("Time 0 :",0,"location_UAV:",location_UAV[0],"location_car:",location_CAR[0])
# print(location_CAR[0][0])

a=1
while a<100:
     
    if a==1:
        time=delaytTime
        
        location_CAR.append(((location_CAR[0][0]+(delaytTime*V_CAR),location_CAR[0][1])))
        location_UAV.append(location_UAV[0])
        # location_UAV不變
        d=abs(((location_UAV[a][0]-location_CAR[a][0])**2+(location_UAV[a][1]-location_CAR[a][1])**2)**0.5)
        print("Time",a,":",time,"location_UAV",a,":",location_UAV[a],"location_car",a,":",location_CAR[a],"d=",d)
       
    else:
        # print(location_CAR[1][0])
        location_CAR.append(((location_CAR[a-1][0]+(0.5*V_CAR),location_CAR[a-1][1])))
        location_UAV.append(((location_UAV[a-1][0]+(0.5*V_UAV),location_UAV[a-1][1])))

        d=((location_UAV[a][0]-location_CAR[a][0])**2+(location_UAV[a][1]-location_CAR[a][1])**2)**0.5
        print("Time",a,":",time,"location_UAV",a,":",location_UAV[a],"location_car",a,":",location_CAR[a],"d=",d)

        if d <= 1 :
            print("追到了")
            break

              
     
    
    time +=0.5
    a+=1
print("over")


print()
    

#S.T. d[k] / UAV_V <= k
