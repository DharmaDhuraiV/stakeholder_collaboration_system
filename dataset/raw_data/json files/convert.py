import pandas as pd
import os

if __name__=='__main__':
    df = pd.read_json('Angular.json')
    lis = []
    for path in os.listdir('.\\')[1:]:
        try:
            df = pd.concat([df, pd.read_json(path)])
        except:
            lis.append(path)
            continue
    df.to_csv('.\\dataset.csv')