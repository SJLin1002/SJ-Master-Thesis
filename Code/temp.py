from random import randint, choice, random


class Car:
    def __init__(self):
        self.x = randint(0, 100)
        self.y = choice((0, 3))
        self.v = randint(15, 30)
    def __str__(self):
        return f'x={self.x}, y={self.y}, v={self.v}'

    def next(self):
        self.x = round((self.x + self.v), 3)
        if random() > 0.2:
            if self.y == 0: self.y = 3
            else: self.y = 0

def createCar(numberOfCar):
    return [Car() for _ in range(numberOfCar)]

def changeCarData(cars):
    for car in cars:
        car.next()

def mainProcess():
    while True:
        print(f"Time {time_step}:", time_step + delaytTime)
        
        # 更新车辆位置
        data = change_car_data(data)
        print(f"Updated Car Positions at Time {time_step}:", data)
        
        # 在每个时间步骤中进行进一步的分析，例如找到车辆位置的中心点
        center_point = kmeans(data)
        print(f"CenterPoint at Time {time_step}:", center_point)


        location_UAV=((location_UAV[0]+location_UAV[2]),location_UAV[1],location_UAV[2])
        
        d=((location_UAV[0]-center_point[0])**2+(location_UAV[1]-center_point[1])**2)**0.5
        print("距離 :",d)
        # if d<5:
        if location_UAV[0] > center_point[0]:
            print("OKOK") 
            break
        time_step+=1
        time.sleep(0.5)


if __name__ == '__main__':
    mainProcess()