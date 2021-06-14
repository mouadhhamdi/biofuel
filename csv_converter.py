import pandas as pd
from googletrans import Translator
import os
from spellchecker import SpellChecker
import re

spell = SpellChecker(language='de')
translator = Translator()


def get_csv_path():
    csv_dir_path = os.path.join(os.curdir, 'data/csv_data')
    csv_path = ''
    with os.scandir(csv_dir_path) as entries:
        for entry in entries:
            csv_path = os.path.join(csv_dir_path, entry.name)
    return csv_path


def read_csv():
    print("read csv")
    df = pd.read_csv(get_csv_path(), delimiter=';""', encoding='latin1', engine='python')
    # remove " quotes from column name
    df.columns = [c.replace('"', '') for c in df.columns.tolist()]
    df.columns = [re.sub(',,,+', '', c) for c in df.columns.tolist()]
    print("transform to ascii")
    df.columns = [c.encode('ascii', errors='ignore').decode() for c in df.columns.tolist()]
    print("correct misspelled")
    df.columns = [correct_misspelled(c) for c in df.columns.tolist()]
    # convert names to english
    print("translate column name")
    df.columns = [translator.translate(c, dest='en', src='de').text.title() for c in df.columns.tolist()]
    return df


def correct_misspelled(col_name):
    col_words = col_name.split(' ')
    corrected_col_name = ''
    for col_word in col_words:
        misspelled = spell.unknown([col_word])
        if col_word in ['ID', 'id']:
            corrected_col_name += 'ID'
            corrected_col_name += ' '
        elif len(misspelled) == 0:
            corrected_col_name += col_word
            corrected_col_name += ' '
        else:
            for word in misspelled:
                # Get the one `most likely` answer
                spell_correction = spell.correction(word)
                if spell_correction in ['Vorgaenger', 'vorgaenger']:
                    corrected_col_name += 'Predecessor'
                    corrected_col_name += ' '
                else:
                    corrected_col_name += spell_correction
                    corrected_col_name += ' '
    return corrected_col_name


def clean_rows(df):
    for i, col in enumerate(df.columns):
        df.iloc[:, i] = df.iloc[:, i].str.replace('"', '')
        df.iloc[:, i] = df.iloc[:, i].str.replace(',,,+', '', regex=True)
    return df


df = read_csv()
df = clean_rows(df)
