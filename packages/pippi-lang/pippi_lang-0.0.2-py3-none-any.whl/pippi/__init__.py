"""init file for pippi."""
from pippi.text_cleaning import (
    Lemmatize,
    RemoveHTMLTags,
    RemovePunctuation,
    RemoveStopWords,
    TransformLettersSize,
)
from pippi.utils import download_dataset
