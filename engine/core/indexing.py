import pickle
import xlrd

from configs import dataset_path, index_file_path
from core.processing import clean_token, remove_html, stop_words

if __name__ == "__main__":
    sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)

    postings_list = {}
    for row in range(1, sheet.nrows):
        token_pos = 1
        content = remove_html(sheet.cell_value(row, 5))
        for word in content.split():
            token_pos += 1
            cleaned_token = clean_token(word)
            if cleaned_token and cleaned_token not in stop_words:
                postings_list.setdefault(cleaned_token, {}).setdefault(row, []).append(token_pos)

    with open(index_file_path, 'wb') as index_file:
        pickle.dump(postings_list, index_file)
