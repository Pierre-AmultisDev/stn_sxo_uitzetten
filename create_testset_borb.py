import pandas as pd
import csv

df = pd.read_csv("./input/retrieve_all_notities.csv", sep=';', quotechar='"', dtype=str)

keep_list = ["27420344", "16091262", "3907881", "33473003", "9247714", "5307071", "2265120"]

df = df[df['HOOFDZAAKID'].isin(keep_list)]

# save dataframe contents
df.to_csv("./input/retrieve_all_notities_uitzonderingen.csv", index=False, sep=';', quotechar='"', quoting=csv.QUOTE_ALL)
