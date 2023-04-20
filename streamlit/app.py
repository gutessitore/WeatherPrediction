import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from functions_models import xgboost_regressor

#inputs user --> area, rendimento%, range data

#CSV's
df_irrad = pd.read_csv('data/openw_irradiation_2005_2020.csv')
df_irrad.drop(['day', 'weather_id'], axis = 1, inplace=True)

y_pred = xgboost_regressor(df_irrad) #irradiation predictions

# y_pred = [118.130264, 114.73563 , 101.42404 , 176.47775 , 112.80841 ,
#        157.99327 , 110.982155, 108.196976, 110.56889 , 137.60085 ,
#        110.87699 , 109.21667 , 102.76564 , 104.48606 , 167.93588 ,
#        109.639755, 188.73145 , 113.77642 , 139.08853 , 114.32364 ,
#        150.87944 , 150.07391 , 167.99814 , 133.70808 , 118.03198 ,
#        133.8792  , 142.81291 , 151.81943 , 145.09813 , 150.08461 ,
#        108.7888  , 154.68489 , 131.83202 , 119.56206 , 156.33952 ,
#        113.300896, 167.98074 , 153.09451 , 132.89561 , 149.40417 ,
#        212.66118 , 115.48822 , 165.70786 , 158.96251 , 104.79509 ,
#        167.0878  ,  96.5487  , 133.39662]

now = datetime.now()
current_month = now.month
current_year = now.year

dates = [datetime(current_year + ((current_month + i - 1) // 12), (current_month + i) % 12 or 12, 1) for i in range(1, 33)]
df = pd.DataFrame({'data':dates, 
                   'irrad kwh/m2':y_pred})


#######################App###################################
st.markdown('# Energy Generation Predictor')
st.dataframe(df)

#user inputs
area = st.number_input('Digite a área total em m2 de painéis solares', step=5, min_value=2)
rend = st.slider('Digite o rendimento médio em % dos painéis', min_value=0, max_value=100, step=1)
range_data = st.number_input('Digite a quantidade em anos para previsão', min_value=1, max_value=20, step=1)

#calc_energy
calc_energy = df['irrad kwh/m2'].sum() * area * rend/100
st.write(f'A energia gerada para os próximos {range_data} anos é', round(calc_energy,2), 'kwh') 
