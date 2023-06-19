from extract import extract_data
import pandas as pd

def transform_data(usersdf, expdf, compoundsdf):
    
    #Question 1
    q1 = pd.merge(usersdf, expdf, on="user_id").groupby(["user_id", "name"])['experiment_id'].count().reset_index()
    q1 = q1.rename(columns = {'experiment_id' : 'count'})
    
    #Question 2
    totalexperiments = len(expdf)
    q2 = pd.merge(usersdf, expdf, on="user_id").groupby(["user_id", "name"])["experiment_id"].count().reset_index()
    q2 = q2.rename(columns = {'experiment_id' : 'average'})
    q2['average'] = q2['average']/totalexperiments
    
    #Question 3
    expdf["experiment_compound_ids"] = expdf["experiment_compound_ids"].str.split(";")
    df3 = expdf.explode("experiment_compound_ids").reset_index(drop=True)
    df3 = df3.astype({"experiment_compound_ids" : "int64"})
    q3 = pd.merge(df3, compoundsdf, left_on='experiment_compound_ids', right_on='compound_id', how='right')
    q3 = q3.groupby(['user_id', 'compound_id', 'compound_name', 'compound_structure'])\
            .count().rename(columns = {'experiment_id' : 'count'})\
            .reset_index()[['user_id','compound_id','compound_name','compound_structure','count']]
    q3 = q3.groupby(['user_id'])\
            .apply(lambda x : x.sort_values(['count'], ascending=False))\
            .reset_index(drop=True)
    q3 = q3.groupby(['user_id']).head(1).reset_index(drop=True)

    return q1, q2, q3