import streamlit as st
from common_container import menu
from data_analysis import song_df

from jamo import h2j, j2hcj

st.set_page_config(layout="wide")
menu()

cluster_id = st.session_state.get("cluster_id")
if cluster_id is None:
    st.switch_page("app.py")

st.session_state["show_lyrics"] = {}


def jamo_contains(haystack, needle):
    haystack_jamo = ''.join(j2hcj(h2j(haystack)))
    needle_jamo = ''.join(j2hcj(h2j(needle)))
    return needle_jamo in haystack_jamo


def search_songs_by(df, value, value_options, max_count=50):

    song_indices = []

    for idx, row in df[df['cluster'] == cluster_id].iterrows():
        if row[value_options].astype(str).apply(lambda x: jamo_contains(x, value)).any():
            song_indices.append(idx)
        if len(song_indices) >= max_count:
            break
    return df.loc[song_indices]


# @st.experimental_fragment
def frag(idx, row):
    with st.container(border=True):

        st.write(f"**Name**: {row['name']}")
        st.write(f"**Album**: {row['album']}")
        st.write(f"**Release Date**: {row['year']}-{row['month']:02d}-{row['day']:02d}")
        st.write(f"**Artist**: {row['artist']}")
        st.write(f"**Genre**: {row['genre']}")
        st.write(f"**Lyric Writer**: {row['lyric_writer']}")
        st.write(f"**Composer**: {row['composer']}")
        st.write(f"**Arranger**: {row['arranger']}")

        # 가사 표시 버튼
        btn = st.button(f"Show/Hide Lyrics for {row['name']}", key=f"button_{idx}")
        if btn:
            st.session_state.get('show_lyrics')[idx] = not st.session_state.get('show_lyrics').get(idx, 0)
        if st.session_state.get('show_lyrics').get(idx, 0):
            st.text(f"**Lyrics**:\n{row['lyrics']}")
            st.page_link(f"https://www.melon.com/song/detail.htm?songId={idx}", label="to Melon Music")

with st.form(key=f"form_{cluster_id}"):

    search = st.text_input(label="search")

    targ_options = ['name', "album", "artist", "genre", "lyric_writer", "composer", "arranger", "lyrics"]
    targ = st.multiselect(label="found words in:", options=targ_options, default="name")

    search_btn = st.form_submit_button()

if search_btn:
    
    song_df_selected = search_songs_by(song_df, search, targ_options)
    
    if song_df_selected is not None:
        for idx, row in song_df_selected.iterrows():
            frag(idx, row)

