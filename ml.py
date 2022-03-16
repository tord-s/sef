import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_annualized_return_and_variance(portfolio_monthly_returns):
    months = len(portfolio_monthly_returns)
    yearly_returns = []
    # Calculates yearly returns
    while months > 0:
        monthly_returns = portfolio_monthly_returns[max(0,months-12): months]
        yearly_return = 1
        for monthly_return in monthly_returns:
            yearly_return = yearly_return * (monthly_return)
        yearly_returns.append(yearly_return)
        months -= 12
    # Calculates annualized_average_return_in_percentage
    partial_calculation_1 = 1
    for yearly_return in yearly_returns:
        partial_calculation_1 = partial_calculation_1 * (1 + yearly_return)
    partial_calculation_2 = partial_calculation_1 ** (1/len(yearly_returns))
    annualized_average_return_in_percentage = ((partial_calculation_2 - 1) * 100) - 100
    # Calculates the volatility
    partial_calculation_inner_sum = 0
    for stock_movement in portfolio_monthly_returns:
        partial_calculation_inner_sum += (stock_movement - annualized_average_return_in_percentage*0.01) ** 2
    sigma = math.sqrt(partial_calculation_inner_sum / len(portfolio_monthly_returns))
    volatility = math.sqrt(12) * sigma
    return annualized_average_return_in_percentage, volatility



def plot_dict(return_volatility_dict):
    # Plot results in scatter plot
    x_array, y_array = np.array([]), np.array([]) 
    for value in return_volatility_dict.values():
        x, y = value[0], value[1]
        plt.plot(x, y, 'bo')
        x_array = np.append(x_array,[x])
        y_array = np.append(y_array,[y])
    z = np.polyfit(x_array, y_array, 1)
    p = np.poly1d(z)
    plt.xlabel('Annualized volatility')
    plt.ylabel('Annualized average return')
    plt.plot(x_array,p(x_array),"r--")
    print("Close diagram or press ctrl/cmd + c in terminal to quit program")
    plt.show()


def main():
    # Extracting all country codes for emerging countries
    countires_to_regions = pd.read_excel("data/CountriesToRegions.xlsx", sheet_name="Feuil1")
    em_country_codes_raw = list(countires_to_regions.loc[countires_to_regions["Unnamed: 4"] == "{'EM'}"]["function Corresp = CodetoName"])
    em_country_codes = [code[2:4] for code in em_country_codes_raw]

    # Extracting all ISINs from the emerging countires
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")
    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"].isin(em_country_codes)]
    isin_list = list(set(stocks_in_country["ISIN"].to_list()))

    # TODO: Filter on ones with governence score

    df = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1", index_col="Unnamed: 0")[isin_list]
    
    # Finding the equal weight each month based on number of firms each month
    nr_of_months = 228
    weights_each_month = []
    for month_nr in range(nr_of_months-1,-1,-1):
        stocks_this_month = 0
        for isin in isin_list:
            if len(df[isin].dropna()) > month_nr:
                stocks_this_month += 1
        weights_each_month.append(1 / stocks_this_month)
        
    portfolio_monthly_returns_equally_weighted = []
    for month_nr in range(nr_of_months):
        montly_return = 1
        for isin in isin_list:
            if len(df[isin].dropna()) > month_nr:
                try:
                    a = df[isin][month_nr] * weights_each_month[month_nr]
                    b = int(a)
                    montly_return += a
                except:
                    continue
        portfolio_monthly_returns_equally_weighted.append(montly_return)

    # Only get last 168 months because size.xlsx only has this data
    portfolio_monthly_returns_equally_weighted = portfolio_monthly_returns_equally_weighted[-168:]

    annualized_average_return_in_percentage_ew, volatility_ew = calculate_annualized_return_and_variance(portfolio_monthly_returns_equally_weighted)
    

    size_sheet = pd.read_excel("data/size.xlsx", sheet_name="Feuil1")
    total_market_value_each_month = size_sheet.sum(axis=1)

    portfolio_monthly_returns_value_weighted = []

    for month_nr in range(168):
        monthly_return = 1
        for isin in isin_list:
            try:
                weight = size_sheet[isin][month_nr] / total_market_value_each_month[month_nr]
                a = df[isin][month_nr] * weight
                b = int(a)
                monthly_return += a
            except:
                continue
        portfolio_monthly_returns_value_weighted.append(monthly_return)

    annualized_average_return_in_percentage_vw, volatility_vw = calculate_annualized_return_and_variance(portfolio_monthly_returns_value_weighted)

    print("Annualized average return value-weighted portfolio: ", annualized_average_return_in_percentage_vw)
    print("Annualized volatility value-weighted portfolio: ", volatility_vw)
    print("Annualized average return equally-weighted portfolio: ", annualized_average_return_in_percentage_ew)
    print("Annualized volatility equally-weighted portfolio: ", volatility_ew)


    # Plot results
    monthly_returns_in_percentage_equally_weighted = np.array(portfolio_monthly_returns_equally_weighted) * 100
    monthly_returns_in_percentage_value_weighted = np.array(portfolio_monthly_returns_value_weighted) * 100
    plt.plot(monthly_returns_in_percentage_equally_weighted, label='Equally weighted')
    plt.plot(monthly_returns_in_percentage_value_weighted, label='Value weighted')
    plt.xlabel('Annualized volatility')
    plt.ylabel('Annualized average return')
    plt.legend()
    plt.show()


    

if __name__ == "__main__":
    main()