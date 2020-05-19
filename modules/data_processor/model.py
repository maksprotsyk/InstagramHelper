"""
Module for creating machine learning model
"""
import pickle
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation
from sklearn.pipeline import Pipeline
from nltk.stem import PorterStemmer


# opening data file and saving it to the list
with open('../../data/phase6.txt', encoding='utf-8') as in_file:
    DATA = re.findall(r'^([^ ]+) *(.*)$', in_file.read(), flags=re.M)

# naming columns
DATAFRAME = pd.DataFrame(data=DATA, columns=['following', 'description'])\
       .drop_duplicates(subset='following')


# processing texts of every user
DATAFRAME['description'] = DATAFRAME['description']\
                                     .str\
                                     .replace(r'([A-Z][a-z]+)', r' \\1')\
                                     .str\
                                     .replace(r"\'", '')\
                                     .str\
                                     .replace(r'\W|\d|_', ' ')\
                                     .str\
                                     .replace(r'\s+', ' ')\
                                     .str.strip()\
                                     .str.lower()

# getting stems of english words
# and removing ukrainian stop words
STEMMER = PorterStemmer()
with open('../../data/stopwords.txt') as in_file:
    STOP_WORDS = in_file.read().split('\n')
DATAFRAME['description'] = DATAFRAME['description'].apply(
    lambda row: ' '.join(
                [STEMMER.stem(word)
                 for word in row.split(' ')
                 if word not in STOP_WORDS]
    )
    )

# deleting short texts
DATAFRAME = DATAFRAME[DATAFRAME['description'].apply(len) > 30]

# creating a pipeline that can vectorize the texts and cluster them
# includes only words with len 3 or more
PIPE = Pipeline([('vectorizer', TfidfVectorizer(stop_words='english',
                                                token_pattern=r'\b\w{3,}\b')),
                 ('clustering', AffinityPropagation())])

# training the model
PIPE.fit(DATAFRAME['description'])

# creating a column for cluster numbers
DATAFRAME['cluster'] = PIPE.named_steps['clustering'].labels_

# saving DataFrame to csv
DATAFRAME.to_csv('../../data/phase7.csv', index=False, encoding='utf-8-sig')

# saving machine learning model to pickle file
with open('../../data/model.pickle', 'wb') as output:
    pickle.dump(PIPE, output)
