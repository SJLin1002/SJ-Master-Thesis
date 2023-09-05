'''
Copyright(c) 2023 mail@miru.cc
'''

from keyboard import read_key
from random import randint, choice, random, uniform
from threading import Thread
from time import sleep

class Car:
  def __init__(self):
    self.x = randint(0, 100)
    self.y = choice([0, 3])
    self.v = randint(20, 100)
    self.history = []

  def __repr__(self):
    return f'{self.x: 3d}, {self.y: 2d}, {self.v: 3d}'

  def next(self):
    self.x += round(self.x + self.v, 3)
    if random() > 0.2:
      if (self.y == 0): self.y = 3
      else: self.y = 0
    
    self.v = round(self.v + self.v * uniform(0.1, -0.1), 3)
    # self.addCurrentStatusToHistory()

  def addCurrentStatusToHistory(self):
    self.history.append({
      x: self.x,
      y: self.y,
      v: self.v
    })

def quitByKeyJudgmentThread(key = 'q'):
  global isRunning
  while (isRunning):
    if read_key() == key: isRunning = False


def mainProcessThread(
  numberOfCar = 5
):
  cars = [Car() for _ in range(numberOfCar)]
  print(f'總計 {numberOfCar} 台車')
  print('  |   x,  y,   v')
  for car in cars:
    print(f'  | {car}')
  
  t = 0
  while isRunning:
    for car in cars: car.next()
    print(f'總計 {numberOfCar} 台車, 在 t = {t}')
    print('  |   x,  y,   v')
    for car in cars:
      print(f'  | {car}')

    sleep(1)
    t += 1

# ---------- #

isRunning = True

threads = [
  Thread(target = quitByKeyJudgmentThread),
  Thread(target = mainProcessThread)
]


for thread in threads: thread.start()
for thread in threads: thread.join()

print('Process Finish!')
