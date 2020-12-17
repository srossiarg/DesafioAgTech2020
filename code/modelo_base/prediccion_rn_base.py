# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:05:56 2020

@author: mdalessandro
"""
#import utils
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import preprocessing
from sklearn import metrics
from sklearn.utils import class_weight

import tensorflow as tf
import keras
import numpy as np
#import utils 
import os

modelo_base= keras.models.load_model('code/modelo_base/modelo_base.h5')

# Carga del dataset
path_final = 'dataset/raw/df_test_rn_base.csv'
data_test_final = pd.read_csv(path_final)
data_test_final.head()

data_test_final.shape

list(data_test_final)

# Carga del dataset de test
from numpy import genfromtxt
data=genfromtxt(path_final, delimiter=",",skip_header=1)
x_test_final=data[:,2:324]

n,d_in=x_test_final.shape

# Normalizo las variables de entrada
for i in range(d_in):
    x_test_final[:,i]=(x_test_final[:,i]-x_test_final[:,i].mean())/x_test_final[:,i].std()
    
y_test_final = modelo_base.predict_classes(x_test_final)
y_test_final

y_test_final_df = pd.DataFrame(data=y_test_final)
y_test_final_df = y_test_final_df.rename(columns={0: "prediction"})
y_test_final_df.value_counts()

result = pd.concat([data_test_final[['GlobalId']].reset_index(drop=True), y_test_final_df], axis = 1)
print(result.shape)

df_final = pd.concat([data_test_final.loc[:,'GlobalId'],  pd.DataFrame(y_test_final)], axis=1, sort=False)
df_final  = df_final.rename(columns = {0:"CultivoId"}) 
df_final 

### Agrego agua y urbano en test
puntos_urbanos_agua_test = pd.read_csv('dataset/raw/puntos_urbanos_test.csv')
df_final =  df_final.merge(puntos_urbanos_agua_test, how='outer', on='GlobalId')
df_final.loc[~pd.isna(df_final['CultivoId_y']),'CultivoId_x'] = df_final.loc[~pd.isna(df_final['CultivoId_y']),'CultivoId_y']
df_final = df_final.drop('CultivoId_y',axis=1) 
df_final = df_final.rename(columns = {'CultivoId_x':"CultivoId"})

df_final.value_counts('CultivoId')

df_rf_viejo = pd.read_csv('code/modelo_cart/salida_modelo_base_CART.csv', header=None)
df_rf_viejo = df_rf_viejo.rename(columns = {0:'GlobalId',1:"CultivoId"})
df_rf_viejo =  df_rf_viejo.merge(df_final, how='left', on='GlobalId')
df_rf_viejo.loc[pd.isna(df_rf_viejo['CultivoId_y']),'CultivoId_y'] = df_rf_viejo.loc[pd.isna(df_rf_viejo['CultivoId_y']),'CultivoId_x']

df_rf_viejo = df_rf_viejo.drop('CultivoId_x',axis=1) 
df_rf_viejo = df_rf_viejo.rename(columns = {'CultivoId_y':"CultivoId"})
df_rf_viejo.value_counts('CultivoId')
df_rf_viejo.to_csv('code/modelo_base/result_modelo_base.csv',index=False, header=False)
