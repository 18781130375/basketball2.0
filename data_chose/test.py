# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import pymysql
from flask import Flask, jsonify
import pandas as pd
import json

app = Flask(__name__)


def staff_tojson(df, t1, t2):
  df2 = df.loc[df['time'] < t2].loc[df['time'] > t1].reset_index().drop('index', axis=1)
  df_json = df2.to_json(orient='index')
  df_dic = json.loads(s=df_json)
  result = []
  for i in range(df2.last_valid_index() + 1):
    result.append(df_dic[str(i)])
  return result


def relation_tojson(df0, t1, t2):
  team_player_dic = {'Andre Iguodala': ('GSW', 2738),
                     'Andrew Bogut': ('GSW', 101106),
                     'Brandon Rush': ('GSW', 201575),
                     'Draymond Green': ('GSW', 203110),
                     'Festus Ezeli': ('GSW', 203105),
                     'Ian Clark': ('GSW', 203546),
                     'Iman Shumpert': ('CLE', 202697),
                     'J.R. Smith': ('CLE', 2747),
                     'James Jones': ('CLE', 2592),
                     'James Michael McAdoo': ('GSW', 203949),
                     'Kevin Love': ('CLE', 201567),
                     'Klay Thompson': ('GSW', 202691),
                     'Kyrie Irving': ('CLE', 202681),
                     'LeBron James': ('CLE', 2544),
                     'Leandro Barbosa': ('GSW', 2571),
                     'Marreese Speights': ('GSW', 201578),
                     'Matthew Dellavedova': ('CLE', 203521),
                     'Mo Williams': ('CLE', 2590),
                     'Shaun Livingston': ('GSW', 2733),
                     'Stephen Curry': ('GSW', 201939),
                     'Timofey Mozgov': ('CLE', 202389),
                     'Tristan Thompson': ('CLE', 202684)}
  df2 = df0.loc[df0['time'] < t2].loc[df0['time'] > t1].reset_index().drop('index', axis=1)
  df3 = df2.loc[df2['object_player'] != '0'].reset_index().drop('index', axis=1)
  df = df3
  df['time'] = 1
  grouped = df['time'].groupby([df['action'], df['action_player'], df['object_player']]).sum()
  df4 = grouped.reset_index()
  df5 = df4.loc[df4['action'] != 'sub']
  result = []
  for index, row in df5.iterrows():
    temp_dict = {}
    target = row['object_player']
    source = row['action_player']
    temp_dict['target'] = team_player_dic[target][1]
    temp_dict['source'] = team_player_dic[source][1]
    temp_dict['type'] = "resolved"
    temp_dict['rela'] = row['action']
    temp_dict['time'] = row['time']
    temp_dict['teamsou'] = team_player_dic[source][0]
    temp_dict['teamtar'] = team_player_dic[target][0]
    result.append(temp_dict)
  return result


def tojsons(df, t1, t2):
  df1 = df.loc[df['time'] < t2].loc[df['time'] > t1].reset_index().drop('index', axis=1)
  df_json = df1.to_json(orient='index')
  df_dic = json.loads(s=df_json)
  result = []
  for i in range(df1.last_valid_index() + 1):
    result.append(df_dic[str(i)])
  return result

def result_pos_toarray(df, t1, t2):  # new added
    df1 = df.loc[df['converted_x'] < t2].loc[df['converted_x'] > t1].reset_index().drop('index', axis=1)
    df_json = df1.to_json(orient='index')
    df_dic = json.loads(s=df_json)
    result = []
    for i in range(df1.last_valid_index() + 1):
      result.append([df_dic[str(i)]['converted_x'], df_dic[str(i)]['converted_y'], int(df_dic[str(i)]['result'])])
    return result


def tojsons1(df, t1, t2):
  df1 = df.loc[df['time'] < t2].loc[df['time'] > t1].reset_index().drop('index', axis=1)
  df_json = df1.to_json(orient='index')
  df_dic = json.loads(s=df_json)
  result = []
  for i in range(df1.last_valid_index() + 1):
    result.append([df_dic[str(i)]['time'], df_dic[str(i)]['score_diff']])
  return result

def position(t1, t2):
  t1 = float(t1) + 1.0
  t2 = float(t2) - 3.0
  df = pd.read_csv('./player_locations.csv')
  return tojsons(df, t1, t2)

@app.route('/staff/<t1>,<t2>', methods=['GET'])  # 五线谱
def staff(t1, t2):
  t1 = float(t1)
  t2 = float(t2)
  df = pd.read_csv('./action.csv')
  result1 = staff_tojson(df, t1, t2)
  return jsonify(result1)


@app.route('/relationship/<t1>,<t2>', methods=['GET'])  # 攻防关系
def relationship(t1, t2):
  t1 = float(t1)
  t2 = float(t2)
  df = pd.read_csv('./action.csv')
  result1 = relation_tojson(df, t1, t2)
  nodes = []
  links = []
  sankey = []
  player = {
    2544: ['LeBron James', 'CLE', 23],
    2571: ['Leandro Barbosa', 'GSW', 19],
    2590: ['Mo Williams', 'CLE', 52],
    2592: ['James Jones', 'CLE', 1],
    2733: ['Shaun Livingston', 'GSW', 34],
    2738: ['Andre Iguodala', 'GSW', 9],
    2747: ['J.R. Smith', 'CLE', 5],
    101106: ['Andrew Bogut', 'GSW', 12],
    201567: ['Kevin Love', 'CLE', 0],
    201575: ['Brandon Rush', 'GSW', 4],
    201578: ['Marreese Speights', 'GSW', 5],
    201939: ['Stephen Curry', 'GSW', 30],
    202389: ['Timofey Mozgov', 'CLE', 20],
    202681: ['Kyrie Irving', 'CLE', 2],
    202684: ['Tristan Thompson', 'CLE', 13],
    202691: ['Klay Thompson', 'GSW', 11],
    202697: ['Iman Shumpert', 'CLE', 4],
    203105: ['Festus Ezeli', 'GSW', 31],
    203110: ['Draymond Green', 'GSW', 23],
    203521: ['Matthew Dellavedova', 'CLE', 8],
    203546: ['Ian Clark', 'GSW', 21],
    203949: ['James Michael McAdoo', 'GSW', 20]
  }

  for i in range(len(result1)):
    re = result1[i]
    value = re['time']
    name1 = player[re['source']][0]
    name2 = player[re['target']][0]
    if {'name': name1} not in nodes:
      nodes.append({'name': name1})
    if {'name': name2} not in nodes:
      nodes.append({'name': name2})
    links.append({'source': nodes.index({'name': name1}), 'target': nodes.index({'name': name2}), 'value': value})
  return jsonify(result1);


@app.route('/pass_sequence/<t1>,<t2>', methods=['GET'])  # 传球序列
def pass_sequence(t1, t2):
  t1 = float(t1)
  t2 = float(t2)
  df = pd.read_csv('./pass.csv')
  result1 = tojsons(df, t1, t2)
  return jsonify(result1)


@app.route('/player_position/<t1>,<t2>', methods=['GET'])  # 球员位置
def player_position(t1, t2):
  t1 = float(t1) + 1.0
  t2 = float(t2) - 3.0
  df = pd.read_csv('./player_locations.csv')
  result1 = tojsons(df, t1, t2)
  return jsonify(result1)


@app.route('/Some_Time_player_position/<t>', methods=['GET'])  # 多个时间段球员位置
def Some_Time_player_position(t):
  t = str(t)
  result = []
  strtime = t.split(";")
  strtime = strtime[:-1]
  for time in strtime:
     time = time.split(",")
     t1 = time[0];
     t2 = time[1];
     result1 = position(float(t1),float(t2))
     result.append(result1)
  return jsonify(result)


@app.route('/score/<t1>,<t2>', methods=['GET'])  # 球员得分
def score(t1, t2):
  t1 = int(t1)
  t2 = int(t2)
  df = pd.read_csv('./score_diff.csv')  # 分差
  result1 = tojsons1(df, t1, t2)
  return jsonify(result1)

#wrong
@app.route('/attack_time/<t1>,<t2>', methods=['GET'])  #得分花费的时间
def attack_time(t1, t2):
  t1 = int(t1)
  t2 = int(t2)
  df = pd.read_csv('./play_attack_time.csv') #进攻时间
  result1 = tojsons1(df,t1,t2)
  return jsonify(result1)

@app.route('/result_pos/<t1>,<t2>', methods=['GET'])  # 球员位置热力图
def result_pos(t1, t2):
    t1 = int(t1)
    t2 = int(t2)
    df = pd.read_csv('./result_pos.csv')
    result1 = result_pos_toarray(df, t1, t2)
    return jsonify(result1)

if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=80, debug=True)
