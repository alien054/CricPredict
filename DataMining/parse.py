import yaml
import os
import csv
from datetime import datetime
from queue import Queue

path = "../../../data/odi/"
newPath = "../../../data/csv/odi/"

def create_dir(path):
    if os.path.isdir(path):
        print("Already exist")
    else:
        os.mkdir(path)
        print("Directory created")

create_dir(newPath)

files = [file for file in os.listdir(path) if 'yaml' in file]

csv_row_names = ['toss','venue','match_type','batting_team','fielding_team','innings','over','ball'
                 ,'team_total','team_wicket','team_target','current_ball','01st_last_ball','02nd_last_ball'
                 ,'03rd_last_ball','04th_last_ball','05th_last_ball','06th_last_ball','07th_last_ball','08th_last_ball'
                 ,'09th_last_ball', '10th_last_ball', '11th_last_ball', '12th_last_ball', 'last_1st_over_run', 'last_2nd_over_run'
                 , 'last_3rd_over_run', 'last_4th_over_run', 'last_5th_over_run', 'total_last_2_over', 'total_last_5_over', 'total_last_10_over'
                 , 'wicket_in_last_6', 'wicket_in_last_12', 'wicket_in_last_30', 'batsman_name', 'batsman_team', 'non_strike', 'batting_position'
                 , 'run_scored', 'balls_faced', 'boundary', 'dot_ball', 'single_double', 'fifty', 'hundred', 'is_out', 'balls_before_out'
                 , 'bowler_name', 'bowler_team', 'innings_no', 'run_given', 'balls_delivered', 'boundary_given', 'dot_ball_given', 'single_double_given'
                 , 'five_haul', 'ten_haul', 'wicket_taken']
print(len(csv_row_names))
index = 0

count = 0
for file in files:
    csv_file = open(newPath+file.replace('yaml','csv'), 'w', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=csv_row_names)
    writer.writeheader()
    
    with open(path + file, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        match_data = {'toss': "", 'venue': "", 'match_type': ""}

        # if count > 0:
        #         break
        # count += 1
            
        batsman_data = {}
        bowler_data = {}

        team1 = data['info']['teams'][0]
        team2 = data['info']['teams'][1]
        match_data['toss'] = data['info']['toss']['decision']
        match_data['venue'] = data['info']['venue']
        match_data['match_type'] = data['info']['match_type']

        innings = data['innings']
        pre_team_total = 0
        for inning in innings:
            
            team_data = {'batting_team': "", 'fielding_team': "",
                         'innings': "", 'over': 0, 'ball': 0,
                         'team_total':0,'team_wicket':0,'team_target':0
                         }
            score_data = {'current_ball': 0, '01st_last_ball': 0, '02nd_last_ball': 0,
                          '03rd_last_ball': 0, '04th_last_ball': 0, '05th_last_ball': 0,
                          '06th_last_ball': 0,'07th_last_ball': 0, '08th_last_ball': 0, '09th_last_ball': 0, 
                          '10th_last_ball': 0, '11th_last_ball': 0, '12th_last_ball': 0, 
                          'last_1st_over_run': 0, 'last_2nd_over_run': 0,
                          'last_3rd_over_run': 0, 'last_4th_over_run': 0, 'last_5th_over_run': 0,
                          'total_last_2_over': 0, 'total_last_5_over': 0, 'total_last_10_over': 0,
                          'wicket_in_last_6':0,'wicket_in_last_12':0,'wicket_in_last_30':0
                          }

            innings_key = list(inning.keys())[0]
            team_data['innings'] = innings_key
            team_data['batting_team'] = inning[innings_key]['team']
            team_data['fielding_team'] = team1 if team_data['batting_team'] != team1 else team2
            team_data['team_target'] = pre_team_total
            # print(team_data)

            deliveries = inning[innings_key]['deliveries']
            batsman_order = 0

            prev_over = -1
            this_over_run = 0
            two_over_q = Queue(maxsize=2)
            five_over_q = Queue(maxsize=5)
            ten_over_q = Queue(maxsize=10)
            
            twelve_ball_run_q = Queue(maxsize=12)
            
            six_ball_wicket_q = Queue(maxsize=6)
            twelve_ball_wicket_q = Queue(maxsize=12)
            thirty_ball_wicket_q = Queue(maxsize=30)

            for i in range(2):
                two_over_q.put(0)
            for i in range(5):
                five_over_q.put(0)
            for i in range(10):
                ten_over_q.put(0)
            for i in range(12):
                twelve_ball_run_q.put(0)
            for i in range(6):
                six_ball_wicket_q.put(0)
            for i in range(12):
                twelve_ball_wicket_q.put(0)
            for i in range(30):
                thirty_ball_wicket_q.put(0)

            for delivery in deliveries:
                delivery_key = list(delivery.keys())[0]
                this_over, ball = str(delivery_key).strip().split(".")
                team_data['over'] = this_over
                team_data['ball'] = ball

                current_ball_run = delivery[delivery_key]['runs']['total']
                current_ball_run_for_total = current_ball_run
                # team_data['team_total'] = team_data['team_total'] + current_ball_run
                
                if this_over == prev_over:
                    this_over_run += current_ball_run
                else:
                    if two_over_q.full():
                        two_over_q.get()
                    if five_over_q.full():
                        five_over_q.get()
                    if ten_over_q.full():
                        ten_over_q.get()

                    two_over_q.put(this_over_run)
                    five_over_q.put(this_over_run)
                    ten_over_q.put(this_over_run)

                    last_5_over_list = list(five_over_q.queue)
                    # score_data['5th_last_over_run'] = score_data['4th_last_over_run']
                    # score_data['4th_last_over_run'] = score_data['3rd_last_over_run']
                    # score_data['3rd_last_over_run'] = score_data['2nd_last_over_run']
                    # score_data['2nd_last_over_run'] = score_data['1st_last_over_run']
                    # score_data['1st_last_over_run'] = this_over_run

                    # print(last_5_over_list)
                    score_data['last_5th_over_run'] = last_5_over_list[0]
                    score_data['last_4th_over_run'] = last_5_over_list[1]
                    score_data['last_3rd_over_run'] = last_5_over_list[2]
                    score_data['last_2nd_over_run'] = last_5_over_list[3]
                    score_data['last_1st_over_run'] = last_5_over_list[4]

                    score_data['total_last_2_over'] = sum(list(two_over_q.queue))
                    score_data['total_last_5_over'] = sum(list(five_over_q.queue))
                    score_data['total_last_10_over'] = sum(list(ten_over_q.queue))

                    this_over_run = current_ball_run

                prev_over = this_over
                
                score_data['wicket_in_last_6'] = sum(list(six_ball_wicket_q.queue))
                score_data['wicket_in_last_12'] = sum(list(twelve_ball_wicket_q.queue))
                score_data['wicket_in_last_30'] = sum(list(thirty_ball_wicket_q.queue))
                
                batsman_out = False
                if 'wicket' in list(delivery[delivery_key].keys()):
                    batsman_out = True
                    # team_data['team_wicket'] = team_data['team_wicket'] + 1
                    
                    
                    current_ball_run = 10
                    if six_ball_wicket_q.full():
                        six_ball_wicket_q.get()
                    six_ball_wicket_q.put(1)
                    
                    if twelve_ball_wicket_q.full():
                        twelve_ball_wicket_q.get()
                    twelve_ball_wicket_q.put(1)
                    
                    if thirty_ball_wicket_q.full():
                        thirty_ball_wicket_q.get()
                    thirty_ball_wicket_q.put(1)
                else:
                    if six_ball_wicket_q.full():
                        six_ball_wicket_q.get()
                    six_ball_wicket_q.put(0)

                    if twelve_ball_wicket_q.full():
                        twelve_ball_wicket_q.get()
                    twelve_ball_wicket_q.put(0)

                    if thirty_ball_wicket_q.full():
                        thirty_ball_wicket_q.get()
                    thirty_ball_wicket_q.put(0)
                
                last_12_ball_run_list = list(twelve_ball_run_q.queue)
                score_data['12th_last_ball'] = last_12_ball_run_list[0]
                score_data['11th_last_ball'] = last_12_ball_run_list[1]
                score_data['10th_last_ball'] = last_12_ball_run_list[2]
                score_data['09th_last_ball'] = last_12_ball_run_list[3]
                score_data['08th_last_ball'] = last_12_ball_run_list[4]
                score_data['07th_last_ball'] = last_12_ball_run_list[5]
                score_data['06th_last_ball'] = last_12_ball_run_list[6]
                score_data['05th_last_ball'] = last_12_ball_run_list[7]
                score_data['04th_last_ball'] = last_12_ball_run_list[8]
                score_data['03rd_last_ball'] = last_12_ball_run_list[9]
                score_data['02nd_last_ball'] = last_12_ball_run_list[10]
                score_data['01st_last_ball'] = last_12_ball_run_list[11]
                score_data['current_ball'] = current_ball_run

                if twelve_ball_run_q.full():
                    twelve_ball_run_q.get()
                twelve_ball_run_q.put(current_ball_run)

                #score_data['00Ball'] = delivery_key

                batsman_name = delivery[delivery_key]['batsman']
                bowler_name = delivery[delivery_key]['bowler']

                if batsman_name not in list(batsman_data.keys()):
                    batsman_order += 1
                    batsman_data[batsman_name] = {
                        'batsman_name':batsman_name,
                        'batsman_team': team_data['batting_team'],
                        'non_strike': delivery[delivery_key]['non_striker'],
                        'innings': innings_key,
                        'batting_position': batsman_order,
                        'run_scored': 0,
                        'balls_faced': 0,
                        'boundary': 0,
                        'dot_ball': 0,
                        'single_double': 0,
                        'fifty': 0,
                        'hundred': 0,
                        'is_out': 0,
                        'balls_before_out': 0,
                    }
                if bowler_name not in list(bowler_data.keys()):
                    bowler_data[bowler_name] = {
                        'bowler_name': bowler_name,
                        'bowler_team': team_data['fielding_team'],
                        'innings_no': innings_key,
                        'run_given': 0,
                        'balls_delivered': 0,
                        'boundary_given': 0,
                        'dot_ball_given': 0,
                        'single_double_given': 0,
                        'five_haul': 0,
                        'ten_haul': 0,
                        'wicket_taken': 0,
                    }
                
                row_data = {**match_data,**team_data,**score_data,**batsman_data[batsman_name],**bowler_data[bowler_name]}
                writer.writerow(row_data)

                # batsman_data[batsman_name]['batsman_name'] = batsman_name 
                # batsman_data[batsman_name]['non_strike'] = delivery[delivery_key]['non_striker']
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

                # batsman_data['ball'] = delivery_key

                

                # bowler_data[bowler_name]['bowler_name'] = bowler_name
                bowler_run = delivery[delivery_key]['runs']['total']
                bowler_data[bowler_name]['run_given'] = bowler_data[bowler_name]['run_given'] + bowler_run
                bowler_data[bowler_name]['balls_delivered'] = bowler_data[bowler_name]['balls_delivered'] + 1

                if bowler_run >= 4:
                    bowler_data[bowler_name]['boundary_given'] = bowler_data[bowler_name]['boundary_given'] + 1
                elif bowler_run == 0:
                    bowler_data[bowler_name]['dot_ball_given'] = bowler_data[bowler_name]['dot_ball_given'] + 1
                elif bowler_run <= 3:
                    bowler_data[bowler_name]['single_double_given'] = bowler_data[bowler_name]['single_double_given'] + 1

                if batsman_out:
                    bowler_data[bowler_name]['wicket_taken'] = bowler_data[bowler_name]['wicket_taken'] + 1

                bowler_total = bowler_data[bowler_name]['wicket_taken']
                if bowler_total >= 5 and bowler_total < 10:
                    bowler_data[bowler_name]['five_haul'] = 1
                elif bowler_total > 10:
                    bowler_data[bowler_name]['five_haul'] = 0
                    bowler_data[bowler_name]['ten_haul'] = 1

                # bowler_data['ball'] = delivery_key
                # with open('batsman.yaml', 'a') as batsman:
                #     yaml.dump(batsman_data, batsman, default_flow_style=False)
                # with open('bowler.yaml', 'a') as bowler:
                #     yaml.dump(bowler_data, bowler, default_flow_style=False)
                # with open('score.yaml', 'a') as score:
                #     yaml.dump(score_data, score, default_flow_style=False)
                # print(this_over, " ", ball, " ", score_data['current_ball'])
                
                # row_data = {**match_data,**team_data,**score_data,**batsman_data[batsman_name],**bowler_data[bowler_name]}
                # writer.writerow(row_data)
                
                team_data['team_total'] = team_data['team_total'] + current_ball_run_for_total
                if batsman_out:
                    team_data['team_wicket'] = team_data['team_wicket'] + 1
                    
                
            
            pre_team_total = team_data['team_total']
            
     
        # print(match_data)
    
    csv_file.close()
        
    
    index += 1
    print("{}/{}".format(index, len(files)))
