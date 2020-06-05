import nflgame
import pandas as pd
from abbrev import abbrev, odds_convert
import datetime


# def get_scores():
#     df = pd.read_excel('2010_betting.xlsx')
#     df['schedule_week'] = df['schedule_week'].replace(
#         {'WildCard': 0,
#          'Wildcard': 0,
#          'Division': 1,
#          'Conference': 2,
#          'Superbowl': 3,
#          'SuperBowl': 3})
#     df = df.astype({'schedule_week': 'int64'})
#     df['schedule_date'] = pd.to_datetime(df['schedule_date'])
#     df1 = df.loc[df['schedule_season'] == 2019]
#     df1 = df1.reset_index()
#     df1 = df1.drop(['index', 'Unnamed: 0'], axis=1)
#
#     games = nflgame.games(2019, started=True)
#     for game in games:
#         week = game.schedule['week']
#         home_team = abbrev(game.home, 'team')
#         home_score = game.score_home
#         away_team = abbrev(game.away, 'team')
#         away_score = game.score_away
#         for i in range(len(df1)):
#             if df1.iloc[i]['schedule_week'] == week and df1.iloc[i]['team_home'] == home_team:
#                 df1.loc[i, 'score_home'] = home_score
#                 df1.loc[i, 'score_away'] = away_score
#                 print(f'updated week: {week}. Home: {home_team} vs Away: {away_team}')
#     return df1


def create_schedule(year):
    df = pd.read_excel('2010_betting.xlsx')
    df['schedule_week'] = df['schedule_week'].replace({'WildCard': 0, 'Wildcard': 0, 'Division': 1, 'Conference': 2,
                                                       'Superbowl': 3, 'SuperBowl': 3})
    df = df.astype({'schedule_week': 'int64'})
    df['schedule_date'] = pd.to_datetime(df['schedule_date'])
    df = df.reset_index()
    df = df.drop(['index', 'Unnamed: 0'], axis=1)
    games = nflgame.games(year=year, started=True)
    for game in games:
        week = game.schedule['week']
        date = datetime.datetime(game.schedule['year'], game.schedule['month'], game.schedule['day'])
        home_team = abbrev(game.home, 'team')
        away_team = abbrev(game.away, 'team')
        home_score = game.score_home
        away_score = game.score_away
        df.loc[len(df)] = [date, year, week, 'FALSE', home_team, home_score, away_score, away_team,0,0,0,0,0,0,0,0,0]
    df.to_excel('2010_out.xlsx')
    return df


def get_odds():
    df = pd.read_excel('2010_out.xlsx')
    df["favorite_line"] = ""
    df["dog_line"] = ""
    df["spread_win"] = ""
    df["over_win"] = ""
    odds_df = pd.read_excel('nfl.xlsx')
    odds_df = odds_df.drop(odds_df.apply(lambda x: x.count() == 1527)[lambda x: x].index, axis=1)

    for i in range(len(df)):
        try:
            home_team = df.iloc[i]['team_home']
            away_team = df.iloc[i]['team_away']
            date = df.iloc[i]['schedule_date']
            game_index = odds_df.loc[(odds_df['Date'] == date) & (odds_df['Home Team'] == home_team)].index
            df.loc[i, 'over_under_line'] = odds_df.iloc[game_index]['Total Score Open'].values[0]
            spread = odds_df.iloc[game_index]['Home Line Open'].values[0]
            if spread < 0:
                df.loc[i, 'spread_favorite'] = spread
                df.loc[i, 'team_favorite_id'] = abbrev(home_team, 'abr')
                df.loc[i, 'favorite_line'] = odds_convert(odds_df['Home Odds Open'][game_index].values[0])
                df.loc[i, 'dog_line'] = odds_convert(odds_df['Away Odds Open'][game_index].values[0])
            else:
                df.loc[i, 'spread_favorite'] = spread * -1
                df.loc[i, 'team_favorite_id'] = abbrev(away_team, 'abr')
                df.loc[i, 'favorite_line'] = odds_convert(odds_df['Away Odds Open'][game_index].values[0])
                df.loc[i, 'dog_line'] = odds_convert(odds_df['Home Odds Open'][game_index].values[0])
            if abbrev(df.iloc[i]['team_favorite_id'], 'team') == df.iloc[i]['team_home']:
                if df.iloc[i]['score_home'] + df.iloc[i]['spread_favorite'] > df.iloc[i]['score_away']:
                    df.loc[i, 'spread_win'] = home_team
                elif df.iloc[i]['score_home'] + df.iloc[i]['spread_favorite'] < df.iloc[i]['score_away']:
                    df.loc[i, 'spread_win'] = away_team
                else:
                    df.loc[i, 'spread_win'] = 'PUSH'
            else:
                if df.iloc[i]['score_away'] + df.iloc[i]['spread_favorite'] > df.iloc[i]['score_home']:
                    df.loc[i, 'spread_win'] = away_team
                elif df.iloc[i]['score_away'] + df.iloc[i]['spread_favorite'] < df.iloc[i]['score_home']:
                    df.loc[i, 'spread_win'] = home_team
                else:
                    df.loc[i, 'spread_win'] = 'PUSH'
            if df.iloc[i]['score_home'] + df.iloc[i]['score_away'] > df.iloc[i]['over_under_line']:
                df.loc[i, 'over_win'] = True
            elif df.iloc[i]['score_home'] + df.iloc[i]['score_away'] < df.iloc[i]['over_under_line']:
                df.loc[i, 'over_win'] = False
            else:
                df.loc[i, 'over_win'] = 'PUSH'
        except:
            pass
    df.to_excel('master_file.xlsx')


def update_list():
    # get index and then send that last to odds and score function, they will finish by updating master file
    create_schedule(2019)
    get_odds()


update_list()
