import os
import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert
from importlib import reload
import soccer_db_schema as sds
from datetime import datetime
import requests
import itertools

data_path='sb_data'
db_location='sb_data.sqlite'
engine = create_engine(f'sqlite:///{db_location}')
sds.Base.metadata.create_all(bind=engine)
Session=sessionmaker(bind=engine)


def import_data():
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    matches=requests.get('https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/55/43.json').json()
    match_ids=[i.get('match_id') for i in matches]
    path_events=os.path.join(data_path,'events')
    if not os.path.exists(path_events):
        os.mkdir(path_events)
    event_urls=[f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json" for match_id in match_ids]
    for ev_url in event_urls:
        file_name=os.path.join(path_events,ev_url.split('/')[-1])
        if not os.path.exists(file_name):
            with open(file_name,'w') as fl:
                json.dump(requests.get(ev_url).json(),fl)
    path_360=os.path.join(data_path,'three-sixty')
    if not os.path.exists(path_360):
        os.mkdir(path_360)
    three60_urls=[f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/three-sixty/{match_id}.json" for match_id in match_ids]
    for three60_url in three60_urls:
        file_name=os.path.join(path_360,three60_url.split('/')[-1])
        if not os.path.exists(file_name):
            req=requests.get(three60_url)
            if req.status_code==200:
                with open(file_name,'w') as fl:
                    json.dump(req.json(),fl)
    lineup_urls=[f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/{match_id}.json" for match_id in match_ids]
    path_lineup=os.path.join(data_path,'lineups')
    if not os.path.exists(path_lineup):
        os.mkdir(path_lineup)
    for lineup_url in lineup_urls:
        file_name=os.path.join(path_lineup,lineup_url.split('/')[-1])
        if not os.path.exists(file_name):
            with open(file_name,'w') as fl:
                json.dump(requests.get(lineup_url).json(),fl)

    lineups=[]
    for line_path in filter(lambda x:x.name.endswith(".json"),os.scandir(path_lineup)):
        with open(line_path,'r') as fl:
            lineups.append(json.loads(fl.read()))

    player_dict={}
    for line_team in itertools.chain.from_iterable(lineups):
        team_id=line_team.get('team_id')
        for pdict in line_team['lineup']:
            player_dict[pdict['player_id']]={'id':pdict['player_id'],'name':pdict['player_name'],'team_id':team_id,'jersey_number':pdict['jersey_number']}



    id_dict={'type': {35: {'id': 35, 'name': 'Starting XI'}, 18: {'id': 18, 'name': 'Half Start'}, 30: {'id': 30, 'name': 'Pass'}, 42: {'id': 42, 'name': 'Ball Receipt*'}, 43: {'id': 43, 'name': 'Carry'}, 9: {'id': 9, 'name': 'Clearance'}, 4: {'id': 4, 'name': 'Duel'}, 2: {'id': 2, 'name': 'Ball Recovery'}, 17: {'id': 17, 'name': 'Pressure'}, 16: {'id': 16, 'name': 'Shot'}, 23: {'id': 23, 'name': 'Goal Keeper'}, 6: {'id': 6, 'name': 'Block'}, 22: {'id': 22, 'name': 'Foul Committed'}, 21: {'id': 21, 'name': 'Foul Won'}, 10: {'id': 10, 'name': 'Interception'}, 14: {'id': 14, 'name': 'Dribble'}, 38: {'id': 38, 'name': 'Miscontrol'}, 3: {'id': 3, 'name': 'Dispossessed'}, 39: {'id': 39, 'name': 'Dribbled Past'}, 28: {'id': 28, 'name': 'Shield'}, 36: {'id': 36, 'name': 'Tactical Shift'}, 40: {'id': 40, 'name': 'Injury Stoppage'}, 34: {'id': 34, 'name': 'Half End'}, 19: {'id': 19, 'name': 'Substitution'}, 33: {'id': 33, 'name': '50/50'}, 41: {'id': 41, 'name': 'Referee Ball-Drop'}, 8: {'id': 8, 'name': 'Offside'}, 24: {'id': 24, 'name': 'Bad Behaviour'}, 37: {'id': 37, 'name': 'Error'}, 27: {'id': 27, 'name': 'Player Off'}, 26: {'id': 26, 'name': 'Player On'}, 25: {'id': 25, 'name': 'Own Goal For'}, 20: {'id': 20, 'name': 'Own Goal Against'}}, 'play_pattern': {1: {'id': 1, 'name': 'Regular Play'}, 9: {'id': 9, 'name': 'From Kick Off'}, 7: {'id': 7, 'name': 'From Goal Kick'}, 4: {'id': 4, 'name': 'From Throw In'}, 3: {'id': 3, 'name': 'From Free Kick'}, 2: {'id': 2, 'name': 'From Corner'}, 8: {'id': 8, 'name': 'From Keeper'}, 6: {'id': 6, 'name': 'From Counter'}, 5: {'id': 5, 'name': 'Other'}}, 'position': {23: {'id': 23, 'name': 'Center Forward'}, 5: {'id': 5, 'name': 'Left Center Back'}, 4: {'id': 4, 'name': 'Center Back'}, 2: {'id': 2, 'name': 'Right Back'}, 22: {'id': 22, 'name': 'Right Center Forward'}, 9: {'id': 9, 'name': 'Right Defensive Midfield'}, 8: {'id': 8, 'name': 'Left Wing Back'}, 24: {'id': 24, 'name': 'Left Center Forward'}, 19: {'id': 19, 'name': 'Center Attacking Midfield'}, 15: {'id': 15, 'name': 'Left Center Midfield'}, 10: {'id': 10, 'name': 'Center Defensive Midfield'}, 13: {'id': 13, 'name': 'Right Center Midfield'}, 11: {'id': 11, 'name': 'Left Defensive Midfield'}, 12: {'id': 12, 'name': 'Right Midfield'}, 7: {'id': 7, 'name': 'Right Wing Back'}, 1: {'id': 1, 'name': 'Goalkeeper'}, 3: {'id': 3, 'name': 'Right Center Back'}, 6: {'id': 6, 'name': 'Left Back'}, 16: {'id': 16, 'name': 'Left Midfield'}, 17: {'id': 17, 'name': 'Right Wing'}, 21: {'id': 21, 'name': 'Left Wing'}, 18: {'id': 18, 'name': 'Right Attacking Midfield'}, 20: {'id': 20, 'name': 'Left Attacking Midfield'}}}
    team_dict={1835: {'id': 1835, 'name': 'Finland'}, 796: {'id': 796, 'name': 'Russia'}, 773: {'id': 773, 'name': 'Switzerland'}, 909: {'id': 909, 'name': 'Turkey'}, 782: {'id': 782, 'name': 'Belgium'}, 914: {'id': 914, 'name': 'Italy'}, 768: {'id': 768, 'name': 'England'}, 776: {'id': 776, 'name': 'Denmark'}, 770: {'id': 770, 'name': 'Germany'}, 790: {'id': 790, 'name': 'Sweden'}, 911: {'id': 911, 'name': 'Ukraine'}, 785: {'id': 785, 'name': 'Croatia'}, 772: {'id': 772, 'name': 'Spain'}, 780: {'id': 780, 'name': 'Portugal'}, 915: {'id': 915, 'name': 'Austria'}, 916: {'id': 916, 'name': 'Hungary'}, 942: {'id': 942, 'name': 'Scotland'}, 912: {'id': 912, 'name': 'Czech Republic'}, 771: {'id': 771, 'name': 'France'}, 2358: {'id': 2358, 'name': 'North Macedonia'}, 941: {'id': 941, 'name': 'Netherlands'}, 907: {'id': 907, 'name': 'Wales'}, 908: {'id': 908, 'name': 'Slovakia'}, 789: {'id': 789, 'name': 'Poland'}}
    attr_dict={1: 'Lost', 2: 'Success To Opposition', 3: 'Success To Team', 4: 'Won', 5: 'Red Card', 6: 'Second Yellow', 7: 'Yellow Card', 8: 'Complete', 9: 'Incomplete', 10: 'Aerial Lost', 11: 'Tackle', 13: 'Lost In Play', 14: 'Lost Out', 15: 'Success', 16: 'Success In Play', 17: 'Success Out', 21: 'Dangerous Play', 22: 'Dive', 23: 'Foul Out', 24: 'Handball', 25: 'Collected', 26: 'Goal Conceded', 27: 'Keeper Sweeper', 28: 'Penalty Conceded', 29: 'Penalty Saved', 30: 'Punch', 31: 'Save', 32: 'Shot Faced', 33: 'Shot Saved', 34: 'Smother', 35: 'Both Hands', 36: 'Chest', 37: 'Head', 38: 'Left Foot', 39: 'Left Hand', 40: 'Right Foot', 41: 'Right Hand', 42: 'Moving', 43: 'Prone', 44: 'Set', 45: 'Diving', 46: 'Standing', 47: 'Claim', 48: 'Clear', 49: 'Collected Twice', 50: 'Fail', 52: 'In Play Danger', 53: 'In Play Safe', 55: 'No Touch', 56: 'Saved Twice', 58: 'Touched In', 59: 'Touched Out', 61: 'Corner', 62: 'Free Kick', 63: 'Goal Kick', 64: 'Interception', 65: 'Kick Off', 66: 'Recovery', 67: 'Throw-in', 68: 'Drop Kick', 69: 'Keeper Arm', 70: 'Other', 74: 'Injury Clearance', 75: 'Out', 76: 'Pass Offside', 77: 'Unknown', 87: 'Open Play', 88: 'Penalty', 89: 'Backheel', 90: 'Diving Header', 91: 'Half Volley', 92: 'Lob', 93: 'Normal', 94: 'Overhead Kick', 95: 'Volley', 96: 'Blocked', 97: 'Goal', 98: 'Off T', 99: 'Post', 100: 'Saved', 101: 'Wayward', 102: 'Injury', 103: 'Tactical', 104: 'Inswinging', 105: 'Outswinging', 106: 'No Touch', 107: 'Straight', 108: 'Through Ball', 109: 'Penalty Saved to Post', 113: 'Shot Saved Off Target', 114: 'Shot Saved to Post', 115: 'Saved Off Target', 116: 'Saved to Post', 117: 'Punched out'}


    with Session.begin() as sess:
        sess.execute(insert(sds.LK_Play_Type).values(list(id_dict['type'].values())))
        sess.execute(insert(sds.LK_Play_Pattern).values(list(id_dict['play_pattern'].values())))
        sess.execute(insert(sds.LK_Position).values(list(id_dict['position'].values())))
        sess.execute(insert(sds.LK_Attribute).values([{'id':k,'name':v} for k,v in attr_dict.items()]))
        sess.execute(insert(sds.Team).values(list(team_dict.values())))
        sess.execute(insert(sds.Player).values(list(player_dict.values())))
        
    for match in matches:
        insD={}
        for key in ['match_id','match_date','home_score','away_score']:
            insD[key]=match.get(key)
        insD['match_date']=datetime.fromisoformat(insD['match_date']).date()
        insD['home_team_id']=match.get('home_team').get('home_team_id')
        insD['away_team_id']=match.get('away_team').get('away_team_id')
        with Session.begin() as sess:
            sess.execute(insert(sds.Game,values=insD))

    for match_id in match_ids:
        with open(next(filter(lambda x:str(match_id) in x.name,os.scandir(path_events))).path,'r') as fl:
            ev_json=json.loads(fl.read())
        with open(next(filter(lambda x:str(match_id) in x.name,os.scandir(path_360))).path,'r') as fl:
            three60_json=json.loads(fl.read())
        ids_360=[i.get('event_uuid') for i in three60_json]
        ev_insert_list=[]
        for ev in ev_json:
            ev_dict={i:ev.get(i) for i in sds.Event.__table__.columns.keys()}|{'match_id':match_id,'has_360':ev.get('id') in ids_360}
            ev_dict['timestamp']=datetime.strptime(ev_dict['timestamp'],'%H:%M:%S.%f').time()
            ev_dict['possession_team_id']=ev.get('possession_team',{}).get('id')
            ev_dict['team_id']=ev.get('team',{}).get('id')
            ev_dict['type_id']=ev.get('type',{}).get('id')
            ev_dict['player_id']=ev.get('player',{}).get('id')
            ev_dict['position_id']=ev.get('position',{}).get('id')
            ev_dict['possession_number']=ev.get('possession')
            if 'location' in ev:
                ev_dict['location_x'],ev_dict['location_y']=ev.get('location',[None,None])
            for end_type in filter(lambda x:x in ev,['pass','carry','shot','goalkeeper']):
                end_loc=ev.get(end_type,{}).get('end_location',[None,None])
                if len(end_loc)==2:
                    ev_dict['end_location_x'],ev_dict['end_location_y']=end_loc
                elif len(end_loc)==3:
                    ev_dict['end_location_x'],ev_dict['end_location_y'],ev_dict['end_location_z']=end_loc
                end_outcome_id=ev.get(end_type,{}).get('outcome',{}).get('id')
                if end_outcome_id:
                    ev_dict['outcome_id']=end_outcome_id
                end_pass_type_id=ev.get(end_type,{}).get('type',{}).get('id')
                if end_pass_type_id:
                    ev_dict['pass_type_id']=end_pass_type_id
                if end_type=='pass':
                    ev_dict['cross']=False
                    ev_dict['switch']=False
                    if 'cross' in ev.get(end_type,{}):
                        ev_dict['cross']=True
                    if 'switch' in ev.get(end_type,{}):
                        ev_dict['switch']=True
            ev_dict['recieve_player_id']=ev.get('pass',{}).get('recipient',{}).get('id')
            ev_insert_list.append(ev_dict)
        with Session.begin() as sess:
            sess.execute(insert(sds.Event).values(ev_insert_list))

if __name__=='__main__':
    import_data()