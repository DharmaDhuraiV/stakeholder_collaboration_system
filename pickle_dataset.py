import pickle
import pandas as pd

def filter_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df = df.drop_duplicates(subset=['repo_name', 'username'])
    df['stars'].map(int)
    df['forks'].map(int)
    df['subscribers'].map(int)
    return df
    

def get_project_dict(row:list, ind: pd.DataFrame.columns):
    project = dict(zip(ind.values, row))
    project['node_type'] = 'repo'
    
    topics = project['topics'][2:-2].split('\', \'')
    
    if len(topics)==1 and topics[0]=='':
        return None, None

    for index, topic in enumerate(topics):
        topic = '_'.join(topic.strip().lower().split(' '))
        topics[index] = '_'.join(topic.strip().lower().split('-'))

    del project['topics']

    return project, topics


def get_user_proj_dict(df: pd.DataFrame):
    final_topics = set()
    projects = list()
    edges = list()

    pid = 1

    for row in df.values:
        project, topics = get_project_dict(row, df.columns)
        
        if topics is None:
            continue
        
        for topic in topics:
            final_topics.add(topic)
            edges.append((topic, pid))
        
        projects.append((pid,project))
        pid+=1

    return {"topics":[(topic, {"node_type": "topic"}) for topic in final_topics], "projects": projects, "edges": edges}


if __name__=='__main__':
    
    df = filter_df(pd.read_csv('./dataset/dataset.csv'))

    result = get_user_proj_dict(df)

    with open('./dataset/data_formatted.pkl', 'wb') as file:
        pickle.dump(result, file)