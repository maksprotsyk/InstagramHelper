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
df = pd.DataFrame(data=DATA, columns=['following', 'description'])\
       .drop_duplicates(subset='following')


# processing texts of every user
df['description'] = df['description'].str\
                                     .replace('([A-Z][a-z]+)', ' \\1')\
                                     .str\
                                     .replace("\'", '')\
                                     .str\
                                     .replace('\W|\d|_', ' ')\
                                     .str\
                                     .replace('\s+', ' ')\
                                     .str.strip()\
                                     .str.lower()

# getting stems of english words
# and removing ukrainian stop words
stemmer = PorterStemmer()
with open('../../data/stopwords.txt') as in_file:
    stop_words = in_file.read().split('\n')
df['description'] = df['description']\
                        .apply(lambda row: ' '.join(
                        [stemmer.stem(word)
                        for word in row.split(' ')
                        if word not in stop_words])
                        )

# deleting short texts
df = df[df['description'].apply(len) > 30]

# creating a pipeline that can vectorize the texts and cluster them
# includes only words with len 3 or more
pipe = Pipeline([('vectorizer', TfidfVectorizer(stop_words='english',
                                                token_pattern=r'\b\w{3,}\b')),
                 ('clustering', AffinityPropagation())])

# training the model
pipe.fit(df['description'])

# creating a column for cluster numbers
df['cluster'] = pipe.named_steps['clustering'].labels_

# saving DataFrame to csv
df.to_csv('../../data/phase7.csv', index=False, encoding='utf-8-sig')

# saving machine learning model to pickle file
with open('../../data/model.pickle', 'wb') as output:
    pickle.dump(pipe, output)
