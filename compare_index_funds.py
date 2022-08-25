import pandas as pd
import sys
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

sys.path.append("../data/")

nasdaq_100 = pd.read_csv("./data/nasdaq_100.csv")
nifty_50 = pd.read_csv("./data/nifty_50.csv")

## Parse the csv file and import the required data


def nifty_nasdaq_history(nfty, nsdq):
    """
    Parse csv file and return data required for comparing two index funds

    nfty, nsdq : Pandas dataframe

    Returns:
    nifty50 and nasdaq100 history as dictionary
    """

    ## TODO : Make the script more general by automatically know how to parse
    ## the csv files, so that multiple index and stocks can be compared.
    
    nasdaq = {}
    converted_date = [
        datetime.strptime(mydate, "%Y-%m-%d").strftime("%y-%m") for mydate in nsdq.Date
    ]
    nasdaq["date"] = np.array([str(mydate) for mydate in converted_date])
    nasdaq["value"] = np.array(nsdq.Close)
    nasdaq["percentage"] = (
        (nasdaq["value"] - nasdaq["value"][0]) / nasdaq["value"][0]
    ) * 100
    nasdaq = dict(zip(nasdaq["date"], nasdaq["percentage"]))

    ## NASDAQ and Nifty index history are downloaded from two different websites. Hence the csv data format differs and we need
    # need to parse them differently.
    nifty = {}
    converted_date = [
        datetime.strptime(mydate, "%b %y").strftime("%y-%m") for mydate in nfty.Date
    ]
    nifty["date"] = np.array([str(mydate) for mydate in converted_date])[::-1]
    nifty["value"] = np.array(nfty.Price)[::-1]
    nifty["value"] = np.array(
        [float(value.replace(",", "")) for value in nifty["value"]]
    )
    nifty["percentage"] = (
        (nifty["value"] - nifty["value"][0]) / nifty["value"][0]
    ) * 100
    nifty = dict(zip(nifty["date"], nifty["percentage"]))

    ## Sort the history by date
    nifty_50 = {}
    nasdaq_100 = {}
    for key in sorted(nifty.keys() & nasdaq.keys()):
        nifty_50[key] = nifty[key]
        nasdaq_100[key] = nasdaq[key]

    return nifty_50, nasdaq_100


if __name__ == "__main__":

    nifty_50, nasdaq_100 = nifty_nasdaq_history(nifty_50, nasdaq_100)
    fix, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.plot(nasdaq_100.keys(), nasdaq_100.values(), "--", c="r", label="Nasdaq 100")
    ax.plot(nifty_50.keys(), nifty_50.values(), "b", label="Nifty 50")
    locs = ax.get_xticks()
    ax.set_xticks(locs[::5])
    ax.legend(fontsize=15)

    ax.set_xlabel("Time [Year-month]", fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    ax.set_ylabel("Compound growth [%]", fontsize=15)

    plt.show()

    plt.savefig("nifty_nasdaq_comparison.png", format="png")
