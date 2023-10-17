# main6 + Nopred

import random
import time
import copy
import openpyxl
from openpyxl.styles import Alignment


def all():

    def create_car(car_num): 
        data = []
        for i in range(car_num):
            # data增加car_count台車,[x,y,v]copy
            data.append(
                [random.randint(0, 100), random.choice((0, 3)), random.randint(15, 30)]
                #車輛時速54~108km/hr(15~30m/s)
            )
        return data

    #更新data,1秒?! 
    def actual_change_car_data(dataA):
        for car in dataA:
            #車輛X座標改變
            car[0] = round((car[0] + car[2]),3)  
            k = random.random()
            #更改Y(車道) 80%改變車道
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

    def simulation_change_car_data(dataS):
        for car in dataS:
            #車輛X座標改變
            car[0] = round((car[0] + car[2]),3)        
        return dataS

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

    def act(dataA):
        # 更新車輛位置(1秒)
        dataA = actual_change_car_data(dataA)
        # 在每段時間，找到車輛中心點
        center_point = kmeans(dataA)
        return center_point

    def sim(dataS):
        dataS = simulation_change_car_data(dataS)
        center_point = kmeans(dataS)
        return center_point

    def uav(location_UAV):
        location_UAV = (location_UAV[0]+location_UAV[2],location_UAV[1],location_UAV[2])
        return location_UAV

    def d1(delaytTime,location_UAV):
        Num = 0
        lockA = 0
        lockS = 0

        while True : 
            
            print("Num :",Num)

            if Num>delaytTime:
                location_UAV = uav(location_UAV)
            print("UAV : ",location_UAV)

            if lockA == 0 :
                a = act(dataA)
                print("act : ",a)
                if a[0] < location_UAV[0] :
                    lockA = 1
                    dA = a[0]
                    print("okok")
            else : 
                print("act : ",a,"okok")

            if lockS == 0 : 
                s = sim(dataS)
                print("sim : ",s)
                if s[0] < location_UAV[0] :
                    lockS = 1
                    dS = s[0]
                    print("okok")
            else : 
                print("sim : ",s,"okok")
            
            
            print()
        
            # 無人機追上實際
            
            if ((lockA == 1) and (lockS == 1)) :
                D = abs(dA-dS)
                print("D = ",D)
                break

            Num += 1
        return D

    def d2(dataN):

        center_point = kmeans(dataN)
        d =((location_UAV[0]-center_point[0])**2+(location_UAV[1]-center_point[1])**2)**0.5
        t = round(d/35,3)
        print("初始車輛位置 : ",O_data)
        print("初始中心點 : ",center_point) #k1
        print("初始無人機位置 : ",(location_UAV[0],location_UAV[1]))
        print("距離相差 : ",d)
        print("無人機飛行時間 :",t)


        #以0.5秒為單位，車子等速前進
        # for i in range(0,int(t/0.5)):
        #     dataN = simulation_change_car_data(dataN)

        dataN = constant_speed(dataN,t)

        New_center = kmeans(dataN)
        print("實際車輛中心點為 : ",New_center)  #k2

        ans = ((New_center[0]-center_point[0])**2+(New_center[1]-center_point[1])**2)**0.5
        print("兩點相差距離 : ",ans)

        return ans


    car_num = 10
    O_data=create_car(car_num)
    # O_data = [[36, 0, 19], [88, 3, 22], [53, 3, 20], [65, 3, 16], [18, 3, 18], [24, 3, 21], [92, 3, 27], [37, 3, 23], [91, 0, 26], [50, 3, 24]]
    # timeslot = 0.1
    dataA = copy.deepcopy(O_data)
    dataS = copy.deepcopy(O_data)  
    dataN = copy.deepcopy(O_data)
    V_UAV = 35
    delaytTime = 3 #(s)
    location_UAV=(0,0,V_UAV)  #無人機初始位置
    d1 = d1(delaytTime,location_UAV)

    d2 = d2(dataN)
    # d=abs(d1-d2)
    d=d1-d2
    print("D1 = ",d1)

    print("D2 = ",d2) 

    print("D1 - D2 = ",d)   

    return d1,d2,d
#使用openpyxl 內 Workbook 方法建立一個新的工作簿
workbook = openpyxl.Workbook()
#取得第一個工作表
sheet = workbook.worksheets[0]
sheet['A1'] = "模擬"
sheet['B1'] = "無預測"
sheet['C1'] = "D1 - D2"

for i in range(2,12):
    k = all()
    sheet['A'+str(i)] = k[0]
    sheet['B'+str(i)] = k[1]
    sheet['C'+str(i)] = k[2]


workbook.save('D .xlsx')

