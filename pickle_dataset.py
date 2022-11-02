import pickle
import pandas as pd
from pprint import pprint

def filter_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df['stars'].map(int)
    df['forks'].map(int)
    df['subscribers'].map(int)
    return df
    

def get_project_dict(row:list, ind: pd.DataFrame.columns):
    project = dict(zip(ind.values, row))
    
    del project['username']
    
    project['node_type'] = 'repo'
    
    res = ''
    for topic in project['topics'][2:-2].split('\', \''):
        res+=','+topic
    
    if res==',':
        return None

    project['topics'] = res[1:]

    return project


def get_user_proj_dict(df: pd.DataFrame):
    usernames = set()
    projects = list()
    edges = list()

    pid = 1

    for row in df.values:
        username = row[df.columns.get_loc('username')]
        project = get_project_dict(row, df.columns)
        if project is None:
            continue
        
        usernames.add(username)
        edges.append((username, pid))
        projects.append((pid,project))
        pid+=1

    return {"usernames":[(name, {"node_type": "user"}) for name in usernames], "projects": projects, "edges": edges}

"""
function to remove rows that have empty values and formats topic column to a string 
"""
if __name__=='__main__':
    
    df = filter_df(pd.read_csv('./dataset/dataset.csv'))
    
    result = get_user_proj_dict(df)

    # pprint(result['projects'])
    
    with open('./data_formatted.pkl', 'wb') as file:
        pickle.dump(result, file)