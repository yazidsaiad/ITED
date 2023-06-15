import pandas as pd
import base64
import pickle
import uuid
import re
import streamlit as st
import os
import json



def material_series_init():

    df_couples = pd.read_excel(r"C:\Users\PYSD10221\data_management\fichiers de travail\Séries Matérielles\Fichier entrant pour patron de rame à la série matériel.xlsx", 
                                sheet_name = "Couple des codes roulements")

    df_material_series = pd.read_excel(r"C:\Users\PYSD10221\data_management\fichiers de travail\Séries Matérielles\Fichier entrant pour patron de rame à la série matériel.xlsx", 
                                        sheet_name = "Série associé aux codes rouleme").set_index("Code roulement").transpose()
    
    return df_couples, df_material_series

@st.cache_data

def material_series_creation(df_couples : pd.DataFrame, df_material_series : pd.DataFrame):

    dict_material_series = dict()

    for code in df_material_series.columns:
        dict_material_series[str(code)] = list(df_material_series[code].dropna())

    couples_roulement = [couple.split('-') for couple in df_couples['Patron']]

    dict_output = dict()

    for k in range(0,len(couples_roulement)):

        if len(couples_roulement[k]) == 1:
            dict_output[df_couples['Patron'].loc[k]] = list(df_material_series[df_couples['Patron'].loc[k]].dropna())
            
        if len(couples_roulement[k]) == 2:
            serie = []
            for i in range(0,len(dict_material_series[couples_roulement[k][0]])):
                
                for j in range(0, len(dict_material_series[couples_roulement[k][1]])):
                    serie.append(dict_material_series[couples_roulement[k][0]][i] + '-' + dict_material_series[couples_roulement[k][1]][j])

            dict_output[df_couples['Patron'].loc[k]] = serie
        
    for key in list(dict_output.keys()):
        seen = set()
        uniq = [x for x in dict_output[key] if x not in seen and not seen.add(x)]
        dict_output[key] = uniq

    df__ = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dict_output.items() ]))

    # calculation of total length of material series
    length = 0
    for couple in list(df_couples['Patron'])[0:3]:
        for serie in dict_output[couple]:
            for single in str(serie).split(sep='-'):
                length += 1

    return df__, dict_output, length
    
@st.cache_data

def material_series_string_generation(df_couples : pd.DataFrame, dict_output : dict):
    
    s = str()
    for couple in list(df_couples['Patron']):
        for serie in dict_output[couple]:
            s += (f"consist_pattern;{serie};\n")
            for single in str(serie).split(sep='-'):
                s += (f"consist_pattern_unit;{single};\n")
    return s
    

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'



def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.

    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')

    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download, indent=0)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link

    

def material_series_generation(df_couples : pd.DataFrame, dict_output : dict, CP :str):

    path = r'C:\Users\{id}\Downloads\couples codes rames traduits en séries matérielles.txt'.format(id = CP)
    with open(path, 'w+') as f:
        for couple in list(df_couples['Patron']):
            for serie in dict_output[couple]:
                    f.write("consist_pattern")
                    f.write(";")
                    f.write(serie)
                    f.write(";")
                    f.write('\n')
                    
                    for single in str(serie).split(sep='-'):
                        f.write("consist_pattern_unit")
                        f.write(";")
                        f.write(single)
                        f.write('\n')

        s = f.readlines()
    return s

        




    