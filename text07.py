import random
import time
import keyboard
import threading
import matplotlib.pyplot as plt
import matplotlib.pyplot
matplotlib.interactive(True)

#按下P停止
def checkKeyInput ():
    global running
    while (running):
        if keyboard.read_key() == "p":
            print("You pressed p")
            running = False

#設K群
clusters=2
node1=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
node2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]

car_num = 10
data=[]
#5台車
for i in range(car_num):
    #data增加car_count台車,[x,y,v]
    data.append([random.randint(0,100), random.choice((0,3)),random.randint(20,100)])

# 分散數據點的 X 和 Y 座標
#x_values = [point[0] for point in data]
#y_values = [point[1] for point in data]

# 繪製所有data點
# 設定x軸和y軸的範圍空間 
# plt.xlim((0,120))
# plt.ylim((-1,10))
# plt.title('graph')
# plt.xlabel('Y')
# plt.ylabel('X')
# plt.plot(x_values, y_values, 'o', color='black')
# #畫node1,node2 
# plt.plot(node1[0],node1[1],'o',color = "brown")
# plt.plot(node2[0],node2[1],'o',color = "brown")
running = True


t = threading.Thread(target = checkKeyInput)
t.start()
count=1
while running:
    print(data) 
    #kmeans
    p=0
    while p<50:
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
            print("A群=None")
            continue
        elif len(clusB)==0:
            node2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
            print("B群=None")
            continue
        else:
            x_clusA = [point[0] for point in clusA]
            y_clusA = [point[1] for point in clusA] 
            x_clusB = [point[0] for point in clusB]
            y_clusB = [point[1] for point in clusB]
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

            New_node1 = (Ax/len(clusA),Ay/len(clusA))
            New_node2 = (Bx/len(clusB),By/len(clusB))
            # print("A :",clusA,"Node1 :",New_node1)
            # print("B :",clusB,"Node2 :",New_node2)
            # plt.plot(New_node1[0],New_node1[1],'o',color = "pink")
            # plt.plot(New_node2[0],New_node2[1],'o',color = "green")

            
            if node2 == New_node1 and node1 == New_node2:
                print("找到node1和2")
                break
            else:
                node2=New_node1
                node1=New_node2
        p+=1
    center_point = ((node1[0]+node2[0])/2,(node1[1]+node2[1])/2)
    plt.clf()
    plt.xlim((0,120))
    plt.ylim((-1,10))
    plt.title('graph')
    plt.xlabel('Y')
    plt.ylabel('X')


    #兩群點不同顏色
    print("A :",clusA,"\n","Node1 :",(round(node1[0],3),round(node1[1],3)))
    plt.plot(New_node2[0],New_node2[1],'o',color = "red")
    plt.plot(x_clusA, y_clusA, 'o', color='orange')

    print("B :",clusB,"\n","Node2 :",(round(node2[0],3),round(node2[1],3)))
    plt.plot(New_node1[0],New_node1[1],'o',color = "blue")
    plt.plot(x_clusB, y_clusB, 'o', color='cyan')

    print("center_point = ",(round(center_point[0],3),round(center_point[1],3)))
    plt.plot(center_point[0],center_point[1],'o',color = "green")
    print("***************")

    for j  in range(0,car_num):    
        #車輛X座標改變
        data[j][0] = round((data[j][0] + data[j][2]),3)  
        k = random.random()
        #更改Y(車道) 80%改變車道
        if k > 0.2 :  
            if data[j][1] == 0:
                data[j][1] = 3
            else: data[j][1] = 0      
        #改變車輛速度  (10% ~ -10%)
        a = random.uniform(0.1,-0.1) 
        New_v = data[j][2] * (1+a)
        data[j][2] = round(New_v,3) 
      
     
    #print(car_num,"台車 ,  Time", count, "新座標為" , data)
    
    
    time.sleep(1)
    count+=1
print("OK")


print("")




