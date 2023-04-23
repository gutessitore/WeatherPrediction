# Creatting a dashboard of traffic data using streamlit
import streamlit as st
import folium
from streamlit_folium import st_folium
from PIL import Image
from datetime import datetime

st.set_page_config(page_title='Traffic Jam Predictor', layout='wide', page_icon='🚘')

if 'pressed_change_addr' not in st.session_state:
    st.session_state.pressed_change_addr = False
if 'loc_name' not in st.session_state:
    st.session_state.loc_name = 'São Paulo, SP'
if 'loc_lat' not in st.session_state:
    st.session_state.loc_lat = -23.55
if 'loc_lon' not in st.session_state:
    st.session_state.loc_lon = -46.64

st.header('🚘 Traffic Jam Predictor')

with open('streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Using 3:1 ratio for the main columns
col_main1, col_main2 = st.columns([3, 1])
# SP regions
city_region = ['Norte', 'Oeste', 'Centro', 'Leste', 'Sul']
traffic_jam = [2, 2, 2, 6, 7]
color = ['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099']

# Define the styles for each region
style_norte = f"background-color: {color[0]}; color: white;"
style_oeste = f"background-color: {color[1]}; color: white;"
style_centro = f"background-color: {color[2]}; color: white;"
style_leste = f"background-color: {color[3]}; color: white;"
style_sul = f"background-color: {color[4]}; color: white;"

# Column 1 with 5 sub columns for each region
with col_main1:
    col_mainsub1, col_mainsub2, col_mainsub3, col_mainsub4, col_mainsub5 = st.columns(5)
    with col_mainsub1: # Create a styled colored block for each city region
        st.markdown('.')
        st.markdown(f'<div style="{style_norte}">'
            f'<p style="font-size: 24px; font-weight: bold; margin: 0; text-align: center">{city_region[0]}</p>'
            f'<p style="font-size: 48px; font-weight: bold; margin: 0; text-align: center; line-height: 1">{traffic_jam[0]} Km</p>'
            f'<p style="font-size: 18px; margin: 0; text-align: center">de lentidão</p>'
            '</div>', unsafe_allow_html=True)
    with col_mainsub2:
        st.markdown('.')
        st.markdown(f'<div style="{style_oeste}">'
            f'<p style="font-size: 24px; font-weight: bold; margin: 0; text-align: center">{city_region[1]}</p>'
            f'<p style="font-size: 48px; font-weight: bold; margin: 0; text-align: center; line-height: 1">{traffic_jam[1]} Km</p>'
            f'<p style="font-size: 18px; margin: 0; text-align: center">de lentidão</p>'
            '</div>', unsafe_allow_html=True)
    with col_mainsub3:
        st.markdown('.')
        st.markdown(f'<div style="{style_centro}">'
            f'<p style="font-size: 24px; font-weight: bold; margin: 0; text-align: center">{city_region[2]}</p>'
            f'<p style="font-size: 48px; font-weight: bold; margin: 0; text-align: center; line-height: 1">{traffic_jam[2]} Km</p>'
            f'<p style="font-size: 18px; margin: 0; text-align: center">de lentidão</p>'
            '</div>', unsafe_allow_html=True)
    with col_mainsub4:
        st.markdown('.')
        st.markdown(f'<div style="{style_leste}">'
            f'<p style="font-size: 24px; font-weight: bold; margin: 0; text-align: center">{city_region[3]}</p>'
            f'<p style="font-size: 48px; font-weight: bold; margin: 0; text-align: center; line-height: 1">{traffic_jam[3]} Km</p>'
            f'<p style="font-size: 18px; margin: 0; text-align: center">de lentidão</p>'
            '</div>', unsafe_allow_html=True)
    with col_mainsub5:
        st.markdown('.')
        st.markdown(f'<div style="{style_sul}">'
            f'<p style="font-size: 24px; font-weight: bold; margin: 0; text-align: center">{city_region[4]}</p>'
            f'<p style="font-size: 48px; font-weight: bold; margin: 0; text-align: center; line-height: 1">{traffic_jam[4]} Km</p>'
            f'<p style="font-size: 18px; margin: 0; text-align: center">de lentidão</p>'
            '</div>', unsafe_allow_html=True)


# Column 2 for the map of SP, calendar and time.
image = Image.open('SPcity.png')
min_date = datetime.strptime("2010-01-02", "%Y-%m-%d").date()

with col_main2:
    coltest1,coltest2 = st.columns([1,3])
    with coltest2:
        st.image(image)
    st.markdown('.')
    st.date_input('📅 Data', min_value = min_date)
    st.time_input('🕘 Horário',step= 1800)

