import streamlit as st
import pandas as pd
import numpy as np
import Functions.Modelisation as Model

st.title('SPIAKID Data Reduction System')


col1, col2, col3, col4 = st.columns([1, 0.5, 1, 1])

with col3:
    result_folder = st.text_input('Result folder',value="")

with col4:
    format = st.selectbox('Format', ['.jpg','.svg','.eps'])
with col1:
    data_location = st.text_input('Data Location',value="")
    Launch = st.button('OK')
    if Launch:
        Model.Data_read(data_location,result_folder,format)


