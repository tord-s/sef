import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_annualized_return(portfolio_monthly_returns):
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
    annualized_average_return_in_percentage = (partial_calculation_2 - 1)
    return annualized_average_return_in_percentage - 1

def get_min_and_max_return(portfolio_monthly_returns):
    sorted_returns = sorted(portfolio_monthly_returns)
    return sorted_returns[0], sorted_returns[-1]

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

"""
def make_value_and_equal_weighted(isin_list, weights_each_month):
    df = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1", index_col="Unnamed: 0")[isin_list]
    
        
    portfolio_monthly_returns_equally_weighted = []
    for month_nr in range(168):
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

    annualized_average_return_in_percentage_ew, volatility_ew = calculate_annualized_return_and_variance(
        portfolio_monthly_returns_equally_weighted)
    min_return_ew, max_return_ew = get_min_and_max_return(portfolio_monthly_returns_equally_weighted)
    
    # Finding the value weighted portfolio
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
    return annualized_average_return_in_percentage_vw, annualized_average_return_in_percentage_ew
    # min_return_vw, max_return_vw = get_min_and_max_return(portfolio_monthly_returns_value_weighted)
"""

def main():
    # Extracting all country codes for emerging countries
    countires_to_regions = pd.read_excel("data/CountriesToRegions.xlsx", sheet_name="Feuil1")
    em_country_codes_raw = list(countires_to_regions.loc[countires_to_regions["Unnamed: 4"] == "{'EM'}"]["function Corresp = CodetoName"])
    em_country_codes = [code[2:4] for code in em_country_codes_raw]

    # Extracting all ISINs from the emerging countires
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")
    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"].isin(em_country_codes)]
    isin_list = list(set(stocks_in_country["ISIN"].to_list()))

    filtered_isin_with_gov = []
    gov_df = pd.read_excel("data/Gov.xlsx", sheet_name="Feuil1")
    all_isin_with_gov = gov_df.columns.values.tolist()
    
    for isin in all_isin_with_gov:
        if len(gov_df[isin].dropna()) > 0 and isin in isin_list:
            filtered_isin_with_gov.append(isin)

    df = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")
    # df = df.dropna(axis='columns')

    # Finding the equal weight each month based on number of firms each month
    nr_of_months = 168
    weights_each_month = []
    for month_nr in range(nr_of_months-1,-1,-1):
        stocks_this_month = 0
        for isin in isin_list:
            if len(df[isin].dropna()) > month_nr:
                stocks_this_month += 1
        weights_each_month.append(1 / stocks_this_month)

    # Finding the value weighted portfolio
    size_sheet = pd.read_excel("data/size.xlsx", sheet_name="Feuil1")
    total_market_value_each_month = size_sheet.sum(axis=1)

    all_returns_list_vw = [[],[],[],[],[]]
    all_returns_list_ew = [[],[],[],[],[]]


    for month_nr in range(168):
        # size_tuples = []
        # isin_sorted_on_size = []
        # for isin in df.columns.to_list():
        #     try:
        #         size = size_sheet[isin][month_nr]
        #         b = int(size)
        #         size_tuples.append([isin, size])
        #     except:
        #         continue
        # # print(size_tuples)
        # size_tuples.sort(key=lambda y: y[1])
        # for value in size_tuples:
        #     isin_sorted_on_size.append(value[0])
        # l = len(isin_sorted_on_size)//5
        return_tuples = []
        isin_sorted_on_return = []
        for isin in df.columns.to_list():
            try:
                return_last_12 = 1
                return_last_12_list = df[isin][max(0,month_nr-12):month_nr]
                for stock_return in return_last_12_list:
                    b = int(stock_return)
                    return_last_12 = return_last_12 * stock_return
                    return_last_12 -= 1
                b = int(return_last_12)
                return_tuples.append([isin, return_last_12])
            except:
                continue
        # print(size_tuples)
        return_tuples.sort(key=lambda y: y[1])
        for value in return_tuples:
            isin_sorted_on_return.append(value[0])
        l = len(isin_sorted_on_return)//5

        returns_quintiles = [isin_sorted_on_return[0:l],
        isin_sorted_on_return[l:2*l],
        isin_sorted_on_return[2*l:3*l],
        isin_sorted_on_return[3*l:4*l],
        isin_sorted_on_return[4*l:],
        ]
        for i in range(5):
            q_df = df[returns_quintiles[i]]
            vw_return = 1
            for isin in q_df.columns.to_list():
                try:
                    a = df[isin][month_nr] * weights_each_month[month_nr]
                    b = int(a)
                    vw_return += a
                except:
                    continue
            # print(vw_return)
            all_returns_list_vw[i].append(vw_return)
            ew_return = 1
            for isin in q_df.columns.to_list():
                try:
                    a = df[isin][month_nr] * (size_sheet[isin][month_nr] / total_market_value_each_month[month_nr])
                    b = int(a)
                    ew_return += a
                except:
                    continue
            all_returns_list_ew[i].append(ew_return)
        
    
    for i in range(5):
        print('Vw ' + str(i), calculate_annualized_return(all_returns_list_vw[i]))
        print('Ew ' + str(i), calculate_annualized_return(all_returns_list_ew[i]))


    hedge_portfolio_vw = [0] * 168
    hedge_portfolio_ew = [0] * 168
    # print(all_returns_list_vw[0])
    # print(all_returns_list_ew[0])
    # print(all_returns_list_vw[4])
    # print(all_returns_list_ew[4])
    
    for j in range(168):
        hedge_portfolio_vw[j] = 1 + all_returns_list_vw[0][j] - all_returns_list_vw[4][j]
        hedge_portfolio_ew[j] = 1 + all_returns_list_ew[0][j] - all_returns_list_ew[4][j]
    print('Hedge return ew: ', calculate_annualized_return(hedge_portfolio_ew))
    print('Hedge return vw: ', calculate_annualized_return(hedge_portfolio_vw))

    # returns_list = []
    # for isin in filtered_isin_with_gov:
    #     try:
    #         returns_list.append((isin, df[isin][:24].sum()))
    #     except:
    #         continue
    
    # returns_list.sort(key=lambda y: y[1])

    # isins_list_sorted = []
    # for value in returns_list:
    #     isins_list_sorted.append(value[0])


    # l = len(returns_list)//5
    # returns_quintiles = [isins_list_sorted[0:l],
    # isins_list_sorted[l:2*l],
    # isins_list_sorted[2*l:3*l],
    # isins_list_sorted[3*l:4*l],
    # isins_list_sorted[4*l:],
    # ]


    # print('Results quin 1', make_value_and_equal_weighted(returns_quintiles[0], weights_each_month))
    # print('Results quin 2', make_value_and_equal_weighted(returns_quintiles[1], weights_each_month))
    # print('Results quin 3', make_value_and_equal_weighted(returns_quintiles[2], weights_each_month))
    # print('Results quin 4', make_value_and_equal_weighted(returns_quintiles[3], weights_each_month))
    # print('Results quin 5', make_value_and_equal_weighted(returns_quintiles[4], weights_each_month))

    





    # Highest return: TH0168A10Z01
    # portfolio_monthly_returns_best_stock = df['TH0168A10Z01'][-168:]
    # for i in range(len(portfolio_monthly_returns_best_stock)):
    #     portfolio_monthly_returns_best_stock[i] = portfolio_monthly_returns_best_stock[i] +1 
    # annualized_average_return_in_percentage_os, volatility_os = calculate_annualized_return_and_variance(portfolio_monthly_returns_best_stock)
    # print("Annualized average return one stock portfolio: ", annualized_average_return_in_percentage_os)
    # print("Annualized volatility one stock portfolio: ", volatility_os)

    # Best after two years INE604D01023
    # portfolio_monthly_returns_best_2y = df['INE604D01023'][-168:]
    # for i in range(len(portfolio_monthly_returns_best_2y)):
    #     portfolio_monthly_returns_best_2y[i] = portfolio_monthly_returns_best_2y[i] +1 
    # annualized_average_return_in_percentage_2y, volatility_2y = calculate_annualized_return_and_variance(portfolio_monthly_returns_best_2y)
    # print("Annualized average return one stock 2yr portfolio: ", annualized_average_return_in_percentage_2y)
    # print("Annualized volatility one stock 2yr portfolio: ", volatility_2y)


    # Plot results
    # monthly_returns_in_percentage_best_stock = np.array(portfolio_monthly_returns_best_stock) - 1 
    # monthly_returns_in_percentage_2y = np.array(portfolio_monthly_returns_best_2y) - 1
    # plt.plot(monthly_returns_in_percentage_best_stock, label='One best stock')
    # plt.plot(monthly_returns_in_percentage_2y, label='Best stock after 2yrs')
    # plt.xlabel('Time in months')
    # plt.ylabel('Annualized average return')
    # plt.legend()
    # plt.show()


if __name__ == "__main__":
    main()