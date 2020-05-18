# from nltk.stem.porter import PorterStemmer

text = ("The Centre on Sunday extended the nationwide"
        " lockdown till May 31 to keep a check on the "
        "spread of Covid-19 which has infected over 90,000 "
        "people across India. The Union home ministry has issued"
        " guidelines listing the dos and don'ts during the"
        " lockdown 4.0. Stay with TOI for live updates")


words = text.split()
stemmer = PorterStemmer()
stems = [stemmer.stem(item) for item in words]
print(f'Only stems:\n {" ".join(stems)}')
