import streamlit as st
from common_container import menu
from data_analysis import song_df, BASIC_COL, rank_df

import pandas as pd
from collections import Counter
from data_function import tokenize


menu()

st.write("# 문장의 토큰화")
st.divider()

st.write("본격적인 클러스터링의 시작에 앞서서")

st.code("""
from konlpy.tag import Okt      # Komoran을 쓸 수도 있다.
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.tag import pos_tag
import requests


# nltk 설치할 거 받기
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# 한국어 불용어 사전 & 영어 불용어 사전
url = "https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt"
r = requests.get(url, stream=True)
kr_stopwords = r.text.replace("\\t", "\\n").split('\\n')
en_stopwords = stopwords.words('english')

# 한국어 토크나이저 & 영어 명사 변형(복수 -> 단수 등)
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


if __name__ == '__main__':

    sentence = "이것은 테스트 the sentence입니다."
    result = tokenize(sentence)
    print(result)""")
st.code("""
text_df['tk_lyrics'] = text_df['lyrics'].apply(tokenize)
tokenized_text = text_df["tk_lyrics"].copy()
tokenized_text
""")
st.dataframe(song_df[BASIC_COL + ['tk_full_lyrics']].rename(columns={"tk_full_lyrics": 'tk_lyrics'}))

with st.container(border=True):
    col1, col2 = st.columns(2)
    a = col1.text_area(label="원하는 한글 + 영어 문장")
    b = col2.text(f"토큰화 결과:\n{tokenize(a)}")

st.code("""from collections import Counter

def most_common(start_year=2000, end_year=2023):
    counter = Counter()
    rank_interval = rank_df[rank_df["date"].dt.year.between(start_year, end_year)]
    for idx in rank_interval.index:
        song_id = rank_interval.loc[idx, "song_id"]
        counter.update(text_df.loc[song_id, "tk_lyrics"])
    return counter.most_common(20)

pd.DataFrame({
    "total": most_common(),
    "2000-2004": most_common(2000, 2004),
    "2005-2009": most_common(2005, 2009),
    "2010-2014": most_common(2010, 2014),
    "2015-2019": most_common(2015, 2019),
    "2020-2023": most_common(2020, 2023),
})""")


def most_common(start_year=2000, end_year=2023):
    counter = Counter()
    rank_interval = rank_df[rank_df["date"].dt.year.between(start_year, end_year)]
    for idx in rank_interval.index:
        song_id = rank_interval.loc[idx, "song_id"]
        counter.update(song_df.loc[song_id, "tk_full_lyrics"])
    return list(map(lambda x: (x[0], str(x[1])), counter.most_common(20)))


st.dataframe(pd.DataFrame({
    "total": most_common(),
    "2000-2004": most_common(2000, 2004),
    "2005-2009": most_common(2005, 2009),
    "2010-2014": most_common(2010, 2014),
    "2015-2019": most_common(2015, 2019),
    "2020-2023": most_common(2020, 2023),
}))

st.code("""counter = Counter()
for vec in tokenized_text:
    counter.update(vec)

counter.most_common()[:30]""")
counter = Counter()
for vec in song_df["tk_full_lyrics"]:
    counter.update(vec)

st.code(counter.most_common()[:30])

st.code("""counter.total()""")
st.code(counter.total())

st.code("""
text_df['tk_lyrics'] = text_df['lyrics'].apply(
    lambda x: tokenize(x, kr_add=["사랑", "그대", "사람"], en_add=["baby", "love"])
)

text_df = text_df[text_df["tk_lyrics"].apply(lambda x: x is not [])]
tokenized_text = text_df["tk_lyrics"].copy()
tokenized_text""")

st.dataframe(song_df[BASIC_COL + ["tk_lyrics"]])
