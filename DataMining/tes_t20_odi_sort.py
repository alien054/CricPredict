
import yaml
import os
import shutil


def progress(percent, width=40):
    left = (width * percent) // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%', sep='', end='', flush=True)


path = "../../../data/date_wise/"

paths = {'TEST': "../../../data/test/",
         'T20': "../../../data/t20/",
         'ODI': "../../../data/odi/",
         'OTHER': "../../../data/other/",
         }


# def create_dir(path):
#     print(path)
#     if os.path.isdir(path):
#         print("Already exist")
#         print("Deleting Directory.....")
#         shutil.rmtree(path)
#         print("Creating new Directory.....")
#         os.mkdir(path)
#         print("Directory created")
#     else:
#         os.mkdir(path)
#         print("Directory created")


# for addr in paths:
#     create_dir(paths[addr])
    
files = [file for file in os.listdir(path) if 'yaml' in file]


index = 0

for file in files:
    with open(path+file, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    match_type = str(data['info']['match_type']).upper()
    if match_type not in paths.keys():
        match_type = "OTHER"
    # print(file)
    shutil.copy2(path+file, paths[match_type]+file)

    index += 1
    progress(int(index*100/len(files)))
