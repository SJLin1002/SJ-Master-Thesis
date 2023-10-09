
# 無預測
import random
import time
import copy


def create_car(car_num): 
    data = []
    for i in range(car_num):
        # data增加car_count台車,[x,y,v]copy
        data.append(
            [random.randint(0, 100), random.choice((0, 3)), random.randint(15, 30)]
            #車輛時速54~108km/hr(15~30m/s)
        )
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
    center_point = ((node1[0]+node2[0])/2,(node1[1]+node2[1])/2)    
    return center_point       

def simulation_change_car_data(dataS):
    #車輛X座標等速改變
    #每0.5秒車子改變速度
    for car in dataS:
         car[0] = round((car[0] + (car[2]/2)),3)        
    return dataS

def constant_speed(data,time):
    #車輛在時間time後的位置
    for car in data:
        car[0] = round(car[0] + (car[2] * time))



car_num = 10
O_data=create_car(car_num)
# O_data = [[36, 0, 19], [88, 3, 22], [53, 3, 20], [65, 3, 16], [18, 3, 18], [24, 3, 21], [92, 3, 27], [37, 3, 23], [91, 0, 26], [50, 3, 24]]
dataN = copy.deepcopy(O_data)

center_point = kmeans(dataN)
V_UAV = 35
#無人機時速126km/hr(35m/s)
location_UAV=(0,0,V_UAV)  #無人機初始位置
d =((location_UAV[0]-center_point[0])**2+(location_UAV[1]-center_point[1])**2)**0.5
t = round(d/35,3)
print("初始車輛位置 : ",O_data)
print("初始中心點 : ",center_point) #k1
print("初始無人機位置 : ",(location_UAV[0],location_UAV[1]))
print("距離相差 : ",d)
print("無人機飛行時間 :",t)


#以0.5秒為單位，車子等速前進
for i in range(0,int(t/0.5)):
    dataN = simulation_change_car_data(dataN)

# constant_speed(dataN,t)

New_center = kmeans(dataN)
print("實際車輛中心點為 : ",New_center)  #k2

ans = ((New_center[0]-center_point[0])**2+(New_center[1]-center_point[1])**2)**0.5
print("兩點相差距離 : ",ans)


