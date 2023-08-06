"""This module contains functions for text cleaning."""
import logging
import unicodedata

import coloredlogs
import nltk
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin

nltk.download("stopwords")
nltk.download("wordnet")

coloredlogs.install()
logger = logging.getLogger("text_cleaning.py")


class TransformLettersSize(BaseEstimator, TransformerMixin):
    """Converts all letters to upper case or lower case."""

    def __init__(self, case_transform, columns):
        self.case_transform = case_transform
        self.columns = columns
        logger.info("Transforming letters to upper or lower case")

    def fit(self, X, y=None):
        """fit method is required for sklearn pipeline."""
        return self

    def transform(self, X):
        data = X.copy()
        preproc_data = X.copy()
        if self.case_transform == "lower":
            for column in preproc_data[self.columns]:
                column_str = column
                if preproc_data[column_str].dtype in ["object", "str"]:
                    preproc_data[column_str] = data[column_str].str.lower()

        elif self.case_transform == "upper":
            for column in preproc_data[self.columns]:
                column_str = column
                if preproc_data[column_str].dtype in ["object", "str"]:
                    preproc_data[column_str] = data[column_str].str.upper()

        return preproc_data


class RemoveStopWords(BaseEstimator, TransformerMixin):
    """Removes stop words from the text. By default english stop words are removed."""

    def __init__(self, columns, stop_words=set(stopwords.words("english"))):
        self.stop_words = stop_words
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        logger.info("Removing stop words.")
        preproc_data = X.copy()
        for column in preproc_data[self.columns]:
            if preproc_data[column].dtype in ["object", "str"]:
                preproc_data[column] = preproc_data[column].apply(
                    lambda words: " ".join(
                        word.lower()
                        for word in words.split()
                        if word.lower() not in self.stop_words
                    )
                )
        return preproc_data


class RemoveHTMLTags(BaseEstimator, TransformerMixin):
    """Removes html tags from the text using regex."""

    def __init__(self, columns):
        self.columns = columns
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        logger.info("Removing html tags.")
        preproc_data = X.copy()
        for column in preproc_data[self.columns]:
            if preproc_data[column].dtype in ["object", "str"]:
                preproc_data[column] = preproc_data[column].apply(
                    lambda x: BeautifulSoup(x, "lxml").get_text().strip()
                )
        return preproc_data


class RemovePunctuation(BaseEstimator, TransformerMixin):
    """Remove unnecessary code, like log statements and unused variables.
    Leave the rest of the code the same."""

    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        preproc_data = X.copy()
        for column in preproc_data[self.columns]:
            if preproc_data[column].dtype in ["object", "str"]:
                preproc_data[column] = preproc_data[column].str.replace(
                    r"[^A-Za-z ]+", "", regex=True
                )
        return preproc_data


class RemoveDigits(BaseEstimator, TransformerMixin):
    """Remove digits from the text using regex."""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        preproc_data = X.copy()
        preproc_data.MarketingDescription_DE = (
            preproc_data.MarketingDescription_DE.str.replace("\d+", "")
        )
        return preproc_data


class Lemmatize(BaseEstimator, TransformerMixin):
    def __init__(self, columns, lemmatizer=WordNetLemmatizer()):
        self.lemmatizer = lemmatizer
        self.columns = columns
        logger.info("Starting lemmatization.")

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        preproc_data = X.copy()
        for column in self.columns:
            if preproc_data[column].dtype in ["object", "str"]:
                preproc_data[column] = preproc_data[column].apply(
                    lambda sentence: " ".join(
                        [self.lemmatizer.lemmatize(w) for w in sentence.split(" ")]
                    )
                )
        return preproc_data


class RemoveMultipleSpaces(BaseEstimator, TransformerMixin):
    """Remove multiple spaces from text columns."""

    def __init__(self, columns):
        self.columns = columns
        logger.info("Removing multiple spaces.")

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        preproc_data = X.copy()
        for column_str in preproc_data[self.columns]:
            if preproc_data[column_str].dtype in ["object", "str"]:
                ## remove multiple spaces
                preproc_data[column_str] = preproc_data[column_str].apply(
                    lambda x: " ".join(x.split())
                )
            ## remove leading and trailing spaces
        return preproc_data


class RemoveAccentedChars(BaseEstimator, TransformerMixin):
    """Converts all letters to upper case or lower case."""

    def __init__(self, columns):
        self.columns = columns
        logger.info("Removing multiple spaces.")

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        preproc_data = X.copy()
        for column_str in preproc_data[self.columns]:
            if preproc_data[column_str].dtype in ["object", "str"]:
                preproc_data[column_str] = preproc_data[column_str].apply(
                    lambda x: unicodedata.normalize("NFKD", x)
                    .encode("ascii", "ignore")
                    .decode("utf-8", "ignore")
                )

            return preproc_data


class ReplaceString(BaseEstimator, TransformerMixin):
    """Converts all letters to upper case or lower case."""

    def __init__(self, word, replacement, columns):
        self.word = word
        self.replacement = replacement
        self.columns = columns
        logger.info("Removing multiple spaces.")

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        preproc_data = X.copy()
        for column_str in preproc_data[self.columns]:
            if preproc_data[column_str].dtype in ["object", "str"]:
                preproc_data[column_str] = preproc_data[column_str].str.replace(
                    self.word, self.replacement
                )
            return preproc_data
