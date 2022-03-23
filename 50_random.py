from functools import partial
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def main():
    # Extracting all country codes for emerging countries
    countires_to_regions = pd.read_excel("data/CountriesToRegions.xlsx", sheet_name="Feuil1")
    em_country_codes_raw = list(countires_to_regions.loc[countires_to_regions["Unnamed: 4"] == "{'EM'}"]["function Corresp = CodetoName"])
    em_country_codes = [code[2:4] for code in em_country_codes_raw]

    # Extracting all ISINs from the emerging countires
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")
    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"].isin(em_country_codes)]
    isin_list = list(set(stocks_in_country["ISIN"].to_list()))

    # print(isin_list)

    # print("Before Gov filter ", len(isin_list))

    filtered_isin_with_gov = []
    gov_df = pd.read_excel("data/Gov.xlsx", sheet_name="Feuil1")
    all_isin_with_gov = gov_df.columns.values.tolist()
    
    for isin in all_isin_with_gov:
        if len(gov_df[isin].dropna()) > 0 and isin in isin_list:
            filtered_isin_with_gov.append(isin)

    df = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")
    df = df.dropna(axis='columns')

    returns_list = []
    for isin in filtered_isin_with_gov:
        try:
            returns_list.append((isin, df[isin][:24].sum()))
        except:
            continue
    
    returns_list.sort(key=lambda y: y[1])

    l = len(returns_list)//5
    returns_quintiles = [returns_list[0:l],
    returns_list[l:2*l],
    returns_list[2*l:3*l],
    returns_list[3*l:4*l],
    returns_list[4*l:],
    ]

    print('Results quin ', returns_quintiles)

    lowest_isins = []


    indexses = [10, 15, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 55, 60, 65, 70, 75, 80,85, 90, 95, 100, 110, 120, 130, 140, 150, 175, 200, 210, 225, 230, 240, 250, 260, 270, 275, 290, 300, 325, 350, 375, 400, 425, 450, 475, 500]

    print(len(indexses))
    for i in indexses:
        lowest_isins.append(returns_list[i][0])


    df = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")[lowest_isins]

    print(df.columns.to_list())

    df.to_excel("50_random.xlsx", index=True)

   
   

if __name__ == "__main__":
    main()