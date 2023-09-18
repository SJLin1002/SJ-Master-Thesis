import random
import time
import copy

#一開始的車子位置data
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
    for car  in dataA:
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

 #k-means 分群
def kmeans(data):
    #kmeans 
    # clusters=2
    node1=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
    node2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
    
    while True:

        clusA=[]
        clusB=[]    
        #車(data)到node1,node2的距離-分群
        for i in range(len(data)):
            d1=((data[i][0]-node1[0])**2+(data[i][1]-node1[1])**2)**0.5
            d2=((data[i][0]-node2[0])**2+(data[i][1]-node2[1])**2)**0.5
            if d1 > d2 :
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
            # x_clusA = [point[0] for point in clusA]
            # y_clusA = [point[1] for point in clusA] 
            # x_clusB = [point[0] for point in clusB]
            # y_clusB = [point[1] for point in clusB]
            #兩群點不同顏色
            # plt.plot(x_clusA, y_clusA, 'o', color='orange')
            # plt.plot(x_clusB, y_clusB, 'o', color='cyan')
            # print("A :",clusA)
            # print("B :",clusB)
           
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
            # print("A :",clusA,"Node1 :",New_node1)
            # print("B :",clusB,"Node2 :",New_node2)
            # plt.plot(New_node1[0],New_node1[1],'o',color = "pink")
            # plt.plot(New_node2[0],New_node2[1],'o',color = "green")

            
            if node2 == New_node1 and node1 == New_node2:
                # print("A :",clusA,"Node1 :",New_node1)
                # print("B :",clusB,"Node2 :",New_node2)
                break
            else:
                node2=New_node1
                node1=New_node2
    # print("A :",clusA,"Node1 :",New_node1)
    # print("B :",clusB,"Node2 :",New_node2) 
    center_point = ((node1[0]+node2[0])/2,(node1[1]+node2[1])/2)    
    return center_point        


# 模擬時間循環
def sim(data,location_UAV):
    time_step = 0.5
    times = 1
    print("First Car Positions at Time 0:", kmeans(data))
    for i in range(1, int(delaytTime/0.5)+1): 
        # 更新車輛位置
        data = simulation_change_car_data(data)
        # 在每段時間，找到車輛中心點
        center_point = kmeans(data)
        # print(f"CenterPoint at Time {i}:", center_point)
    print("Time 0:",delaytTime,"s" )
    print("Updated Car Positions at Time 1:", data)
    print("CenterPoint:", center_point)

    while True:
        print(f"Time {times}:", time_step + delaytTime,"秒")
        
        # 更新车辆位置
        data =simulation_change_car_data(data)
        print(f"Updated Car Positions at Time {time_step}:", data)
        
        # 在每个时间步骤中进行进一步的分析，例如找到车辆位置的中心点
        center_point = kmeans(data)
        print(f"CenterPoint at Time {time_step}:", center_point)


        location_UAV=((location_UAV[0]+location_UAV[2]),location_UAV[1],location_UAV[2])
        
        d=((location_UAV[0]-center_point[0])**2+(location_UAV[1]-center_point[1])**2)**0.5
        print("距離 :",d)
        # if d<5:
        if location_UAV[0] > center_point[0]:
            print("sim",time_step + delaytTime,"秒 OKOK") 
            break
        time_step+=.5
        times+=1
        time.sleep(0.5)
    print("")
# 實際時間循環
def act(data,location_UAV):
    time_step = 0.5
    times  = 1
    #經delaytime，車子的位置及車輛中心點
    print("First Car Positions at Time 0:", kmeans(data))
    for i in range(1, int(delaytTime/0.5)+1):  
        # 更新車輛位置
    
        data = actual_change_car_data(data)
        # 在每段時間，找到車輛中心點

        center_point = kmeans(data)
        # print(f"CenterPoint at Time {i}:", center_point)
    print("Time 0:",delaytTime )
    print("Updated Car Positions at Time 1:", data)
    print("CenterPoint:", center_point)

    while True:
        print(f"Time {time_step}:", time_step + delaytTime,"秒")
        
        # 更新车辆位置
        data =actual_change_car_data(data)
        print(f"Updated Car Positions at Time {time_step}:", data)
        
        # 在每个时间步骤中进行进一步的分析，例如找到车辆位置的中心点
        center_point = kmeans(data)
        print(f"CenterPoint at Time {time_step}:", center_point)


        location_UAV=((location_UAV[0]+location_UAV[2]),location_UAV[1],location_UAV[2])
        
        d=((location_UAV[0]-center_point[0])**2+(location_UAV[1]-center_point[1])**2)**0.5
        print("距離 :",d)
        # if d<5:
        if location_UAV[0] > center_point[0]:
            print("act",time_step + delaytTime,"秒 OKOK") 
            break
        time_step+=0.5
        times += 1
        time.sleep(0.5)
    print("")

#initial
car_num = 5
O_data=create_car(car_num)
dataS = copy.deepcopy(O_data)
dataA = copy.deepcopy(O_data)   

print("初始車輛位置 : ",O_data) 
#無人機時速126km/hr(35m/s)
V_UAV=35
delaytTime = 3 #(s)
location_UAV=(0,0,V_UAV)  #無人機初始位置


sim(dataS,location_UAV)
print("sim OK")

act(dataA,location_UAV)
print("act OKOK")

print()