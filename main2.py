
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

    #更新data,每timeslot秒秒?! 
    def actual_change_car_data(dataA):
        for car in dataA:
            #車輛X座標改變
            car[0] = round((car[0] + (car[2]*timeslot)),3)  
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
            car[0] = round((car[0] + (car[2]*timeslot)),3)        
        return dataS

    def constant_speed(data,time):
        #車輛在時間time後的位置(等速)
        for car in data:
            car[0] = round(car[0] + (car[2] * time))
        return data

    # 兩點中點(新)
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
        # 更新車輛位置(每timeslot秒)
        dataA = actual_change_car_data(dataA)
        # 在每段時間，找到車輛中心點
        center_point = kmeans(dataA)
        return center_point

    def sim(dataS):
        center_point = kmeans(dataS)
        dataS = simulation_change_car_data(dataS)
        return center_point

    def uav(location_UAV):
        location_UAV = (location_UAV[0]+location_UAV[2]*timeslot,location_UAV[1],location_UAV[2])
        return location_UAV

    def SimAct(location_UAV,dataA):
        Num = 0
        location_UAV0 = location_UAV
        while True : 
            #無人機delaytTime秒後追
            print("Num :",Num)
            if Num>delaytTime:
                location_UAV = uav(location_UAV)
            print("UAV : ",location_UAV)

            s = sim(dataS)
            print("sim : ",s)
            

            #d1，sim在delaytTime時
            if Num == delaytTime:
                # 位置
                latency_S = s
                latency_D = ((latency_S[0]**2-location_UAV0[0]**2)+(latency_S[1]**2-location_UAV0[1]**2))**0.5
                # 時間
                latency_T =  latency_D/V_UAV
                print("ACT okok")

            #d2 無人機追上sim時
            if s[0] < location_UAV[0] :
                dS = s #記下無人機追上dataS中點時，center_point的位置
                tS = Num #記下無人機追上dataS中點的時間
                print("SIM okok")
                break
    
            print()
            Num += timeslot 
        print("D2追到的位置 : ",dS)
        print("D2追到的時間 : ",tS)
        
        # D2
        for i in range(int(tS/timeslot)):
            dataA = actual_change_car_data(dataA)
            # D1
            if i == int(latency_T/timeslot) :
                dA = dataA
                a = kmeans(dA)
        s = kmeans(dataA)
        print(tS,"秒時，實際車群中心位置 :",s)
        #D1 車輛群經過delaytimec(3秒)後，實際車輛群的位置(a-latency_S)
        d1 = ((a[0]-latency_S[0])**2+(a[1]-latency_S[1])**2)**0.5

        #D2 無人機追上時SIM時，ACT實際位置(s - dS)
        
        d2 =((s[0]-dS[0])**2+(s[1]-dS[1])**2)**0.5

        print("d1距離 : ",d1)
        print("d2距離 : ",d2)

        return d1,d2


    car_num = 10
    O_data = create_car(car_num)
    # O_data = [[36, 0, 19], [88, 3, 22], [53, 3, 20], [65, 3, 16], [18, 3, 18], [24, 3, 21], [92, 3, 27], [37, 3, 23], [91, 0, 26], [50, 3, 24]]
    timeslot = 0.5 #時間間隔
    dataA = copy.deepcopy(O_data)
    dataS = copy.deepcopy(O_data)  
    dataN = copy.deepcopy(O_data)
    V_UAV = 35
    delaytTime = 3 #(s)
    location_UAV=(0,0,V_UAV)  #無人機初始位置


    SimAct= SimAct(location_UAV,dataA)

    print("D1 = ",SimAct[0],"D2 = ",SimAct[1])
    print()
    return SimAct


# #使用openpyxl 內 Workbook 方法建立一個新的工作簿
# workbook = openpyxl.Workbook()
# 開啟Excel文件
workbook = openpyxl.load_workbook('main2_data .xlsx')
#取得第一個工作表
sheet = workbook.worksheets[0]



D1_total = 0
D2_total = 0
n = 10
sheet['A1'] = "NO"
sheet['B1'] = "D1無預測"
sheet['C1'] = "D2模擬"
sheet['A13'] = "Total"
sheet['A14'] = "Average"
for i in range(2,n+3):
    k = all()
    sheet['A'+str(i)] = i-2
    sheet['B'+str(i)] = k[0]

    sheet['C'+str(i)] = k[1]
    
    D1_total += k[0]
    D2_total += k[1]
sheet['B'+str(n+3)] =D1_total
sheet['C'+str(n+3)] =D2_total
sheet['B'+str(n+4)] =(D1_total/n)
sheet['C'+str(n+4)] =(D2_total/n)
workbook.save('main2_data .xlsx')












