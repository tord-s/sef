import pandas as pd

def read_test():
    countires_to_regions = pd.read_excel("data/CountriesToRegions.xlsx", sheet_name="Feuil1")
    monthly_returns_dataframe = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1")
    firm_names_dataframe = pd.read_excel("data/firm_names.xlsx", sheet_name="Feuil1")

    em_country_codes_raw = list(countires_to_regions.loc[countires_to_regions["Unnamed: 4"] == "{'EM'}"]["function Corresp = CodetoName"])
    em_country_codes = [code[2:4] for code in em_country_codes_raw]

    stocks_in_country = firm_names_dataframe.loc[firm_names_dataframe["Country"].isin(em_country_codes)]
    ISINs_in_country = stocks_in_country["ISIN"].to_list()
    
    stocks_with_return_dict = {}

    for ISIN in ISINs_in_country:
        earnings = 0
        for value in monthly_returns_dataframe[ISIN]:
            earnings += value
        stocks_with_return_dict[ISIN] = value

    sorted_stocks_with_return_list = sorted(stocks_with_return_dict.items(), key=lambda x:x[1])
    print('5 best stocks in EM: ', sorted_stocks_with_return_list[-5:])

if __name__ == "__main__":
    read_test()