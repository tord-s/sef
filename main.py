from functools import partial
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def get_relevant_isins_and_montly_returns():
    # Extracting all country codes for emerging countries
    countires_to_regions = pd.read_excel("data/CountriesToRegions.xlsx", sheet_name="Feuil1")
    em_country_codes_raw = list(countires_to_regions.loc[countires_to_regions["Unnamed: 4"] == "{'EM'}"]["function Corresp = CodetoName"])
    em_country_codes = [code[2:4] for code in em_country_codes_raw]

    # Extracting all ISINs from the emerging countires
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")
    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"].isin(em_country_codes)]
    isin_list = list(set(stocks_in_country["ISIN"].to_list()))

    # TODO: Filter on ones with governence score
    
    monthly_returns_dataframe = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")

    # Removes items without data
    stocks_without_data = []
    for isin in isin_list:
        stock_movements = monthly_returns_dataframe[isin].dropna()
        if len(stock_movements) == 0:
            stocks_without_data.append(isin)
    for stock in stocks_without_data:
        isin_list.remove(stock)
    print('# of firms used: ', len(isin_list))
    
    return isin_list, monthly_returns_dataframe

def plot_dict(return_volatility_dict):
    # Plot results in scatter plot
    x_array, y_array = np.array([]), np.array([]) 
    for value in return_volatility_dict.values():
        x, y = value[0], value[1]
        plt.plot(x, y, 'bo', ms=0.5)
        x_array = np.append(x_array,[x])
        y_array = np.append(y_array,[y])
    z = np.polyfit(x_array, y_array, 1)
    p = np.poly1d(z)
    plt.xlabel('Annualized volatility')
    plt.ylabel('Annualized average return')
    plt.plot(x_array,p(x_array),"r--")
    print("Close diagram or press ctrl/cmd + c in terminal to quit program")
    plt.show()


def plot_dict_task7(return_volatility_dict):
    # To plot size against return and volatility
    size_sheet = pd.read_excel("data/size.xlsx", sheet_name="Feuil1")
    dict_with_size = {}
    intersect = list(set(size_sheet.columns.to_list()) & set(return_volatility_dict.keys()))
    for isin in intersect:
        try:
            a = size_sheet[isin].mean()
            b = int(a)
            c = return_volatility_dict[isin]
            dict_with_size[isin] = c + (a,)
        except:
            continue
    x_array, y_array, z_array = np.array([]), np.array([]), np.array([])
    for value in dict_with_size.values():
        print(value)
        x, y, z = value[0], value[1], value[2]
        # plt.plot(x, y, 'bo', ms=0.5)
        x_array = np.append(x_array,[x])
        y_array = np.append(y_array,[y])
        z_array = np.append(y_array,[y])
    # z = np.polyfit(x_array, y_array, 1)
    # p = np.poly1d(z)
    plt.xlabel('Annualized volatility')
    plt.ylabel('Annualized average return')


    plt.scatter(x_array, y_array, s=200, c=z_array[:-1], cmap='gray')
    print("Close diagram or press ctrl/cmd + c in terminal to quit program")
    plt.show()


    

def get_return_and_volatility(isin_list, monthly_returns_dataframe):
    return_volatility_dict = {}
    # Calculating annualized average return and volatility
    for isin in isin_list:
        stock_movements = monthly_returns_dataframe[isin].dropna()
        months = len(stock_movements)
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
        if len(monthly_returns) > 0:
            partial_calculation_1 = 1
            for monthly_return in monthly_returns:
                partial_calculation_1 = partial_calculation_1 * (1 + monthly_return)
            partial_calculation_2 = partial_calculation_1 ** (1/len(monthly_returns))
            annualized_average_return_in_percentage = ((partial_calculation_2 - 1) * 100) - 100

        # Calculates the volatility
        partial_calculation_inner_sum = 0
        for stock_movement in yearly_returns:
            partial_calculation_inner_sum += (stock_movement - annualized_average_return_in_percentage*0.01) ** 2
        sigma = math.sqrt(partial_calculation_inner_sum / len(yearly_returns))
        volatility = math.sqrt(12) * sigma

        return_volatility_dict[isin] =  (volatility, annualized_average_return_in_percentage)

    return return_volatility_dict

def task_1():
    isin_list, monthly_returns_dataframe = get_relevant_isins_and_montly_returns()
    return_volatility_dict = get_return_and_volatility(isin_list, monthly_returns_dataframe)
    # Remove huge outliers
    outliers = []
    best_stock = ('', 0)
    for key, value in return_volatility_dict.items():
        if value[0] > 50:
            outliers.append(key)
        elif value[1] > 150:
            outliers.append(key)
        else:
            if value[1] > best_stock[1] and len(monthly_returns_dataframe[key].dropna()) > 227:
                best_stock = (key, value[1])
    for outlier in outliers:
        return_volatility_dict.pop(outlier)
    print('Best stock: ', best_stock)
    print("Removed huge outliers: ", outliers)
    # print("Martinus stock", return_volatility_dict["AEA000201011"])
    # print("Martinus stock", return_volatility_dict["AEA001501013"])
    
    plot_dict(return_volatility_dict)
  

# def task_2():
#     isin_list, monthly_returns_dataframe = get_relevant_isins_and_montly_returns()
#     # Equaly weighted
#     max_months = 0
#     weight_dict = {}
#     for isin in isin_list:
#         length = len(monthly_returns_dataframe[isin].dropna())
#         if length > max_months:
#             max_months = length
#     for isin in isin_list:
#         weight_dict[isin] = [0] * max_months
#     month_weight_dict = {}
#     for month_nr in range(max_months):
#         nr_of_stocks_with_data_for_month = 0
#         for isin in isin_list:
#             if (len(monthly_returns_dataframe[isin].dropna())-1) >= month_nr:
#                 nr_of_stocks_with_data_for_month += 1
#         month_weight_dict[month_nr] = (1 / nr_of_stocks_with_data_for_month)
#     for month_nr in range(max_months):
#         for isin in isin_list:
#             if (len(monthly_returns_dataframe[isin].dropna())-1) >= month_nr:
#                 weight_dict[isin][month_nr] = month_weight_dict[month_nr]
                
#     # Calculate returns and volatility
#     portfolio_montly_returns = []
#     stock_returns = monthly_returns_dataframe[isin].dropna()
#     for month_nr in range(max_months):
#         montly_return = 1
#         for isin in isin_list:
#             if weight_dict[isin][month_nr] != 0:
#                 montly_return += stock_returns[month_nr] * weight_dict[isin][month_nr]
#         portfolio_montly_returns.append(montly_return)
 
#     # Calculates yearly returns
#     yearly_returns = []
#     month_index = max_months
#     while month_index > 0:
#         monthly_returns = portfolio_montly_returns[max(0,month_index-12): month_index]
#         yearly_return = 1
#         for monthly_return in monthly_returns:
#             yearly_return = yearly_return * (monthly_return)
#         yearly_returns.append(yearly_return)
#         month_index -= 12
#     partial_calculation_1 = 1
#     for yearly_return in yearly_returns:
#         partial_calculation_1 = partial_calculation_1 * (1 + yearly_return)
#     partial_calculation_2 = partial_calculation_1 ** (1/len(yearly_returns))
#     annualized_average_return_in_percentage = ((partial_calculation_2 - 1) * 100) - 100
#     print("Annualized average return: ", annualized_average_return_in_percentage)
#     # Calculates the volatility
#     partial_calculation_inner_sum = 0
#     for stock_movement in portfolio_montly_returns:
#         partial_calculation_inner_sum += (stock_movement - annualized_average_return_in_percentage*0.01) ** 2
#     sigma = math.sqrt(partial_calculation_inner_sum / len(portfolio_montly_returns))
#     volatility = math.sqrt(12) * sigma
#     print("Annualized volatility: ", volatility)

#     # Plot results in scatter plot
#     monthly_returns_in_percentage = np.array(portfolio_montly_returns) * 100
#     plt.plot(monthly_returns_in_percentage)
#     plt.show()

        
    

if __name__ == "__main__":
    task_1()
    # task_2()