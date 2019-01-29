import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_data(df):
    df['neighborhood'] = df['neighborhood'].str.replace(' - Capital Federal', 
                                                        '', regex=False)
    df['neighborhood'] = df['neighborhood'].str.lower()
    
    df['age'] = df['age'].str.replace('[^0-9]+', '', regex=True)
    df['age'] = df.age.astype('float64')
    
    df = df[(df.age <= 80) | (df.age.isna())]
    df = df[df.bedrooms < 7]
    
    df['expenses'] = np.where(df.expenses < 100, np.nan, df.expenses)
    
    return df


def outliers(x, thr=1.5):
    x = np.log(x)
    q1, q3 = np.nanpercentile(x, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (iqr * thr)
    upper_bound = q3 + (iqr * thr)
    return np.where((x > upper_bound) | (x < lower_bound))[0]


df = pd.read_csv('deptos_eng.csv')
df = read_data(df)

df.head()
