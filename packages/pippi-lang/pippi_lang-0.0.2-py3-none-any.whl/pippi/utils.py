"""utils.py contains all the utility functions used in pippi."""
import os

import pandas as pd
import requests


def download_dataset() -> pd.DataFrame:
    """Downloads the dataset from github."""
    if os.path.exists("dataset.csv"):
        return pd.read_csv("dataset.csv")
    url = "https://raw.githubusercontent.com/SK7here/Movie-Review-Sentiment-Analysis/master/IMDB-Dataset.csv"
    dataset = requests.get(url, allow_redirects=True, timeout=None)
    open("dataset.csv", "wb").write(dataset.content)
    df = pd.read_csv("dataset.csv")
    return df
