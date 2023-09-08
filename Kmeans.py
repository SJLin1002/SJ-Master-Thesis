import random
import matplotlib.pyplot as plt
import matplotlib.pyplot
matplotlib.interactive(True)
#設K群
clusters=2
node1=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
node2=[round(random.uniform(0,100),3),round(random.uniform(0,3),3)]
# k1=(4,3)
# k2=(5,20)
car_count = 30
data=[]
#5台車
for i in range(car_count):
    data.append([random.randint(0,100), random.choice((0,3))])
print(data)    
    

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
#畫node1,node2 
plt.plot(node1[0],node1[1],'o',color = "brown")
plt.plot(node2[0],node2[1],'o',color = "brown")
p=0

#kmeans
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
        plt.plot(x_clusA, y_clusA, 'o', color='orange')
        plt.plot(x_clusB, y_clusB, 'o', color='cyan')
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
        print("A :",clusA,"Node1 :",New_node1)
        print("B :",clusB,"Node2 :",New_node2)
        plt.plot(New_node1[0],New_node1[1],'o',color = "pink")
        plt.plot(New_node2[0],New_node2[1],'o',color = "green")

        
        if node2 == New_node1 and node1 == New_node2:
            print("break")
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

print("center_point = ",center_point)
plt.plot(center_point[0],center_point[1],'o',color = "green")
print("")
#X總和/數量+Y總和/數量



