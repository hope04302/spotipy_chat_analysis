import streamlit as st
from common_container import menu
from data_analysis import your_df, song_df, rank_df, BASIC_COL

menu()


# 하나의 부품 =========================================================

st.write("# 🎵 Kpop-lyric-datasets")
st.divider()

st.write("""
There are json-formated datas of 25696 k-pop songs, which was from **Melon's Monthly Chart Ranking 100 (2000 ~ 2023 Oct.)**.

Also providing python functions for data handling.

*I DO NOT claim any ownership of this dataset, All copyrights belong to the authors, of each song.*

*You can freely use this dataset on RESEARCH PURPOSE, but if you want to use COMMERCIALLY this dataset, You should Talk with Lyricists, Artists, Composers, etc.*
""")

st.code("""
{
    "info": [
        {
            "year": 2023,
            "month": 7,
            "rank": 16,
            "type": "월별차트",
            "website": "Melon"
        },
        ""
    ],
    "song_id": "35454425",
    "song_name": "Attention",
    "album": "NewJeans 1st EP 'New Jeans'",
    "release_date": "2022.08.01",
    "artist": "NewJeans",
    "genre": "댄스",
    "lyric_writer": "Gigi",
    "composer": "Duckbay (Cosmos Studios Stockholm)",
    "arranger": "다니엘(DANIELLE)",
    "lyrics": {
        "row_num": 79,
        "lines": [
            "You and me",
            "내 맘이 보이지",
            "한참을 쳐다봐",
            "가까이 다가가",
            "You see",
            "You see, ey ey ey ey",
            "",
            "One, two, three",
            "(... etc.)"
        ]
    }
}
""")

st.write("*각 칼럼이 무엇을 의미하는지 잘 이해되지 않는다면 아래 래퍼런스에 들어가 설명을 읽어보기를 권장한다.*")

col1, col2 = st.columns([1, 7])
col1.page_link("https://github.com/EX3exp/Kpop-lyric-datasets", label="Reference", icon=":material/info:")
col2.write("This document was written by EX3exp")

st.write(""); st.write(""); st.write("")


# 하나의 부품 =========================================================

st.write("# 데이터 베이스 정규화")
st.divider()

st.write("""
가공하기 전 데이터셋은 같은 노래가 여러 번 중복되어 있는 제대로 정규화되어 있지 않은 상태이다.
가공하기 전 데이터셋 `your_df`는 아래와 같다.
""")
st.code("""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline
%precision 5
""")
st.code("""
!git clone https://github.com/EX3exp/Kpop-lyric-datasets.git
%cd Kpop-lyric-datasets

from utils import data_parser
your_df = data_parser.get_df(2000, 2023)

%cd ..
""")
st.code("""your_df""")
st.dataframe(your_df)

st.write("""한 노래가 여러 번 랭킹에 오를 수 있는데, 그렇기에 같은 노래가 반복적으로 등장한다.
즉, 노래를 별도로 저장할 필요성이 있다.
학습의 용의성을 위해 데이터 구조를 노래를 저장하는 `song_df`랑 랭킹을 저장하는 `rank_df`로 나누겠다.""")
st.write("먼저, `song_df`는 아래와 같다.")
st.code("""
song_df = your_dict.copy()

# 필요 없는 칼럼 제거
song_df = song_df.drop(["year", "month", "rank"], axis=1)

# 중복 제거, song_id가 없는 경우 제거
song_df = song_df.drop_duplicates("song_id")
song_df = song_df.dropna(subset=["song_id"], axis=0)

# released_... 칼럼들의 이름 수정 및 자료형 수정
song_df.rename(columns={'released_year': 'year', 'released_month': 'month', 'released_day': 'day', 'song_name': 'name'}, inplace=True)
song_df[["year", "month", "day"]] = song_df[["year", "month", "day"]].astype('Int64')

# lyrics의 자료형 수정
song_df["lyrics"] = song_df['lyrics'].map(lambda x: '\\n'.join(x))

# 인덱스 지정
song_df = song_df.set_index("song_id", inplace=True)
""")
st.code("""song_df""")
st.dataframe(song_df[BASIC_COL])

st.write("""
`song_df`의 구조는 아래와 같다. `your_df`에서 중복을 제거하고, `song_id`를 인덱스로 하였다.
`realized_year`, `realized_month`, `realized_day`는 각각 `year`, `month`, `day`로 바꿨다.
이외에도 노래 가사 `lyrics`의 자료형을 문자열로 바꾸는 등 학습에 알맞게 변형을 가했다.
""")
st.code("song_df.info()")
st.code("""
Index: 8054 entries, 38541 to 36705594
Data columns (total 12 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   name          8054 non-null   object
 1   album         8054 non-null   object
 2   year          8051 non-null   Int64 
 3   month         8041 non-null   Int64 
 4   day           7992 non-null   Int64 
 5   artist        8054 non-null   object
 6   genre         8054 non-null   object
 7   lyric_writer  8054 non-null   object
 8   composer      8054 non-null   object
 9   arranger      8054 non-null   object
 10  lyrics_row    8054 non-null   int64 
 11  lyrics        8054 non-null   object
""")

st.write("`rank_df`의 구조와 각 칼럼은 아래와 같다. `year` 칼럼과 `month` 칼럼을 합쳐 `date` 칼럼으로 바꿨다.")
st.code("""
rank_df = your_dict[["month", "year", "rank", "song_id"]]
rank_df = rank_df.dropna(subset=["song_id"], axis=0)

# year, month 칼럼을 date로 합침
rank_df['date'] = pd.to_datetime(rank_df[['year', 'month']].assign(day=1))
rank_df = rank_df.drop(['year', 'month'], axis=1)
""")
st.code("""rank_df""")
st.dataframe(rank_df)

st.code("""rank_df.info()""")
st.code("""
Index: 25352 entries, 0 to 25695
Data columns (total 3 columns):
 #   Column   Non-Null Count  Dtype         
---  ------   --------------  -----         
 0   rank     25352 non-null  int64         
 1   song_id  25352 non-null  object        
 2   date     25352 non-null  datetime64[ns]
""")
