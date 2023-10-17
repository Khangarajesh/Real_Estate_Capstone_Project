import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommendetion")
st.title("Recommendetion Module")

with open('location_df.pkl', 'rb') as f:
    location_df = pickle.load(f)

#st.dataframe(location_df)

st.header('Recommendation based on selected location and distance')
location = st.selectbox('Select the location', sorted(list(location_df.columns)))
range = st.number_input('Enter the distance range in Kms')

st.dataframe(round(location_df[location_df[location] <= round(range*1000)][location].sort_values()/1000,2))

st.header("Recommendetion based on simillarity of selected property")

with open('cosine_sim_1.pkl', 'rb') as file:
    cosine_sim_1 = pickle.load(file)

with open('cosine_sim_2.pkl', 'rb') as file:
    cosine_sim_2 = pickle.load(file)

with open('cosine_sim_3.pkl', 'rb') as file:
    cosine_sim_3 = pickle.load(file)

with open('df.pkl', 'rb') as file:
    df = pickle.load(file)
property_name = st.selectbox('Select Property', sorted(list(location_df.index)))

df = location_df.reset_index().rename(columns = {'index' : 'PropertyName'})


def recommend_properties_with_score(prop_name):

  cos_sim = (3*cosine_sim_1+ 20*cosine_sim_2 + cosine_sim_3)
  idx = df[df['PropertyName'] == prop_name].index[0]

  sim_score = sorted(list(enumerate(cos_sim[idx])), key = lambda x : x[1], reverse = True)

  prop_name = [df['PropertyName'].iloc[[indx]].values[0] for indx, score in sim_score[:6]]
  score = [score for indx, score in sim_score[:6]]

  recommendations_df = pd.DataFrame(
      {
          "PropertyName": prop_name,
          "score": score
      }
  )

  return recommendations_df.sort_values(by = 'score', ascending = False)

st.dataframe(recommend_properties_with_score(property_name))