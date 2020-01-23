from os import listdir
import pandas as pd

from configs import dataset_path

sheet = pd.read_csv(dataset_path)
# df = pd.DataFrame()
# for dataset in listdir(dataset_path):
#     df = df.append(pd.read_csv(f'{dataset_path}{dataset}'))
sheet.drop(['source_url'], axis=1, inplace=True)
sheet.drop(['category'], axis=1, inplace=True)
sheet.drop(['subcategory'], axis=1, inplace=True)
for naHeader in ['title', 'summary', 'thumbnail']:
    sheet[naHeader] = sheet[naHeader].fillna('')
sheet['publish_date'] = sheet['publish_date'].apply(lambda x: x[:-7])

doc_count = len(sheet.index)
