import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from branca.colormap import linear
import h3
import numpy as np

from multiapp import MultiApp
from apps import home, data, results

def app():
	multiapp = MultiApp()

	multiapp.add_app("Home", home.app)
	multiapp.add_app("Data Stats", data.app)
	multiapp.add_app("Results", results.app)

	multiapp.run()

	st.title("Where do you open a new Franchise?")
	st.title("Bubble tea store")

#code for hex centers
	df_hexcenters = pd.read_csv('hex-centers.csv')
	df_hexcenters = df_hexcenters.rename(columns={'Unnamed: 0': 'h3_loc'})
	df_hexcenters['h3_index'] = ''
	for i in range(len(df_hexcenters)):
		df_hexcenters['h3_index'][i] = h3.geo_to_h3(df_hexcenters['0'][i], df_hexcenters['1'][i], 9)

#with st.echo():
#Code for data with category1
	df_final1 = pd.read_csv('allentrieswCat1.csv')
	df_groupbyh3_cat1 = df_final1.groupby(['h3_loc'])['id'].agg('count').reset_index()
	df_h3allCat1 = df_groupbyh3_cat1.merge(df_hexcenters)
	df_h3allCat1 = df_h3allCat1.rename(columns={'id': 'count'})

#Code for false positives from ML model
	falsepos = [882.0, 584.0, 147.0, 706.0, 906.0]
	df_falsepos = pd.DataFrame()
	for i in falsepos:
		df_falsepos = pd.concat([df_falsepos, df_h3allCat1[df_h3allCat1['h3_loc'] == int(i)]])

#Code for coloring

	def colors(i, h3, falsepos):
		falseposint = list(map(int, falsepos))
		if h3 not in falseposint:
			colormap = linear.YlGn_09.scale(
				df_h3allCat1['count'].min(), 50 #df_h3allCat1['count'].max() #Anything above 50 has same color
			)
			return colormap(i)
		else:
			mark = 'red'
			return mark

	trial7 = folium.Map(location=[40.75034087457838, -73.98936233989697], zoom_start=12)

	def get_hexagon(h):
		geo_lst = list(h3.h3_to_geo_boundary(h))
		geo_lst.append(geo_lst[0])
		return np.array(geo_lst)

#Code for plotting
	tooltip = f"{df_falsepos['count']}"
	for i in range(len(df_h3allCat1)):
		hexagon = get_hexagon(df_h3allCat1['h3_index'].iloc[i])
		polygon = folium.vector_layers.Polygon(locations=hexagon, tooltip=df_h3allCat1['count'][i],
											   fill_color=str(
												   colors(df_h3allCat1['count'][i], df_h3allCat1['h3_loc'][i],
														  falsepos)),
											   # 'DeepPink3',#'##ffff87',#str(colormap(df_falsepos['count'].iloc[i])),
											   fill_opacity=0.7, weight=3, opacity=0.2
											   )
		polygon.add_to(trial7)
	folium_static(trial7)

if __name__ == '__main__':
	app()