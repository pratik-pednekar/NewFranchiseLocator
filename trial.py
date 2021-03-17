import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from branca.colormap import linear
import h3
import numpy as np

from multiapp import MultiApp
from apps import home, data, results

def df_trial():
	df_100 = pd.DataFrame(df1['name'].value_counts()[:100])
	df_100.columns = ['Number']
	return df_100