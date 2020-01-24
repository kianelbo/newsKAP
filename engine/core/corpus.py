from os import listdir
import pandas as pd

from configs import dataset_path

# sheet = pd.read_csv(dataset_path)
sheet = pd.DataFrame()
for csv_file in listdir(dataset_path):
    sheet = sheet.append(pd.read_csv(f'{dataset_path}{csv_file}'))
sheet.drop(['source_url'], axis=1, inplace=True)
sheet.drop(['category'], axis=1, inplace=True)
sheet.drop(['subcategory'], axis=1, inplace=True)
for naHeader in ['title', 'summary', 'thumbnail']:
    sheet[naHeader] = sheet[naHeader].fillna('')
sheet['publish_date'] = sheet['publish_date'].apply(lambda x: x[:-7])

doc_count = len(sheet.index)
print("successfully loaded the corpus")
