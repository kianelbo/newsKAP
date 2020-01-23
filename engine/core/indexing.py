from core.corpus import sheet
from core.dictionary import Dictionary
from core.processing import clean_token, fix_compounds, remove_html, stop_words
from core.ranking import build_doc_vectors

if __name__ == "__main__":
    # building index file
    dictionary = Dictionary()
    for row, content in enumerate(sheet['content']):
        token_pos = -1
        text = remove_html(content)
        text = fix_compounds(text)
        for word in text.split():
            token_pos += 1
            cleaned_token = clean_token(word)
            if cleaned_token and cleaned_token not in stop_words:
                dictionary.add(cleaned_token, row, token_pos)

    dictionary.save()
    print("successfully created the index file")

    # building doc vectors file
    build_doc_vectors(dictionary)
    print("successfully created the vectors file")
