import requests
import datetime
import urllib3
from abbrev import abbrev
from backtest import backtest
from weather import get_weather
import json
import pandas as pd

urllib3.disable_warnings()

BORDER = '#' * 50
SUBSET = '-' * 50


def main():
    action = input('What would you like to do? ')
    if action[0] == 'l':
        get_lines()
    if action[0] == 't':
        print()
        next_action = input('You selected ' + abbrev(action[2:], 'abr') + '. What would you like to do next? ')
        # function to get various stats about team


def get_lines():
    count = 0


    game_list = []
    r = {}
    while type(r) != list:
        league = input('What league? ')
        r = requests.get("https://www.bovada.lv/services/sports/event/v2/events/A/description/football/" + league,
                         verify=False).json()

    print(BORDER)
    data = r[0]
    for game in data:
        for team in data['events']:
            try:
                count += 1
                EpochTime = team['startTime']
                Epoch = datetime.datetime.fromtimestamp(EpochTime / 1e3)
                date = Epoch.strftime('%m-%d-%Y %H:%M:%S')
                team_1 = team['competitors'][0]['name'].rstrip()
                team_2 = team['competitors'][1]['name'].rstrip()
                if team_1 in game_list:
                    break
                else:
                    try: odd_1_1 = team['displayGroups'][0]['markets'][1]['outcomes'][0]['price']['handicap']
                    except KeyError: odd_1_1 = None
                    try: odd_1_2 = team['displayGroups'][0]['markets'][1]['outcomes'][0]['price']['american']
                    except KeyError: odd_1_2 = None
                    try: odd_2_1 = team['displayGroups'][0]['markets'][1]['outcomes'][1]['price']['handicap']
                    except KeyError: odd_2_1 = None
                    try: odd_2_2 = team['displayGroups'][0]['markets'][1]['outcomes'][1]['price']['american']
                    except KeyError: odd_2_2 = None
                    try: ML_2 = team['displayGroups'][0]['markets'][0]['outcomes'][0]['price']['american']
                    except KeyError: ML_2 = None
                    try: ML_1 = team['displayGroups'][0]['markets'][0]['outcomes'][1]['price']['american']
                    except KeyError: ML_1 = None
                    try: o = team['displayGroups'][0]['markets'][2]['outcomes'][0]['price']['handicap']
                    except KeyError: o = None
                    try: o_1 = team['displayGroups'][0]['markets'][2]['outcomes'][0]['price']['american']
                    except KeyError: o_1 = None
                    try: u = team['displayGroups'][0]['markets'][2]['outcomes'][1]['price']['handicap']
                    except KeyError: o = None
                    try: u_1 = team['displayGroups'][0]['markets'][2]['outcomes'][1]['price']['american']
                    except KeyError: o_1 = None
                    if team['displayGroups'][0]['markets'][0]['period']['live'] is True:
                        print('{0}  | {1}'.format(count, 'LIVE!'))
                    else:
                        print('{0}  |'.format(count))
                    print(date)
                    print("{0} ({1},{2}) | {3} | o({4},{5})".format(team_2,odd_1_1, odd_1_2, ML_2, o, o_1))
                    print("{0} ({1},{2}) | {3} | u({4},{5})".format(team_1,odd_2_1, odd_2_2, ML_1, u, u_1))
                    if team['competitors'][0]['home'] is True:
                        print(get_weather(abbrev(team_1,'city'), date))
                    else:
                        print(get_weather(abbrev(team_2, 'city'), date))
                    print(SUBSET)
                    game_list.append(team_1)
                    game_info = [{'Time': date, 'Away Team': team_2, 'odds': odd_1_1, 'Win': odd_1_2,
                                 'Money Line': ML_2, 'Over': o, 'Over Line': o_1, 'Under': u,
                                 'Under Line': u_1, 'Home Team': team_1, 'odds': odd_2_1, 'Win': odd_2_2,
                                 'Money Line': ML_1}]
                    backtest(game_info)
            except KeyError: odd_1_1 = None
            except IndexError:
                pass


    #main()


def start_up():
    team = input('Enter team: ')




if __name__ == "__main__":
    print(BORDER)
    print((' ' * 5) + 'DRAFT DAY')
    print((' ' * 5) + 'CREATED BY: DAVID JAMROG')
    print((' ' * 5) + 'V1.0')
    print(BORDER + '\n')
    main()