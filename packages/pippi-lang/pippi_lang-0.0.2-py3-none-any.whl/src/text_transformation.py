# from sklearn.base import BaseEstimator, TransformerMixin
# from sklearn.feature_selection import VarianceThreshold
# from sklearn.preprocessing import LabelEncoder
# import pandas as pd

# # from .training import (
# #     get_bert,
# #     get_bert_whitened,
# #     text_to_numbers,
# #     normalize_subset,
# #     bag_of_words,
# #     tf_idf,
# # )
# from os.path import exists


# class EncodeText(BaseEstimator, TransformerMixin):
#     def __init__(self):
#         pass

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         # Encode all text variables
#         encoded_df, le_dict = text_to_numbers(X.copy(deep=True))
#         return encoded_df


# class CustomLabelEncoder(BaseEstimator, TransformerMixin):
#     def __init__(self, cat_cols):
#         self.cat_cols = cat_cols

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X, y=None):
#         cat_cols = self.cat_cols
#         le = LabelEncoder()
#         for i in X[cat_cols]:
#             X[i] = le.fit_transform(X[i])
#         return X


# class NormalizeValues(BaseEstimator, TransformerMixin):
#     def __init__(self):
#         pass

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         # Encode all text variables
#         normalized_df = normalize_subset(X.copy(deep=True))
#         return normalized_df


# class DropAttributes(BaseEstimator, TransformerMixin):
#     def __init__(self, attributes_to_be_dropped):
#         self.attributes_to_be_dropped = attributes_to_be_dropped
#         pass

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         attributes_to_be_dropped = self.attributes_to_be_dropped
#         trimmed_df = X.drop(columns=attributes_to_be_dropped)
#         return trimmed_df


# class RemoveVariance(BaseEstimator, TransformerMixin):
#     def __init__(self, threshold):
#         self.threshold = threshold

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         constant_filter = VarianceThreshold(threshold=0.0001)
#         x_temp = X.copy(deep=True)
#         constant_filter.fit(x_temp)
#         return x_temp[x_temp.columns[constant_filter.get_support(indices=True)]]


# class OneHotEncodeCategoricalFeatures(BaseEstimator, TransformerMixin):
#     def __init__(self, columns_to_be_encoded):
#         self.columns_to_be_encoded = columns_to_be_encoded

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         x_temp = X.copy()
#         try:
#             x_temp = pd.get_dummies(
#                 x_temp,
#                 prefix=self.columns_to_be_encoded,
#                 columns=self.columns_to_be_encoded,
#                 drop_first=True,
#             )
#             return x_temp
#         except KeyError:
#             return X.copy()


# class NormalizeValues(BaseEstimator, TransformerMixin):
#     def __init__(self, normalize):
#         self.normalize = normalize

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         df = X.copy(deep=True)
#         if self.normalize == "yes":
#             df = X.copy(deep=True)
#             for col in df.columns:
#                 if df[col].dtype not in ["bool", "str"]:
#                     df[col] = (
#                         (df[col] - df[col].min()) / (df[col].max() - df[col].min())
#                         if df[col].max() != 0
#                         else 0
#                     )
#             return df
#         return df


# # class PcaTextReductions(BaseEstimator, TransformerMixin):
# #     def __init__(self, NumberOfDimensions):
# #         self.NumberOfDimensions = NumberOfDimensions
# #         pass

# #     def fit(self, X, y=None):
# #         return self

# #     def transform(self, X):
# #         NumberOfDimensions = self.NumberOfDimensions
# #         return trimmed_df


# class MarketingDescriptionsEncoder(BaseEstimator, TransformerMixin):
#     def __init__(self, trasformation, labels, p, max_features, n_gram_range, dim):
#         self.transformation = trasformation
#         self.labels = labels
#         self.max_features = max_features
#         self.p = p
#         self.dim = dim
#         self.n_gram_range = n_gram_range

#         pass

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         transformation = self.transformation
#         p = self.p
#         labels = self.labels
#         dim = self.dim
#         max_features = self.max_features

#         MarketingDescriptions_vectorized = None
#         n_gram_range = self.n_gram_range
#         X.columns = X.columns.astype(str)

#         if transformation == "bow":
#             print("BOW")
#             MarketingDescriptions_vectorized = bag_of_words(
#                 p_value_limit=p,
#                 max_features=max_features,
#                 n_gram_range=n_gram_range,
#                 words_to_vectorize=X.MarketingDescription_DE,
#                 labels=labels,
#             )

#         if transformation == "tf_idf":
#             print("TF-IDF")
#             MarketingDescriptions_vectorized = tf_idf(
#                 p_value_limit=p,
#                 max_features=max_features,
#                 n_gram_range=n_gram_range,
#                 words_to_vectorize=X.MarketingDescription_DE,
#                 labels=labels,
#                 pca=dim,
#             )

#         if transformation == "bert":
#             print("BERT")
#             MarketingDescriptions_vectorized = get_bert(X.MarketingDescription_DE)
#             # file_path = "/data1/userspace/szymon/Galaxus/Output/embeddings.parquet"
#             # MarketingDescriptions_vectorized = (
#             #     pd.read_parquet(file_path)
#             #     if exists(file_path)
#             #     else get_bert(X.MarketingDescription_DE)
#             # )

#         if transformation == "bert_whitened":
#             file_path = (
#                 "/data1/userspace/szymon/Galaxus/Output/whitened_embeddings.parquet"
#             )
#             MarketingDescriptions_vectorized = get_bert_whitened(
#                 X.MarketingDescription_DE, dim
#             )
#             # MarketingDescriptions_vectorized = (
#             #     pd.read_parquet(file_path)
#             #     if exists(file_path)
#             #     else get_bert_whitened(X.MarketingDescription_DE, dim)
#             # )

#         if transformation == "no":
#             print("No")
#             return X.copy(deep=True)

#         merged_x_marketing_desc = pd.concat(
#             [X, MarketingDescriptions_vectorized], axis=1
#         )

#         return merged_x_marketing_desc
