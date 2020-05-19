"""
Example for nltk
"""
import nltk

TEXT = ("The Centre on Sunday extended the nationwide"
        " lockdown till May 31 to keep a check on the "
        "spread of Covid-19 which has infected over 90,000 "
        "people across India. The Union home ministry has issued"
        " guidelines listing the dos and don'ts during the"
        " lockdown 4.0. Stay with TOI for live updates")


WORDS = TEXT.split()
STEMMER = nltk.stem.PorterStemmer()
STEMS = [STEMMER.stem(item) for item in WORDS]
print(f'Only stems:\n {" ".join(STEMS)}')
