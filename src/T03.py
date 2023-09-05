'''
Copyright(c) 2023 mail@miru.cc
'''

from random import uniform, choice
from math import sqrt


def mainProcessThread(
  numberOfCluster = 2,
  numberOfCar = 5,
  times = 50
):
  ks = [generateRandomK() for _ in range(numberOfCluster)]
  cars = [generateRandomCarCoordinate() for _ in range(numberOfCar)]

  xValues = [car['x'] for car in cars]
  yValues = [car['y'] for car in cars]

  plt.xlim((0, 120))
  plt.ylim((-1, 10))
  plt.plot(xValues, yValues, 'o', color='black')

  t = 0
  while (times > t)
    clusters = [[] * numberOfCluster]
    nodes = []
    for car in cars:
      kValues = []
      for k in ks:
        subX = car['x'] - k['x']
        subY = car['y'] - k['y']
        kValues.append(sqrt(subX ** 2 + subY ** 2))
      minValue = min(kValues)
      indexOfMin = kValues.index(minValue)
      clusters[indexOfMin].append(car)

    if any(len(cluster) == 0 for cluster in clusters):
      ks = [generateRandomK() for _ in range(numberOfCluster)] 
      continue

    for cluster in clusters:
      point = [0, 0]
      for car in cluster:
        point[0] += car['x']
        point[1] += car['y']
      length = len(cluster)
      point[0] /= length
      point[1] /= length

    setPlot(nodes)

    t += 1
      

def generateRandomK():
  return {
    'x': round(uniform(0, 100), 3),
    'y': round(uniform(0, 3), 3)
  }

def generateRandomCarCoordinate():
  return {
    'x': round(uniform(0, 100), 3),
    'y': round(choice([0, 3]), 3)
  }

def setPlot(datas):
  colors = ['blue', 'red', 'green', 'yellow', 'pink', 'purple', 'orange', 'brown', 'gray', 'olive','cyan']
  for index, data in enumerate(datas):
    plt.plot(data[0], data[1], 'o', color = colors[index % len(colors)])

# ---------- #

mainProcessThread()