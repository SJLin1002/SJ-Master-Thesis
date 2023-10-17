# 依距離作比較

import random
import time
import copy
import openpyxl
from openpyxl.styles import Alignment

def create_car(car_num): 
    data = []
    for i in range(car_num):
        # data增加car_count台車,[x,y,v]copy
        data.append(
            [random.randint(0, 100), random.choice((0, 3)), random.randint(15, 30)]
            #車輛時速54~108km/hr(15~30m/s)
        )
    return data

#更新data,0.5秒
def actual_change_car_data(dataA):
    for car in dataA:
        #車輛X座標改變
        car[0] = round((car[0] + (car[2]*timeslot)),3)  
        
        #更改Y(車道) 80%改變車道
        k = random.random()
        if k > 0.2 :
            if car[1] == 0:
                car[1] = 3
            else: car[1] = 0      
        #改變車輛速度  (10% ~ -10%)
        a = random.uniform(0.1,-0.1) 
        New_v = car[2] * (1+a)
        car[2] = round(New_v,3) 
    # print(data)
    return dataA


def constant_speed(data,time):
    #車輛在時間time後的位置
    for car in data:
        car[0] = round(car[0] + (car[2] * time))
    return data


def kmeans(data):
    #kmeans 
    # clusters=2，隨機生成兩點
    node1=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
    node2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
    while True:
        clusA=[]
        clusB=[]    
        #車(data)到node1,node2的距離-分群
        for i in range(len(data)):
            d1=((data[i][0]-node1[0])**2+(data[i][1]-node1[1])**2)**0.5
            d2=((data[i][0]-node2[0])**2+(data[i][1]-node2[1])**2)**0.5
            if d1 < d2 :
                clusA.append([data[i][0],data[i][1]])
            else: 
                clusB.append([data[i][0],data[i][1]])
            # print("d1 :",d1)
            # print("d2 :",d2)
        #重心點
        if len(clusA)==0 :
            node1=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
            #print("A群=None")
            continue
        elif len(clusB)==0:
            node2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
            #print("B群=None")
            continue
        else:
            Ax = 0
            Ay = 0
            Bx = 0
            By = 0

            for j in range(len(clusA)):
                Ax += clusA[j][0]
                Ay += clusA[j][1]
            for k in range(len(clusB)):
                Bx += clusB[k][0]
                By += clusB[k][1]

            New_node1 = (round(Ax/len(clusA),3),round(Ay/len(clusA),3))
            New_node2 = (round(Bx/len(clusB),3),round(By/len(clusB),3))
         
            if node1 == New_node1 and node2 == New_node2:
                # print("A :",clusA,"Node1 :",New_node1)
                # print("B :",clusB,"Node2 :",New_node2)
                break
            else:
                node1=New_node1
                node2=New_node2
    # print("A :",clusA,"Node1 :",New_node1)
    # print("B :",clusB,"Node2 :",New_node2) 
    close = 1000
    for q in range(len(clusA)):
        for w in range(len(clusB)):
            dis = ((clusA[q][0]-clusB[w][0])**2+(clusA[q][1]-clusB[w][1])**2)**0.5
            if dis < close :
                close = dis
                closeA = clusA[q]
                closeB = clusB[w]
    # center_point = ((node1[0]+node2[0])/2,(node1[1]+node2[1])/2)  
    # print(closeA,closeB)
    center_point = ((closeA[0]+closeB[0])/2, (closeA[1]+closeB[1])/2)
    return center_point

def act(dataA,location_UAV):
    i=1
    while i < int(delaytTime/timeslot):
        dataA = actual_change_car_data(dataA)
        if i >= t/timeslot :
            N_New_center = kmeans(dataA)

        i+=1
    


    timeA = delaytTime
    
    #經過delaytime之後，車群位置(車速每0.1秒改變一次)
    for i in range(0,int(delaytTime/timeslot)):
        dataA = actual_change_car_data(dataA)


    while True :
        center_pointA = kmeans(dataA)
        
        d = ((center_pointA[0]-location_UAV[0])**2 + (center_pointA[1]-location_UAV[1])**2)**0.5
        # 無人機飛過去需要t1的時間
        t1 = d/V_UAV 

        for i in range(int(t1/timeslot)):
            dataA = actual_change_car_data(dataA)
        timeA = timeA + t1
        print("act 時間 : ",timeA)
        print("center_point : ",center_pointA,"UAV_location :",location_UAV)
        print("距離 : ",d,"時間：",t1) 
        # 更新無人機位置
        location_UAV = (center_pointA[0], center_pointA[1], location_UAV[2])
        print()
        if d<=1:
            break
    return N_New_center , center_pointA ,timeA


def sim(dataS,location_UAV):
    #經過delaytime之後，車群位置(等速)
    dataS = constant_speed(dataS,delaytTime)
    timeS = delaytTime
    while True :
        center_pointS = kmeans(dataS)
        
        d = ((center_pointS[0]-location_UAV[0])**2 + (center_pointS[1]-location_UAV[1])**2)**0.5
        # 無人機飛過去需要t1的時間
        t1 = d/V_UAV 
        
        dataS = constant_speed(dataS,t1)
        timeS = timeS + t1
        print("sim 時間 : ",timeS)
        print("center_point : ",center_pointS,"UAV_location :",location_UAV)
        print("距離 : ",d,"時間：",t1) 
        # 更新無人機位置
        location_UAV = (center_pointS[0], center_pointS[1], location_UAV[2])
        print()
        if d<=1:
            break
    
    return center_pointS , timeS

#時間間隔
timeslot = 0.1

V_UAV = 35
delaytTime = 3 #(s)
location_UAV=(0,0,V_UAV)  #無人機初始位置

car_num = 10
# O_data=create_car(car_num)
O_data = [[36, 0, 19], [88, 3, 22], [53, 3, 20], [65, 3, 16], [18, 3, 18], [24, 3, 21], [92, 3, 27], [37, 3, 23], [91, 0, 26], [50, 3, 24]]

dataA = copy.deepcopy(O_data)
dataS = copy.deepcopy(O_data)

# 第一次位置(用於無預測)
center_point = kmeans(O_data)
d =((location_UAV[0]-center_point[0])**2+(location_UAV[1]-center_point[1])**2)**0.5
t = round(d/35,3)

sim = sim(dataS,location_UAV)
act = act(dataA,location_UAV)



# 這個(sim和act是追上的centerpoint)，不是(act追上後，sim的位置)
d1 = ((sim[0][0]-act[1][0])**2+(sim[0][1]-act[1][1])**2)**0.5

print("sim_location :",sim[0])
print("sim_time :",sim[1])
print("act_location :",act[1])
print("act_time:",act[2])


New_center = act[0]
d2 = ((New_center[0]-center_point[0])**2+(New_center[1]-center_point[1])**2)**0.5

print("d1 = ",d1)
print("d2 = ",d2)

