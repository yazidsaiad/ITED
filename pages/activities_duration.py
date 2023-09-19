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

    files_data_source = st.file_uploader(label="Veuillez sélectionner le fichier des couples de codes roulements et séries associées")
    files_data_prod = st.file_uploader(label="Veuillez sélectionner le fichier des temps d'activité de véhicule")
    
    df_prod = pd.DataFrame()
    df_material_series = pd.DataFrame()

    if files_data_source is not None:
        df_material_series = pd.read_excel(files_data_source, sheet_name = "Série associé aux codes rouleme").set_index("Code roulement").transpose()
    if files_data_prod is not None:
        df_prod = pd.read_excel(files_data_prod)

    st.divider()
   
    if  df_prod.empty or df_material_series.empty:
        st.warning("Veuillez importer les fichiers d'entrées.")
    else:
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Fichier d'entrée - Séries matérielles</h1>", unsafe_allow_html=True)
        st.dataframe(df_material_series)
    
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Fichier d'entrée - Temps d'activité</h1>", unsafe_allow_html=True)
        st.dataframe(df_prod)
        st.divider()

        st.info('Génération du fichier en cours...')
        df_output = utils.data__filling(data=df_prod, unit_series=utils.get__unit__series(codes_data=df_material_series.T.reset_index()))
        st.success('Génération terminée.')
        st.divider()
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Tableau des temps d'activité</h1>", unsafe_allow_html=True)
        st.dataframe(df_output)
        st.divider()

