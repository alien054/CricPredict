import yaml
import os
from shutil import copy2
import csv

def progress(percent, width=40):
    left = (width * percent) // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%', sep='', end='', flush=True)


path = "../../data/all_male/"
newPath = "../../data/date_wise/"

if os.path.isdir(newPath):
    print("Already exist")
else:
    os.mkdir(newPath)
    print("Directory creaetd")

files = [path + file for file in os.listdir(path) if 'yaml' in file]


index = 0

for file in files:
    with open(path+file, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    play_date = str(data['info']['dates'][0])
    # print(type(play_date))
    if os.path.isfile(newPath + play_date + '.yaml'):
        # print("Match in same day!!!")
        play_date = play_date + "-" + str(index)
    copy2(path+file, newPath+play_date+'.yaml')
    # print(play_date)
    index += 1
    progress(int(index*100/len(files)))
