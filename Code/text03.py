import random
import matplotlib.pyplot as plt
import matplotlib.pyplot
matplotlib.interactive(True)
#設K群
clusters=2
k1=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
k2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
# k1=(4,3)
# k2=(5,20)
car_count = 5
#5台車
data=[[random.randint(0,100), random.choice((0,3))], [random.randint(0,100), random.choice((0,3))], [random.randint(0,100), random.choice((0,3))], [random.randint(0,100),random.choice((0,3))], [random.randint(0,100), random.choice((0,3))]]

# 分散數據點的 X 和 Y 座標
x_values = [point[0] for point in data]
y_values = [point[1] for point in data]

# 繪製所有data點
# 設定x軸和y軸的範圍空間 
plt.xlim((0,120))
plt.ylim((-1,10))
plt.title('graph')
plt.xlabel('Y')
plt.ylabel('X')
plt.plot(x_values, y_values, 'o', color='black')
p=0
while p<50:
    clusA=[]
    clusB=[]    
     
    #車(data)到node1,node2的距離
    for i in range(len(data)):
        d1=((data[i][0]-k1[0])**2+(data[i][1]-k1[1])**2)**0.5
        d2=((data[i][0]-k2[0])**2+(data[i][1]-k2[1])**2)**0.5
        if d1 > d2 :
            clusA.append([data[i][0],data[i][1]])
        else: 
            clusB.append([data[i][0],data[i][1]])
        # print(d1)
        # print(d2)
    Ax = 0
    Ay = 0
    Bx = 0
    By = 0
    node1 = 0
    node2 = 0
    for j in range(len(clusA)):
        Ax += clusA[j][0]
        Ay += clusA[j][1]
    for k in range(len(clusB)):
        Bx += clusB[k][0]
        By += clusB[k][1]
    #重心點
    if len(clusA)==0 or len(clusB)==0:
        k1=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
        k2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
        continue
    else:
        node1 = (Ax/len(clusA),Ay/len(clusA))
        node2 = (Bx/len(clusB),By/len(clusB))
        print("A :",clusA,"Node1 :",node1)
        print("B :",clusB,"Node2 :",node2)
        #畫node1,node2 
        plt.plot(node1[0],node1[1],'o',color = "blue")
        plt.plot(node2[0],node2[1],'o',color = "red")
    
        k1=node1
        k2=node2
        p+=1
print()
#X總和/數量+Y總和/數量



