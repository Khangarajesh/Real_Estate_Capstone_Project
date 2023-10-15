import streamlit as st
import pandas as pd
import numpy as np
import pickle

import os
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="Price Prediction")
st.title("Price Prediction")

#df = pd.read_pickle("df.pkl")
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)
#st.dataframe(df)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)
st.header("Enter Your Input")

#property type
prop_type = st.selectbox('Property Type',['flat', 'house'])
#built_up_area
built_up_area = st.number_input('Built Up Area')
#sector
sector = st.selectbox('Sector', sorted(np.unique(df['sector'])))
#Bedrroms
bedroom = float(st.selectbox('Number of Bedrooms', sorted(np.unique(df['bedRoom']))))
#Bathrooms
bathroom = float(st.selectbox('Number of Bathrooms', sorted(np.unique(df['bathroom']))))
#Balcony
balcony = st.selectbox('Number of Balconies', sorted(np.unique(df['balcony'])))
#property_age
propert_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))
#servent_room
servent_room = st.selectbox('Servent Room', np.unique(df['servant room']))
#store_room
store_room = st.selectbox('Store Room', np.unique(df['store room']))
#furnishing_type
furnishing_type = st.selectbox('Furnishing Type', sorted(np.unique(df['furnishing_type'])))
#luxary_category
luxary_category = st.selectbox('Luxary Category', sorted(np.unique(df['luxury_category'])))
#floor_category
floor_category = st.selectbox('Floor Category', sorted(np.unique(df['floor_category'])))

if st.button('Predict'):
    data =[[prop_type, built_up_area, sector, bedroom, bathroom, balcony, propert_age, servent_room, store_room, furnishing_type, luxary_category, floor_category]]
    columns = ['property_type', 'built_up_area', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']
    one_df = pd.DataFrame(data , columns = columns)

    #st.dataframe(one_df)
    base_price = np.expm1(pipeline.predict(one_df))[0]
    st.write(f"The price of the {prop_type} wil be between {round(base_price - 0.22, 2)} Cr to {round(base_price + 0.22, 2)} Cr")
