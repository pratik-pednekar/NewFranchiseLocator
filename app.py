import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from branca.colormap import linear
import h3
import numpy as np

from multiapp import MultiApp
from apps import home, data, ML, results, summary


def app():
	st.title('New Franchise Locator')
	multiapp = MultiApp()

	#st.title("Where do you open a new Franchise?")
	#st.title("Bubble tea store")

	multiapp.add_app("Home", home.app)
	multiapp.add_app("Data Analysis", data.app)
	multiapp.add_app("Machine Learning", ML.app)
	multiapp.add_app("Results", results.app)
	multiapp.add_app("Summary", summary.app)

	multiapp.run()

if __name__ == '__main__':
	app()