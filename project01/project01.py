import pandas as pd
import json
import re
import pickle

df = pd.read_csv("proj1_ex01.csv")
df.head()

info = []
for col in df.columns:
    dict1 = {'name': None, 'missing': None, 'type': None}
    
    dict1['name'] = df[col].name
    dict1['missing'] = df[col].isnull().sum() / len(df[col])
    # print(df[col].dtypes)
    if df[col].dtypes == "float":
        dict1['type'] = 'float'
    elif df[col].dtypes == "int":
        dict1['type'] = 'int'
    else:
        dict1['type'] = 'other'
    info.append(dict1)
    
print(info)
with open('proj1_ex01_fields.json', 'w') as file:
    json.dump(info, file)


dict2 = {}

for col in df.columns:
    dict_c = {}
    
    dict_c["count"] = float(df[col].count())
    if df[col].dtypes in ("int", "float"):
        dict_c['mean'] = float(df[col].mean())
        dict_c['std'] = float(df[col].std())
        dict_c['min'] = float(df[col].min())
        dict_c['25%'] = float(df[col].quantile(0.25))
        dict_c['50%'] = float(df[col].quantile(0.5))
        dict_c['75%'] = float(df[col].quantile(0.75))
        dict_c['max'] = float(df[col].max())
    else:
        dict_c['unique'] = float(df[col].nunique(dropna=True))
        freq = df[col].value_counts().max()
        # the_most_freq = df[col].value_counts().loc[lambda x: x==a].index
        # print(the_most_freq)
        # for x in the_most_freq:
        #     dict_c['top'].append(x)
        dict_c['top'] = df[col].value_counts().idxmax()
        dict_c['freq'] = float(freq)
    
    dict2[df[col].name] = dict_c
    print(dict_c)

with open('proj1_ex02_stats.json', 'w') as file:
    json.dump(dict2, file, indent=4)


for col in df.columns:
    print(df[col].name)
    x = re.sub('[^A-Za-z0–9_ ]', '', df[col].name).lower().replace(' ', '_')
    print(x)
    df.rename(columns = {df[col].name: x}, inplace=True)

df.to_csv('proj1_ex03_columns.csv', index=False)


df.to_excel('proj1_ex04_excel.xlsx', engine='openpyxl', index=False)
df.to_json('proj1_ex04_json.json', orient='records', lines=False)
df.to_pickle('proj1_ex04_pickle.pkl')


with open('proj1_ex05.pkl', 'rb') as file:
    data = pickle.load(file)
    columns = data.iloc[:, [1, 2]]
    print(columns)
    rows = columns[columns.index.str.startswith('v')].fillna('')
    print(rows)
    rows.to_markdown('proj1_ex05_table.md')



with open('proj1_ex06.json', 'r') as file:
    json_data = json.load(file)
    normalized = pd.json_normalize(json_data)
    # print(normalized)
    normalized.to_pickle('proj1_ex06_pickle.pkl')

