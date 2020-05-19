"""
Module for creating word cloud
"""
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords

DATAFRAME = pd.read_csv('../data/phase7.csv')

rcParams['figure.figsize'] = 12, 18

STOPWORDS = stopwords.words('english')

WORDCLOUD = WordCloud(stopwords=STOPWORDS,
                      background_color='white',
                      width=600, height=400,
                      max_font_size=80,
                      max_words=200).generate(
                          DATAFRAME['description'].sum()
                      )
WORDCLOUD.recolor(random_state=312)
plt.imshow(WORDCLOUD)
plt.axis("off")
plt.show()
