Code written by: Russlan Jaafreh


import numpy as np
import pandas as pd
import os
import pymatgen.core as pg

df = pd.read_csv('Final_Dataset.csv') ## Import the training dataset
Y = df['LTC']
Before_Features = df.drop(['LTC','Compound'],axis = 1) ## Drop the commpound name and targeted property

## VT Analysis
from sklearn.feature_selection import VarianceThreshold
var_thres = VarianceThreshold(threshold=.8*(1-0.8))
var_thres.fit(Before_Features)
var_thres.get_support()
constant_columns = [column for column in Before_Features.columns if column not in Before_Features.columns[var_thres.get_support()]]
After_Variance = Before_Features.drop(constant_columns,axis=1)

## PC Analysis
import matplotlib.pyplot as plt 
import seaborn as sns
def correlation(dataset, threshold):
    col_corr = set()  # Set of all the names of correlated columns
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                colname = corr_matrix.columns[i]  # getting the name of column
                col_corr.add(colname)
    af_corr = dataset.drop(col_corr,axis=1)
    return af_corr

af_both2 = correlation(After_Variance, 0.80)
af_both2.shape

##Scaling
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(af_both2)
df_scaled = pd.DataFrame(df1_scaled)
df_scaled.columns =af_both2.columns

##Vizualizing the split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df_scaled, Y, test_size=0.25, random_state=90)
sns.histplot(data=Y,bins=20,kde=True,legend=True)
sns.histplot(data=y_train,color = "g",bins=20,kde=True)
sns.histplot(data=y_test,color="r",bins=20,kde=True)

##RF Algorithm
from sklearn.ensemble import RandomForestRegressor
rf_reg = RandomForestRegressor()
rf_reg.fit(X_train,y_train)
rf_reg.score(X_test,y_test)

##Repeated K-fold
scores = []
counter = 0
from sklearn.model_selection import RepeatedKFold
fold = RepeatedKFold(n_splits = 10,n_repeats=10, random_state=30)
for train_index, test_index in fold.split(af_both2):
    counter = counter + 1
    X_train, X_test = af_both2.iloc[train_index], af_both2.iloc[test_index]
    y_train, y_test = Y.iloc[train_index], Y.iloc[test_index]
    rf_reg.fit(X_train,y_train)
    scores.append(get_score(rf_reg,X_train,y_train,X_test,y_test))


