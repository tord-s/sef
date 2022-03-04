import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_test():

    # Extracting all country codes for emerging countries
    countires_to_regions = pd.read_excel("data/CountriesToRegions.xlsx", sheet_name="Feuil1")
    em_country_codes_raw = list(countires_to_regions.loc[countires_to_regions["Unnamed: 4"] == "{'EM'}"]["function Corresp = CodetoName"])
    em_country_codes = [code[2:4] for code in em_country_codes_raw]

    # Extracting all ISINs from the emerging countires
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")
    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"].isin(em_country_codes)]
    isin_list = set(stocks_in_country["ISIN"].to_list())
    
    stocks_with_return_and_variance_dict = {}
    monthly_returns_dataframe = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")

    # Attempting to calculate mean and variance - the calculations are probably wrong atm
    for isin in isin_list:
        earnings = 0
        variance = 0
        n = len(isin_list)
        stock_movements = monthly_returns_dataframe[isin]
        for i in range(len(stock_movements)):
            earnings += stock_movements[i]
            variance += stock_movements[i]**2
        stocks_with_return_and_variance_dict[isin] = (earnings, (variance / (n-1)))

    # Remove huge outlier
    stocks_with_return_and_variance_dict.pop('TH0168A10Z01')

    # Plot results in scatter plot
    for value in stocks_with_return_and_variance_dict.values():
        x, y = value[0], value[1]
        plt.plot(x, y, 'bo')
    plt.show()

if __name__ == "__main__":
    read_test()