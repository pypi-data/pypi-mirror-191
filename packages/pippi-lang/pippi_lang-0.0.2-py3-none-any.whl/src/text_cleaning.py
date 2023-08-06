import pandas as pd
import spacy
import coloredlogs, logging
import nltk
from tqdm import tqdm
from spacy.lang.en.examples import sentences
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin

nltk.download("stopwords")
coloredlogs.install()
logger = logging.getLogger("text_cleaning.py")


class TransformLettersSize(BaseEstimator, TransformerMixin):
    """Converts all letters to upper case or lower case."""

    def __init__(self, case_transform, columns):
        self.case_transform = case_transform
        self.columns = columns
        logger.info("Transforming letters to upper or lower case")

    def fit(self, X, y=None):
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

    def transform(self, X):
        logger.info("Removing stop words.")
        preproc_data = X.copy()
        for column in tqdm(preproc_data):
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

    def transform(self, X):
        logger.info("Removing html tags.")
        preproc_data = X.copy()
        for column in preproc_data[self.columns]:
            if preproc_data[column].dtype in ["object", "str"]:
                preproc_data[column] = preproc_data[column].str.replace("<[^<]+?>", "")
        return preproc_data


class RemovePunctuation(BaseEstimator, TransformerMixin):
    """Remove unnecessary code, like log statements and unused variables. Leave the rest of the code the same."""

    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
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
    def __init__(self, lemmatizer=spacy.load("en_core_web_sm")):
        self.lemmatizer = lemmatizer
        logger.info("Lemmatizing text.")

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        preproc_data = X.copy()
        lemmatized_sentences = []
        for column in preproc_data:
            if preproc_data[column].dtype in ["object", "str"]:
                for sentence in preproc_data[column].values:
                    x = self.lemmatizer(sentence)
                    list_of_strings = [i.text for i in x]
                    x = " ".join(list_of_strings)
                    lemmatized_sentences.append(x)
                preproc_data[column] = lemmatized_sentences
        return preproc_data
