import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title='Energy Generation Predictor', layout='wide', page_icon='🔌')

if 'pressed_change_addr' not in st.session_state:
    st.session_state.pressed_change_addr = False
if 'loc_name' not in st.session_state:
    st.session_state.loc_name = 'São Paulo, SP'
if 'loc_lat' not in st.session_state:
    st.session_state.loc_lat = -23.55
if 'loc_lon' not in st.session_state:
    st.session_state.loc_lon = -46.64

st.header('🔌 Energy Generation Predictor')

with open('streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

col_main1, col_main2 = st.columns([3, 1])

with col_main1:
    col_mainsub1, col_mainsub2 = st.columns(2)
    with col_mainsub1:
        st.metric(label='Total Estimated Generated Energy', value=f'⚡ {18_240:,} kW/h')

    with col_mainsub2:
        st.metric(label='Estimated saving', value=f'💲 R$ {11_965.44:,.2f}')

    # st.line_chart(data=df, x='data', y='irrad kwh/m2')

with col_main2:
    # user inputs
    area = st.number_input('📐 Área total em m² dos painéis solares', step=5, min_value=2, value=18)
    rend = st.slider('💱 Eficiência média dos painéis solares', min_value=0, max_value=100, step=1, format='%d%%',
                     value=15)
    range_data = st.number_input('🗓️ Anos para previsão', min_value=1, max_value=20, step=1)

    col_desc_loc, col_alt_loc = st.columns(2)
    with col_desc_loc:
        st.markdown(f'📌 {st.session_state.loc_name}')
    with col_alt_loc:
        change_addr = st.button(label='Alterar', key='alt_loc')

    if change_addr or st.session_state.pressed_change_addr:
        st.session_state.pressed_change_addr = True
        loc_input = st.text_input('Digite a localização')
        if loc_input:
            st.session_state.pressed_change_addr = False
            try:
                geolocator = Nominatim(user_agent="draw2text2")
                location = geolocator.geocode(loc_input, addressdetails=True)
                new_loc_name = f"{location.raw['address']['city']}, {location.raw['address']['ISO3166-2-lvl4'][-2:]}"
            except BaseException:
                st.error('Could not find address')
            else:
                st.session_state.loc_name = new_loc_name
                st.session_state.loc_lat, st.session_state.loc_lon = float(location.raw['lat']), float(location.raw['lon'])
                st.experimental_rerun()

    m = folium.Map(location=[st.session_state.loc_lat, st.session_state.loc_lon],
                   zoom_start=10,
                   zoom_control=False,
                   scrollWheelZoom=False,
                   dragging=False)
    folium.Marker(
        [st.session_state.loc_lat, st.session_state.loc_lon]
    ).add_to(m)
    st_folium(m, height=100, width=None)


#######################App###################################
# st.dataframe(df)

# # calc_energy
# calc_energy = df['irrad kwh/m2'].sum() * area * rend / 100
# st.write(f'A energia gerada para os próximos {range_data} anos é', round(calc_energy, 2), 'kwh')
