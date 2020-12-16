import yaml
import os
import csv
from datetime import datetime

path = "../../data/2005_male/"

match_data = {'toss': "", 'venue': "", 'match_type': ""}
team_data = {'batting_team': "", 'fielding_team': "",
             'innings': "", 'over': "", 'ball': ""}
batsman_data = {}
bowler_data = {}
class_label = {'outcome':""}

files = [path + file for file in os.listdir(path) if 'yaml' in file]
file = files[0]

index = 0

for i in range(1):
    with open(path+file, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        
        team1 = data['info']['teams'][0]
        team2 = data['info']['teams'][1]
        match_data['toss'] = data['info']['toss']['decision']
        match_data['venue'] = data['info']['venue']
        match_data['match_type'] = data['info']['match_type']

        innings = data['innings']

        count = 0
        for inning in innings:
            if count > 0:
                break
            count = 1
            innings_key = list(inning.keys())[0]
            team_data['innings'] = innings_key
            team_data['batting_team'] = inning[innings_key]['team']
            team_data['fielding_team'] = team1 if team_data['batting_team'] != team1 else team2

            print(team_data)
            deliveries = inning[innings_key]['deliveries']
            batsman_order = 0
            
            for delivery in deliveries:
                delivery_key = list(delivery.keys())[0]
                over,ball = str(delivery_key).strip().split(".")
                team_data['over'] = over
                team_data['ball'] = ball
                
                batsman_out = False
                class_label['outcome'] = delivery[delivery_key]['runs']['total']
                if 'wicket' in list(delivery[delivery_key].keys()):
                    batsman_out = True
                    class_label['outcome'] = 10
                
                batsman_name = delivery[delivery_key]['batsman']
                bowler_name = delivery[delivery_key]['bowler']
                
                if batsman_name not in list(batsman_data.keys()):
                    batsman_order += 1
                    batsman_data[batsman_name] = {
                        'a_team': team_data['batting_team'],
                        'non_strike':"",
                        'innings':innings_key,
                        'batting_position':batsman_order,
                        'run_scored':0,
                        'balls_faced':0,
                        'boundary':0,
                        'dot_ball':0,
                        'single_double':0,
                        'fifty': 0,
                        'hundred': 0,
                        'is_out':0,
                        'balls_before_out':0,
                        }
                    
                batsman_data[batsman_name]['non_strike'] = delivery[delivery_key]['non_striker']
                batsman_run = delivery[delivery_key]['runs']['batsman']
                batsman_data[batsman_name]['run_scored'] = batsman_data[batsman_name]['run_scored'] + batsman_run
                batsman_data[batsman_name]['balls_faced'] = batsman_data[batsman_name]['balls_faced'] + 1
                
                if batsman_run == 4 or batsman_run == 6:
                    batsman_data[batsman_name]['boundary'] = batsman_data[batsman_name]['boundary'] + 1
                elif batsman_run == 0:
                    batsman_data[batsman_name]['dot_ball'] = batsman_data[batsman_name]['dot_ball'] + 1
                elif batsman_run <= 3:
                    batsman_data[batsman_name]['single_double'] = batsman_data[batsman_name]['single_double'] + 1
                
                batsman_total = batsman_data[batsman_name]['run_scored']
                if batsman_total >= 50 and batsman_total < 100:
                    batsman_data[batsman_name]['fifty'] = 1
                elif batsman_total >= 100:
                    batsman_data[batsman_name]['fifty'] = 0
                    batsman_data[batsman_name]['hundred'] = 1
                    
                if batsman_out:
                    batsman_data[batsman_name]['is_out'] = 1
                    batsman_data[batsman_name]['balls_before_out'] = batsman_data[batsman_name]['balls_faced']
                
                batsman_data['ball'] = delivery_key    
                with open('test.yaml', 'a') as output:
                    yaml.dump(batsman_data, output, default_flow_style=False)
                print(over," ",ball," ",class_label['outcome'])
        print(match_data)
        

    
    index += 1
    print("{}/{}".format(index,len(files)))
