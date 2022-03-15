from functools import partial
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def read_test():

    # Extracting all country codes for emerging countries
    countires_to_regions = pd.read_excel("data/CountriesToRegions.xlsx", sheet_name="Feuil1")
    em_country_codes_raw = list(countires_to_regions.loc[countires_to_regions["Unnamed: 4"] == "{'EM'}"]["function Corresp = CodetoName"])
    em_country_codes = [code[2:4] for code in em_country_codes_raw]

    # Extracting all ISINs from the emerging countires
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")
    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"].isin(em_country_codes)]
    isin_list = list(set(stocks_in_country["ISIN"].to_list()))

    # TODO: Filter on ones with governence score
    
    return_volatility_dict = {}
    monthly_returns_dataframe = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")


    
    # Calculating annualized average return and volatility
    for isin in isin_list:
        stock_movements = monthly_returns_dataframe[isin].dropna()
        months = len(stock_movements)
        # Removes items without data
        if months == 0:
            continue
        yearly_returns = []
        # Calculates yearly returns
        while months > 0:
            monthly_returns = stock_movements.iloc[max(0,months-12): months]
            yearly_return = 1
            for monthly_return in monthly_returns:
                yearly_return = yearly_return * (1+monthly_return)
            yearly_returns.append(yearly_return)
            months -= 12
        # Calculates annualized_average_return_in_percentage
        if len(yearly_returns) > 0:
            partial_calculation_1 = 1
            for yearly_return in yearly_returns:
                partial_calculation_1 = partial_calculation_1 * (1 + yearly_return)
            partial_calculation_2 = partial_calculation_1 ** (1/len(yearly_returns))
            annualized_average_return_in_percentage = ((partial_calculation_2 - 1) * 100) - 100

        # Calculates the volatility
        partial_calculation_inner_sum = 0
        for stock_movement in stock_movements:
            partial_calculation_inner_sum += (stock_movement - annualized_average_return_in_percentage*0.01) ** 2
        sigma = math.sqrt(partial_calculation_inner_sum / len(stock_movements))
        volatility = math.sqrt(12) * sigma

        return_volatility_dict[isin] =  (volatility, annualized_average_return_in_percentage)

    # Remove huge outliers
    outliers = []
    for key, value in return_volatility_dict.items():
        if value[0] > 50:
            outliers.append(key)
    for outlier in outliers:
        return_volatility_dict.pop(outlier)
    print("Removed huge outliers: ", outliers)

    # Plot results in scatter plot
    x_array, y_array = np.array([]), np.array([]) 
    for value in return_volatility_dict.values():
        x, y = value[0], value[1]
        plt.plot(x, y, 'bo')
        x_array = np.append(x_array,[x])
        y_array = np.append(y_array,[y])
    z = np.polyfit(x_array, y_array, 1)
    p = np.poly1d(z)
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.plot(x_array,p(x_array),"r--")
    print("Close diagram or press ctrl/cmd + c in terminal to quit program")
    plt.show()

    

if __name__ == "__main__":
    read_test()