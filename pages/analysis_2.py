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

col1, col2 = st.columns([1, 3])
col1.page_link("https://github.com/EX3exp/Kpop-lyric-datasets", label="Reference", icon=":material/info:")
col2.write("This document was written by EX3exp")

st.write(""); st.write(""); st.write("")


# 하나의 부품 =========================================================

st.write("# 데이터 베이스 정규화")
st.divider()

st.write("""
한 노래가 여러 번 랭킹에 오를 수 있는데, 그렇기에 해당 데이터셋에서는 같은 노래가 반복적으로 등장한다.

이는 학습에 악영향을 줄 수 있으며, 데이터베이스 용량도 쓸데 없이 많이 잡아먹는다.
가공하기 전 데이터셋은 아래와 같다.
""")
st.dataframe(your_df)


st.write("""학습의 용의성을 위해 데이터 구조를 노래를 저장하는 `song_df`랑 랭킹을 저장하는 `rank_df`로 나누겠다.""")
st.write("""
`song_df`의 구조는 아래와 같다. `your_df`에서 중복을 제거하고, `song_id`를 인덱스로 하였다.
`realized_year`, `realized_month`, `realized_day`는 각각 `year`, `month`, `day`로 바꿨다.
이외에도 노래 가사 `lyrics`의 자료형을 문자열로 바꾸는 등 학습에 알맞게 변형을 가했다.
""")
st.dataframe(song_df[BASIC_COL])

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
dtypes: Int64(3), int64(1), object(8)
memory usage: 841.6+ KB
""")

st.write("`rank_df`의 구조는 아래와 같다. `year` 칼럼과 `month` 칼럼을 합쳐 `date` 칼럼으로 바꿨다.")

st.dataframe(rank_df)

st.code("""
Index: 25352 entries, 0 to 25695
Data columns (total 3 columns):
 #   Column   Non-Null Count  Dtype         
---  ------   --------------  -----         
 0   rank     25352 non-null  int64         
 1   song_id  25352 non-null  object        
 2   date     25352 non-null  datetime64[ns]
dtypes: datetime64[ns](1), int64(1), object(1)
memory usage: 792.2+ KB
""")
