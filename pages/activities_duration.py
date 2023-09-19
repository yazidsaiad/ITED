import streamlit as st
import pandas as pd
import utils



def app():

    """
    This funtion generates the project features using streamlit library
    """

    # display images in separated columns
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        st.markdown("<h1 style='text-align: center; color: black; font-size : 25px;'>Interface de Traitement de l'Equipe Données</h1>", unsafe_allow_html=True)
    with col3 : 
        st.image('images/logo_sncf.png')
    with col1:
        st.image('images/logo-progres-simplifie.png')

    st.divider()
    st.markdown('<style>body{background-color: Grey;}</style>',unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black; font-size : 25px;'>Temps d'Activité de Véhicules</h1>", unsafe_allow_html=True)    
    st.divider()

    


