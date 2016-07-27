import matplotlib

import matplotlib.pyplot as plt
import pandas as pd

'''
I can't upload the dataset that I used because it's a free but copyrighted downloadable sample from a stats website.
'''
dataset = pd.read_excel('nba-sample.xlsx')

len(dataset)

dataset.columns.values

sanantonio = dataset[dataset['OWN TEAM'] == 'San Antonio']
miami = dataset[dataset['OWN TEAM'] == 'Miami']
miami = miami[miami['OPP TEAM'] == 'San Antonio']

f_size = (25, 10)

def barplot_comparison(feature, axes):
    indices = sanantonio[feature].value_counts().index.union(miami[feature].value_counts().index)
    def barplot(data, color, label, pos):
        return data.plot(kind = 'bar', figsize = f_size, color = color, position = pos, label = label, legend = True, ax = axes, width = 0.3)
    barplot(data = miami[feature].value_counts()[indices], color = 'red', label = 'Miami', pos = 0)
    barplot(data = sanantonio[feature].value_counts()[indices], color='black', label = 'San Antonio', pos = 1)

axes = plt.axes()
axes.set_xlabel('Position')
axes.set_ylabel('Number of Players')
axes.set_ylim(0, 6)
barplot_comparison('POSITION', plt.axes())
plt.show()


def boxplot_comparison(feature, axes, figsize = None):
    f = None
    if figsize:
        f = figsize
    else:
        f = f_size
    def boxplot(data, pos, ax):
        data.plot(kind = 'box', figsize = f, grid = True, showmeans = True, showcaps = True, whis = 'range', positions = pos, ax = ax)
    pos = 0
    teams = set(dataset['OWN TEAM'])
    teamsList = sorted(list(teams))
    for team in teamsList:
        team_data = dataset[dataset['OWN TEAM'] == team]
        team_data = team_data[team_data['DATE'] == team_data['DATE'][team_data.index[0]]]
        pos += 1
        boxplot(data = team_data[feature], ax = axes, pos = [pos])

    teamsList.insert(0, '')
    teamsList.append('')
    axes.set_xticklabels(teamsList)
    axes.set_xticks(range(0, len(team_data) + 2, 1))

axes = plt.axes()
axes.set_xlabel('Teams')
axes.set_ylabel('Points')
boxplot_comparison('PTS', axes)
plt.show()

def define_position_number(pos):
    if pos == 'C':
        return 5.0
    elif pos == 'PF':
        return 4.0
    elif pos == 'SF':
        return 3.0
    elif pos == 'SG':
        return 2.0
    elif pos == 'PG':
        return 1.0
    else:
        return 0.0

def assign_pos_number_category(data):
    data['POSITION NUMBER'] = data['POSITION'].apply(lambda pos:define_position_number(pos))

assign_pos_number_category(dataset)
    
ax = dataset.plot(kind = 'scatter', x = 'POSITION NUMBER', y = 'PTS', figsize = f_size)
ax.set_xlabel('Position')
ax.set_ylabel('Points')
ax.set_ylim(0, 40)
ax.set_xlim(0, 6)
ax.set_xticklabels(['', 'PG', 'SG', 'SF', 'PF', 'C', ''])

plt.show()
