import time

import streamlit as st
from menu import menu
from datausing import pickle2df


from jamo import h2j, j2hcj

from konlpy.tag import Okt      # Komoran을 쓸 수도 있다.
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk
import requests

menu()

with st.sidebar:

    menu_lst = ["1. Introduction", "2. Data Processing", "3. Tokenization", "4. Topic Modeling", "5. K-Means Clustering", "6. Data Analysis"]

    choice = st.selectbox(label="종류", options=menu_lst, index=0)

if choice == "1. Introduction":
    st.title("1. 노래 주제별 군집화")

    st.subheader("목적: 노래를 주제별로 군집화하여...")

if choice == "2. Data Processing":

    st.title("1. 노래 주제별 군집화")

    txt = st.text_input("search")

    basic_col = ['name', "album", "year", "month", "day", "artist", "genre", "lyric_writer", "composer", "arranger", "lyrics_row", "lyrics"]
    show_col = ['name', "album", "year", "month", "day", "artist", "genre", "lyric_writer", "composer", "arranger"]

    song_df = pickle2df("song_df.pickle")
    rank_df = pickle2df("rank_df.pickle")


    def jamo_contains(haystack, needle):
        # 주어진 문자열들을 자모 단위로 변환하여 비교
        haystack_jamo = j2hcj(h2j(haystack))
        needle_jamo = j2hcj(h2j(needle))
        return needle_jamo in haystack_jamo

    @st.cache_data
    def filter_rows_by_jamo(df, value):

        idxss = []

        for idx, row in df.iterrows():
            if row.astype(str).apply(lambda x: jamo_contains(x, value)).any():
                idxss.append(idx)
            if len(idxss) == 50:
                return df.loc[idxss][show_col]

    sp = filter_rows_by_jamo(song_df[basic_col], txt)

    st.data_editor(
        sp,
        column_config={
            "favorite": st.column_config.CheckboxColumn(
                "Your favorite?",
                help="Select your **favorite** widgets",
                default=False,
            )
        },
        disabled=["widgets"],
        hide_index=False,
    )

if choice == "3. Tokenization":
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')

    url = "https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt"
    r = requests.get(url, stream=True)
    kr_stopwords = r.text.replace("\t", "\n").split('\n')

    en_stopwords = stopwords.words('english')

    okt = Okt()
    wlem = nltk.WordNetLemmatizer()


    def tokenize(sentence, kr_add=[], en_add=[]):

        kr_tokens = okt.pos(sentence)

        extracted_words = []
        for word, pos in kr_tokens:
            if pos == 'Noun' and word not in kr_stopwords + kr_add and len(word) > 1:
                extracted_words.append(word)
            elif pos == 'Alpha':
                extracted_words.append(word)

        extracted_sentence = ' '.join(extracted_words)

        en_tokens = pos_tag(word_tokenize(extracted_sentence.lower()))

        result = []
        for word, pos in en_tokens:
            if '가' <= word[0] <= '힣':
                result.append(word)
            elif pos[:2] == 'NN' and word not in en_stopwords + en_add and len(word) > 2:
                new_word = wlem.lemmatize(word)
                result.append(new_word)

        return result


if choice == "4. Topic Modeling":
    pass

if choice == "5. K-Means Clustering":
    pass

if choice == "6. Data Analysis":
    pass