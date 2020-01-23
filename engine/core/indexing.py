from configs import doc_count, sheet
from core.dictionary import Dictionary
from core.processing import clean_token, fix_compounds, remove_html, stop_words
from core.ranking import build_doc_vectors

if __name__ == "__main__":
    # building index file
    dictionary = Dictionary()
    for row in range(1, doc_count):
        token_pos = -1
        content = remove_html(sheet.cell_value(row, 5))
        content = fix_compounds(content)
        for word in content.split():
            token_pos += 1
            cleaned_token = clean_token(word)
            if cleaned_token and cleaned_token not in stop_words:
                dictionary.add(cleaned_token, row, token_pos)

    dictionary.save()
    print("successfully created the index file")

    # building doc vectors file
    build_doc_vectors(dictionary)
    print("successfully created the vectors file")
