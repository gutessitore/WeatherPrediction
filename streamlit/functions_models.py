#IMPORTS
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.metrics import r2_score


#FUNCTIONS_MODELS


def xgboost_regressor(df):
    #features and target
    X = df.drop(['irrad kwh/m2'], axis=1)
    y = df[['irrad kwh/m2']]

    #train test split
    tscv = TimeSeriesSplit(n_splits=5)
    # Loop folds
    for train_index, test_index in tscv.split(df['year'], df['month']):
    
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #XGBoost with default parameters
    xg_reg = xgb.XGBRegressor()
    # training the model
    xg_reg.fit(X_train,y_train)

    # predicting
    xgb_preds = xg_reg.predict(X_test)
    return xgb_preds

    #r score
    # print('R score is :', r2_score(y_test, xgb_preds))
    

