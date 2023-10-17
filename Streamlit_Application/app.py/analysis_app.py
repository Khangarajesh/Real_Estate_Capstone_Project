import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.set_page_config(page_title="Analysis App")
st.title("Analysis")

new_df  = pd.read_csv("dataset/data_viz1.csv")
#st.dataframe(new_df)

#------------------------------------------------------------------Geomap---------------------------------------------------------------------------------------------
group_df = new_df.groupby('sector').mean()[['price_per_sqft', 'built_up_area', 'latitude', 'longitude']].reset_index()
st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name= 'sector')
st.plotly_chart(fig, use_container_width= True)


#------------------------------------------------------------------Wordcloud---------------------------------------------------------------------------------------------
st.header('Features Wordcloud')
sector_features = pd.read_csv("dataset/sector_features.csv")

sector = st.selectbox('Select sector to see mostly available features', sorted(np.unique(sector_features['sector'])))

filtered_sec = sector_features[sector_features['sector'] == sector]
list_feature = []

for fet in filtered_sec['features']:
  list_feature.extend(fet)

text = ''.join(list_feature)

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='black',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(text)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)


#------------------------------------------------------------------Area vs Price---------------------------------------------------------------------------------------------

st.header("Area vs Price")

prop_type = st.selectbox("Select Property Type", ['flat', 'house', 'overall'])

sector_options = list(np.unique(new_df['sector']))
sector_options.insert(0, 'overall')
sector_area = st.selectbox('Select sector', sector_options)

if sector_area == 'overall' and prop_type == 'overall':
    fig1 = px.scatter(new_df, x = "built_up_area", y = "price", color = 'bedRoom')
    st.plotly_chart(fig1, use_container_width=True)
elif sector_area == 'overall' and prop_type:
    fig1 = px.scatter(new_df[new_df['property_type'] == prop_type], x = "built_up_area", y = "price", color = 'bedRoom')
    st.plotly_chart(fig1, use_container_width=True)
elif sector_area != 'overall' and prop_type == 'overall':
    fig1 = px.scatter(new_df[new_df['sector'] == sector_area], x = "built_up_area", y = "price", color = 'bedRoom')
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[(new_df['property_type'] == prop_type) & (new_df['sector'] == sector_area)], x = "built_up_area", y = "price", color = 'bedRoom')
    st.plotly_chart(fig1, use_container_width=True)

#------------------------------------------------------------------BHK Distribution---------------------------------------------------------------------------------------------

st.header('BHK Distribution')
sector_options = list(np.unique(new_df['sector']))
sector_options.insert(0, 'Overall')
sector_area = st.selectbox('Select sector for bhk', sector_options)

if sector_area == 'Overall':
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, user_container_width = True)
else:
    fig2 = px.pie(new_df[new_df['sector']==sector_area], names='bedRoom')
    st.plotly_chart(fig2, user_container_width = True)

#------------------------------------------------------------------Side By Side BHK Comparison---------------------------------------------------------------------------------------------

st.header("Side By Side BHK Comparison")
fig3 = px.box(new_df[new_df['bedRoom']<=4], x = 'bedRoom', y = 'price')
st.plotly_chart(fig3, user_container_width = True)


st.header('Side by Side Distplot for property type')

fig4 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig4)