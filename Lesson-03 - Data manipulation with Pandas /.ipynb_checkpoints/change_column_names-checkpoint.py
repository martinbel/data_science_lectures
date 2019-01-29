# This script is just the names conversion from spanish to english
import pandas as pd

df = pd.read_csv('../Lesson-01 - Intro to Python & Scraping example/deptos.csv')

cols = {'Ambientes':'rooms', 'Antigüedad':'age', 'Baños':'bath', 
        'Departamentos por piso':'aparment_floor', 
        'Disposición':'view', 'Dormitorios':'bedrooms',
       'Expensas':'expenses', 
       'Piso (unidad)':'floor', 'Pisos':'nbr_floors', 
        'Superficie cubierta':'covered area', 
        'Superficie total':'total_area',
        'Tipo de departamento':'type', 'address':'address', 
        'price':'price', 'neighborhood':'neighborhood'}

df.rename(columns=cols, inplace=True)

df = df[['rooms', 'age', 'bath', 'neighborhood',
        'aparment_floor', 'view', 'bedrooms', 
        'expenses', 'floor', 'nbr_floors',
        'covered area', 'total_area', 'type', 'address', 'price']]

df.to_csv('deptos_eng.csv', index=False)
