import streamlit as st
import numpy as np
import pandas as pd
#from data.create_data import create_table

def app():
    st.write("Summary")
    #st.title('WHERE DO YOU OPEN A NEW FRANCHISE?')

    st.markdown("## The advantages of using this app are:")
    st.markdown("* It can be generalized to other cities")
    st.markdown("* It can be used for food franchises, gyms, drugstores, food trucks, luxury good stores etc.")
    st.markdown("* It can help gain non-intuitive insights about the relation between the occurence of stores")
    st.markdown("* It inherently captures the effects of demography, logistics, activity based on existing stores")
    st.markdown("* It can be used to identify lower rent or upcoming neighbourhoods based on franchises opening or closing in the area")
