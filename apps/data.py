import streamlit as st
import numpy as np
import pandas as pd
#from data.create_data import create_table

def app():
    st.write("Data")
    st.title('WHERE DO YOU OPEN A NEW FRANCHISE?')

    st.write("The data for this work is obtained from Yelp\'s API:https://api.yelp.com/v3/businesses/search")
    st.write("For this project, NYC (minus Staten Island) is considered as the city of interest.")
    st.write("The city is divided into hexagons using the h3 library of ~0.5 miles width (size 9). A total of 6000 hexagons were used! All food places in the city are categorized into these hexagons.  ")
    st.write("A total of 120,000 places were extracted from Yelp for New York City!!")

    df1=pd.read_csv('cleanedYelpDataframe.csv')
    st.write('A sample of the dataset is as follows:')
    st.dataframe(df1.head())
    st.write('')
    st.write('The top 100 franchises in the city are:')
    df_100=pd.DataFrame(df1['name'].value_counts()[:100])
    df_100.columns=['Number']
    st.dataframe(df_100)

    st.write('')
    st.write('It looks like the list includes Coffee or Tea shops, restaurants, food franchises, bakeries, pharmacies etc..')

    st.write('We are interested in the location and category of each joint. Let\'s look at the top 100 categories')

    title1 = pd.read_csv('title1.csv')
    title1.columns = ['Category', 'Number']
    title1 = title1.set_index('Category')
    st.dataframe(title1[:100])
    st.write('')
    st.write('We will use the places that belong to the top 100 categories to make predictions on the category of the franchise of our choice')


    #st.markdown("### Plot Data")
    #df = create_table()

    #st.line_chart(df)