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
        df__ , dict_output, _ = utils.material_series_creation(df_couples=df_couples, df_material_series=df_material_series)
        material_series_string = utils.material_series_string_generation(df_couples=df_couples, dict_output=dict_output)
        st.success('Génération terminée.')
        st.divider()
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Tableau des séries matérielles</h1>", unsafe_allow_html=True)
        st.dataframe(df__)
        df_to_save = utils.to_excel(df__)
        st.download_button(label="📥 Télécharger le fichier généré en format excel", data=df_to_save, file_name='couples codes rames traduits en séries matérielles.xlsx')
        st.divider()
        st.markdown("<h1 style='text-align: center; color: black; font-size : 20px;'>Téléchargement du fichier généré</h1>", unsafe_allow_html=True)
        st.download_button('📥 Télécharger en format .txt', material_series_string, file_name='couples codes rames traduits en séries matérielles.txt')

    st.divider()

    
    
