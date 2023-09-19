import pandas as pd
import streamlit as st
from io import BytesIO
import numpy as np



def isNaN(string):
    """
    This function checks if the keyword argument (string or float) type in nan.
    Returns True if keyword argument is nan and False if keyword argument is not nan.
    """
    return string != string


def flatten(l : list):
    """
    This function flattens a list of lists. 
    """
    return [item for sublist in l for item in sublist]


def series__init():
    """
    Cette fonction sert de test pour la mise en place du framework.
    Elle retourne deux dataframes :
    - df_couples qui est le dataframe des patrons de rames (ou couples de codes roulement);
    - df_material_series qui est le dataframe des séries matérielles associées aux codes roulement (1 code roulement = 1 lettre unitaire = 1 série matérielle)
    """

    df_couples = pd.read_excel(r"C:\Users\PYSD10221\data_management\Chantiers Données\Séries Matérielles\Fichier entrant pour patron de rame à la série matériel QSI.xlsx", 
                                sheet_name = "Couple des codes roulements")

    df_material_series = pd.read_excel(r"C:\Users\PYSD10221\data_management\Chantiers Données\Séries Matérielles\Fichier entrant pour patron de rame à la série matériel QSI.xlsx", 
                                        sheet_name = "Série associé aux codes rouleme").set_index("Code roulement").transpose()
    
    return df_couples, df_material_series


#@st.cache_data
def get__unit__series(codes_data : pd.DataFrame) -> dict:
    """
    Cette fonction prend en argument un dataframe comprenant les données des codes roulement.
    Le dataframe présente en première colonne les codes roulement unitaires et présente à partir 
    de la deuxième colonne la série matérielle associée au code unitaire.

    Ex : (format du df d'entrée)
        Col1 Col2 Col3 Col4
        A    A1   A2
        B    B1
        C    C1   C2    C3

    Cette fonction retourne un dictionnaire de toutes les séries matérielle.
    
    Ex : 
    {A : [A1, A2], B : [B1], C : [C1, C2, C3]}
    """
    keys = list(codes_data.iloc[:,0])
    values = [[x for x in list(codes_data.T.iloc[1:,k]) if x == x] for k in range(0,len(codes_data))]

    return dict(zip(keys, values))

    
#@st.cache_data
def get__multiple__series(couple : str, unit_series : dict) -> list:
    """
    Cette fonction permet d'associer à un patron de rame (ie couple de codes roulement)
    sa série matérielle. 
    Les régles de combinatoires sont les suivantes :
        si X et Y sont deux codes roulement tels que 
        X = (X1, ..., Xn) et Y = (Y1, ..., Yp)
        alors la série matérielle associée à X-Y est donnée par:
        X1-Y1, X1-Y2, ..., X1-Yp, X2-Y1, X2-Y2, ..., X2-Yp, ... ...,Xn-Y1, Xn-Y2,... Xn-Yp
    Elle renvoie la liste des éléments de la série matérielle correspondant au couple d'entrée.
    """
    if isNaN(couple):
        return np.nan
    
    else:
        if len(str(couple).split('-')) < 2:
            if couple not in list(unit_series.keys()):
                return couple
            else:
                return " ".join([str(item) for item in unit_series[couple]])
        
        elif len(couple.split('-')) == 2:
            X = couple.split('-')[0]
            Y = couple.split('-')[1]

            return " ".join([str(item) for item in flatten([["{x}-{y}".format(y=y, x=x) for y in unit_series[Y]] for x in unit_series[X]])])



def data__filling(data : pd.DataFrame, unit_series : dict) -> pd.DataFrame:
    """
    Cette fonction prend en argument un tableau pandas et renvoie le même tableau avec les séries matérielles
    associés aux codes roulements et patrons de rames présents sur les colonnes 2, 3 et 4.
    N.B. : Une fonctionnalité intéressante serait de pouvoir choisir manuellement au niveau de l'interface
    les colonnes à traduire.
    """
    df_to_fill = data.copy()

    for col in data.columns[1:4]:
        df_to_fill[col] = [get__multiple__series(couple=code, unit_series=unit_series)\
                              for code in list(data[col])]
    
    return df_to_fill


#@st.cache_data
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
    

#@st.cache_data
def series__to__string(df_couples : pd.DataFrame, dict_output : dict):
    
    s = str()
    for couple in list(df_couples['Patron']):
        for serie in dict_output[couple]:
            s += (f"consist_pattern;{serie};\n")
            for single in str(serie).split(sep='-'):
                s += (f"consist_pattern_unit;{single}\n")
    return s


def series__to__string__v2(df_couples : pd.DataFrame, dict_output : dict, CP :str):

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


def to_excel(df: pd.DataFrame):
    """
    This function converts a pandas dataframe to an excel file.

    Keyword argument : pandas dataframe.
    """
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()

    




    