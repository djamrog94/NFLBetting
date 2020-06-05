import json


def abbrev(team, option):
    with open('nfl.json') as json_file:
        data = json.load(json_file)

    for i in range(len(data)):
        try:
            if team.lower() == data[i]['city'].lower() or team.lower() == data[i]['name'].lower() or \
                    team.lower() == data[i]['abr'].lower() or team.lower() == data[i]['conf'].lower() or \
                    team.lower() == data[i]['div'].lower() or team.lower() == data[i]['team'].lower() or\
                    team.lower() == data[i]['alt'].lower():
                return data[i][option]
        except:
            pass


def odds_convert(odds):
    if odds >= 2:
        return int((odds - 1) * 100)
    else:
        return int(-100 / (odds - 1))



