import streamlit as st
import pandas as pd
import utils
# from datetime import datetime
# import os


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
    st.markdown("<h1 style='text-align: center; color: black; font-size : 25px;'>Génération des Séries Matérielles</h1>", unsafe_allow_html=True)    
    st.divider()

    files = st.file_uploader(label="Veuillez sélectionner le fichier des couples de codes roulements et séries associées")
    df_couples = pd.DataFrame()
    df_material_series = pd.DataFrame()
    if files is not None:
        df_couples = pd.read_excel(files, sheet_name = "Couple des codes roulements")
        df_material_series = pd.read_excel(files, sheet_name = "Série associé aux codes rouleme").set_index("Code roulement").transpose()

    st.divider()
   
    if  df_couples.empty or df_material_series.empty:
        st.warning("Veuillez importer le fichier des codes roulements et séries associées")
    else:
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Fichiers d'entrées</h1>", unsafe_allow_html=True)
        col1_, col2_ = st.columns([0.2, 0.8])
        with col1_:
            st.dataframe(df_couples)
        with col2_:
            st.dataframe(df_material_series)
        st.divider()
        
        st.info('Génération du fichier en cours...')
        CP = st.text_input('Veuillez entrer votre CP')
        if CP:
            df__ , dict_output, _ = utils.material_series_creation(df_couples=df_couples, df_material_series=df_material_series)
            #material_series_string = utils.material_series_string_generation(df_couples=df_couples, dict_output=dict_output)
            utils.material_series_generation(df_couples=df_couples, dict_output=dict_output, CP=CP)
            st.success('Génération terminée.')
            st.divider()
            st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Tableau des séries matérielles</h1>", unsafe_allow_html=True)
            st.dataframe(df__)
    
    st.divider()


    '''
    if st.button('Télécharger le fichier généré :'):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        tmp_download_link = utils.download_button(material_series_string, 'couples codes rames traduits en séries matérielles_' + dt_string + '.txt', 'Cliquez ici pour télécharger le fichier!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
    
    '''
