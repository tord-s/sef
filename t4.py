import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web

def main():

    # calculating expected annual return and annualized sample covariance matrix of daily assets returns

    random_firms = ['BRTNLPACNPR0', 'KR7030200000', 'GRS294003009', 'HU0000073507', 'MYL3735OO007',
    'PK0067901022', 'TH0068010Z07', 'MXP4987V1378', 'PLTLKPL00017', 'TW0002384005', 'BROIBRACNPR8',
    'ZAE000161832', 'ZAE000096541', 'HK0267001375', 'MXP740451010', 'MYL1562OO007', 'PLBPH0000019',
    'KR7008060006', 'CLP9796J1008', 'MYL4588OO009', 'CNE0000005Q7', 'MYL4197OO009', 'MYL6033OO004',
    'TW0002353000', 'CNE000001139', 'PHY6028G1361', 'SA0007879097', 'CNE000000DD4', 'TW0002801008',
    'CNE0000009B1', 'SA0007879782', 'CLP0939W1081', 'PHY0967S1694', 'CNE0000018X6', 'MXP001691213',
    'CNE000000B42', 'TW0002347002', 'CLP3880F1085', 'TW0002915006', 'TW0002356003', 'CNE000001733',
    'INE257A01026', 'TW0001301000', 'KR7020560009', 'TW0001717007', 'CNE000000KT5', 'RU0007661625',
    'KR7035760008', 'CNE000000Q29', 'CNE000001782'] 

    
    # To plot size against return and volatility
    size_sheet = pd.read_excel("data/size.xlsx", sheet_name="Feuil1")
    list_with_size = []
    intersect = list(set(size_sheet.columns.to_list()) & set(random_firms))
    for isin in intersect:
        try:
            a = size_sheet[isin].mean()
            b = int(a)
            list_with_size.append((isin, a))
        except:
            continue
    list_with_size.sort(key=lambda y: y[1])
    biggest_inins = []
    print(list_with_size)
    for i in range(len(list_with_size)//3, len(list_with_size)):
        biggest_inins.append(list_with_size[i][0])

    print('Biggest isins', biggest_inins)
    df = pd.read_excel("data/monthlyreturns.xlsx", sheet_name="Feuil1", index_col="Unnamed: 0")[biggest_inins]

    cov_mat = df.cov() * 12
    # print(cov_mat)


    # Simulating 5000 portfolios
    num_port = 50000
    # Creating an empty array to store portfolio weights
    all_wts = np.zeros((num_port, len(df.columns.to_list())))
    # Creating an empty array to store portfolio returns
    port_returns = np.zeros((num_port))
    # Creating an empty array to store portfolio risks
    port_risk = np.zeros((num_port))
    # Creating an empty array to store portfolio sharpe ratio
    sharpe_ratio = np.zeros((num_port))

    for i in range(num_port):
        wts = np.random.uniform(size = len(df.columns.to_list()))
        wts = wts/np.sum(wts)
        
        # saving weights in the array
        
        all_wts[i,:] = wts
        
        # Portfolio Returns
        
        port_ret = np.sum(df.mean() * wts)
        port_ret = (port_ret + 1) ** 12 - 1
        
        # Saving Portfolio returns
        
        port_returns[i] = port_ret
        
        
        # Portfolio Risk
        
        port_sd = np.sqrt(np.dot(wts.T, np.dot(cov_mat, wts)))
        
        port_risk[i] = port_sd
        
        # Portfolio Sharpe Ratio
        # Assuming 0% Risk Free Rate
        
        sr = port_ret / port_sd
        sharpe_ratio[i] = sr
        
    print('Max return', port_returns.max())
    print('Min return', port_returns.min())

    names = df.columns.to_list()
    min_var = all_wts[port_risk.argmin()]
    min_var = pd.Series(min_var, index=names)
    min_index = 0
    for i in range(len(min_var)):
        if min_var[i] < min_var[min_index]:
            min_index = i
    print("Min var returs", port_returns[min_index])
    print("Min var var", min_var[min_index])
    print("Min var sr", sharpe_ratio[min_index])

    # print(port_returns)


if __name__ == "__main__":
    main()
