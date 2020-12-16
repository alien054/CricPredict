import yaml
import os
import csv
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H_%M_%S")

def progress(percent, width=40):
    left = (width * percent) // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%', sep='', end='', flush=True)


path = "../../data/date_wise/"


files = [path + file for file in os.listdir(path) if 'yaml' in file]


index = 0
venue_data = {"match_type":"","city": "", "venue": ""}

csv_file = open('venueData'+current_time+'.csv', 'w', newline='')
fieldnames = list(venue_data.keys())
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()


for file in files:
    with open(path+file, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    try:
        city = str(data['info']['city'])
    except:
        city = ''
    venue = str(data['info']['venue'])
    match_type = str(data['info']['match_type'])
    
    venue_data['match_type'] = match_type
    venue_data['city'] = city
    venue_data['venue'] = venue
    writer.writerow(venue_data)

    index += 1
    progress(int(index*100/len(files)))

    


