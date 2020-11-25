from DataMining.algorithms.a_priori import Apriori
import pandas as pd 

csv_file = pd.read_csv("apriori_demo.csv")
print(csv_file)
ap = Apriori(csv_file,min_supp=2.,min_conf=0,min_lift=2, min_k=2)
#print(ap.apriori())
ap.apriori()
