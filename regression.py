import pandas as pd
data = pd.read_table('out.txt', names=['student', 'classname', 'dt', 'test', 'score'], sep="|", parse_dates=True)
data["dt"]=pd.to_datetime(data["dt"], format='%Y-%m-%d %H:%M:%S')
data.sort(['student', 'classname', 'dt'])
grouped = data.groupby(['student']).size()
grouped.sort(ascending=False)
grouped
data[data["student"]=='Tina Joyner']

data[data["test"]=='best']
data[data["student"]=='Tyronza Wyche']

