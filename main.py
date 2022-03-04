import pandas as pd

def read_test():
    monthly_returns_dataframe = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")

    country_code = "CN"
    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"] == country_code]
    ISINs_in_country = stocks_in_country["ISIN"].to_list()
    
    stocks_with_return_dict = {}

    for ISIN in ISINs_in_country:
        earnings = 0
        for value in monthly_returns_dataframe[ISIN]:
            earnings += value
        stocks_with_return_dict[ISIN] = value

    sorted_stocks_with_return_list = sorted(stocks_with_return_dict.items(), key=lambda x:x[1])
    print('5 best stocks in' + country_code + ': ', sorted_stocks_with_return_list[-5:])

if __name__ == "__main__":
    read_test()