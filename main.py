import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import warnings
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

from codebase.dashboard_graphs import MaternalHealthDashboard

maternal_model = pickle.load(open("model/finalized_maternal_model.sav",'rb'))

# sidebar for navigation
with st.sidebar:
    st.title("E-Doctor System")
    st.write("Welcome to the E-Doctor Multiple Disease Prediction System. "
             "Choose an option from the menu below to get started.")

    selected = option_menu('E- Doctor Multiple Disease Prediction System',
                          
                          ['Pregnancy Risk Prediction',
                           'Dashboard',
                           'Chat bot'],
                          icons=['activity','heart','person'],
                          default_index=0)
    
if (selected == 'Pregnancy Risk Prediction'):
    
    # page title
    st.title('Pregnancy Risk Prediction')
    
    
    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.text_input('Age of the Person', key = "age")
        
    with col2:
        diastolicBP = st.text_input('diastolicBP in mmHg')
    
    with col3:
        BS = st.text_input('Blood glucose in mmol/L')
    
    with col1:
        bodyTemp = st.text_input('Body Temperature in Celsius')

    with col2:
        heartRate = st.text_input('Heart rate in beats per minute')
    
    riskLevel=""
    predicted_risk = [0] 
    # creating a button for Prediction
    with col1:
        if st.button('Predict Pregnancy Risk'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                predicted_risk = maternal_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
            # st
            st.subheader("Risk Level:")
            if predicted_risk[0] == 0:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: green;">Low Risk</p></bold>', unsafe_allow_html=True)
            elif predicted_risk[0] == 1:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></Bold>', unsafe_allow_html=True)
            else:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: red;">High Risk</p><bold>', unsafe_allow_html=True)
    with col2:
        if st.button("Clear"): 
            st.rerun()


 

if (selected == "Dashboard"):
    api_key = "579b464db66ec23bdd00000139b0d95a6ee4441c5f37eeae13f3a0b2"
    api_endpoint = api_endpoint= f"https://api.data.gov.in/resource/6d6a373a-4529-43e0-9cff-f39aa8aa5957?api-key={api_key}&format=csv"
    dashboard = MaternalHealthDashboard(api_endpoint)

    dashboard.create_bubble_chart()
    with st.expander("Show More"):
    # Display a portion of the data
        content = dashboard.get_bubble_chart_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)

    dashboard.create_pie_chart()
    with st.expander("Show More"):
    # Display a portion of the data
        content = dashboard.get_pie_graph_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)


