import pandas as pd

from configs import dataset_path

sheet = pd.read_csv(dataset_path)
print("successfully loaded the corpus")
